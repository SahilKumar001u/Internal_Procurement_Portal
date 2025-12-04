# Internal Procurement Request System

A Django-based web application for managing internal purchase requisitions with a two-level approval workflow (Requester → Manager).

## Features

- **Requester Role**: Create purchase requisitions with multiple line items, upload attachments, track status
- **Manager Role**: View all requisitions, approve/reject with comments, audit trail
- **Status Tracking**: Pending → Approved/Rejected workflow
- **Audit Logging**: Complete history of all approval actions
- **File Uploads**: Support for PDF/image attachments

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations (already done):
```bash
python manage.py migrate
```

3. Setup demo users (already done):
```bash
python setup_demo_data.py
```

## Demo Users

- **Admin**: `admin` / `admin123` (Django admin access)
- **Manager**: `manager` / `manager123` (Can approve/reject requisitions)
- **Requester**: `requester` / `requester123` (Can create requisitions)

## Running the Application

```bash
python manage.py runserver
```

Access at: http://127.0.0.1:8000/

## Usage Flow

1. **Login** as requester (requester/requester123)
2. **Create Requisition** - Add items with details (name, quantity, price, category, purpose, optional attachment)
3. **Submit** - Requisition status set to "Pending"
4. **Logout** and login as manager (manager/manager123)
5. **View Dashboard** - See all pending requisitions
6. **Open Requisition** - Review details
7. **Approve/Reject** - Add comments and submit decision
8. **Audit Trail** - All actions logged with timestamp

## Project Structure

```
procurement_system/
├── requisitions/           # Main app
│   ├── models.py          # UserProfile, Requisition, LineItem, ApprovalLog
│   ├── views.py           # Dashboard, create, detail, approve views
│   ├── forms.py           # LineItem and Approval forms
│   ├── urls.py            # App URL routing
│   └── templates/         # HTML templates
├── manage.py
├── requirements.txt
└── README.md
```

## Models

- **UserProfile**: Extends User with role (Requester/Manager)
- **Requisition**: Main request with status tracking
- **LineItem**: Individual items in a requisition
- **ApprovalLog**: Audit trail of manager actions

## Security Features

- Role-based access control
- Login required for all views
- Requesters cannot approve their own requisitions
- File upload validation
- CSRF protection

## Admin Panel

Access Django admin at: http://127.0.0.1:8000/admin/
Login with admin credentials to manage users and data.

## Deploying to Render

### Quick Deploy (Blueprint)
1. Push this repo to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click **New +** → **Blueprint**
4. Connect your GitHub repo
5. Render auto-detects `render.yaml` and sets up everything
6. Click **Apply** and wait for deployment

### Manual Deploy
1. Create a **PostgreSQL** database on Render (free tier)
2. Create a **Web Service** with these settings:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn procurement_system.wsgi:application --bind 0.0.0.0:$PORT`
3. Add environment variables:
   - `SECRET_KEY`: Generate a secure random string
   - `DATABASE_URL`: Copy from your Render PostgreSQL database
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com`

### Post-Deployment
Create a superuser via Render Shell:
```bash
python manage.py createsuperuser
```
