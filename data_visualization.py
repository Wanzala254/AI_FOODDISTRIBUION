from typing import List, Dict
import json

class DataVisualizer:
    @staticmethod
    def plot_inventory_levels(inventory_data: List[Dict]) -> str:
        """
        Generate inventory levels data for plotting
        Returns a JSON string for web visualization
        """
        data = {
            'timestamps': [],
            'levels': [],
            'items': []
        }
        
        for record in inventory_data:
            data['timestamps'].append(str(record['timestamp']))
            data['levels'].append(record['current_level'])
            data['items'].append(record['food_item'])
            
        return json.dumps(data)

    @staticmethod
    def plot_demand_prediction(historical_demand: List[float], predicted_demand: float) -> str:
        """
        Generate demand prediction data for plotting
        Returns a JSON string for web visualization
        """
        data = {
            'historical': historical_demand,
            'predicted': predicted_demand,
            'time_periods': list(range(len(historical_demand))),
        }
        
        return json.dumps(data)

    @staticmethod
    def plot_resource_allocation(allocations: Dict[str, Dict]) -> str:
        """
        Generate resource allocation data for plotting
        Returns a JSON string for web visualization
        """
        data = {
            'areas': list(allocations.keys()),
            'base_quantities': [alloc['base_quantity'] for alloc in allocations.values()],
            'adjusted_quantities': [alloc['adjusted_quantity'] for alloc in allocations.values()]
        }
        
        return json.dumps(data)

    @staticmethod
    def generate_text_report(inventory_data: List[Dict]) -> str:
        """
        Generate a text-based report of inventory levels
        """
        report = "Inventory Report\n" + "="*20 + "\n"
        
        for record in inventory_data:
            report += f"Item: {record['food_item']}\n"
            report += f"Level: {record['current_level']}\n"
            report += f"Time: {record['timestamp']}\n"
            report += "-"*20 + "\n"
            
        return report

    @staticmethod
    def generate_summary_statistics(data: Dict) -> Dict:
        """
        Generate summary statistics for numerical data
        """
        numbers = [x for x in data.values() if isinstance(x, (int, float))]
        if not numbers:
            return {}
            
        return {
            'min': min(numbers),
            'max': max(numbers),
            'average': sum(numbers) / len(numbers),
            'total': sum(numbers),
            'count': len(numbers)
        }

    @staticmethod
    def prepare_chart_data(inventory_data: List[Dict]) -> tuple:
        """
        Prepare data for Chart.js visualization
        """
        # Group data by food item
        items = {}
        timestamps = set()
        
        for record in inventory_data:
            item = record['food_item']
            if item not in items:
                items[item] = []
            items[item].append({
                'timestamp': record['timestamp'],
                'level': record['current_level']
            })
            timestamps.add(record['timestamp'])
        
        # Sort timestamps
        timestamps = sorted(list(timestamps))
        
        # Prepare datasets for Chart.js
        datasets = []
        for item, data in items.items():
            datasets.append({
                'label': item,
                'data': [next((d['level'] for d in data if d['timestamp'] == ts), None) 
                        for ts in timestamps],
                'borderColor': f'#{hash(item) % 0xFFFFFF:06x}',
                'fill': False
            })
        
        return list(timestamps), datasets