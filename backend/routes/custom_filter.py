from flask import Blueprint, jsonify
from config.sqlserver import get_connection
import traceback

calls_bp = Blueprint("calls", __name__)

@calls_bp.route("/calls", methods=["POST"])
def get_agents():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT agent FROM calls")  # Check if this table exists
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

        return jsonify({"status": "success", "data": results})

    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()  # This prints full traceback to console
        return jsonify({"status": "error", "message": str(e)}), 500