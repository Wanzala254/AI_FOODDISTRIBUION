from typing import Dict, List
from datetime import datetime

class InventoryManager:
    def __init__(self):
        self.inventory = {}
        self.transactions = []

    def update_inventory(self, food_item: str, quantity: float, operation: str = 'add'):
        """
        Update inventory levels and record the transaction
        """
        if food_item not in self.inventory:
            self.inventory[food_item] = 0
            
        if operation == 'add':
            self.inventory[food_item] += quantity
        elif operation == 'remove':
            if self.inventory[food_item] >= quantity:
                self.inventory[food_item] -= quantity
            else:
                raise ValueError(f"Insufficient inventory for {food_item}")
        
        self.transactions.append({
            'food_item': food_item,
            'quantity': quantity,
            'operation': operation,
            'timestamp': datetime.now().isoformat(),
            'current_level': self.inventory[food_item]
        })

    def get_inventory_levels(self) -> Dict[str, float]:
        """
        Get current inventory levels
        """
        return self.inventory

    def get_transaction_history(self) -> List[Dict]:
        """
        Get transaction history
        """
        return self.transactions

    def generate_inventory_report(self) -> List[Dict]:
        """
        Generate a report of inventory levels and transactions
        """
        report = []
        for transaction in self.transactions:
            report_entry = {
                'timestamp': transaction['timestamp'],
                'food_item': transaction['food_item'],
                'current_level': transaction['current_level'],
                'operation': transaction['operation'],
                'quantity': transaction['quantity']
            }
            report.append(report_entry)
        
        return report

    def to_dict(self, format_type: str = 'records') -> List[Dict]:
        """
        Convert inventory data to dictionary format
        Mimics pandas DataFrame.to_dict() functionality
        """
        if format_type == 'records':
            return self.generate_inventory_report()
        else:
            raise ValueError("Unsupported format type. Use 'records'.")

    def get_low_stock_items(self, threshold: float = 100) -> List[Dict]:
        """
        Get items with stock levels below threshold
        """
        low_stock = []
        for item, quantity in self.inventory.items():
            if quantity < threshold:
                low_stock.append({
                    'food_item': item,
                    'current_level': quantity,
                    'threshold': threshold
                })
        return low_stock

    def get_stock_summary(self) -> Dict:
        """
        Get summary statistics of current inventory
        """
        if not self.inventory:
            return {
                'total_items': 0,
                'total_quantity': 0,
                'average_quantity': 0,
                'low_stock_count': 0
            }

        total_quantity = sum(self.inventory.values())
        return {
            'total_items': len(self.inventory),
            'total_quantity': total_quantity,
            'average_quantity': total_quantity / len(self.inventory),
            'low_stock_count': len(self.get_low_stock_items())
        }