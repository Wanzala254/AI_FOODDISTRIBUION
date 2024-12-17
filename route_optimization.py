from typing import List, Tuple
import math

class RouteOptimizer:
    @staticmethod
    def optimize_route(start_point: Tuple[float, float], delivery_points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Optimize delivery route using nearest neighbor algorithm
        """
        optimized_route = [start_point]
        unvisited = delivery_points.copy()
        
        while unvisited:
            current = optimized_route[-1]
            nearest = min(unvisited, 
                        key=lambda p: RouteOptimizer.calculate_distance(current, p))
            optimized_route.append(nearest)
            unvisited.remove(nearest)
            
        return optimized_route

    @staticmethod
    def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        Calculate Euclidean distance between two points
        """
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)