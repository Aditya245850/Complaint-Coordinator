from DB_CONNECTION import get_db_connection


def downloadContent(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()

    cursor.execute("SELECT id, category FROM categories WHERE user_id = %s", (user_id,))
    categories = cursor.fetchall()

    category_map = {id: category for id, category in categories}

    complaints_details = []

    for id, category in categories:
        cursor.execute("SELECT category_id, summary, sentiment FROM complaints WHERE category_id = %s", (id,))
        complaints = cursor.fetchall()

        for category_id, summary, sentiment in complaints:
            complaints_details.append(f"{summary} - Tone: {sentiment} - Type of complaint: {category_map.get(category_id)}.\n")

    
    cursor.close()
    conn.close()

    return complaints_details
    
