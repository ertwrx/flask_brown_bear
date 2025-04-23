from flask import render_template, Blueprint

# Create a blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# Add more routes here as needed
# @main_bp.route('/about')
# def about():
#     return render_template('about.html')

def register_routes(app):
    """Register all blueprints to the app."""
    app.register_blueprint(main_bp)
    
    # Register other blueprints here if you have them
    # app.register_blueprint(other_bp, url_prefix='/other')
