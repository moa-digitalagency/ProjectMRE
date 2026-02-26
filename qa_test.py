from playwright.sync_api import sync_playwright, expect
import os
import re

def run_tests():
    # Ensure screenshots are saved in the current directory
    current_dir = os.getcwd()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        print("--- Step 1: Verify Home Page ---")
        try:
            page.goto("http://127.0.0.1:5000/")
            page.wait_for_load_state("networkidle")

            # Verify slider exists
            slider = page.locator("#slider")
            expect(slider).to_be_visible()

            # Scroll down to load lazy images if any
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000) # Wait for images to load
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(500)

            page.screenshot(path="etape_1.png", full_page=True)
            print("Step 1 Success: Home page loaded and screenshot taken.")
        except Exception as e:
            print(f"Step 1 Failed: {e}")
            return

        print("\n--- Step 2: Access Admin Dashboard ---")
        try:
            page.goto("http://127.0.0.1:5000/admin")
            page.wait_for_load_state("networkidle")

            expect(page.get_by_role("heading", name="Admin Dashboard")).to_be_visible()

            page.screenshot(path="etape_2.png")
            print("Step 2 Success: Admin dashboard accessed and screenshot taken.")
        except Exception as e:
            print(f"Step 2 Failed: {e}")
            return

        print("\n--- Step 3: Test Upload (Add to Slider) ---")
        try:
            # Locate the "Ajouter une image" form area
            # Assuming file input is named 'image' and inside the form for adding slider image
            # Since there are multiple forms, we target the one with 'slider/add' action or by text context

            # Fill form
            page.set_input_files('input[name="image"]', "test_assets/test_slider.jpg")
            page.fill('input[name="alt_text"]', "Image de Test QA")
            page.fill('input[name="order"]', "99")

            # Submit
            page.click('button:has-text("Ajouter au Slider")')
            page.wait_for_load_state("networkidle")

            # Verify success message
            expect(page.get_by_text("Slider image added successfully.")).to_be_visible()

            # Verify image appears in grid (we can look for the alt text)
            # The grid might not update immediately if it's not SPA, but here it's a reload
            expect(page.get_by_alt_text("Image de Test QA").first).to_be_visible()

            page.screenshot(path="etape_3.png")
            print("Step 3 Success: Slider image added and validated.")
        except Exception as e:
            print(f"Step 3 Failed: {e}")
            return

        print("\n--- Step 4: Test Upload (Update Section) ---")
        try:
            # Find the section "contexte" form
            # The HTML shows <h3 ...>contexte</h3> (but styled capitalized)
            # We locate by text content "contexte"

            # Use specific locator for the heading
            section_header = page.locator('h3:has-text("contexte")')

            # If multiple, pick the first one (should be unique per section ideally)
            if section_header.count() > 1:
                section_header = section_header.first

            # Find the form containing this header
            # We need to go up to the form element
            # The structure is: form > h3
            section_form = page.locator("form").filter(has=section_header)

            # Upload file to this specific form
            section_form.locator('input[name="image"]').set_input_files("test_assets/test_section.jpg")

            # Click update button in this specific form
            section_form.get_by_role("button", name="Mettre à jour l'image").click()
            page.wait_for_load_state("networkidle")

            # Verify success message
            expect(page.get_by_text("Image updated successfully.")).to_be_visible()

            # Verify visual update in admin (optional but good)
            # The image src should update.
            # We need to find the image preview associated with this section.
            # Structure:
            # <div class="... flex ...">
            #   <div>...image preview...</div>
            #   <div><form>...</form></div>
            # </div>
            # So form is sibling to image preview container.

            # Let's just verify success message as per requirement "verify the success message".

            page.screenshot(path="etape_4.png")
            print("Step 4 Success: Section image updated and validated.")
        except Exception as e:
            print(f"Step 4 Failed: {e}")
            # Debug screenshot
            page.screenshot(path="debug_step_4_retry.png")
            return

        print("\n--- Step 5: Final Frontend Validation ---")
        try:
            page.goto("http://127.0.0.1:5000/")
            page.wait_for_load_state("networkidle")

            # 1. Verify new slider image
            # It should be in the slider. The slider images are img tags.
            # We look for the one with our alt text.
            new_slide = page.get_by_alt_text("Image de Test QA").first
            expect(new_slide).to_be_attached()

            # 2. Scroll to "Contexte" section
            # The section has id="contexte".
            contexte_section = page.locator("#contexte")
            contexte_section.scroll_into_view_if_needed()
            page.wait_for_timeout(1000) # Wait for scroll and any animations

            # Verify the image in this section is our new image?
            # We can check if the src contains 'test_section.jpg' (or the uploaded filename).
            contexte_img = contexte_section.locator("img")

            # Use regex for substring match
            expect(contexte_img).to_have_attribute("src", re.compile(r"test_section\.jpg"))

            # Take targeted screenshot of the section
            # We can element.screenshot()
            contexte_section.screenshot(path="etape_5.png")
            print("Step 5 Success: Frontend validated and screenshot taken.")

        except Exception as e:
            print(f"Step 5 Failed: {e}")
            page.screenshot(path="debug_step_5.png")
            return

        browser.close()

if __name__ == "__main__":
    run_tests()
