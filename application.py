from flask import Flask, redirect, render_template, request, send_file, url_for
from helper.download import downloadContent
from helper.graph import category_graph
from process.Image import process_Image
from process.Text import process_Text
from process.Video import process_Video
from process.Voice import process_Voice
import os
from datetime import datetime
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from DB_CONNECTION import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
API_KEY = ''
username = ''
password = ''


app = Flask(__name__)
upload_folder = 'uploads/'
app.config['upload_folder'] = upload_folder
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
@app.route("/")
def home():
    return render_template('home.html')
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    global username, password
    username = ''
    password = ''
    return render_template('home.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    global username
    graph_html = category_graph(username)
    return render_template('index.html', graph = graph_html)
@app.route('/login', methods=['GET', 'POST'])
def login():
    global username, password
    if request.method == "POST":
        username = request.form['username'].lower()
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            stored_password_hash = result[0]
            
            if check_password_hash(stored_password_hash, password):
                return redirect(url_for('index'))
            else:
                error = "Password incorrect."
        else:
            error = "Login not found."

        return render_template('login.html', error=error)



    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global username, password
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()

        user_id = user_id[0]

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
        for category in categories:
            cursor.execute("INSERT INTO categories (user_id, category) VALUES (%s, %s);", (user_id, category))

        cursor.execute("UPDATE categories SET num = 0 WHERE user_id = %s;", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/Video", methods=["POST"])
def video_action():
    if 'video_file' in request.files:
        video_file = request.files['video_file']
        if video_file.filename != '':
            file_path = os.path.join(app.config['upload_folder'], video_file.filename)
            video_file.save(file_path)
            process_Video(file_path, username, API_KEY)
            os.remove(file_path)
    return redirect(url_for('index'))

@app.route("/Text", methods=["POST"])
def text_action():
    if 'text_file' in request.files:
        text_file = request.files['text_file']
        if text_file.filename != '':
            file_path = os.path.join(app.config['upload_folder'], text_file.filename)
            text_file.save(file_path)
            process_Text(file_path, username, API_KEY)
            os.remove(file_path)
    return redirect(url_for('index'))
    
@app.route("/Voice", methods=["POST"])
def voice_action():
    if 'voice_file' in request.files:
        voice_file = request.files['voice_file']
        if voice_file.filename != '':
            file_path = os.path.join(app.config['upload_folder'], voice_file.filename)
            voice_file.save(file_path)
            process_Voice(file_path, username, API_KEY)
            os.remove(file_path)
    return redirect(url_for('index'))

@app.route("/Image", methods=["POST"])
def image_action():
    if 'image_file' in request.files:
        image_file = request.files['image_file']
        if image_file.filename != '':
            file_path = os.path.join(app.config['upload_folder'], image_file.filename)
            image_file.save(file_path)
            process_Image(file_path, username, API_KEY)
            os.remove(file_path)
    return redirect(url_for('index'))

@app.route("/download", methods = ["POST"])
def download():
    global username
    complaints = downloadContent(username)

    timestamp = int(time.time())
    pdf_file_path = f"complaints_report_{username}_{timestamp}.pdf"

    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=16,
        leading=20,
        alignment=1, 
        spaceAfter=20,
    )
    current_date = datetime.now().strftime("%Y-%m-%d")
    title = f"Complaints Report - {current_date}"
    title = Paragraph(title, title_style)

    pdf_file = [title, Spacer(1,12)]

    for complaint in complaints:
        pdf_file.append(Paragraph(complaint, styles["BodyText"]))
        pdf_file.append(Spacer(1, 12)) 

    doc.build(pdf_file)

    response = send_file(pdf_file_path, as_attachment=True)

    os.remove(pdf_file_path)

    return response
if __name__ == '__main__':
   app.run(debug=True)

