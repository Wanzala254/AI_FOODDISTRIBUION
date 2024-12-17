from typing import Dict, List

class ResourceAllocator:
    def __init__(self, vulnerable_areas: Dict[str, Dict]):
        self.vulnerable_areas = vulnerable_areas

    def allocate_resources(self, area_id: str, required_quantity: float, 
                         available_inventory: Dict[str, float]) -> Dict[str, float]:
        """
        Allocate food resources based on vulnerability score and available inventory
        """
        if area_id not in self.vulnerable_areas:
            raise ValueError(f"Area {area_id} not found in vulnerable areas")
            
        vulnerability_score = self.vulnerable_areas[area_id]['vulnerability_score']
        population = self.vulnerable_areas[area_id]['population']
        priority_multiplier = 1 + (vulnerability_score / 10)
        
        adjusted_quantity = required_quantity * priority_multiplier
        
        # Adjust allocation based on available inventory
        total_available = sum(available_inventory.values())
        if total_available < adjusted_quantity:
            adjusted_quantity = total_available
        
        # Calculate proportional allocation for each food item
        food_allocation = {}
        for food_item, quantity in available_inventory.items():
            proportion = quantity / total_available if total_available > 0 else 0
            food_allocation[food_item] = min(quantity, adjusted_quantity * proportion)
        
        return {
            'base_quantity': required_quantity,
            'adjusted_quantity': adjusted_quantity,
            'vulnerability_score': vulnerability_score,
            'population': population,
            'food_allocation': food_allocation
        } 