import os
from flask import Flask, send_from_directory
from flask_cors import CORS

# Import blueprints
from routes.agents import agents_bp
from routes.onboarding import onboarding_bp
from routes.calls import calls_bp
from routes.key_assignment import key_assignment_bp
from routes.agent_hourly_metrics import agent_hourly_metrics_bp
from routes.archives import archives_bp

# Initialize Flask app with proper configuration
app = Flask(__name__, static_folder=None)
CORS(app)

# ================= Frontend Configuration =================
# Get absolute path to frontend directory
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(current_dir, '../frontend')

# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(frontend_path, path)

# ================= API Routes =================
app.register_blueprint(agents_bp, url_prefix="/api")
app.register_blueprint(onboarding_bp, url_prefix="/api")
app.register_blueprint(calls_bp, url_prefix="/api")
app.register_blueprint(key_assignment_bp, url_prefix="/api")
app.register_blueprint(agent_hourly_metrics_bp, url_prefix="/api")
app.register_blueprint(archives_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
