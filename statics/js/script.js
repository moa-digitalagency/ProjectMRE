        document.addEventListener('DOMContentLoaded', () => {
            // Slider Logic
            const slides = document.querySelectorAll('.fade-slide');
            const dots = document.querySelectorAll('.slider-dot');
            let currentSlide = 0;
            const slideInterval = 5000;

            function goToSlide(index) {
                if(!slides.length) return;
                slides[currentSlide].classList.remove('active');
                dots[currentSlide].classList.remove('bg-white');
                dots[currentSlide].classList.add('bg-white/30');

                currentSlide = index;

                slides[currentSlide].classList.add('active');
                dots[currentSlide].classList.remove('bg-white/30');
                dots[currentSlide].classList.add('bg-white');
            }

            function nextSlide() {
                if(!slides.length) return;
                let next = (currentSlide + 1) % slides.length;
                goToSlide(next);
            }

            let sliderTimer = setInterval(nextSlide, slideInterval);

            dots.forEach((dot, index) => {
                dot.addEventListener('click', () => {
                    clearInterval(sliderTimer);
                    goToSlide(index);
                    sliderTimer = setInterval(nextSlide, slideInterval);
                });
            });

            // Mobile Menu Logic
            const menuBtn = document.getElementById('mobile-menu-btn');
            const mobileMenu = document.getElementById('mobile-menu');
            const iconOpen = document.getElementById('menu-icon-open');
            const iconClose = document.getElementById('menu-icon-close');
            const mobileLinks = document.querySelectorAll('.mobile-link');
            let menuOpen = false;

            function toggleMenu() {
                menuOpen = !menuOpen;
                if (menuOpen) {
                    mobileMenu.classList.remove('translate-x-full');
                    iconOpen.classList.add('hidden');
                    iconClose.classList.remove('hidden');
                    document.body.style.overflow = 'hidden'; // Empêche le scroll quand le menu est ouvert
                } else {
                    mobileMenu.classList.add('translate-x-full');
                    iconOpen.classList.remove('hidden');
                    iconClose.classList.add('hidden');
                    document.body.style.overflow = '';
                }
            }

            menuBtn.addEventListener('click', toggleMenu);

            // Fermer le menu au clic sur un lien
            mobileLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (menuOpen) toggleMenu();
                });
            });
        });
