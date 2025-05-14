from flask import Blueprint, jsonify
from config.sqlserver import get_connection
import traceback
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

archives_bp = Blueprint("archives", __name__)

@archives_bp.route("/archives", methods=["GET"])
def get_archives():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM archives")  # Check if this table exists
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

        return jsonify({"status": "success", "data": results})

    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()  # This prints full traceback to console
        return jsonify({"status": "error", "message": str(e)}), 500