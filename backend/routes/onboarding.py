# routes/onboarding.py

from flask import Blueprint, jsonify
from config.sqlserver import get_connection
import traceback

onboarding_bp = Blueprint('onboarding', __name__)



@onboarding_bp.route('/onboarding/users', methods=['GET'])
def get_onboarding_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM onboarding")  # Check if this table exists
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

        return jsonify({"status": "success", "data": results})

    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()  # This prints full traceback to console
        return jsonify({"status": "error", "message": str(e)}), 500
