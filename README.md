# Flex-Work Demo 🚀

A simple CRM (Customer Relationship Management) system built with Flask. This is a demonstration project showcasing basic CRM functionality including user management, organization management, administrative task management, inventory tracking, and announcements.

## Key Features & Implementation ⚡

### 1. Authentication System 🔐
- 🔒 Secure user registration and login
- 🔑 Password hashing using Werkzeug security
- 🎫 Session-based authentication
- 🛡️ CSRF protection on all forms
- 💾 Remember-me functionality
- 🔄 Password reset capability

### Login Page:

![alt text](<assets/Screenshot 2025-04-03 at 9.34.07 PM.png>)

### Sign Up Page:

![alt text](<assets/Screenshot 2025-04-03 at 9.34.14 PM.png>)

### 2. Dashboard 📊
- 📈 Real-time statistics and counts
- ⚡ Quick access to all major features
- 👋 Personalized welcome message
- 📰 Activity feed
- 🎯 Quick-action buttons for common tasks
- 📱 Responsive grid layout

### Dashboard:

![alt text](<assets/Screenshot 2025-04-03 at 11.48.20 PM.png>)

### 3. Groups/Organizations 👥
- 🏢 Create and manage organizations
- 👑 Role-based access control (Admin/Member)
- ✉️ Member invitation system
- ⚙️ Organization settings management
- 📋 Member list with roles
- 👥 Bulk member management
- 🚪 Leave/Delete organization options

### Organization Management:

![alt text](<assets/Screenshot 2025-04-03 at 9.31.09 PM.png>)


### 4. Inventory Management 📦
- ✨ Add/Edit/Delete inventory items
- 📎 File attachment support (PDF, DOCX, CSV)
- 🔍 Search and filter functionality
- 🏷️ Categories and tags
- 📊 Stock level tracking
- 📤 Export to CSV feature
- 🔄 Bulk operations support

### Inventory Management:

![alt text](<assets/Screenshot 2025-04-03 at 9.30.38 PM.png>)


### 5. WorkPad 📝
- 📋 Kanban-style task management
- 🔄 Drag-and-drop interface
- 📆 Task priorities and deadlines
- 👥 Task assignments
- 📊 Progress tracking
- 💬 Task comments and attachments
- 🔍 Filter by status/assignee

### WorkPad - Task Management:

![alt text](<assets/Screenshot 2025-04-03 at 11.52.07 PM.png>)

### 6. Bulletin Board 📰
- 📢 Organization-wide announcements
- 📝 Rich text editor
- 📎 File attachments
- ⚠️ Priority levels
- 🔍 Search functionality
- 📁 Archive system
- 📧 Email notifications (configurable)

### Bulletin Board:

![alt text](<assets/Screenshot 2025-04-03 at 11.52.07 PM-1.png>)


### 7. Account Manager/Settings 🛠️
- 👥 Profile management
- 🔑 Password change
- 📣 Notification preferences
- 🎨 Theme customization
- 📊 Session management
- 🚪 Account deletion option
- 📤 Export personal data


## Technical Implementation 🤖

### Backend Architecture 📈
- **Framework**: Flask 3.0.2
- **Database**: SQLite with SQL Alchemy
- **Authentication**: Session-based with Werkzeug Security
- **File Storage**: Local file system with secure naming
- **API Design**: RESTful with JSON responses
- **Error Handling**: Comprehensive with status codes

### Security Features 🔒
- 🛡️ CSRF Protection
- 🔑 Password Hashing
- 🚫 SQL Injection Prevention
- 🚫 XSS Protection
- 🔒 Secure File Uploads
- ⏱️ Rate Limiting
- 📊 Session Security
- 📝 Input Validation

### Database Design 📊
- 📈 Normalized Schema
- 🔗 Foreign Key Constraints
- 🔍 Index Optimization
- 🔄 Transaction Support
- 📁 Backup System
- 🔁 Migration Support

## Frontend Features 🎨

### UI Components 📈
- 📱 Responsive Design
- 📈 Modern CSS Grid/Flexbox
- 📝 Interactive Modals
- 📣 Toast Notifications
- 🔄 Loading States
- 📝 Error Handling
- 📝 Form Validation

### JavaScript Features 📈
- 🔄 Async/Await API Calls
- 📈 Real-time Updates
- 🔄 Drag-and-Drop
- 📝 Form Handling
- 📎 File Upload Preview
- 📝 Input Validation
- 📝 Error Handling

## Project Structure 📁
```
Flex-CRM/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # Route handlers
│   └── utils/          # Utility functions
├── database/
│   ├── migrations/     # Database migrations
│   └── create_db.py    # Database initialization
├── static/
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
├── templates/          # HTML templates
├── scripts/           # Setup scripts
├── tests/            # Unit tests
└── docs/             # Documentation
```

## Technology Stack 📈

### Backend 🤖
- Python 3.8+
- Flask 3.0.2
- Werkzeug 3.0.1
- SQLite
- PyTZ

### Frontend 🎨
- HTML5
- CSS3
- JavaScript (ES6+)
- Font Awesome Icons
- Custom CSS Framework

### Development Tools 🛠️
- Git
- Windsurf IDE
- SQLite Browser
- Python venv
- Flask Debug Toolbar

## Getting Started 🚀
See [Installation.md](Installation.md) for setup instructions.

## License 📜
MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments 
- Flask documentation and community
- Font Awesome for icons
- SQLite documentation
- Python community