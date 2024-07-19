from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import sys

app = Flask(__name__)

def get_database_path(db_file: str) -> str:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, db_file)

def create_database():
    db_path = get_database_path('data/temperature_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY,
        date TEXT,
        time TEXT,
        indoor_temperature REAL,
        outdoor_temperature REAL
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/receive_json', methods=['POST'])
def receive_json():
    data = request.get_json()
    response = {
        "message": "JSON received!",
        "data": data
    }

    # Save data to db
    db_path = get_database_path('data/temperature_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO measurements (date, time, indoor_temperature, outdoor_temperature)
        VALUES (?, ?, ?, ?)
    ''', (data['date'], data['time'], data['indoor_temperature'], data['outdoor_temperature']))
    conn.commit()
    conn.close()

    return jsonify(response), 200

def get_latest_temperatures():
    db_path = get_database_path('data/temperature_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        SELECT indoor_temperature, outdoor_temperature
        FROM measurements
        ORDER BY id DESC
        LIMIT 1
    ''')
    latest_record = c.fetchone()

    conn.close()

    if latest_record:
        indoor_temperature, outdoor_temperature = latest_record
        return round(indoor_temperature, 1), round(outdoor_temperature, 1)
    else:
        return None, None
    
@app.route('/history')
def history():
    db_path = get_database_path('data/temperature_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        SELECT date, time, indoor_temperature, outdoor_temperature
        FROM measurements
        ORDER BY id DESC
        LIMIT 20
    ''')
    measurements = c.fetchall()

    conn.close()

    return render_template('history.html', measurements=measurements)

@app.route('/')
def index():
    indoor_temp, outdoor_temp = get_latest_temperatures()
    return render_template('index.html', indoor_temp=indoor_temp, outdoor_temp=outdoor_temp)

if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=5000, debug=False)