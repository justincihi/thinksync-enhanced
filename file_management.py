"""
File Management Module for ThinkSync
Handles file upload, download, and management
"""

import os
import logging
from flask import jsonify, send_from_directory, request
from functools import wraps

logger = logging.getLogger(__name__)

def add_file_management_routes(app, get_db, require_auth):
    """Add file management routes to the Flask app"""
    
    @app.route('/api/files/<int:session_id>/download')
    @require_auth
    def download_file(session_id):
        """Download the audio file associated with a session"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT file_path, client_name FROM therapy_sessions 
                    WHERE id = ? AND user_id = ?
                ''', (session_id, request.current_user['user_id']))
                session = cursor.fetchone()
                
                if not session:
                    return jsonify({'error': 'Session not found or access denied'}), 404
                
                file_path = session['file_path']
                if not file_path or not os.path.exists(file_path):
                    return jsonify({'error': 'File not found'}), 404
                
                return send_from_directory(
                    os.path.dirname(file_path),
                    os.path.basename(file_path),
                    as_attachment=True,
                    download_name=f"{session['client_name']}_{os.path.basename(file_path)}"
                )
        except Exception as e:
            logger.error(f"File download error: {e}")
            return jsonify({'error': 'Download failed'}), 500

    @app.route('/api/files/list')
    @require_auth
    def list_files():
        """List all uploaded files for the current user"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, session_id, client_name, file_path, created_at 
                    FROM therapy_sessions 
                    WHERE user_id = ? AND file_path IS NOT NULL
                    ORDER BY created_at DESC
                ''', (request.current_user['user_id'],))
                sessions = cursor.fetchall()
                
                files = []
                for session in sessions:
                    file_path = session['file_path']
                    file_exists = os.path.exists(file_path) if file_path else False
                    file_size = os.path.getsize(file_path) if file_exists else 0
                    
                    files.append({
                        'id': session['id'],
                        'sessionId': session['session_id'],
                        'clientName': session['client_name'],
                        'fileName': os.path.basename(file_path) if file_path else None,
                        'fileSize': file_size,
                        'uploadDate': session['created_at'],
                        'fileExists': file_exists
                    })
                
                return jsonify({'success': True, 'files': files})
        except Exception as e:
            logger.error(f"File list error: {e}")
            return jsonify({'error': 'Failed to list files'}), 500

    @app.route('/api/files/<int:session_id>', methods=['DELETE'])
    @require_auth
    def delete_file(session_id):
        """Delete the audio file associated with a session"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT file_path FROM therapy_sessions 
                    WHERE id = ? AND user_id = ?
                ''', (session_id, request.current_user['user_id']))
                session = cursor.fetchone()
                
                if not session:
                    return jsonify({'error': 'Session not found or access denied'}), 404
                
                file_path = session['file_path']
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"File deleted: {file_path}")
                
                # Update database to remove file_path
                cursor.execute('''
                    UPDATE therapy_sessions 
                    SET file_path = NULL 
                    WHERE id = ?
                ''', (session_id,))
                conn.commit()
                
                return jsonify({'success': True, 'message': 'File deleted successfully'})
        except Exception as e:
            logger.error(f"File deletion error: {e}")
            return jsonify({'error': 'Deletion failed'}), 500

def save_uploaded_file(uploaded_file, user_id, upload_dir='uploads'):
    """
    Save an uploaded file to disk
    
    Args:
        uploaded_file: FileStorage object from request.files
        user_id: ID of the user uploading the file
        upload_dir: Directory to save files to
        
    Returns:
        tuple: (file_path, file_info) or (None, error_message)
    """
    try:
        from datetime import datetime
        
        # Create uploads directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{user_id}_{timestamp}_{uploaded_file.filename}"
        file_path = os.path.join(upload_dir, safe_filename)
        
        # Save file to disk
        uploaded_file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        file_info = {
            'original_name': uploaded_file.filename,
            'size': file_size,
            'type': uploaded_file.content_type,
            'path': file_path
        }
        
        logger.info(f"File saved: {file_path} ({file_size} bytes)")
        
        return file_path, file_info
        
    except Exception as e:
        logger.error(f"File save error: {e}")
        return None, str(e)

