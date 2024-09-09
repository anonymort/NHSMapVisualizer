from flask import Flask, render_template, jsonify
import csv
import os
from functools import lru_cache
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

CSV_FILE = 'etr_cleaned_new_with_MAPs_geocoded.csv'

@lru_cache(maxsize=1)
def load_nhs_trust_data():
    trusts = []
    try:
        with open(CSV_FILE, 'r') as file:
            csv_reader = csv.DictReader(file)
            trusts = [{
                'name': row['Trust Name'],
                'total': int(row['Total PAs and AAs']),
                'lat': float(row['Latitude']),
                'lng': float(row['Longitude'])
            } for row in csv_reader]
    except FileNotFoundError:
        app.logger.error(f"CSV file not found: {CSV_FILE}")
    except (ValueError, KeyError) as e:
        app.logger.error(f"Error processing CSV data: {e}")
    return trusts

@app.route('/')
@cache.cached(timeout=3600)  # Cache for 1 hour
def index():
    google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render_template('index.html', google_maps_api_key=google_maps_api_key)

@app.route('/api/trusts')
@cache.cached(timeout=3600)  # Cache for 1 hour
def get_trusts():
    return jsonify(load_nhs_trust_data())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
