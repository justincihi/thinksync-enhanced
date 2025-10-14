# WellTech AI MedSuite™ - AI Coding Agent Instructions

## Architecture Overview

This is a Flask-based healthcare AI platform (formerly ThinkSync™) for therapy session analysis with comprehensive user management. The system has a **dual-file architecture**:

- `app.py` - Main integrated application (Port 8080, SQLite, production-ready)
- `user_management.py` - Standalone user management module with separate database
- `admin_dashboard.py` - Blueprint-based admin interface with embedded HTML

### Key Architectural Patterns

**Database Strategy**: SQLite with context managers using `@contextmanager` and `with get_db()` pattern. Multiple databases:
- `welltech_medsuite.db` (main app)  
- `user_management.db` (user module)

**Authentication Flow**: JWT tokens + decorators (`@require_auth`, `@require_admin`, `@require_active_user`) with comprehensive audit logging.

**Frontend Integration**: React build files in `/static/` served by Flask, with mobile-optimized interface at `/mobile`.

## Critical Developer Workflows

### Local Development
```bash
python3 app.py  # Starts on port 8080
# Admin access: admin / 3942-granite-35
```

### Database Initialization
The app auto-creates SQLite schema on startup via `init_database()`. Default admin user created automatically.

### Authentication Testing
```bash
# Get JWT token
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin", "password": "3942-granite-35"}'

# Use in protected endpoints
curl -H "Authorization: Bearer <token>" http://localhost:8080/api/auth/profile
```

## Project-Specific Conventions

### Password Security
Uses SHA-256 with salt stored as `salt:hash` format. See `hash_password()` and `verify_password()` functions.

### Session Analysis Generation
The `generate_comprehensive_analysis()` function creates mock SOAP/BIRP notes. In production, this would integrate with OpenAI/Gemini APIs.

### File Upload Handling
Supports audio files (MP3, WAV, M4A, MP4) up to 100MB via multipart/form-data with validation in `create_session()`.

### Admin Dashboard Pattern
Uses Flask `render_template_string()` with embedded HTML/CSS/JS - see `admin_dashboard.py` for the complete self-contained interface pattern.

## Key Integration Points

### Deployment Options
- **Firebase**: Complete setup in `/firebase_deployment/` with Node.js functions
- **Google Cloud**: Deployment guides in `/deployment_guides/`
- **Local**: Direct Flask serving on port 8080

### Database Schema Evolution
Tables are created via `CREATE TABLE IF NOT EXISTS` with comprehensive fields for healthcare compliance (license tracking, audit logs, user preferences).

### API Response Pattern
Consistent JSON structure: `{'success': bool, 'message': str, 'data': object, 'error': str}`

## File Structure Importance

- `/static/` - React build output (index.html + assets/)
- `/firebase_deployment/` - Complete Firebase Cloud Functions setup
- `/deployment_guides/` - Multi-platform deployment documentation
- `requirements.txt` - Minimal deps (Flask, Flask-CORS, PyJWT)

## Security & Compliance Features

**Account Lockout**: 5 failed attempts = 30min lockout (see `authenticate_user()`)
**Audit Logging**: All actions logged to `audit_log` table with IP/user-agent
**Role-Based Access**: `admin` vs `clinician` roles with decorator enforcement
**Session Isolation**: Users can only access their own therapy sessions

## Development Anti-Patterns to Avoid

- Don't modify the dual-database architecture without understanding user isolation
- Avoid bypassing the JWT decorator system for protected endpoints  
- Don't change the SQLite row_factory pattern - breaks the dict-style access
- Never expose password hashes in API responses (see `get_profile()` implementation)

## Testing Workflows

**Neural Simulation**: `POST /api/therapy/demo` - No auth required, generates sample analysis
**File Upload Test**: Use `/mobile` interface or `POST /api/therapy/sessions` with multipart data
**Admin Functions**: Login as admin to test user approval/rejection workflows