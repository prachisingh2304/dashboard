from flask import Blueprint, jsonify
from config.sqlserver import get_connection
import traceback
from datetime import datetime

key_assignment_bp = Blueprint("key_assignment", __name__)

# Predefined list of agents
agents = [
    "KzQARb", "0BISAf", "XnuAZc", "oeoxBz", "WPfVFG", "U1s0kd", "zSBAz5", "2NSii6",
    "1xztsE", "7vW55G", "a0s9aX", "XDywrS", "0FFbo8", "rTgrdF", "Afr2Cx", "51jJTm",
    "BmAVtT", "Rnl32J", "qYtZ70", "atzKg1", "2FiYkP", "uSifeY", "NpBHJ3", "ZH1jIz",
    "3xQ3kk", "qkQvS9", "7rekQG", "zF4vAE", "WAZE46", "CoqMPq", "tQk0rH", "ocSKNg",
    "gGPvZf", "tuG7VI", "ZtoYp4", "Y3Ini9", "Xo6zqu", "xA5Vk8", "f5RYkI", "0j7ra0",
    "ul5r5T", "hmulNk", "xVrkcx", "74diWG", "vGXisN", "lTUOJu", "3yT3At", "lhJUOf",
    "ADwIbN", "12xFJV", "iTSaXc", "11JKxz", "1sTbJS", "AzDAvV", "BkR9iD", "Mezduh",
    "hVfLRy", "zq39o3", "qT1lEK", "Q3U9Sh", "6VPpTP", "V4rux0", "iv3yQY", "vSZpKT",
    "BBB0Su", "rlytMw", "38rEF0", "EQ6KqH", "dhH8M9", "ZQxIdY", "4QvTsq", "fWH2Mi",
    "yMo01L", "dNBQJy", "ggwJYW", "C5loKj", "qFKTSP", "fwnVkh", "SVK9HR", "nt5QIX",
    "3ZiCr6", "zOieFd", "zKhBGH", "FWfhvb", "JYDzqA", "veLtsc", "EMH8N6", "N3QZtd",
    "J5M2Bv", "YZTnWm", "bUc3C9", "XPNwDd", "VPzqPr", "UmPWqr", "hAYYSr", "wjqC7R",
    "av12Ys", "FWZCDg", "TQldbr", "kQFy3L"
]

@key_assignment_bp.route("/key_assignment", methods=["POST"])
def assign_keys_to_new_joinees():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Step 1: Insert agents from the predefined list into the database if not already present
        for agent in agents:
            cursor.execute(""" 
                SELECT COUNT(*) FROM key_assignment WHERE agent = ? 
            """, (agent,))
            if cursor.fetchone()[0] == 0:  # If agent doesn't exist in the database
                cursor.execute("""
                    INSERT INTO key_assignment (agent, full_name, doj, exit_date, assignable, business_developer_associate)
                    VALUES (?, NULL, NULL, NULL, 'Yes', 'No')
                """, (agent,))
        
        conn.commit()

        # Step 2: Fetch BDAs who joined today or in future
        today = datetime.now().date()
        cursor.execute("""
            SELECT DISTINCT full_name, doj, exit_date
            FROM onboarding
            WHERE job_position = 'business development associate'
              AND doj >= ?
        """, (today,))
        users = cursor.fetchall()
        if not users:
            return jsonify({"status": "success", "message": "No BDAs to assign today."})

        # Step 3: Get available, unassigned agents from key_assignment
        cursor.execute("""
            SELECT agent FROM key_assignment
            WHERE assignable = 'Yes'
              AND business_developer_associate = 'No'
            ORDER BY assignable DESC
        """)
        available_keys = [row[0] for row in cursor.fetchall()]

        assigned = []

        # Step 4: Assign available keys to BDAs
        for i, user in enumerate(users):
            if i >= len(available_keys):
                break  # Not enough keys

            full_name, doj, exit_date = user
            agent_key = available_keys[i]

            # Ensure key is from predefined list and not already assigned
            if agent_key in agents:
                cursor.execute("""
                    SELECT COUNT(*) FROM key_assignment
                    WHERE agent = ? AND business_developer_associate = 'Yes'
                """, (agent_key,))
                if cursor.fetchone()[0] > 0:
                    continue  # If already assigned to a BDA, skip

                # Check if the user already has an assignment for the same full_name and doj
                cursor.execute("""
                    SELECT COUNT(*) FROM key_assignment
                    WHERE full_name = ? AND doj = ? 
                """, (full_name, doj))
                
                if cursor.fetchone()[0] > 0:
                    continue  # Skip if this combination already exists

                # Insert into key_assignment if no duplicate
                cursor.execute("""
                    INSERT INTO key_assignment (agent, full_name, doj, exit_date, assignable, business_developer_associate)
                    VALUES (?, ?, ?, ?, 'No', 'Yes')
                """, (agent_key, full_name, doj, exit_date))

                # Mark as not assignable
                cursor.execute("""
                    UPDATE key_assignment
                    SET assignable = 'No'
                    WHERE agent = ?
                """, (agent_key,))

                assigned.append({
                    "agent": agent_key,
                    "full_name": full_name,
                    "doj": str(doj),
                    "exit_date": str(exit_date)
                })

        conn.commit()

        # Step 5: Archive expired records
        cursor.execute("""
            SELECT agent, full_name, exit_date
            FROM key_assignment
            WHERE exit_date < ?
        """, (today,))
        expired = cursor.fetchall()

        for agent, full_name, exit_date in expired:
            cursor.execute("""
                INSERT INTO archives (agent, full_name, date_of_exit)
                VALUES (?, ?, ?)
            """, (agent, full_name, exit_date))

            cursor.execute("""
                DELETE FROM key_assignment WHERE agent = ?
            """, (agent,))

        conn.commit()

        # Step 6: Remove duplicates (for cases where an agent may have multiple records in key_assignment)
        cursor.execute("""
            DELETE FROM key_assignment
            WHERE agent IN (
                SELECT agent
                FROM key_assignment
                GROUP BY agent
                HAVING COUNT(*) > 1
            ) AND business_developer_associate = 'No'
        """)
        conn.commit()

        # Step 7: Final list (assigned + unassigned) - non-assignable on top
        cursor.execute("""
            SELECT agent, full_name, doj, exit_date, assignable, business_developer_associate
            FROM key_assignment
            ORDER BY assignable ASC, agent
        """)
        data_from_db = cursor.fetchall()

        all_records = [
            {
                "agent": row[0],
                "full_name": row[1] or "",
                "doj": str(row[2]) if row[2] else "",
                "exit_date": str(row[3]) if row[3] else "",
                "assignable": row[4],
                "business_developer_associate": row[5]
            }
            for row in data_from_db
        ]

        conn.close()
        return jsonify({"status": "success", "assigned_keys": all_records})

    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})
