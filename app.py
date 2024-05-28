from flask import Flask, jsonify, request
from property import property_bp

app = Flask(__name__)

app.register_blueprint(property_bp)

if __name__ == "__main__":
    app.run(debug=True)
