from flask import Flask
from flask_cors import CORS
from property import property_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.register_blueprint(property_bp)

if __name__ == "__main__":
    app.run(debug=True)
