import os
import subprocess

# Environment Variables
os.environ['SECRET_KEY'] = 'your-secure-secret-key'
os.environ['DB_PASSWORD'] = 'aYR?vCIUeA6m)K*z64OqLKNBedbfa3iB'

# Step 1: Set up Virtual Environment
print("Creating virtual environment...")
subprocess.run(["python3", "-m", "venv", "eski_env"])
print("Activating virtual environment and installing Django...")
subprocess.run(["eski_env/bin/pip", "install", "Django"])

# Step 2: Install Required Packages
print("Installing required packages...")
subprocess.run(["eski_env/bin/pip", "install", "django", "djangorestframework", "djangorestframework-simplejwt", "django-cors-headers", "psycopg2-binary", "gunicorn", "nats-py"])

# Step 3: Create Django Project
print("Creating Django project...")
subprocess.run(["eski_env/bin/django-admin", "startproject", "eski"])

# Step 4: Create Django App
os.chdir("eski")
print("Creating Django app...")
subprocess.run(["../eski_env/bin/python", "manage.py", "startapp", "shop"])

# Step 5: Update settings.py
settings_path = os.path.join("eski", "settings.py")
with open(settings_path, "r") as file:
    settings_content = file.read()

updated_settings = settings_content.replace(
    "INSTALLED_APPS = [",
    "INSTALLED_APPS = [\n    'rest_framework',\n    'rest_framework_simplejwt',\n    'corsheaders',\n    'shop',"
).replace(
    "MIDDLEWARE = [",
    "MIDDLEWARE = [\n    'corsheaders.middleware.CorsMiddleware',"
).replace(
    "DATABASES = {",
    "DATABASES = {\n    'default': {\n        'ENGINE': 'django.db.backends.postgresql',\n        'NAME': 'postgres',\n        'USER': 'postgres',\n        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),\n        'HOST': '127.0.0.1',\n        'PORT': '5432'\n    }\n}"
)

with open(settings_path, "w") as file:
    file.write(updated_settings)

# Step 6: Apply Migrations
print("Applying migrations...")
subprocess.run(["../eski_env/bin/python", "manage.py", "migrate"])

# Step 7: Collect Static Files
print("Collecting static files...")
subprocess.run(["../eski_env/bin/python", "manage.py", "collectstatic", "--noinput"])

# Step 8: Configure Gunicorn
print("Setting up Gunicorn...")
gunicorn_config = """[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/ubuntu/eski_shop
ExecStart=/home/ubuntu/eski_shop/eski_env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/eski_shop/eski.sock eski.wsgi:application

[Install]
WantedBy=multi-user.target
"""

with open("gunicorn.service", "w") as file:
    file.write(gunicorn_config)
subprocess.run(["sudo", "mv", "gunicorn.service", "/etc/systemd/system/"])
subprocess.run(["sudo", "systemctl", "daemon-reload"])
subprocess.run(["sudo", "systemctl", "start", "gunicorn"])
subprocess.run(["sudo", "systemctl", "enable", "gunicorn"])

# Step 9: Install and Configure NGINX
print("Installing and configuring NGINX...")
subprocess.run(["sudo", "apt", "install", "nginx", "-y"])
nginx_config = """server {
    listen 80;
    server_name ec2-3-120-108-48.eu-central-1.compute.amazonaws.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/eski_shop;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/eski_shop/eski.sock;
    }
}
"""

with open("nginx_config", "w") as file:
    file.write(nginx_config)
subprocess.run(["sudo", "mv", "nginx_config", "/etc/nginx/sites-available/eski"])
subprocess.run(["sudo", "ln", "-s", "/etc/nginx/sites-available/eski", "/etc/nginx/sites-enabled"])
subprocess.run(["sudo", "nginx", "-s", "reload"])

print("Setup complete! Visit your server's IP to access the application.")
