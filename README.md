# HRMS Lite

A lightweight web application for managing employee records and tracking attendance.

## Live Demo

- **Application URL**: https://hrms-lite-voey.onrender.com/
- **GitHub Repository**: https://github.com/ayush-baghel-dev/hrms-lite

## Tech Stack

**Frontend:** HTML, Bootstrap 5, JavaScript  
**Backend:** Django 5.0.1, Django REST Framework  
**Database:** SQLite (development), PostgreSQL (production)  
**Deployment:** Railway / Render

## Features

- Add, view, and delete employee records
- Mark daily attendance (Present/Absent)
- Filter attendance by employee and date
- Display total present days summary
- Server-side validation (required fields, email format, duplicate handling)
- Proper HTTP status codes and meaningful error messages


## Future Improvements

- Authentication & role-based access
- Update employee and attendance records
- Dashboard analytics
- Export attendance reports
- Pagination for large datasets



## Local Setup

1. **Clone and navigate to project:**
```bash
git clone https://github.com/ayush-baghel-dev/hrms-lite.git
cd hrms-lite
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Start server:**
```bash
python manage.py runserver
```

Visit `http://localhost:8000`

## Deployment

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

**Quick Railway Deploy:**
1. Push code to GitHub
2. Connect repository to Railway
3. Add environment variables (SECRET_KEY, DEBUG=False)
4. Railway auto-deploys

## API Endpoints

- `GET/POST /api/employees/` - List/Create employees
- `DELETE /api/employees/{id}/` - Delete employee
- `GET/POST /api/attendance/` - List/Create attendance
- `DELETE /api/attendance/{id}/` - Delete attendance

## Assumptions

- Single admin user (no authentication)
- SQLite for development
- One attendance record per employee per day
- Deleting employee removes their attendance records
