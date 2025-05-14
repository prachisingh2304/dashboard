from flask import Blueprint, jsonify, request
from config.sqlserver import get_connection
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

calls_bp = Blueprint("calls", __name__)

@calls_bp.route("/calls", methods=["GET"])
def get_calls():
    try:
        days = request.args.get("days", type=int)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        if days is not None and days >= 0:
            date_threshold = datetime.utcnow() - timedelta(days=days)
            query = """
                SELECT c.call_id, c.agent, c.duration, c.phone, c.connected_status,
                       c.call_back_status, c.date_time, o.full_name
                FROM calls c
                LEFT JOIN onboarding o ON c.agent = o.agent
                WHERE c.date_time >= %s
            """
            cursor.execute(query, (date_threshold,))
            logger.debug(f"Days filter: {days}, Date threshold: {date_threshold}")
        else:
            query = """
                SELECT c.call_id, c.agent, c.duration, c.phone, c.connected_status,
                       c.call_back_status, c.date_time, o.full_name
                FROM calls c
                LEFT JOIN onboarding o ON c.agent = o.agent
            """
            cursor.execute(query)
        
        data = cursor.fetchall()  # Results are already dictionaries
        data = [{**row, "full_name": row.get("full_name", "")} for row in data]
        
        logger.debug(f"Query returned {len(data)} calls")
        conn.close()
        
        if not data:
            logger.warning("No calls found")
            return jsonify([]), 200
        
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error fetching calls: {str(e)}")
        return jsonify({"error": f"Failed to fetch calls: {str(e)}"}), 500
