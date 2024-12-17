from typing import Dict, Tuple
from datetime import datetime

class FoodDistributionSystem:
    def __init__(self):
        self.inventory = {}
        self.distribution_centers = {}
        self.vulnerable_areas = {}
        
    def add_distribution_center(self, center_id: str, location: Tuple[float, float], capacity: float):
        """
        Add a new distribution center
        """
        self.distribution_centers[center_id] = {
            'location': location,
            'capacity': capacity,
            'current_load': 0
        }
    
    def add_vulnerable_area(self, area_id: str, location: Tuple[float, float], 
                          population: int, vulnerability_score: float):
        """
        Add a new vulnerable area
        """
        self.vulnerable_areas[area_id] = {
            'location': location,
            'population': population,
            'vulnerability_score': vulnerability_score,
            'last_delivery': None
        }
    
    def get_distribution_centers(self) -> Dict:
        """
        Get all distribution centers
        """
        return self.distribution_centers
    
    def get_vulnerable_areas(self) -> Dict:
        """
        Get all vulnerable areas
        """
        return self.vulnerable_areas
    
    def update_center_load(self, center_id: str, quantity: float, operation: str = 'add'):
        """
        Update the current load of a distribution center
        """
        if center_id not in self.distribution_centers:
            raise ValueError(f"Distribution center {center_id} not found")
            
        center = self.distribution_centers[center_id]
        if operation == 'add':
            if center['current_load'] + quantity <= center['capacity']:
                center['current_load'] += quantity
            else:
                raise ValueError(f"Exceeds capacity of distribution center {center_id}")
        elif operation == 'remove':
            if center['current_load'] >= quantity:
                center['current_load'] -= quantity
            else:
                raise ValueError(f"Insufficient load in distribution center {center_id}")
    
    def record_delivery(self, area_id: str, quantity: float, timestamp: datetime):
        """
        Record a delivery to a vulnerable area
        """
        if area_id not in self.vulnerable_areas:
            raise ValueError(f"Area {area_id} not found")
            
        self.vulnerable_areas[area_id]['last_delivery'] = timestamp
    
    def get_area_status(self, area_id: str) -> Dict:
        """
        Get the status of a vulnerable area
        """
        if area_id not in self.vulnerable_areas:
            raise ValueError(f"Area {area_id} not found")
            
        area = self.vulnerable_areas[area_id]
        return {
            'population': area['population'],
            'vulnerability_score': area['vulnerability_score'],
            'last_delivery': area['last_delivery'],
            'location': area['location']
        }
    
    def get_center_status(self, center_id: str) -> Dict:
        """
        Get the status of a distribution center
        """
        if center_id not in self.distribution_centers:
            raise ValueError(f"Distribution center {center_id} not found")
            
        center = self.distribution_centers[center_id]
        return {
            'capacity': center['capacity'],
            'current_load': center['current_load'],
            'location': center['location'],
            'utilization': center['current_load'] / center['capacity']
        } 