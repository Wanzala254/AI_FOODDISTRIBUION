from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample data for demonstration
delivery_data = {
    'turkana': {'deliveries': 15, 'success_rate': 0.9},
    'kisii': {'deliveries': 12, 'success_rate': 0.85},
    'marsabit': {'deliveries': 10, 'success_rate': 0.88}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results')
def results():
    total_deliveries = sum(data['deliveries'] for data in delivery_data.values())
    avg_success_rate = sum(data['success_rate'] for data in delivery_data.values()) / len(delivery_data)
    
    return render_template('results.html',
                         total_deliveries=total_deliveries,
                         success_rate=avg_success_rate,
                         avg_response_time=24,
                         areas_covered=len(delivery_data),
                         detailed_results=[
                             {
                                 'region': region,
                                 'deliveries': data['deliveries'],
                                 'success_rate': data['success_rate'],
                                 'response_time': 24,
                                 'population': 100000,
                                 'efficiency': 0.85
                             }
                             for region, data in delivery_data.items()
                         ],
                         regions=list(delivery_data.keys()),
                         delivery_data=[data['deliveries'] for data in delivery_data.values()],
                         resource_labels=['Food', 'Transport', 'Storage', 'Personnel', 'Other'],
                         resource_distribution=[40, 25, 15, 15, 5],
                         coverage_data=[
                             {
                                 'region': 'Turkana',
                                 'lat': 3.1166,
                                 'lng': 35.5966,
                                 'population': 926976,
                                 'success_rate': 0.9
                             },
                             {
                                 'region': 'Kisii',
                                 'lat': -0.6698,
                                 'lng': 34.7717,
                                 'population': 1266860,
                                 'success_rate': 0.85
                             },
                             {
                                 'region': 'Marsabit',
                                 'lat': 2.3284,
                                 'lng': 37.9991,
                                 'population': 459785,
                                 'success_rate': 0.88
                             }
                         ],
                         inventory_dates=['2024-01-01', '2024-01-02', '2024-01-03'],
                         inventory_datasets=[],
                         delivery_labels=list(delivery_data.keys()),
                         delivery_data_chart=[data['deliveries'] for data in delivery_data.values()],
                         feedback_distribution=[20, 30, 25, 15, 10],
                         recent_feedback=[])

if __name__ == '__main__':
    app.run(debug=True) 