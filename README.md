# Task Manager (Django)

A task management web app built with Django using a custom user model (email login), authentication, and user-specific task CRUD.

## What It Does

This project allows users to:
- create an account and log in with email + password
- manage personal tasks (create, edit, complete/undo, delete)
- view all tasks, completed tasks, and pending tasks
- access Django Admin for user/task management (admin users)

Users must be authenticated to access task pages and CRUD operations.

## Features

- Custom user model (`accounts.CustomUser`)
- Function-based authentication views:
  - login
  - signup
  - logout
- User-scoped task access (each user sees only their own tasks)
- Task CRUD operations:
  - add task
  - edit task
  - toggle complete/pending
  - delete task
- Filtered views:
  - all tasks
  - completed tasks
  - pending tasks
- Django Admin integration:
  - Users visible under Accounts
  - Task ownership visible in admin
- Tailwind CSS based UI templates
- Success/error message feedback

## Tech Used

- Python 3.14
- Django 6.0.3
- SQLite (default Django database)
- HTML templates + Tailwind CSS (CDN)
- Django Admin

## Project Structure

- `accounts/` authentication app and custom user model
- `task/` task CRUD app
- `taskmanager/` project settings and root URLs
- `db.sqlite3` local database

## Quick Start

1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies
4. Run migrations
5. Start server

```bash
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
```

Open:
- `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- Signup: `http://127.0.0.1:8000/accounts/signup/`

## Screenshots

These screenshots are arranged to match the flow you shared.

Save images in `docs/screenshots/` with the exact names below:

| Page | Route | File name |
|---|---|---|
| Login Page | `/accounts/login/` | `login-page.png` |
| Signup Page | `/accounts/signup/` | `signup-page.png` |
| Task List | `/tasks/` | `task-list.png` |
| Edit Task | `/tasks/edit/1/` | `edit-task.png` |
| Delete Task | `/tasks/delete/1/` | `delete-task.png` |
| Completed Tasks | `/tasks/completed/` | `completed-tasks.png` |
| Pending Tasks | `/tasks/pending/` | `pending-tasks.png` |
| Admin Dashboard | `/admin/` | `admin-dashboard.png` |
| Admin Users | `/admin/accounts/customuser/` | `admin-users.png` |
| Admin Tasks | `/admin/task/task/` | `admin-tasks.png` |

After you place files with these names, they will render below.

### Login Page
![Login Page](docs/screenshots/login-page.png)

### Signup Page
![Signup Page](docs/screenshots/signup-page.png)

### Task List
![Task List](docs/screenshots/task-list.png)

### Edit Task
![Edit Task](docs/screenshots/edit-task.png)

### Delete Task
![Delete Task](docs/screenshots/delete-task.png)

### Completed Tasks
![Completed Tasks](docs/screenshots/completed-tasks.png)

### Pending Tasks
![Pending Tasks](docs/screenshots/pending-tasks.png)

### Admin Dashboard
![Admin Dashboard](docs/screenshots/admin-dashboard.png)

### Admin Users
![Admin Users](docs/screenshots/admin-users.png)

### Admin Tasks
![Admin Tasks](docs/screenshots/admin-tasks.png)

## Notes

- Existing tasks are user-owned and shown per logged-in user.
- Admin-created tasks are assigned with ownership logic in admin customization.
- Root and auth flow are configured for login-gated task access.
