# Django E-commerce: Full-Stack Store Demo

This project is a comprehensive demonstration of a modern e-commerce platform built with Django. It showcases a complete shopping workflow, from product discovery to secure checkout and order management, designed with a focus on clean architecture and responsive user experience.

## Key Features

### 🛍️ Shopping Experience
- **Dynamic Product Catalog**: Browse products with real-time stock tracking and deep-link detail pages.
- **Interactive Deals Page**: Highlighted "Today's Deals" with case-insensitive search optimizations.
- **Robust Cart System**: Add, remove, and manage items seamlessly, supporting both authenticated users and guest sessions.
- **Customer Ratings & Reviews**: Integrated feedback system allowing customers to leave star ratings and comments on products.

### 🔐 Authentication & Accounts
- **Unified Registration**: A streamlined signup flow that captures all essential customer info (shipping, contact, and payment placeholders) in one step.
- **Google "Add Account" Integration**: Support for social login using Google for a modern, frictionless experience.
- **Secure Profile Management**: Personal dashboard to update shipping addresses and payment details.

### 📦 Order Management & Logistics
- **Tracking & Returns**: Functional package tracking and a "Return or Replace" system that automatically handles inventory restocking and order status updates.
- **Dynamic Delivery Location**: Session-based location system allowing users to change their country and state from the header.

### 📊 Administrative Backend
- **Staff Dashboard**: High-level business metrics including total revenue, order volume, and shipping statuses.
- **Inventory Control**: Real-time stock alerts and summaries of top-selling products.
- **Transaction History**: Detailed view of all customer transactions for efficient backend management.

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
