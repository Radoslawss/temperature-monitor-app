from flask import Flask, request, jsonify
import csv

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)