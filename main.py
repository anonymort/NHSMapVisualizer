from flask import Flask, render_template, jsonify
import csv
import os
from functools import lru_cache

app = Flask(__name__)

@lru_cache(maxsize=1)
def load_nhs_trust_data():
    trusts = []
    csv_file = 'etr_cleaned_new_with_MAPs_geocoded.csv'
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                trusts.append({
                    'name': row['Trust Name'],
                    'total': int(row['Total PAs and AAs']),
                    'lat': float(row['Latitude']),
                    'lng': float(row['Longitude'])
                })
    except FileNotFoundError:
        app.logger.error(f"CSV file not found: {csv_file}")
    except (ValueError, KeyError) as e:
        app.logger.error(f"Error processing CSV data: {e}")
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
    app.run(host='0.0.0.0', port=port, debug=False)
