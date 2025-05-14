from config.sqlserver import get_connection
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SQLServerService:
    @staticmethod
    def get_table_data(table):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            queries = {
                "onboarding": """
                        SELECT id, timestamp, email_address, full_name, phone_number, email_id,
                            job_position, google_drive_link,last_in_hand_salary, interview_status, reminder_status, results,
                            salary, doj, exit_date, days_left, 
                        FROM onboarding
                    """,
                "agents": """
                    SELECT a.agent, a.total_call_attempt, a.unique_dialed, a.connected,
                           a.total_call_duration, a.not_connected, a.call_back_later,
                           a.time_clock_hrs, a.status, o.full_name
                    FROM agents a
                    LEFT JOIN onboarding o ON a.agent = o.agent
                """,
                "agent_hourly_metrics": """
                    SELECT ahm.id, ahm.agent, ahm.total_call_attempt, ahm.unique_dialed,
                           ahm.connected, ahm.total_call_duration, ahm.not_connected,
                           ahm.call_back_later, ahm.hour_timestamp, o.full_name
                    FROM agent_hourly_metrics ahm
                    LEFT JOIN onboarding o ON ahm.agent = o.agent
                """,
                "calls": """
                    SELECT c.call_id, c.agent, c.duration, c.phone, c.connected_status,
                           c.call_back_status, c.date_time, o.full_name
                    FROM calls c
                    LEFT JOIN onboarding o ON c.agent = o.agent
                """,
                "key_assignment": """
                    SELECT ka.agent, ka.full_name, ka.business_developer_associate,
                           ka.date_of_exit, ka.date_of_joining, ka.assignable, o.full_name AS onboarding_full_name
                    FROM key_assignment ka
                    LEFT JOIN onboarding o ON ka.agent = o.agent
                """,
                "archives": """
                    SELECT a.agent, a.full_name, a.date_of_exit, a.attendance_count,
                           a.total_talktime, a.no_of_calls, o.full_name AS onboarding_full_name
                    FROM archives a
                    LEFT JOIN onboarding o ON a.agent = o.agent
                """
            }

            query = queries.get(table)
            if not query:
                raise ValueError(f"Invalid table name: {table}")

            cursor.execute(query)
            data = cursor.fetchall()  # Already returns dictionaries
            
            # Ensure full_name consistency
            if table == "onboarding":
                data = [{**row, "full_name": row.get("full_name", "")} for row in data]
            elif table in ["key_assignment", "archives"]:
                data = [
                    {
                        **row,
                        "full_name": row["full_name"],
                        "onboarding_full_name": row.get("onboarding_full_name", "")
                    }
                    for row in data
                ]
            else:
                data = [{**row, "full_name": row.get("full_name", "")} for row in data]

            logger.debug(f"Fetched {len(data)} rows from {table}")
            conn.close()
            return data
        except Exception as e:
            logger.error(f"Error fetching {table} data: {str(e)}")
            return []

    @staticmethod
    def get_table_columns(table):
        columns = {
            "agents": ["agent", "total_call_attempt", "unique_dialed", "connected", "total_call_duration", "not_connected", "call_back_later", "time_clock_hrs", "status", "full_name"],
            "onboarding": ["id","timestamp","email_address","full_name","phone_number","email_id","job_position","google_drive_link","last_in_hand_salary","interview_status","reminder_status","results","salary","doj","exit_date","days_left"],
            "agent_hourly_metrics": ["id", "agent", "total_call_attempt", "unique_dialed", "connected", "total_call_duration", "not_connected", "call_back_later", "hour_timestamp", "full_name"],
            "calls": ["call_id", "agent", "duration", "phone", "connected_status", "call_back_status", "date_time", "full_name"],
            "key_assignment": ["agent", "business_developer_associate", "date_of_exit", "date_of_joining", "assignable", "full_name", "onboarding_full_name"],
            "archives": ["agent", "full_name", "date_of_exit", "attendance_count", "total_talktime", "no_of_calls", "onboarding_full_name"]
        }
        return columns.get(table, [])
