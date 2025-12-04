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
