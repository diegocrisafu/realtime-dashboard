# Real‑Time Data Visualisation Dashboard

This project demonstrates how to build a real‑time data visualisation using the **Dash** framework (built on top of Flask and Plotly).  It generates a simple data stream and plots it live in the browser.  You can adapt the data generation logic to connect to an API, sensor or message queue to display your own metrics.

## Features

This dashboard is designed to be both **interactive** and **customisable**.  A few highlights:

* **Live updates** – The chart refreshes on a timer without reloading the page.
* **Interactive chart** – Hover over the line to see exact values or zoom in by dragging to explore specific ranges.
* **Data source selector** – Choose between a **Random Walk** and a **Sine Wave** using the dropdown at the top of the page.
* **Adjustable update interval** – Use the slider to set the refresh rate between 0.5 and 5 seconds.  Smaller intervals generate more frequent updates.
* **Customisable data generation** – Replace the logic in `update_data()` with your own API calls or sensor readings to stream live metrics.

## Getting Started

1. Ensure you have Python 3.8+ installed.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your browser at [http://127.0.0.1:8050](http://127.0.0.1:8050).  You should see the dashboard updating in real time.

## Deployment

To deploy this app on a platform like Heroku or Railway, expose the `server` object provided by Dash.  The code already assigns `server = app.server`, so you can follow platform‑specific instructions to deploy a Flask server.

## Customising the Data Source

The function `update_data()` in `app.py` is responsible for generating each new data point.  Currently it appends a random walk value.  To connect to a real data source, modify this function to read from a file, database, API or message queue.

## License

Released under the MIT license.  See `LICENSE` for details.