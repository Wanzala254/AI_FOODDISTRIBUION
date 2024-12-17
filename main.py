import sys
import os
from datetime import datetime, timedelta

# Add the directory containing your modules to Python's path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from food_distribution_system import FoodDistributionSystem
from demand_prediction import DemandPredictor
from route_optimization import RouteOptimizer
from inventory_management import InventoryManager
from resource_allocation import ResourceAllocator
from alert_system import AlertSystem
from data_visualization import DataVisualizer

def display_separator():
    print("\n" + "="*50 + "\n")

def main():
    print("Initializing AI-Driven Food Distribution System...")
    display_separator()
    
    # Initialize components
    fds = FoodDistributionSystem()
    demand_predictor = DemandPredictor()
    route_optimizer = RouteOptimizer()
    inventory_manager = InventoryManager()
    alert_system = AlertSystem()
    
    # Setup distribution centers
    print("Setting up distribution centers...")
    fds.add_distribution_center('dc1', (0, 0), 5000)
    fds.add_distribution_center('dc2', (10, 10), 3000)
    print("Distribution centers added: dc1, dc2")
    
    # Setup vulnerable areas
    vulnerable_areas = {
        'area1': {'vulnerability_score': 8.5, 'population': 1000, 'location': (2, 3)},
        'area2': {'vulnerability_score': 6.2, 'population': 1500, 'location': (5, 4)},
        'area3': {'vulnerability_score': 9.1, 'population': 800, 'location': (3, 7)}
    }
    
    for area_id, data in vulnerable_areas.items():
        fds.add_vulnerable_area(
            area_id, 
            data['location'], 
            data['population'], 
            data['vulnerability_score']
        )
    print("Vulnerable areas added:", list(vulnerable_areas.keys()))
    
    resource_allocator = ResourceAllocator(vulnerable_areas)
    display_separator()
    
    try:
        # Initialize inventory
        print("Initializing inventory...")
        initial_inventory = {
            'rice': 1000,
            'beans': 800,
            'oil': 500,
            'flour': 600,
            'sugar': 400
        }
        
        for item, quantity in initial_inventory.items():
            inventory_manager.update_inventory(item, quantity)
        print("Initial inventory loaded:", initial_inventory)
        display_separator()
        
        # Display current inventory levels
        print("Current Inventory Levels:")
        for item, quantity in inventory_manager.get_inventory_levels().items():
            print(f"{item}: {quantity} units")
        display_separator()
        
        # Train demand prediction model
        print("Training demand prediction model...")
        historical_data = {
            'area1': [100, 120, 95, 105, 115, 98, 102],
            'area2': [150, 160, 140, 155, 165, 145, 158],
            'area3': [80, 85, 75, 82, 88, 79, 83]
        }
        features = [[1, 25], [2, 26], [3, 24], [4, 25], [5, 27], [6, 23], [7, 24]]
        demand_predictor.train(historical_data, features)
        print("Demand prediction model trained successfully")
        display_separator()
        
        # Predict demand for each area
        print("Demand Predictions:")
        for area_id in vulnerable_areas:
            predicted_demand = demand_predictor.predict(area_id, [1, 26])
            print(f"{area_id}: Predicted demand = {predicted_demand:.2f} units")
        display_separator()
        
        # Resource allocation for each area
        print("Resource Allocation Details:")
        available_inventory = inventory_manager.get_inventory_levels()
        for area_id in vulnerable_areas:
            predicted_demand = demand_predictor.predict(area_id, [1, 26])
            allocation = resource_allocator.allocate_resources(
                area_id, 
                predicted_demand, 
                available_inventory
            )
            print(f"\n{area_id} Allocation:")
            print(f"Base quantity: {allocation['base_quantity']:.2f}")
            print(f"Adjusted quantity: {allocation['adjusted_quantity']:.2f}")
            print("Food allocation:")
            for food_item, qty in allocation['food_allocation'].items():
                print(f"  - {food_item}: {qty:.2f} units")
        display_separator()
        
        # Route optimization
        print("Optimizing delivery routes...")
        start_point = (0, 0)  # Distribution center location
        delivery_points = [area_data['location'] for area_data in vulnerable_areas.values()]
        optimized_route = route_optimizer.optimize_route(start_point, delivery_points)
        
        print("Optimized Delivery Route:")
        for i, point in enumerate(optimized_route):
            if i == 0:
                print(f"Start: Distribution Center {point}")
            else:
                print(f"Stop {i}: Location {point}")
        display_separator()
        
        # Check inventory levels and generate alerts
        print("Checking inventory levels and generating alerts...")
        alert_system.check_inventory_levels(inventory_manager.get_inventory_levels())
        
        active_alerts = alert_system.get_active_alerts()
        if active_alerts:
            print("\nActive Alerts:")
            for alert in active_alerts:
                print(f"- {alert['message']} (Time: {alert['timestamp']})")
        else:
            print("No active alerts")
        display_separator()
        
        # Generate and display visualizations
        print("Generating visualizations...")
        inventory_report = inventory_manager.generate_inventory_report()
        DataVisualizer.plot_inventory_levels(inventory_report)
        
        # Plot demand predictions for all areas
        for area_id, history in historical_data.items():
            predicted = demand_predictor.predict(area_id, [1, 26])
            DataVisualizer.plot_demand_prediction(history, predicted)
        
        print("System simulation completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main() 