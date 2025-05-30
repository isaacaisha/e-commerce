# 🛒 Django E-Commerce Platform

A powerful, scalable, Django-based e-commerce platform with Stripe & PayPal support, full admin dashboard, inventory tracking, SEO optimizations, and email notifications.

![Platform Demo](static/assets/images/e-commerce.jpeg)

---

## 🚀 Key Features

* **User Authentication** 🔐
* **Product Catalog** (search, categories, filters) 🛍️
* **Shopping Cart & Orders** 📦
* **Stripe & PayPal Integration** 💳
* **Admin Dashboard** with analytics 📊
* **SEO-Optimized Pages** 🔍
* **Email Notifications** 📧

---

## 🧑‍💻 Technology Stack

| Layer        | Technologies                                |
| ------------ | ------------------------------------------- |
| **Backend**  | Django 4.2.7, Python 3.10+, PostgreSQL      |
| **Frontend** | Bootstrap 5, JavaScript                     |
| **Payments** | Stripe (`stripe`), PayPal (`django-paypal`) |
| **DevOps**   | Docker, Docker Compose, Nginx, Gunicorn     |
| **CI/CD**    | GitHub Actions (optional)                   |
| **Security** | CSRF, HSTS, Secure & HttpOnly cookies       |

---

## 🛠️ Installation (Development)

1. **Clone repo**

```bash
git clone https://github.com/isaacaisha/e-commerce.git
cd e-commerce
```

2. **Create & activate venv**

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Create `.env.dev` from example**

* Copy and edit `.env.dev`:

```bash
cp .env.example .env.dev
```

```dotenv
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
PAYPAL_RECEIVER_EMAIL=you@sandbox.paypal.com
```

5. **Run migrations & create superuser**

```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Collect static files** (optional for prod)

```bash
python manage.py collectstatic --noinput
```

7. **Start dev server**

```bash
python manage.py runserver
```

---

## ⚙️ Production Configuration

1. **Build & deploy with Docker**

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

2. **Set production env vars** in `.env.prod`:

```dotenv
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

3. **Certificates & SSL**

* Obtain & install Let's Encrypt certs
* Enable HSTS

4. **Configure Nginx & Gunicorn**

* Proxy to Gunicorn on port 8005

---

## 🎯 Usage

1. Browse catalog and add items to cart
2. Fill in shipping details and choose payment method
3. Complete payment via Stripe or PayPal
4. Orders auto-mark via webhook (Stripe) or IPN (PayPal)
5. Admin: manage orders and shipping status

---

## 📂 Project Structure

```plaintext
e-commerce/
├── ecommerce/                 # Django project root
│   ├── settings.py            # Env-backed config
│   ├── urls.py                # URL routing
│   └── wsgi.py                # WSGI entrypoint
├── payment/                   # Payment & order app
│   ├── views.py               # Stripe & PayPal flows
│   ├── models.py              # Order, OrderItem, ShippingAddress
│   └── forms.py               # ShippingForm, PaymentForm
├── store/                     # Product management app
│   ├── views.py
│   ├── models.py
│   └── templates/store/
├── cart/                      # Cart logic
│   └── cart.py
├── templates/                 # Shared templates
│   └── base.html
├── static/                    # CSS, JS, images
│   └── assets/images/e-commerce.jpeg
├── media/                     # User uploads
├── docker-compose.dev.yml     # Dev Docker Compose
├── docker-compose.prod.yml    # Prod Docker Compose
├── Dockerfile                 # Production Dockerfile
├── entrypoint.sh              # Docker entrypoint script
├── requirements.txt           # Python dependencies
├── .env.example               # Example env vars
└── manage.py                  # Django CLI
```

---

## 🔒 Security Features

* **HTTPS & HSTS** in production
* **CSRF Protection** on all forms
* **PBKDF2 Password Hashing**
* **Secure Cookies** (Secure & HttpOnly)
* **Content Security Policy (CSP)**
* **Environment Variables** for secrets
* **Logging** for error tracking

---

## 📦 Dependencies

```text
Django==4.2.7
psycopg2-binary==2.9.7
stripe==5.5.0
django-paypal==2.0
dj-database-url==1.0.0
python-dotenv==1.0.0
whitenoise==6.5.0
```

---

## 📬 Support & Contribution

* Report bugs via GitHub issues
* Submit PRs for enhancements

---

## 📜 License

MIT License – see [LICENSE.md](LICENSE.md) for details.

---

*Made with ❤️ by Isaac Aïsha – contributions welcome!*
