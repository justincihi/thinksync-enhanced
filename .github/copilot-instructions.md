# WellTech AI MedSuite™ - AI Coding Agent Instructions

This document provides comprehensive guidance for AI coding agents working on the WellTech AI MedSuite™ (formerly ThinkSync™ Enhanced Edition) project.

## 🎯 Project Overview

**WellTech AI MedSuite™** is a professional clinical AI platform designed for mental health professionals to analyze therapy sessions and generate professional clinical documentation. The system provides advanced sentiment analysis, SOAP/BIRP note generation, complete user authentication, role-based access control, and session management capabilities.

### Key Technologies
- **Backend**: Python 3.11+, Flask 2.3+
- **Frontend**: React 18+, HTML5, JavaScript
- **Database**: SQLite (development), PostgreSQL (production), Firebase Firestore (cloud)
- **Authentication**: JWT tokens, password hashing with SHA-256
- **Deployment**: Firebase, Google Cloud Platform, Docker, Heroku
- **APIs**: OpenAI GPT-4, Google Gemini

## 📁 Architecture Overview

### Project Structure
```
thinksync-enhanced/
├── app.py                      # Main Flask application entry point
├── src/
│   └── main.py                # Production-ready main file (mirrors app.py)
├── static/                     # Frontend React build files
│   ├── index.html             # Main UI
│   ├── mobile-upload.html     # Mobile-optimized interface
│   ├── debug-upload-test.html # Debug/testing interface
│   └── assets/                # React compiled assets
├── firebase_deployment/        # Firebase deployment configuration
│   ├── firebase.json
│   ├── functions/
│   │   └── index.js           # Firebase Cloud Functions (mirrors Python API)
│   └── public/
├── deployment_guides/          # Deployment documentation
├── requirements.txt            # Python dependencies
└── README.md                  # Main project documentation
```

### Core Components

#### 1. Main Application (`app.py` and `src/main.py`)
- **Purpose**: Flask application serving REST API and static files
- **Key Responsibilities**:
  - User authentication and authorization
  - Therapy session management
  - File upload handling (audio/video)
  - Database operations
  - JWT token management
- **Port**: 8080 (default)

#### 2. Firebase Functions (`firebase_deployment/functions/index.js`)
- **Purpose**: Cloud deployment equivalent of Flask app
- **Key Responsibilities**:
  - Same API endpoints as Flask app
  - Firebase Authentication integration
  - Firestore database operations
- **Note**: Mirrors Python API structure but uses Node.js/Express

#### 3. Frontend (`static/`)
- **Main UI** (`index.html`): Primary React-based interface
- **Mobile UI** (`mobile-upload.html`): Mobile-optimized upload interface
- **Debug UI** (`debug-upload-test.html`): Testing and debugging interface
- **React Assets**: Pre-compiled React application in `assets/`

#### 4. Database Schema
- **users**: User authentication, profiles, and license information
- **therapy_sessions**: Session data, transcripts, analysis results
- **user_sessions**: Active session tokens and tracking
- **audit_log**: Security events and user actions
- **user_preferences**: User-specific settings

## 🔧 Development Workflows

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/justincihi/thinksync-enhanced.git
cd thinksync-enhanced

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Environment Variables

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|
| `OPENAI_API_KEY` | OpenAI GPT-4 API access | Yes (for AI features) | None |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google Gemini credentials JSON path | Yes (for AI features) | None |
| `SECRET_KEY` | Flask session secret | No | Auto-generated |
| `JWT_SECRET_KEY` | JWT token signing key | No | Auto-generated |

### Running the Application

```bash
# Development (with auto-reload)
python app.py

# Access at http://localhost:8080
# Admin credentials: admin / 3942-granite-35
```

### Testing Workflows

1. **Health Check**: `curl http://localhost:8080/api/health`
2. **Neural Simulation** (no file upload): Use demo endpoint `/api/therapy/demo`
3. **File Upload**: Use debug interface at `/debug-upload-test.html`
4. **Mobile Testing**: Use mobile interface at `/mobile`

## 📝 Project-Specific Conventions

### Code Style

#### Python
- **Indentation**: 4 spaces
- **Docstrings**: Triple-quoted strings at module/function/class level
- **Imports**: Standard library, third-party, local (separated by blank lines)
- **Line Length**: Generally 127 characters (GitHub editor width)
- **Naming**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods: `_leading_underscore`

