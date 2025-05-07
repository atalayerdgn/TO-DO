# ✅ To-Do Application

A modern task management application built with PyQt5 and qfluentwidgets for a beautiful, responsive UI.

## 🏗️ Architecture

The application follows a clean, modular architecture for better maintainability and scalability:

```
├── app.py                # Application entry point
├── db/                   # Database modules
│   ├── database.py       # Database connection and operations
│   ├── initdb.py         # Database initialization
│   ├── tasks.py          # Task-related database operations
│   └── user.py           # User-related database operations
├── ui/                   # User interface modules
│   ├── HomeUI.py         # Home screen UI
│   ├── LoginUI.py        # Login screen UI
│   ├── MenuUI.py         # Main menu UI
│   ├── RedirectUI.py     # Transition screen UI
│   ├── RegisterUI.py     # Registration screen UI
│   └── SettingsUI.py     # Settings screen UI
├── utils/                # Utility modules
│   ├── config.py         # Application configuration
│   ├── LoginUtils.py     # Login-related utilities
│   ├── RegisterUtils.py  # Registration-related utilities
│   └── SettingsUtils.py  # Settings-related utilities
├── logs/                 # Application logs directory
└── data/                 # Database files directory
```

### 🔑 Key Components

1. **ApplicationManager**: Central manager for the application state and UI flow
2. **Database Classes**: Abstract database operations with proper error handling
3. **Configuration Module**: Centralized application settings and constants
4. **UI Components**: Individual screens implemented as PyQt5 windows

## 🧩 Design Principles

The application follows these design principles:

1. **Single Responsibility**: Each class has a single responsibility
2. **Dependency Injection**: Dependencies are provided from the outside
3. **Separation of Concerns**: UI, business logic, and data access are separated
4. **Error Handling**: Robust error handling throughout the application
5. **Logging**: Comprehensive logging for debugging and monitoring

## ✨ Features

- User authentication (login/registration)
- Task creation, editing, and deletion
- Task categorization and prioritization
- Due date management
- Task filtering and searching
- Light and dark theme support
- Responsive and modern UI with Fluent design

## 🚀 Improvements

The architecture has been improved in several ways:

1. **Centralized Configuration**: All constants and settings in one place
2. **Robust Error Handling**: Proper error handling and user feedback
3. **Abstract Database Access**: Cleaner database operations with transactions
4. **Organized UI Flow**: Centralized UI navigation management
5. **Logging System**: Comprehensive logging for debugging and troubleshooting
6. **Settings Management**: Persistent user settings and preferences
7. **Enhanced Task Management**: More comprehensive task features

## 📋 Installation

1. Ensure you have Python 3.6+ installed
2. Install required packages:
   ```
   pip install PyQt5
   pip install "PyQt-Fluent-Widgets[full]" -i https://pypi.org/simple/
   ```
3. Run the application:
   ```
   python app.py
   ```

## 🔧 Requirements

- Python 3.6+
- PyQt5 >= 5.15.0
- PyQt-Fluent-Widgets >= 1.0.0
- SQLite3 (included in Python standard library)

## 👤 Author

Atalay Erdogan

---
