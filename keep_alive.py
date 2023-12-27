from flask import Flask, render_template, send_from_directory
from threading import Thread

app = Flask(__name__) 
@app.route('/')
def index():
    total_servers = 4
    
    import sqlite3

    conn = sqlite3.connect('counter.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM server_count')
    result = cursor.fetchall()
    conn.close()

    print(f"---{result}---")
    
    return render_template('index.html', total_servers=total_servers)

@app.route('/file/<filename>')
def download_file(filename):
    return send_from_directory('files', filename)

@app.route('/alt')
def alt():
    with open("./web/alt.html", 'r') as file:
        content = file.read()
    return content
    
@app.route('/hello')
def hello():
        return "Hello, World!"

@app.route('/html')
def html():
        return render_template("jotalea.html")

@app.route('/user/<username>')
def show_user_profile(username):
        return f'User {username}'

@app.route('/logs')
def show_logs():
        import jotalea, json
        logs = json.dumps(jotalea.log, indent=2, separators=(',', ':'))
        return render_template('index.php') # f'{logs}'

def run():
         app.run(host='0.0.0.0',port=8080)

def server():
    t = Thread(target=run) 
    t.start()