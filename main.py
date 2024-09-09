from flask import Flask, render_template, jsonify
import csv
import os
from functools import lru_cache

# Logger configuration
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Constants
CSV_FILE = 'etr_cleaned_new_with_MAPs_geocoded.csv'

def validate_env_variables():
    """Validate the presence of important environment variables."""
    if not os.environ.get('GOOGLE_MAPS_API_KEY'):
        app.logger.error('Environment variable "GOOGLE_MAPS_API_KEY" is not set')
    if not os.environ.get('PORT'):
        app.logger.warning('Environment variable "PORT" is not set, using default port 5000')

@lru_cache(maxsize=1)
def load_nhs_trust_data():
    """Load NHS Trust data from a CSV file."""
    trusts = []
    try:
        with open(CSV_FILE, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    trusts.append({
                        'name': row['Trust Name'],
                        'total': float(row['Total PAs and AAs']),  # Convert to float
                        'lat': float(row['Latitude']),
                        'lng': float(row['Longitude'])
                    })
                except (ValueError, KeyError) as e:
                    app.logger.error(f"Error processing row {row}: {e}")
    except FileNotFoundError:
        app.logger.error(f"CSV file not found: {CSV_FILE}")
    return trusts

@app.route('/')
def index():
    """Render the index page."""
    google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render_template('index.html', google_maps_api_key=google_maps_api_key)

@app.route('/api/trusts')
def get_trusts():
    """Get NHS Trust data and return it as JSON."""
    trusts = load_nhs_trust_data()
    return jsonify(trusts)

if __name__ == '__main__':
    validate_env_variables()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)