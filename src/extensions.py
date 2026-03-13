from flask_cors import CORS

def init_extensions(app):
    """Initialize Flask extensions"""
    
    # CORS configuration
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
