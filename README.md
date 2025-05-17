🛒 E-Commerce Platform
A powerful, scalable, and modern Django-based e-commerce platform with customizable features for sellers, customers, and administrators.

🚀 Features
✅ User authentication (sign up, login, logout)

🛍️ Product listing, search, categories, and filters

💼 Shopping cart and order management

💳 Payment gateway integration: Stripe and PayPal-ready

🛠️ Admin dashboard with analytics

🌐 SEO-optimized product pages

📦 Inventory and stock tracking

📬 Email notifications for orders and registration

## 🖼️ Screenshots

| Homepage | Product Page | Admin Panel |
|----------|--------------|-------------|
| ![Home](https://via.placeholder.com/300x150.png?text=Homepage) | ![Product](https://via.placeholder.com/300x150.png?text=Product+Page) | ![Admin](https://via.placeholder.com/300x150.png?text=Admin+Dashboard) |
	

🧑‍💻 Tech Stack
Backend: Django, PostgreSQL

Frontend: HTML5 / Bootstrap, JavaScript

Payments: Stripe API, django-paypal

DevOps: Docker, Nginx, Gunicorn

Hosting: DigitalOcean

CI/CD: GitHub Actions (optional)

🛠️ Installation
bash
Copy
Edit
# Clone the repository
git clone https://github.com/isaacaisha/e-commerce.git
cd e-commerce

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables (.env or export in shell)
# Example:
# SECRET_KEY=your-secret-key
# DEBUG=True
# STRIPE_SECRET_KEY=your-stripe-secret-key
# STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
# PAYPAL_RECEIVER_EMAIL=your-paypal-email@example.com
# DATABASE_URL=postgres://user:password@host:port/dbname
# SECURE_SSL_REDIRECT=False (for dev)

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Start the development server
python manage.py runserver
⚙️ Configuration Details
Stripe Integration
Add your Stripe keys in environment variables:

ini
Copy
Edit
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
Stripe payment flow handled via checkout sessions and webhook for payment confirmation.

PayPal Integration
Set PayPal receiver email in environment:

ini
Copy
Edit
PAYPAL_RECEIVER_EMAIL=your-paypal-email@example.com
Uses django-paypal for PayPal Payments Standard and IPN (Instant Payment Notification) handling.

🚦 Usage
Browse products and add to cart

Proceed to checkout and fill in shipping details

Choose payment method: Stripe or PayPal

Complete payment on respective platform

Order status updated automatically via Stripe webhook or PayPal IPN

Admin dashboard shows shipped and unshipped orders with management features

🛡️ Security & Best Practices
HTTPS enforced in production with HSTS enabled

CSRF protection active on all forms

Secure cookies with Secure and HttpOnly flags in production

Sensitive keys and credentials stored in environment variables, never in source code

📝 Project Structure Overview
php
Copy
Edit
├── ecommerce/                  # Django project root
│   ├── settings.py             # Project settings with env variable config
│   ├── urls.py                 # URL routing including payment endpoints
│   └── wsgi.py / asgi.py
├── payment/                    # App for payment and order processing
│   ├── views.py                # Checkout, payment, webhook, PayPal integration
│   ├── models.py               # Order, OrderItem, ShippingAddress models
│   ├── forms.py                # Shipping and payment forms
│   └── urls.py                 # Payment-related URL patterns
├── store/                     # Product app and user profile management
├── cart/                      # Shopping cart logic
├── templates/                 # HTML templates for frontend views
├── static/                    # Static assets (CSS, JS, images)
├── requirements.txt           # Python dependencies
└── manage.py                  # Django CLI tool
📦 Dependencies
Django

psycopg2-binary (PostgreSQL adapter)

stripe (Stripe SDK)

django-paypal

dj-database-url

python-dotenv

whitenoise (for serving static files)

📬 Contact / Support
For issues or contributions, please open an issue or pull request on GitHub.

📜 License
MIT License
