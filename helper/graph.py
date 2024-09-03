import plotly.graph_objs as graph_obj
import numpy as np
import time
from DB_CONNECTION import get_db_connection

def category_graph(username):
    categories = [
        'product-related',
        'service-related',
        'delivery-and-shipping',
        'billing-and-payments',
        'technical',
        'user-experience',
        'legal-and-compliance',
        'marketing-and-advertising',
        'returns-and-exchanges',
        'miscellaneous'
    ]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()
    user_id = user_id[0]

    y_values = []
    for category in categories:
        cursor.execute("SELECT num FROM categories WHERE user_id = %s AND category = %s", (user_id,category))
        y_values.append(cursor.fetchone()[0])
    
    values = y_values

    category_figure = graph_obj.FigureWidget([graph_obj.Bar(x=categories, y=values)])

    category_figure.update_layout(
        title={
        'text': "Complaint Tracker",
        'font': {'color': 'white'} 
    },
    xaxis_title="Subject",
    yaxis_title="Number of Complaints",
    xaxis=dict(
        title_font=dict(color='white'),
        tickfont=dict(color='white')  
    ),
    yaxis=dict(
        title_font=dict(color='white'),
        tickfont=dict(color='white')  
    ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(51, 51, 51, 1)'
    )
    graph = category_figure.to_html(full_html = False)

    return graph