#### JavaScript
- **Indentation**: 2 spaces
- **Style**: Modern ES6+ syntax
- **Async/Await**: Preferred over callbacks
- **Error Handling**: Try-catch blocks for async operations

### Database Patterns

#### Context Manager Pattern
```python
@contextmanager
def get_db():
    conn = sqlite3.connect('welltech_medsuite.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
```

Always use context managers for database connections to ensure proper cleanup.

#### Query Patterns
- Use parameterized queries (never string interpolation)
- Use `?` placeholders for SQLite
- Always commit after write operations

### Authentication Patterns

#### Decorators
```python
@require_auth          # Requires valid JWT token
@require_admin         # Requires admin role
@require_active_user   # Requires active user status
```

Apply decorators in this order: `@app.route` → `@require_auth` → `@require_admin`/`@require_active_user`

#### JWT Token Format
```python
{
  'user_id': int,
  'email': str,
  'role': 'admin' | 'clinician',
  'exp': timestamp
}
```

### API Response Format

#### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... }
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

### File Upload Conventions

#### Supported Formats
- Audio: `.mp3`, `.wav`, `.m4a`, `.ogg`
- Video: `.mp4`, `.webm`
- Max Size: 100MB

#### Upload Validation
1. Check file extension
2. Validate content type header
3. Check file size
4. Sanitize filename
5. Generate unique session ID

## 🔌 Integration Points

### REST API Endpoints

#### Public Endpoints (No Auth Required)
- `GET /api/health` - Health check
- `POST /api/therapy/demo` - Neural simulation demo
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

#### Protected Endpoints (Auth Required)
- `GET /api/auth/profile` - Get user profile
- `POST /api/auth/logout` - User logout
- `POST /api/therapy/sessions` - Create therapy session (with file upload)
- `GET /api/therapy/sessions` - List user sessions
- `GET /api/therapy/sessions/<id>` - Get specific session
- `PUT /api/therapy/sessions/<id>` - Update session
- `DELETE /api/therapy/sessions/<id>` - Delete session

#### Admin-Only Endpoints
- `GET /api/admin/users` - List all users
- `POST /api/admin/users/<id>/approve` - Approve user
- `POST /api/admin/users/<id>/reject` - Reject user
- `DELETE /api/admin/users/<id>` - Delete user
- `GET /api/admin/stats` - System statistics

### Authentication Flow

1. **Registration**: `POST /api/auth/register` → User created with `pending` status
2. **Admin Approval**: Admin approves via dashboard or API
3. **Login**: `POST /api/auth/login` → Returns JWT token
4. **API Access**: Include `Authorization: Bearer <token>` header
5. **Token Refresh**: Tokens expire after 24 hours (configurable)

### External API Integration

#### OpenAI GPT-4
- **Purpose**: Primary analysis engine for transcripts
- **Usage**: Analysis generation, sentiment analysis
- **Error Handling**: Graceful fallback to demo data if API fails

#### Google Gemini
- **Purpose**: Secondary validation and cross-verification
- **Usage**: Validation analysis, additional insights
- **Error Handling**: Optional, system works without it

## 🧪 Testing Guidelines

### Testing Strategy

Since the project currently has no automated test infrastructure:
- **Manual Testing**: Use debug interface at `/debug-upload-test.html`
- **API Testing**: Use curl, Postman, or provided test script `test_upload.sh`
- **Browser Testing**: Test on Chrome, Firefox, Safari, Edge
- **Mobile Testing**: Test on iOS Safari, Android Chrome

### Test Checklist

#### Authentication Tests
- [ ] User registration creates pending user
- [ ] Login fails for unapproved users
- [ ] Login succeeds for approved users with correct credentials
- [ ] JWT token is returned on successful login
- [ ] Protected endpoints require valid token
- [ ] Admin endpoints require admin role

#### File Upload Tests
- [ ] MP3 files upload successfully
- [ ] MP4 files upload successfully
- [ ] WAV, M4A, OGG files upload successfully
- [ ] Files >100MB are rejected
- [ ] Invalid file types are rejected
- [ ] Upload requires authentication

