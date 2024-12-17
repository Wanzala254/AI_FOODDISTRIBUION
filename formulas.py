import math
from typing import Tuple, Dict

class SystemFormulas:
    @staticmethod
    def calculate_demand(base_demand: float, population: int, 
                        vulnerability_score: float, seasonality_factor: float) -> float:
        """
        Formula: Predicted Demand = Base Demand × Population Factor × Vulnerability Factor × Seasonality Factor
        """
        population_factor = population / 1000  # normalize per 1000 people
        vulnerability_factor = 1 + (vulnerability_score / 10)
        
        predicted_demand = (
            base_demand * 
            population_factor * 
            vulnerability_factor * 
            seasonality_factor
        )
        
        return predicted_demand

    @staticmethod
    def calculate_resource_allocation(required_quantity: float, 
                                   vulnerability_score: float, 
                                   available_inventory: float) -> float:
        """
        Formula: Allocation = Required Quantity × Priority Multiplier × Availability Factor
        """
        priority_multiplier = 1 + (vulnerability_score / 10)
        availability_factor = min(1, available_inventory / required_quantity)
        
        allocation = required_quantity * priority_multiplier * availability_factor
        
        return allocation

    @staticmethod
    def calculate_distance(point1: Tuple[float, float], 
                         point2: Tuple[float, float]) -> float:
        """
        Formula: Distance = √[(x₂-x₁)² + (y₂-y₁)²]
        """
        return math.sqrt(
            (point2[0] - point1[0])**2 + 
            (point2[1] - point1[1])**2
        )

    @staticmethod
    def calculate_efficiency(delivered_quantity: float, target_quantity: float,
                           delivery_time: float, target_time: float) -> float:
        """
        Formula: Efficiency = (Quantity Factor × 0.6) + (Time Factor × 0.4)
        """
        quantity_factor = min(delivered_quantity / target_quantity, 1)
        time_factor = min(target_time / delivery_time, 1)
        
        efficiency_score = (quantity_factor * 0.6) + (time_factor * 0.4)
        
        return efficiency_score

    @staticmethod
    def calculate_priority(vulnerability_score: float, 
                         days_since_last_delivery: int,
                         current_inventory: float) -> float:
        """
        Formula: Priority Score = (Vulnerability Weight × 0.4) + 
                                (Days Factor × 0.3) + 
                                (Inventory Factor × 0.3)
        """
        vulnerability_weight = vulnerability_score / 10
        days_factor = min(days_since_last_delivery / 7, 1)
        inventory_factor = 1 - (current_inventory / 1000)
        
        priority_score = (
            (vulnerability_weight * 0.4) + 
            (days_factor * 0.3) + 
            (inventory_factor * 0.3)
        )
        
        return priority_score

    @staticmethod
    def calculate_coverage(center_location: Tuple[float, float], 
                         radius: float,
                         population_density: float) -> float:
        """
        Formula: Coverage = π × radius² × population_density × accessibility_factor
        """
        accessibility_factor = 0.8  # assuming 80% accessibility
        area = math.pi * (radius ** 2)
        population_covered = area * population_density * accessibility_factor
        
        return population_covered

    @staticmethod
    def calculate_response_time(distance: float, 
                              average_speed: float,
                              loading_time: float) -> float:
        """
        Formula: Total Response Time = Travel Time + Loading Time + Distribution Time
        """
        travel_time = distance / average_speed
        distribution_time = loading_time * 0.5
        
        total_time = travel_time + loading_time + distribution_time
        
        return total_time

    @staticmethod
    def calculate_success_rate(successful_deliveries: int,
                             total_deliveries: int,
                             on_time_factor: float) -> float:
        """
        Formula: Success Rate = (Delivery Success × 0.7) + (On-Time Factor × 0.3)
        """
        delivery_success = successful_deliveries / max(total_deliveries, 1)
        success_rate = (delivery_success * 0.7) + (on_time_factor * 0.3)
        
        return success_rate

    @staticmethod
    def calculate_vulnerability_index(population: int,
                                   infrastructure_score: float,
                                   food_security_score: float,
                                   accessibility_score: float) -> float:
        """
        Formula: Vulnerability Index = (Population Factor × 0.3) +
                                     (Infrastructure Score × 0.2) +
                                     (Food Security Score × 0.3) +
                                     (Accessibility Score × 0.2)
        """
        population_factor = min(population / 10000, 1)  # normalize for large populations
        
        vulnerability_index = (
            (population_factor * 0.3) +
            (infrastructure_score * 0.2) +
            (food_security_score * 0.3) +
            (accessibility_score * 0.2)
        )
        
        return vulnerability_index

    @staticmethod
    def calculate_distribution_score(delivery_success: float,
                                  coverage_rate: float,
                                  response_time_factor: float,
                                  efficiency_score: float) -> float:
        """
        Formula: Distribution Score = (Delivery Success × 0.4) +
                                    (Coverage Rate × 0.2) +
                                    (Response Time Factor × 0.2) +
                                    (Efficiency Score × 0.2)
        """
        distribution_score = (
            (delivery_success * 0.4) +
            (coverage_rate * 0.2) +
            (response_time_factor * 0.2) +
            (efficiency_score * 0.2)
        )
        
        return distribution_score 