# NHS Trust Data Visualization Project

This project is a Flask web application that visualizes NHS Trust MAPs governance data on a Google Map. It displays a table with the total number of PAs and AAs for each trust and links to Governance documents. Users can click on the markers on the map or rows in the table to highlight corresponding data points.

## Features

- **Interactive Google Map**: Displays markers for each NHS Trust.
- **Data Table**: Lists the name and total number of PAs and AAs for each trust.
- **Dynamic Interactions**: Clicking a marker highlights and scrolls to the corresponding row in the table, and vice versa.
- **Governance Policy Links**: Each trust name includes a placeholder link to its governance policy.

### File Structure

- `main.py`: Main application script.
- `templates/index.html`: HTML template for the main page.
- `static/styles.css`: CSS styles for the web application.
- `static/map.js`: JavaScript code for initializing the Google Map and handling dynamic interactions.