from flask import Flask, render_template, request, jsonify
import csv
import pandas as pd

app = Flask(__name__)
csv_file = 'data/temperature_data.csv'

@app.route('/receive_json', methods=['POST'])
def receive_json():
    data = request.get_json()
    response = {
        "message": "JSON received!",
        "data": data
    }

    # Save data to csv
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['date'], data['time'], data['indoor_temperature'], data['outdoor_temperature']])

    return jsonify(response), 200

def get_latest_temperatures():
    df = pd.read_csv('data/temperature_data.csv')
    latest_record = df.iloc[-1]
    return round(latest_record['indoor_temperature'], 1), round(latest_record['outdoor_temperature'], 1)

@app.route('/')
def index():
    indoor_temp, outdoor_temp = get_latest_temperatures()
    return render_template('index.html', indoor_temp=indoor_temp, outdoor_temp=outdoor_temp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)