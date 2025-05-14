from flask import Blueprint, jsonify
from config.sqlserver import get_connection
import traceback

agents_bp = Blueprint("agents", __name__)

@agents_bp.route("/agents", methods=["GET"])
def get_agents():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM agents")  # Check if this table exists
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

        return jsonify({"status": "success", "data": results})

    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()  # This prints full traceback to console
        return jsonify({"status": "error", "message": str(e)}), 500