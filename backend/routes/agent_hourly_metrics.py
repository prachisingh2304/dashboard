from flask import Blueprint, jsonify
from config.sqlserver import get_connection
import traceback
agent_hourly_metrics_bp = Blueprint("agent_hourly_metrics", __name__)

@agent_hourly_metrics_bp.route("/agent_hourly_metrics", methods=["GET"])
def get_metrics():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                        SELECT * FROM agent_hourly_metrics
                        WHERE hour_timestamp >= DATEADD(HOUR, -1, GETDATE())
                    """)  
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

        return jsonify({"status": "success", "data": results})

    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()  # This prints full traceback to console
        return jsonify({"status": "error", "message": str(e)}), 500