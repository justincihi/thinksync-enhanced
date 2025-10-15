# File Management System - User Guide

## Overview

The ThinkSync application now includes a comprehensive file management system that allows users to upload, store, download, and manage audio files associated with therapy sessions.

## Features

### 1. **Automatic File Storage**
When you upload an audio file for session analysis, the file is automatically saved to the server with a unique filename that includes:
- Your user ID
- Upload timestamp
- Original filename

Example: `1_20251012_143022_counseling_session.mp3`

### 2. **File Download**
You can download any audio file you've previously uploaded by accessing the download endpoint with the session ID.

### 3. **File Listing**
View all your uploaded files with details including:
- Session ID
- Client name
- Original filename
- File size
- Upload date
- File existence status

### 4. **File Deletion**
Remove uploaded files you no longer need. This will:
- Delete the physical file from the server
- Update the database to remove the file reference
- Keep the session analysis data intact

## API Endpoints

### List All Files
**Endpoint:** `GET /api/files/list`

**Authentication:** Required (JWT token)

**Response:**
```json
{
  "success": true,
  "files": [
    {
      "id": 1,
      "sessionId": "session_20251012_143022",
      "clientName": "John Doe",
      "fileName": "1_20251012_143022_session.mp3",
      "fileSize": 2458624,
      "uploadDate": "2025-10-12 14:30:22",
      "fileExists": true
    }
  ]
}
```

### Download File
**Endpoint:** `GET /api/files/<session_id>/download`

**Authentication:** Required (JWT token)

**Parameters:**
- `session_id` (integer): The database ID of the therapy session

**Response:** File download with appropriate filename

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://0vhlizcgej03.manus.space/api/files/1/download \
  -o downloaded_file.mp3
```

### Delete File
**Endpoint:** `DELETE /api/files/<session_id>`

**Authentication:** Required (JWT token)

**Parameters:**
- `session_id` (integer): The database ID of the therapy session

**Response:**
```json
{
  "success": true,
  "message": "File deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://0vhlizcgej03.manus.space/api/files/1
```

## Security Features

### Access Control
- **User Isolation**: Users can only access their own files
- **Admin Override**: Admin users can access all files (for support purposes)
- **JWT Authentication**: All endpoints require valid authentication tokens

### File Validation
- **File Type Checking**: Only allowed audio formats (.mp3, .wav, .m4a, .mp4, .webm, .ogg)
- **Size Limits**: Maximum file size enforced (100MB default)
- **Unique Filenames**: Prevents filename collisions

### Data Integrity
- **Database Tracking**: All file operations are logged in the database
- **Orphan Prevention**: File paths are stored with session data
- **Audit Trail**: File operations are logged for security monitoring

## Storage Location

Files are stored in the `uploads/` directory with the following structure:

```
uploads/
├── README.md
├── 1_20251012_143022_session1.mp3
├── 1_20251012_150045_session2.wav
├── 2_20251012_160000_client_recording.mp4
└── ...
```

## Database Schema

The `therapy_sessions` table has been updated to include:

```sql
ALTER TABLE therapy_sessions ADD COLUMN file_path TEXT;
```

This column stores the relative path to the uploaded file (e.g., `uploads/1_20251012_143022_session.mp3`)

## Usage Examples

### JavaScript/Frontend Example

```javascript
// List all files
async function listFiles() {
  const response = await fetch('/api/files/list', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  console.log(data.files);
}

// Download a file
function downloadFile(sessionId, filename) {
  window.location.href = `/api/files/${sessionId}/download`;
}

// Delete a file
async function deleteFile(sessionId) {
  const response = await fetch(`/api/files/${sessionId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  console.log(data.message);
}
```

### Python Example

```python
import requests

# Your JWT token
token = "your_jwt_token_here"
headers = {"Authorization": f"Bearer {token}"}

# List files
response = requests.get(
    "https://0vhlizcgej03.manus.space/api/files/list",
    headers=headers
)
files = response.json()['files']

# Download file
session_id = 1
response = requests.get(
    f"https://0vhlizcgej03.manus.space/api/files/{session_id}/download",
    headers=headers
)
with open("downloaded_file.mp3", "wb") as f:
    f.write(response.content)

# Delete file
response = requests.delete(
    f"https://0vhlizcgej03.manus.space/api/files/{session_id}",
    headers=headers
)
print(response.json())
```

## Error Handling

### Common Error Responses

**404 Not Found**
```json
{
  "error": "Session not found or access denied"
}
```
- The session doesn't exist
- You don't have permission to access this file

**404 File Not Found**
```json
{
  "error": "File not found"
}
```
- The file was deleted from the filesystem
- The file path in the database is incorrect

**500 Internal Server Error**
```json
{
  "error": "Download failed"
}
```
- Server error during file operation
- Check server logs for details

## Best Practices

1. **Regular Cleanup**: Periodically delete old files you no longer need
2. **File Naming**: Use descriptive original filenames for easier identification
3. **Backup**: Important files should be downloaded and backed up locally
4. **Privacy**: Remember that uploaded files contain sensitive client information
5. **Storage Limits**: Monitor your storage usage to avoid exceeding limits

## Troubleshooting

### File Not Appearing in List
- Ensure the file was successfully uploaded
- Check that authentication is working correctly
- Verify the session was created successfully

### Download Fails
- Check that the file still exists on the server
- Verify you have permission to access the file
- Ensure your JWT token is valid and not expired

### Upload Fails
- Check file format is supported
- Verify file size is within limits
- Ensure you're authenticated

## Future Enhancements

Planned features for future releases:
- Bulk file operations
- File sharing between users
- Automatic transcription integration
- Cloud storage integration (S3, Google Cloud Storage)
- File compression and optimization
- Advanced search and filtering

## Support

For issues or questions about file management:
- Check the application logs for error details
- Contact your system administrator
- Submit an issue on GitHub: https://github.com/justincihi/thinksync-enhanced/issues

---

**Last Updated:** October 12, 2025  
**Version:** 3.1.0

