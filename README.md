# 🛒 Django E-Commerce Platform

A powerful, scalable, Django-based e-commerce platform with Stripe **&** PayPal support, full admin dashboard, inventory tracking, SEO optimizations, and email notifications.

![Platform Demo](static/assets/images/e-commerce.jpeg)

---

## 🚀 Key Features

- **User Authentication** 🔐  
- **Product Catalog** (search, categories, filters) 🛍️  
- **Shopping Cart & Orders** 📦  
- **Stripe & PayPal Integration** 💳  
- **Admin Dashboard** with analytics 📊  
- **SEO-Optimized Pages** 🔍  
- **Email Notifications** 📧  

---

## 🧑‍💻 Technology Stack

| Layer        | Technologies                             |
| ------------ | ---------------------------------------- |
| **Backend**  | Django 4, Python 3.10+, PostgreSQL       |
| **Frontend** | Bootstrap 5, JavaScript                  |
| **Payments** | Stripe (`stripe`), PayPal (`django-paypal`) |
| **DevOps**   | Docker, Docker Compose, Nginx, Gunicorn  |
| **CI/CD**    | GitHub Actions (optional)                |  
| **Security** | CSRF, HSTS, Secure & HttpOnly cookies    |

---

## 🛠️ Installation (Development)

# 1. Clone repo
git clone https://github.com/isaacaisha/e-commerce.git
cd e-commerce

# 2. Create & activate venv

python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install deps
```shell
pip install --upgrade pip
pip install -r requirements.txt
```

# 4. Create .env.dev from example
cp .env.example .env.dev
Edit .env.dev:
```python
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
PAYPAL_RECEIVER_EMAIL=you@sandbox.paypal.com
```

# 5. Run migrations & create superuser
```python
python manage.py migrate
python manage.py createsuperuser
```
# 6. Collect static files (optional for production)
```python
python manage.py collectstatic --noinput
```
# 7. Start dev server
```python
python manage.py runserver
```
⚙️ Configuration (Production)

# 1. Build & deploy with Docker
```shell
docker-compose -f docker-compose.prod.yml up --build -d
```

# 2. Set environment variables in .env.prod:
```python
DEBUG=False
ALLOWED_HOSTS=e-commerce.siisi.online,www.e-commerce.siisi.online
SECURE_SSL_REDIRECT=True
DATABASE_URL=postgres://django_user:secret_password@db:5432/django_db
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET_PROD=whsec_...
PAYPAL_RECEIVER_EMAIL=you@business.email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

# 3. Obtain and install Let’s Encrypt certificates, enable HSTS
# 4. Configure Nginx to proxy to Gunicorn on port 8005

🎯 Usage
# 1. Browse catalog, add items to cart
# 2. Checkout: fill shipping → choose Stripe or PayPal
# 3. Complete payment on Stripe/PayPal
# 4. Order auto-marked paid via webhook (Stripe) or IPN (PayPal)
# 5. Admin: view & toggle shipped status in dashboard

📂 Project Structure
```python
e-commerce/
├── ecommerce/                 # Django project root
│   ├── __init__.py
│   ├── settings.py            # Env-backed config (Stripe, PayPal, DB)
│   ├── urls.py                # URL routing (including payment endpoints)
│   └── wsgi.py                # WSGI entrypoint
│
├── payment/                   # Payment & order app
│   ├── __init__.py
│   ├── views.py               # Stripe & PayPal flows + webhooks
│   ├── models.py              # Order, OrderItem, ShippingAddress
│   ├── forms.py               # ShippingForm, PaymentForm
│   ├── urls.py                # checkout, webhook URLs
│   └── templates/payment/     # HTML templates for payment views
│
├── store/                     # Product & profile management
│   ├── __init__.py
│   ├── views.py
│   ├── models.py
│   └── templates/store/       # Templates for product pages, categories, etc.
│
├── cart/                      # Shopping cart logic
│   ├── __init__.py
│   └── cart.py
│
├── templates/                 # Shared base templates
│   └── base.html
│
├── static/                    # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── assets/
│       └── images/
│           └── e-commerce.jpeg
│
├── media/                     # Uploaded media (user uploads)
│
├── docker-compose.dev.yml     # Dev Docker Compose
├── docker-compose.prod.yml    # Prod Docker Compose
├── Dockerfile                 # Production Dockerfile
├── entrypoint.sh              # Docker entrypoint script
├── requirements.txt           # Python dependencies
├── .env.example               # Example env vars
└── manage.py                  # Django CLI
```

🔒 Security Features
HTTPS & HSTS in production

CSRF Protection on all forms

Password Hashing with PBKDF2

Secure Cookies (Secure & HttpOnly flags)

Content Security Policy (CSP) headers

Environment Variables for all secrets (no hard-coding)

Logging to console & file for error tracking

📦 Dependencies
```python
Django==4.2.7
psycopg2-binary==2.9.7
stripe==5.5.0
django-paypal==2.0
dj-database-url==1.0.0
python-dotenv==1.0.0
whitenoise==6.5.0
```

📬 Support & Contribution
Found a bug? Open an issue on GitHub.
Want to contribute? Submit a PR!

📜 License
MIT License – See LICENSE.md for details.

Made with ❤️ by IsaacAïsha – contributions welcome!
