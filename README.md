# ComputerStore - My Django E-commerce Demo

This is my full-stack e-commerce project built with Django. I created this to show off what a modern store can do, from browsing cool tech like mechanical keyboards to a full checkout and return system. I focused on making the code clean, the design responsive, and the data management efficient.

## What it can do:

### 🛍️ The Shopping Experience
- **Real-Time Product Catalog**: I built a dynamic catalog that tracks stock automatically.
- **"Today's Deals" with Style**: I added a special highlighting feature for "mechanical switches" to make them stand out.
- **Smart Cart**: You can add and remove items whether you're signed in or just browsing as a guest.
- **Customer Feedback**: I implemented a star rating and review system so people can share their thoughts.

### 🔐 Accounts & Security
- **One-Step Registration**: When you sign up, you can enter all your info—name, address, phone, and even payment placeholders—in one simple form.
- **Google Login**: I integrated Google OAuth so users can sign in with their Google accounts instantly.
- **Your Profile**: A dedicated space to manage your shipping info and payment methods.

### 📦 Logistics & Support
- **Package Tracking**: You can actually see the status of your order in real-time.
- **Returns & Replacements**: If something isn't right, the system handles returns by putting items back into inventory and updating the order status automatically.
- **Global Delivery**: I added a location selector in the header so you can change your delivery country and state on the fly.

### 📊 Backend Admin Dashboard
I built a custom dashboard for staff to keep an eye on the business:
- **Financial Metrics**: Track total revenue and order volume.
- **Order Status**: See what's shipped, pending, or returned.
- **Inventory Tracking**: A list of exactly what's left to sell and which items are the top sellers.

## Technical Stack
- **Framework**: Django
- **Database**: SQLite (Development)
- **Frontend**: Responsive HTML5 / CSS3
- **Auth**: Django Contrib Auth & Django-Allauth

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install django django-allauth requests pyjwt cryptography
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

## Deployment on Render

1. **Connect GitHub**: Connect this repository to your Render account.
2. **Web Service Settings**:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn mysite.wsgi:application --chdir mysite`
3. **Environment Variables**:
   - `SECRET_KEY`: Your unique production secret key.
   - `DEBUG`: `False`
   - `DATABASE_URL`: Your Render PostgreSQL connection string.
   - `GOOGLE_CLIENT_ID`: Your Google OAuth Client ID.
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth Client Secret.

### 📝 Important Note on Media Files
Since this demo is hosted on Render's ephemeral filesystem, any product images you upload via the admin panel will be **deleted whenever the site restarts or you deploy new code**. For a permanent production store, you would connect this to a persistent storage service like AWS S3 or Cloudinary. For now, simply re-upload your product photos if they appear broken after a new deployment.