#### Session Management Tests
- [ ] Sessions are created with unique IDs
- [ ] Users can only see their own sessions
- [ ] Admins can see all sessions
- [ ] Sessions can be updated and deleted
- [ ] Transcript and analysis are saved correctly

### Testing Tools

#### Debug Interface
Access at `http://localhost:8080/debug-upload-test.html`
- Built-in file upload testing
- API endpoint testing
- Real-time activity logging
- Performance metrics

#### Shell Script
```bash
./test_upload.sh
```
Automated curl-based testing for all major endpoints

## 🚀 Deployment Guidelines

### Deployment Targets

#### 1. Local Development
```bash
python app.py
# Runs on http://localhost:8080
```

#### 2. Firebase (Recommended for Production)
```bash
cd firebase_deployment
./deploy-firebase.sh
```

#### 3. Google Cloud Platform
See `deployment_guides/GOOGLE_CLOUD_DEPLOYMENT.md`

#### 4. Docker
See `deployment_guides/DOCKER_DEPLOYMENT.md`

### Pre-Deployment Checklist

- [ ] Update version number in README.md
- [ ] Update release notes in RELEASE_NOTES_V3.md
- [ ] Test all authentication flows
- [ ] Test file upload functionality
- [ ] Verify environment variables are set
- [ ] Update Firebase configuration if needed
- [ ] Test database migrations
- [ ] Verify API endpoints work
- [ ] Check security headers and CORS
- [ ] Review audit logs

### Environment-Specific Configuration

#### Development
- SQLite database
- Debug mode enabled
- Detailed error messages
- Auto-reload enabled

#### Production
- PostgreSQL or Firestore
- Debug mode disabled
- Generic error messages
- SSL/TLS required
- Environment variable for secrets

## 🔒 Security Best Practices

### Authentication Security

1. **Password Storage**: SHA-256 with salt (consider upgrading to bcrypt)
2. **Token Security**: JWT with 24-hour expiration
3. **Rate Limiting**: Implement for login endpoints
4. **Account Lockout**: After 5 failed login attempts
5. **HTTPS Only**: All production traffic must use HTTPS

### Data Security

1. **Input Validation**: Validate all user inputs
2. **SQL Injection Prevention**: Use parameterized queries only
3. **XSS Prevention**: Sanitize all user-generated content
4. **CSRF Protection**: Implement CSRF tokens for state-changing operations
5. **File Upload Security**: Validate file types, sizes, and scan for malware

### HIPAA Compliance Considerations

1. **Data Encryption**: Encrypt sensitive data at rest and in transit
2. **Access Logs**: Maintain comprehensive audit logs
3. **User Isolation**: Users can only access their own data
4. **Admin Oversight**: Admins can monitor but not modify clinical data
5. **Data Retention**: Implement appropriate retention policies

## 📚 Key Files and Their Purposes

### Python Files
- **app.py**: Main application entry point (Flask app, routes, authentication)
- **src/main.py**: Production copy of app.py (same functionality)
- **user_management.py**: User management utilities (if separate)
- **auth_routes.py**: Authentication route handlers (if separate)
- **admin_dashboard.py**: Admin-specific functionality (if separate)

### Configuration Files
- **requirements.txt**: Python dependencies (Flask, Flask-CORS, PyJWT, Werkzeug)
- **firebase.json**: Firebase hosting and functions configuration
- **.github/workflows/python-app.yml**: GitHub Actions CI/CD pipeline

### Documentation Files
- **README.md**: Main project documentation
- **DEPLOYMENT_V3.md**: Deployment guide for v3.0.0
- **DEBUG_GUIDE.md**: Debugging and troubleshooting guide
- **DEBUG_README.md**: Quick reference for debugging
- **QUICK_START.md**: Quick start guide
- **RELEASE_NOTES_V3.md**: Release notes for v3.0.0
- **UPLOAD_VERIFICATION_REPORT.md**: File upload verification documentation

