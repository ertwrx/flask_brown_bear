# main/routes/__init__.py
from flask import Blueprint, render_template, Response, abort
from main.models import StaticFile
from main import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/static_db/<path:filename>')
def serve_static_from_db(filename):
    print(f"Attempting to serve: {filename}")

    # Try the exact filename first
    file = StaticFile.query.filter_by(filename=filename).first()
    if file:
        print(f"Found file at {filename}")
        response = Response(file.data, mimetype=file.content_type)
        response.headers['Cache-Control'] = 'public, max-age=86400'
        return response

    # If not found, try with common subdirectories
    for subdir in ['images', 'js', 'audio']:
        path = f"{subdir}/{filename}"
        print(f"Trying path: {path}")
        file = StaticFile.query.filter_by(filename=path).first()
        if file:
            print(f"Found file at {path}")
            response = Response(file.data, mimetype=file.content_type)
            response.headers['Cache-Control'] = 'public, max-age=86400'
            return response

    print(f"File {filename} not found in database")
    abort(404)
    
    print(f"Serving {filename} ({len(file.data)} bytes)")
    response = Response(file.data, mimetype=file.content_type)
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response

def register_routes(app):
    app.register_blueprint(main_bp)
