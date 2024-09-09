from flask import Flask, render_template, jsonify
import csv
import os

app = Flask(__name__)

def load_nhs_trust_data():
    trusts = []
    with open('etr_cleaned_new_with_MAPs_geocoded.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            trusts.append({
                'name': row['Trust Name'],
                'total': row['Total PAs and AAs'],
                'lat': float(row['Latitude']),
                'lng': float(row['Longitude'])
            })
    return trusts

@app.route('/')
def index():
    google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render_template('index.html', google_maps_api_key=google_maps_api_key)

@app.route('/api/trusts')
def get_trusts():
    trusts = load_nhs_trust_data()
    return jsonify(trusts)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
