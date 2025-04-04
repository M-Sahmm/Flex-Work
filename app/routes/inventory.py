import os
import time
from flask import Flask, request, session, jsonify, render_template, redirect, url_for, flash, send_from_directory, abort
from werkzeug.utils import secure_filename
from app.utils.db_utils import execute_query, execute_single_query, execute_write_query, DatabaseError

# File upload settings
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def inventory():
    if 'user_id' not in session:
        return redirect(url_for('login_credentials'))
        
    try:
        # Get user's inventory items
        items = execute_query('''
            SELECT * FROM inventory 
            WHERE user_id = ?
            ORDER BY date_added DESC
        ''', (session['user_id'],))
        
        return render_template('inventory.html', items=items, username=session.get('username', 'User'))
        
    except DatabaseError as e:
        flash('Error loading inventory')
        print(f"Database error: {str(e)}")
        return redirect(url_for('dashboard'))

def add_inventory_item():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    name = request.form.get('name')
    description = request.form.get('description')
    file_type = request.form.get('file_type', 'url')  # url or file
    url = request.form.get('url')
    
    if not name or not file_type:
        return jsonify({'error': 'Name and file type are required'}), 400
        
    try:
        if file_type == 'file':
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
                
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
                
            if not allowed_file(file.filename):
                return jsonify({'error': 'File type not allowed'}), 400
                
            # Get the actual file extension
            actual_file_type = file.filename.rsplit('.', 1)[1].lower()
                
            # Create a unique filename to prevent overwrites
            filename = f"{session['user_id']}_{int(time.time())}_{secure_filename(file.filename)}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Ensure upload directory exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Save file
            try:
                file.save(filepath)
            except Exception as e:
                print(f"Error saving file: {str(e)}")
                return jsonify({'error': 'Failed to save file'}), 500
            
            # Create inventory item with file and actual file type
            item_id = execute_write_query('''
                INSERT INTO inventory (user_id, name, description, file_type, file_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (session['user_id'], name, description, actual_file_type, filename))
            
        else:  # url type
            if not url:
                return jsonify({'error': 'URL is required for URL type items'}), 400
                
            # Create inventory item with URL
            item_id = execute_write_query('''
                INSERT INTO inventory (user_id, name, description, file_type, url)
                VALUES (?, ?, ?, ?, ?)
            ''', (session['user_id'], name, description, file_type, url))
            
        # Get the created item
        item = execute_single_query(
            'SELECT * FROM inventory WHERE id = ?',
            (item_id,)
        )
        
        return jsonify({
            'message': 'Item added successfully',
            'item': dict(item)
        })
        
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Failed to add inventory item'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to process file'}), 500

def delete_inventory_item(item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    try:
        # Get item details
        item = execute_single_query(
            'SELECT * FROM inventory WHERE id = ? AND user_id = ?',
            (item_id, session['user_id'])
        )
        
        if not item:
            return jsonify({'error': 'Item not found or unauthorized'}), 404
            
        # If it's a file type item, delete the file
        if item['file_type'] in ['pdf', 'docx', 'csv'] and item['file_path']:
            try:
                file_path = os.path.join(UPLOAD_FOLDER, item['file_path'])
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file: {str(e)}")
                # Continue with deletion even if file removal fails
                
        # Delete the inventory item
        execute_write_query(
            'DELETE FROM inventory WHERE id = ? AND user_id = ?',
            (item_id, session['user_id'])
        )
        
        return jsonify({'message': 'Item deleted successfully'})
        
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Failed to delete inventory item'}), 500

def download_file(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login_credentials'))
        
    try:
        # Get item and verify ownership
        item = execute_single_query('''
            SELECT * FROM inventory 
            WHERE id = ? AND user_id = ?
        ''', (item_id, session['user_id']))
        
        if not item:
            abort(404)  # Item not found or doesn't belong to user
            
        if item['file_type'] == 'url':
            return redirect(item['url'])  # Redirect to URL if it's a URL type item
            
        if not item['file_path']:
            abort(404)  # No file associated with this item
            
        # Get the original filename from the stored path
        filename = item['file_path'].split('_', 2)[-1]  # Get part after user_id and timestamp
        
        try:
            return send_from_directory(
                UPLOAD_FOLDER,
                item['file_path'],
                as_attachment=True,
                download_name=filename  # Use original filename for download
            )
        except FileNotFoundError:
            abort(404)  # File not found in filesystem
            
    except DatabaseError as e:
        print(f"Database error in download: {str(e)}")
        abort(500)
    except Exception as e:
        print(f"Error in download: {str(e)}")
        abort(500)

def preview_file(item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    try:
        # Get item and verify ownership
        item = execute_single_query('''
            SELECT * FROM inventory 
            WHERE id = ? AND user_id = ?
        ''', (item_id, session['user_id']))
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
            
        # Handle different file types
        if item['file_type'] == 'url':
            return jsonify({
                'url': item['url']
            })
            
        if not item['file_path']:
            return jsonify({'error': 'No file associated with this item'}), 404
            
        file_path = os.path.join(UPLOAD_FOLDER, item['file_path'])
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        file_type = item['file_type'].lower() if item['file_type'] else ''
        
        try:
            if file_type == 'pdf':
                return send_from_directory(
                    UPLOAD_FOLDER,
                    item['file_path'],
                    mimetype='application/pdf',
                    as_attachment=False
                )
                
            elif file_type == 'csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                html_table = df.to_html(classes='preview-table', index=False)
                return jsonify({
                    'html': html_table
                })
                
            elif file_type == 'docx':
                from docx import Document
                doc = Document(file_path)
                html_content = ['<div class="docx-preview">']
                
                for paragraph in doc.paragraphs:
                    if paragraph.text:
                        html_content.append(f'<p>{paragraph.text}</p>')
                        
                html_content.append('</div>')
                return jsonify({
                    'html': '\n'.join(html_content)
                })
            else:
                return jsonify({'error': f'Unsupported file type: {file_type}'}), 400
                
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        