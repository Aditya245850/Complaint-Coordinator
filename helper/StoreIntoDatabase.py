from DB_CONNECTION import get_db_connection
def storeIntoDatabase(summary, category, sentiment, username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()

    cursor.execute("SELECT id FROM categories WHERE user_id = %s AND category = %s", (user_id, category))
    category_id = cursor.fetchone()

    cursor.execute(
        "INSERT INTO complaints (user_id, category_id, summary, sentiment) VALUES (%s, %s, %s, %s)",
        (user_id[0], category_id[0], summary, sentiment)
    )
    cursor.execute("UPDATE categories SET num = num + 1 WHERE user_id = %s AND category = %s;", (user_id, category))
    conn.commit()

    cursor.close()
    conn.close()