### Frontend Files
- **static/index.html**: Main React application UI
- **static/mobile-upload.html**: Mobile-optimized upload interface
- **static/debug-upload-test.html**: Comprehensive testing interface
- **static/assets/**: Compiled React application and images

## 🎨 UI/UX Guidelines

### Design Principles
- **Medical Professional Focus**: Clean, professional, clinical interface
- **Accessibility**: WCAG 2.1 compliant
- **Responsive**: Works on desktop, tablet, and mobile
- **Futuristic Medical Theme**: Blue/teal color scheme with gradients

### Color Scheme
- Primary: Blue/Teal gradient
- Accent: Purple/Pink
- Success: Green
- Warning: Yellow/Orange
- Error: Red
- Background: Dark theme with subtle gradients

### Typography
- Headings: System fonts, bold
- Body: System fonts, regular
- Code: Monospace

## 🔄 Version Control Guidelines

### Branch Strategy
- **main**: Production-ready code
- **develop**: Development branch
- **feature/**: Feature branches
- **hotfix/**: Urgent production fixes

### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Request Requirements
- Descriptive title and description
- Reference related issues
- All tests pass (when tests exist)
- Code reviewed by at least one person
- No merge conflicts

## 🐛 Debugging Tips

### Common Issues

#### Database Lock Errors
- **Cause**: Multiple simultaneous writes to SQLite
- **Solution**: Use context managers, ensure connections close properly

#### JWT Token Expired
- **Cause**: Token older than 24 hours
- **Solution**: Re-login to get new token

#### File Upload Fails
- **Cause**: Missing authentication, file too large, wrong format
- **Solution**: Check token, file size <100MB, supported format

#### CORS Errors
- **Cause**: Frontend/backend on different origins
- **Solution**: Ensure CORS configured correctly in Flask app

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Useful Debug Endpoints
- `/api/health` - Check system status
- `/debug-upload-test.html` - Interactive testing interface
- Browser DevTools Network tab - Monitor API requests

## 📊 Performance Considerations

### Optimization Tips
1. **Database Queries**: Use indexes for frequently queried columns
2. **File Processing**: Process files asynchronously when possible
3. **Caching**: Cache analysis results for duplicate sessions
4. **Connection Pooling**: Use connection pooling for production databases
5. **Static Assets**: Use CDN for static files in production

### Resource Limits
- **Max Upload Size**: 100MB per file
- **Token Expiration**: 24 hours
- **Session Timeout**: 30 minutes of inactivity
- **Max Concurrent Users**: Depends on deployment (Flask: ~1000, Firebase: scalable)

## 🎯 Best Practices for AI Agents

### When Making Changes

1. **Understand Context**: Read relevant documentation first
2. **Minimal Changes**: Make the smallest change that solves the problem
3. **Test Thoroughly**: Test your changes before committing
4. **Follow Patterns**: Match existing code patterns and styles
5. **Update Documentation**: Update docs if changing public APIs
6. **Security First**: Never introduce security vulnerabilities
7. **Preserve Functionality**: Don't break existing features

### Code Generation Guidelines

1. **Use Existing Patterns**: Follow patterns already in the codebase
2. **Include Error Handling**: Always handle potential errors
3. **Add Comments Sparingly**: Comment complex logic, not obvious code
4. **Validate Inputs**: Always validate user inputs
5. **Use Type Hints**: Add type hints for Python 3.11+
6. **Follow Naming Conventions**: Use established naming patterns

### What NOT to Do

1. ❌ Don't remove working code unless absolutely necessary
2. ❌ Don't introduce new dependencies without justification
3. ❌ Don't change security-critical code without careful review
4. ❌ Don't hard-code credentials or secrets
5. ❌ Don't break API compatibility without version bump
6. ❌ Don't ignore linting errors (flake8)
7. ❌ Don't commit generated files (databases, logs, __pycache__)

## 📞 Contact and Support

### Project Information
- **Project Name**: WellTech AI MedSuite™ (formerly ThinkSync™ Enhanced Edition)
- **Developer**: Justin Cihi
- **Organization**: Cadenza Therapeutics™
- **License**: Proprietary
- **Repository**: https://github.com/justincihi/thinksync-enhanced

### Regulatory Compliance
This application is part of final vetting by the NIH, FDA, and HIPAA regulatory bodies governing AI in Healthcare. The system is designed as an informational aid to enhance (not replace) human clinician diagnostic and treatment capabilities.

---

**Last Updated**: 2024-10-14  
**Document Version**: 1.0.0  
**Compatible with**: WellTech AI MedSuite™ v3.0.0+
