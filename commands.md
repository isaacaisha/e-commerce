# e-commerce commands eg.:

python manage.py collectstatic
sudo systemctl daemon-reload
sudo systemctl restart e-commerce.service
sudo systemctl status e-commerce.service

sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx

python manage.py makemigrations
python manage.py migrate

sudo journalctl -u e-commerce.service -f
python manage.py runserver 0.0.0.0:8005

# CONNECT POSTGRES
sudo -i -u postgres
sudo nano /var/lib/pgsql/data/postgresql.conf

# systemd
sudo nano /etc/systemd/system/e-commerce.service

# nginx
sudo nano /etc/nginx/sites-available/e-commerce.conf

# CREATE SSL CERTIFICATE
sudo dnf install certbot python-certbot-nginx
sudo certbot --nginx

# link the configuration to enable it
sudo ln -s /etc/nginx/sites-available/e-commerce /etc/nginx/sites-enabled/

sudo certbot certificates
sudo certbot --nginx -d e-commerce.siisi.online -d www.e-commerce.siisi.online

sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

sudo systemctl enable certbot.timer
sudo certbot renew --dry-run

# kill all port runing
sudo lsof -t -iTCP:8005 -sTCP:LISTEN | xargs sudo kill

# Find Your Computer's Local IP Address
ifconfig | grep inet

# Testing
python -m gunicorn --workers 3 --bind unix:/home/siisi/e-commerce/e-commerce.sock siisi.wsgi:application


# Docker 
docker --version
<!-- Build an image from Dockerfile in current dir -->
docker build -t ecommerce:latest .
<!-- List local images -->
docker images
<!-- List all containers (running + stopped) -->
docker ps -a
<!-- Create & start container in detached mode -->
docker run -d --name web -p 8000:8005 ecommerce:latest
<!!-- View logs from a container -->
docker logs web
<!-- Start an interactive shell inside a running container -->
docker exec -it web bash
<!--Gracefully stop a running container -->
docker stop web
# Start DB + Django runserver
# Rebuild static assets & restart
<!-- prod -->
docker compose -f docker-compose.dev.yml run ecommerce python manage.py collectstatic
docker-compose -f docker-compose.prod.yml down --volumes --remove-orphans
docker system prune -a --volumes 
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml logs -f nginx
docker-compose -f docker-compose.prod.yml logs -f web

<!-- dev -->
docker compose -f docker-compose.dev.yml run ecommerce python manage.py collectstatic
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
docker system prune -a --volumes 
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d --build
docker-compose -f docker-compose.dev.yml ps
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
docker-compose -f docker-compose.dev.yml logs -f nginx
docker-compose -f docker-compose.dev.yml logs -f web

# Apply migrations or create superuser
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
