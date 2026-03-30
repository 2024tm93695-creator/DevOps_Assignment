# ACEest Fitness & Gym Management - Desktop UI

A comprehensive Tkinter-based desktop application that serves as a frontend client for the ACEest Fitness Flask API. This application provides a complete graphical user interface for managing gym operations, member data, workout tracking, and administrative functions.

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [UI Pages & Features](#ui-pages--features)
- [API Integration](#api-integration)
- [Usage Examples](#usage-examples)
- [UI Design Features](#ui-design-features)
- [Error Handling](#error-handling)
- [Development Notes](#development-notes)
- [Troubleshooting](#troubleshooting)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

### 🔐 **Authentication System**
- Secure login screen with username/password validation
- Demo mode for testing and development
- Session management and user role handling

### 👥 **Member Management**
- Complete member profile creation and editing
- Advanced search and filtering capabilities
- Automatic BMI and calorie calculations
- Target weight and adherence goal tracking
- Membership status monitoring

### 🏋️ **Workout Management**
- Comprehensive workout logging system
- Multi-exercise workout sessions
- Exercise database with sets, reps, and weight tracking
- Workout history with detailed analytics
- Progress tracking and performance metrics

### 📊 **Analytics & Reporting**
- Real-time progress charts and graphs
- BMI calculation and health risk assessment
- Adherence trend analysis
- Weight progression visualization
- Custom reporting capabilities

### 👨‍🏫 **Trainer Management**
- Trainer profile administration
- Specialization and certification tracking
- Experience level management
- Contact information and scheduling
- Performance evaluation tools

### 💳 **Subscription & Billing**
- Multi-tier subscription plan management
- Automated billing and renewal tracking
- Payment history and transaction logs
- Membership status and expiration alerts
- Financial reporting and analytics

### 🎯 **AI-Style Program Generation**
- Intelligent workout program suggestions
- Goal-based program customization
- Randomized exercise selection algorithms
- Progressive overload planning
- Adaptive training recommendations

### 🔧 **Administrative Tools**
- System configuration and settings
- Data backup and restore functionality
- User role and permission management
- Audit logging and security monitoring
- Performance optimization tools

## Architecture Overview

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Tkinter UI    │◄──────────────►│   Flask API      │
│   (Frontend)    │                │   (Backend)      │
└─────────────────┘                └─────────────────┘
         │                                   │
         │                                   │
         ▼                                   ▼
┌─────────────────┐                  ┌─────────────────┐
│   SQLite DB     │                  │   Business      │
│   (Local Data)  │                  │   Logic Layer   │
└─────────────────┘                  └─────────────────┘
```

### Component Breakdown

- **UI Layer**: Tkinter-based desktop application with multiple windows and tabs
- **API Layer**: RESTful Flask API handling data operations and business logic
- **Data Layer**: SQLite database for persistent storage
- **Service Layer**: Business logic and data processing modules

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python Version**: 3.8 or higher
- **Memory**: Minimum 4GB RAM, 8GB recommended
- **Storage**: 500MB free space for application and data

### Software Dependencies
- Python 3.8+
- pip package manager
- Git (for cloning repositories)
- SQLite3 (usually included with Python)

### Network Requirements
- Local network access for API communication
- Internet connection for dependency installation
- Firewall permissions for local port access (default: 5000)

## Installation & Setup

### Step 1: Clone or Download Project
```bash
# Navigate to your desired directory
cd "C:\Users\prasa\Downloads"

# The project should already be in the specified location
# If cloning from repository:
# git clone <repository-url>
# cd aceest-fitness-management
```

### Step 2: Backend API Setup
```bash
# Navigate to Flask API directory
cd "The code versions for DevOps Assignment/The code versions for DevOps Assignment/flask_app"

# Install backend dependencies
pip install -r requirements.txt

# Verify installation
python -c "import flask, flask_sqlalchemy; print('Backend dependencies installed successfully')"
```

### Step 3: Frontend UI Setup
```bash
# Navigate to UI application directory
cd "../ui_app"

# Install UI dependencies
pip install -r requirements.txt

# Verify installation
python -c "import tkinter, requests, matplotlib; print('UI dependencies installed successfully')"
```

### Step 4: Database Initialization
The SQLite database will be automatically created when the Flask API starts for the first time. The database file `aceest_fitness.db` will be created in the `flask_app` directory.

## Configuration

### API Configuration
The application uses the following default configuration:

```python
# In config.py (Flask app)
API_BASE_URL = "http://localhost:5000"  # Default API endpoint
DEBUG = True                           # Development mode
SECRET_KEY = "dev-secret-key"          # Session security
DATABASE_URI = "sqlite:///aceest_fitness.db"  # Database location
```

### UI Configuration
```python
# In aceest_ui.py
API_BASE_URL = "http://localhost:5000"  # API endpoint
WINDOW_SIZE = "1400x900"               # Main window dimensions
THEME_COLORS = {
    "bg": "#1a1a1a",                   # Background color
    "fg": "#d4af37",                   # Accent color
    "text": "white"                    # Text color
}
```

### Environment Variables
Create a `.env` file in the `flask_app` directory for custom configuration:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///aceest_fitness.db
API_HOST=localhost
API_PORT=5000
```

## Running the Application

### Method 1: Manual Startup (Recommended for Development)

1. **Start the Flask API Backend:**
   ```bash
   cd flask_app
   python app.py
   ```
   The API will start on `http://localhost:5000`

2. **Start the UI Application:**
   Open a new terminal/command prompt:
   ```bash
   cd ui_app
   python aceest_ui.py
   ```
   The desktop application will launch

### Method 2: Batch Script (Windows)
Create `start_aceest.bat`:
```batch
@echo off
echo Starting ACEest Fitness Management System...

REM Start Flask API in background
start "Flask API" cmd /c "cd flask_app && python app.py"

REM Wait for API to start
timeout /t 3 /nobreak > nul

REM Start UI application
cd ui_app
python aceest_ui.py
```

### Method 3: Python Script Launcher
Create `launcher.py`:
```python
import subprocess
import time
import sys
import os

def start_application():
    # Start Flask API
    api_path = os.path.join(os.path.dirname(__file__), 'flask_app')
    api_process = subprocess.Popen([sys.executable, 'app.py'], cwd=api_path)

    # Wait for API to initialize
    time.sleep(3)

    # Start UI
    ui_path = os.path.join(os.path.dirname(__file__), 'ui_app')
    ui_process = subprocess.Popen([sys.executable, 'aceest_ui.py'], cwd=ui_path)

    try:
        # Wait for processes
        api_process.wait()
        ui_process.wait()
    except KeyboardInterrupt:
        api_process.terminate()
        ui_process.terminate()

if __name__ == "__main__":
    start_application()
```

## UI Pages & Features

### 1. **Login Screen**
- **Username/Password Fields**: Secure authentication
- **Demo Mode Button**: Skip authentication for testing
- **Error Display**: Login failure notifications
- **Remember Me**: Optional session persistence

### 2. **Main Dashboard**
- **Header Bar**: Application title and user information
- **Status Bar**: Real-time operation feedback
- **Left Panel**: Quick access controls and navigation
- **Right Panel**: Main content area with tabs

#### Left Panel Components:
- **Client Selection Dropdown**: Active member selection
- **Client Information Form**: Name, age, height, weight, program
- **Goal Setting**: Target weight and adherence inputs
- **Action Buttons**: Save, Load, Generate Program, Log Workout
- **Management Buttons**: Trainer and Subscription management

#### Right Panel Tabs:

### 3. **Client Summary Tab**
- **Member Profile Display**: Complete member information
- **BMI Calculator**: Automatic BMI calculation and categorization
- **Progress Metrics**: Recent workouts and adherence data
- **Membership Status**: Current subscription information
- **Embedded Charts**: Visual progress representation

### 4. **Workouts & Exercises Tab**
- **Workout History Table**: Date, type, duration, notes
- **Add Workout Button**: Opens workout creation dialog
- **Exercise Details**: Expandable exercise information
- **Performance Metrics**: Sets, reps, weight tracking
- **Search/Filter**: Workout history filtering options

### 5. **Progress & Analytics Tab**
- **Adherence Chart**: Weekly adherence percentage trends
- **Weight Chart**: Weight progression over time
- **BMI Analysis**: BMI trends and health indicators
- **Goal Tracking**: Progress towards targets
- **Export Options**: Chart and data export functionality

### 6. **Trainer Management Window**
- **Trainer List**: Grid view of all trainers
- **Add Trainer Form**: New trainer registration
- **Edit Capabilities**: Inline trainer information editing
- **Search/Filter**: Trainer search and filtering
- **Specialization Tracking**: Certification and skill management

### 7. **Subscription Management Window**
- **Subscription Grid**: All member subscriptions
- **Add Subscription Dialog**: New subscription creation
- **Billing Information**: Fee calculation and payment tracking
- **Status Management**: Active, expired, cancelled states
- **Renewal Alerts**: Automatic expiration notifications

## API Integration

### REST Endpoints Used

#### Members API
```http
GET    /api/members                    # List all members
GET    /api/members/{id}              # Get member by ID
POST   /api/members                   # Create new member
PUT    /api/members/{id}              # Update member
DELETE /api/members/{id}              # Delete member
GET    /api/members/{name}/summary    # Get member summary
```

#### Workouts API
```http
GET    /api/workouts?member={name}    # Get workouts by member
GET    /api/workouts/{id}             # Get workout details
POST   /api/workouts                  # Create new workout
PUT    /api/workouts/{id}             # Update workout
DELETE /api/workouts/{id}             # Delete workout
```

#### Trainers API
```http
GET    /api/members/trainers          # List all trainers
POST   /api/members/trainers          # Create new trainer
PUT    /api/members/trainers/{id}     # Update trainer
DELETE /api/members/trainers/{id}     # Delete trainer
```

#### Subscriptions API
```http
GET    /api/subscriptions             # List all subscriptions
GET    /api/subscriptions?member={name} # Get by member
GET    /api/subscriptions/{id}        # Get subscription details
POST   /api/subscriptions             # Create new subscription
PUT    /api/subscriptions/{id}        # Update subscription
DELETE /api/subscriptions/{id}        # Delete subscription
GET    /api/subscriptions/active      # Get active subscriptions
```

### Data Models

#### Member Model
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 30,
  "height": 175.0,
  "weight": 80.0,
  "program": "Fat Loss (FL) – 3 day",
  "calories": 2200,
  "target_weight": 75.0,
  "target_adherence": 80,
  "membership_status": "active",
  "membership_end": "2024-12-31"
}
```

#### Workout Model
```json
{
  "id": 1,
  "client_name": "John Doe",
  "date": "2024-01-15",
  "workout_type": "Upper Body",
  "duration_min": 60,
  "notes": "Great session",
  "exercises": [
    {
      "name": "Bench Press",
      "sets": 4,
      "reps": 10,
      "weight": 80.0
    }
  ]
}
```

## Usage Examples

### Complete Member Onboarding Process

1. **Add New Member:**
   - Click "Add / Save Client"
   - Enter: Name="John Doe", Age=30, Height=175, Weight=80
   - Select Program: "Fat Loss (FL) – 3 day"
   - Set Target Weight: 75kg, Target Adherence: 80%
   - Click "Save Client"

2. **Generate Initial Program:**
   - Select member from dropdown
   - Click "Generate AI Program"
   - Review suggested program

3. **Log First Workout:**
   - Click "Log Workout"
   - Enter: Date=today, Type="Full Body", Duration=60
   - Add exercises: "Squats 3x10@100kg", "Bench Press 4x8@80kg"
   - Save workout

4. **View Progress:**
   - Navigate to "Client Summary" tab
   - Review BMI, recent workouts, and progress charts

### Trainer Management Workflow

1. **Add New Trainer:**
   - Click "Manage Trainers"
   - Click "Add Trainer"
   - Enter: Name, Specialization, Experience, Email
   - Save trainer profile

2. **Assign Trainer to Member:**
   - Select member from dropdown
   - Access trainer assignment feature
   - Link trainer to member profile

### Subscription Management

1. **Create Membership:**
   - Click "Manage Subscriptions"
   - Click "Add Subscription"
   - Select member, plan, start/end dates
   - System calculates fees automatically

2. **Monitor Renewals:**
   - View subscription grid
   - Check expiration dates
   - Process renewals as needed

## UI Design Features

### Color Scheme
- **Primary Background**: `#1a1a1a` (Dark Gray)
- **Secondary Background**: `#111111` (Darker Gray)
- **Accent Color**: `#d4af37` (Gold)
- **Text Color**: `#ffffff` (White)
- **Error Color**: `#ff6b6b` (Red)

### Typography
- **Headers**: Arial Bold, 24pt
- **Subheaders**: Arial Bold, 12pt
- **Body Text**: Consolas Regular, 11pt
- **Buttons**: Arial Regular, 10pt

### Layout Principles
- **Responsive Design**: Adapts to window resizing
- **Consistent Spacing**: 10px margins, 5px padding
- **Visual Hierarchy**: Clear information organization
- **Accessibility**: High contrast ratios, keyboard navigation

### Interactive Elements
- **Hover Effects**: Button color changes on mouseover
- **Focus Indicators**: Clear focus outlines for keyboard users
- **Loading States**: Progress indicators for long operations
- **Context Menus**: Right-click options for advanced features

## Error Handling

### Network Errors
- **Connection Timeout**: Automatic retry with exponential backoff
- **API Unavailable**: Graceful degradation with offline mode
- **Invalid Responses**: User-friendly error messages
- **Rate Limiting**: Request throttling and queue management

### Data Validation
- **Input Sanitization**: XSS prevention and SQL injection protection
- **Type Checking**: Runtime type validation for all inputs
- **Range Validation**: Min/max value enforcement
- **Required Fields**: Mandatory field validation

### User Feedback
- **Status Messages**: Real-time operation status in status bar
- **Error Dialogs**: Modal error notifications with details
- **Success Confirmations**: Positive feedback for completed actions
- **Progress Indicators**: Loading bars for long-running operations

## Development Notes

### Code Structure
```
ui_app/
├── aceest_ui.py          # Main application class
├── requirements.txt      # Dependencies
├── README.md            # Documentation
└── [future modules]     # Additional components
```

### Key Classes
- **ACEestUIApp**: Main application controller
- **Login Screen**: Authentication interface
- **Dashboard**: Main application window
- **Modal Windows**: Specialized input dialogs

### Design Patterns
- **MVC Pattern**: Model-View-Controller separation
- **Observer Pattern**: Event-driven updates
- **Factory Pattern**: Dynamic UI component creation
- **Singleton Pattern**: Shared resource management

### Performance Considerations
- **Lazy Loading**: UI components loaded on demand
- **Caching**: API response caching for improved performance
- **Background Processing**: Non-blocking operations
- **Memory Management**: Efficient resource cleanup

## Troubleshooting

### Common Issues

#### API Connection Issues
**Problem**: "Failed to connect to API"
**Solutions**:
- Verify Flask API is running on port 5000
- Check firewall settings
- Confirm correct API_BASE_URL configuration
- Test API endpoint manually with curl/Postman

#### Chart Display Issues
**Problem**: Charts not rendering properly
**Solutions**:
- Ensure matplotlib and numpy are installed
- Check Tkinter backend compatibility
- Verify matplotlib version compatibility
- Try updating graphics drivers

#### Data Loading Errors
**Problem**: "Failed to load member/trainer data"
**Solutions**:
- Verify database file exists and is accessible
- Check API response format
- Ensure proper JSON parsing
- Validate member/trainer names

#### UI Responsiveness Issues
**Problem**: Application becomes unresponsive
**Solutions**:
- Check for infinite loops in event handlers
- Verify API calls are not blocking UI thread
- Monitor memory usage
- Close unused windows and dialogs

### Debug Mode
Enable debug logging by modifying the application:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log Files
Application logs are stored in:
- Windows: `%APPDATA%\ACEest\logs\`
- Linux/macOS: `~/.aceest/logs/`

### Performance Monitoring
Use Python's built-in profiler:
```bash
python -m cProfile aceest_ui.py
```

## Dependencies

### Core Dependencies
- **tkinter**: Python's standard GUI library (usually included)
- **requests==2.31.0**: HTTP library for API communication
- **matplotlib==3.7.2**: Charting and visualization library
- **numpy==1.24.3**: Numerical computing library

### Backend Dependencies (Flask App)
- **Flask==2.3.3**: Web framework
- **Flask-SQLAlchemy==3.0.5**: Database ORM
- **Flask-CORS==4.0.0**: Cross-origin resource sharing
- **python-dotenv==1.0.0**: Environment variable management

### Optional Dependencies
- **pandas**: Advanced data manipulation (future feature)
- **pillow**: Image processing (future feature)
- **reportlab**: PDF generation (future feature)

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Install development dependencies
4. Make your changes
5. Run tests and linting
6. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to all functions
- Include type hints where possible
- Write unit tests for new features

### Testing
```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python test_api.py

# Manual testing checklist
- [ ] Login functionality
- [ ] Member CRUD operations
- [ ] Workout logging
- [ ] Chart generation
- [ ] API error handling
```

### Documentation
- Update README.md for new features
- Add inline code comments
- Update API documentation
- Include usage examples

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### Third-Party Licenses
- **Flask**: BSD License
- **SQLAlchemy**: MIT License
- **matplotlib**: PSF License
- **requests**: Apache 2.0 License

## Version History

### Version 1.0.0 (Current)
- Initial release with full UI implementation
- Complete API integration
- Basic CRUD operations for all entities
- Charting and analytics features
- Trainer and subscription management

### Planned Features (Future Versions)
- **v1.1.0**: Advanced reporting and export features
- **v1.2.0**: Mobile app companion
- **v2.0.0**: Multi-location support and cloud sync
- **v2.1.0**: AI-powered workout recommendations

## Support

### Documentation
- [API Documentation](./flask_app/README.md)
- [UI User Guide](./docs/user-guide.md)
- [Developer Guide](./docs/developer-guide.md)

### Community
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and community support
- **Wiki**: Detailed guides and tutorials

### Contact
- **Email**: support@aceestfitness.com
- **Website**: https://aceestfitness.com
- **Documentation**: https://docs.aceestfitness.com

---

**ACEest Fitness & Gym Management System**
*Built with Python, Tkinter, and Flask*
*Professional fitness management made simple*