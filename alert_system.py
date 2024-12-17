from typing import Dict, List
from datetime import datetime

class AlertSystem:
    def __init__(self):
        self.alerts = []
        
    def check_inventory_levels(self, inventory: Dict[str, float], threshold: float = 100):
        """
        Monitor inventory levels and generate alerts
        """
        for item, quantity in inventory.items():
            if quantity < threshold:
                self.generate_alert(
                    f"Low inventory alert: {item} is below threshold ({quantity} units remaining)",
                    alert_type="inventory"
                )
    
    def check_demand_spike(self, area_id: str, current_demand: float, average_demand: float, threshold: float = 1.5):
        """
        Check for unusual spikes in demand
        """
        if current_demand > average_demand * threshold:
            self.generate_alert(
                f"Demand spike detected in {area_id}: Current demand ({current_demand}) is significantly higher than average ({average_demand})",
                alert_type="demand"
            )
    
    def generate_alert(self, message: str, alert_type: str):
        """
        Generate and store alerts
        """
        alert = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'type': alert_type,
            'status': 'active'
        }
        self.alerts.append(alert)

    def get_active_alerts(self) -> List[Dict]:
        """
        Get all active alerts
        """
        return [alert for alert in self.alerts if alert['status'] == 'active']

    def resolve_alert(self, alert_index: int):
        """
        Mark an alert as resolved
        """
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index]['status'] = 'resolved'
        else:
            raise ValueError("Invalid alert index") 