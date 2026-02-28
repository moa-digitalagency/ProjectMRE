#!/bin/bash
set -e

echo "Starting deployment..."

# 1. Navigate to the project directory (optional, but good practice if called from elsewhere)
# cd /path/to/your/project/dir || exit

# 2. Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found! Please create one at 'venv'."
    exit 1
fi

# 3. Pull latest code
echo "Pulling latest code from main..."
git pull origin main

# 4. Update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# 5. Database migrations
echo "Running database migrations..."
if [ ! -d "migrations" ]; then
    echo "Initializing migrations..."
    flask db init
    flask db migrate -m "Initial migration"
fi
flask db upgrade

# 6. Create uploads directory and set permissions
echo "Setting up statics/uploads..."
mkdir -p statics/uploads
chmod -R 775 statics/uploads

# 7. Restart Gunicorn
echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

echo "Deployment completed successfully!"
