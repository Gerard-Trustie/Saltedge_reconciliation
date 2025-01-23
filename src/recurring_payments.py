"""
Module for identifying recurring payments in transaction data.
"""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from difflib import SequenceMatcher
import statistics
import json
from pathlib import Path
import pandas as pd

class RecurringPaymentDetector:
    def __init__(
        self,
        monthly_date_tolerance: int = 3,  # days
        weekly_date_tolerance: int = 1,    # days
        amount_tolerance: float = 0.05,    # 5%
        description_similarity: float = 0.85  # 85% similar
    ):
        self.monthly_date_tolerance = monthly_date_tolerance
        self.weekly_date_tolerance = weekly_date_tolerance
        self.amount_tolerance = amount_tolerance
        self.description_similarity = description_similarity

    def find_recurring_payments(
        self, transactions: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Identify recurring payments in transaction data.
        
        Args:
            transactions: List of normalized transactions (negative amounts for outgoing)
            
        Returns:
            Dictionary of recurring payment groups with their transactions
        """
        # Filter for outgoing transactions (negative amounts)
        outgoing = [tx for tx in transactions if tx.get('amount', 0) < 0]
        
        # Group similar transactions by description
        description_groups = self._group_by_description(outgoing)
        
        # Identify recurring patterns in each group
        recurring_payments = {}
        
        for desc, group in description_groups.items():
            if len(group) >= 2:  # Need at least 2 transactions to form a pattern
                monthly_pattern = self._find_monthly_pattern(group)
                weekly_pattern = self._find_weekly_pattern(group)
                
                if monthly_pattern:
                    recurring_payments[f"{desc} (Monthly)"] = monthly_pattern
                if weekly_pattern:
                    recurring_payments[f"{desc} (Weekly)"] = weekly_pattern
        
        return recurring_payments

    def _group_by_description(
        self, transactions: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group transactions with similar descriptions."""
        groups = defaultdict(list)
        processed_descriptions = set()
        
        for tx in transactions:
            # Add debug prints to check the transaction and description at each step
            print("\nOriginal transaction:", tx)
            print("Original data:", tx.get('original_data', {}))
            
            # The description might be in the original_data
            original_desc = tx.get('original_data', {}).get('description', '')
            normalized_desc = original_desc.strip().lower()
            
            print("Original description:", original_desc)
            print("Normalized description:", normalized_desc)
            
            if not normalized_desc:
                # If no description in normalized data, try to find it in the raw transaction
                for key in tx:
                    print(f"Checking key: {key}, value: {tx[key]}")
                
            if normalized_desc:
                # Skip if already processed this description
                if normalized_desc in processed_descriptions:
                    groups[normalized_desc].append(tx)
                    continue
                
                # Find similar descriptions
                similar_group = None
                for existing_desc in processed_descriptions:
                    if self._are_descriptions_similar(normalized_desc, existing_desc):
                        similar_group = existing_desc
                        break
            
                if similar_group:
                    groups[similar_group].append(tx)
                else:
                    groups[normalized_desc].append(tx)
                    processed_descriptions.add(normalized_desc)
        
        return dict(groups)

    def _are_descriptions_similar(self, desc1: str, desc2: str) -> bool:
        """Check if two descriptions are similar using sequence matcher."""
        return SequenceMatcher(None, desc1, desc2).ratio() >= self.description_similarity

    def _find_monthly_pattern(
        self, transactions: List[Dict[str, Any]]
    ) -> Optional[List[Dict[str, Any]]]:
        """Identify monthly recurring pattern in transactions."""
        # Breakpoint 1: Check input to monthly pattern
        print("\nChecking monthly pattern for:")
        print(f"Number of transactions: {len(transactions)}")
        print("First few transactions:")
        for tx in transactions[:3]:
            print(f"Date: {tx['date']}, Amount: {tx['amount']}, Desc: {tx['original_data']['description']}")
        
        sorted_tx = sorted(transactions, key=lambda x: x.get('date', ''))
        
        # Breakpoint 2: Check sorting
        print("\nAfter sorting:")
        for tx in sorted_tx[:3]:
            print(f"Date: {tx['date']}, Amount: {tx['amount']}")
        
        recurring = []
        prev_tx = None
        
        for tx in sorted_tx:
            if prev_tx:
                # Breakpoint 3: Check interval calculation
                prev_date = datetime.strptime(prev_tx['date'], '%Y-%m-%d')
                curr_date = datetime.strptime(tx['date'], '%Y-%m-%d')
                days_diff = (curr_date - prev_date).days
                
                print(f"\nComparing transactions:")
                print(f"Previous: {prev_tx['date']} - {prev_tx['amount']}")
                print(f"Current:  {tx['date']} - {tx['amount']}")
                print(f"Days difference: {days_diff}")
                print(f"Monthly match? {abs(days_diff - 30) <= self.monthly_date_tolerance}")
                
                if abs(days_diff - 30) <= self.monthly_date_tolerance:
                    # Breakpoint 4: Check amount comparison
                    print(f"Checking amounts: {prev_tx['amount']} vs {tx['amount']}")
                    if self._are_amounts_similar(prev_tx['amount'], tx['amount']):
                        print("Amounts match!")
                        if not recurring:
                            recurring.extend([prev_tx, tx])
                        else:
                            recurring.append(tx)
            
            prev_tx = tx
        
        # Breakpoint 5: Check final recurring set
        if recurring:
            print("\nFound recurring pattern:")
            for tx in recurring:
                print(f"Date: {tx['date']}, Amount: {tx['amount']}")
        
        return recurring if len(recurring) >= 2 else None

    def _find_weekly_pattern(
        self, transactions: List[Dict[str, Any]]
    ) -> Optional[List[Dict[str, Any]]]:
        """Identify weekly recurring pattern in transactions."""
        # Sort by date
        sorted_tx = sorted(transactions, key=lambda x: x.get('date', ''))
        
        # Check for weekly intervals
        recurring = []
        prev_tx = None
        
        for tx in sorted_tx:
            if prev_tx:
                # Calculate days between transactions
                prev_date = datetime.strptime(prev_tx['date'], '%Y-%m-%d')
                curr_date = datetime.strptime(tx['date'], '%Y-%m-%d')
                days_diff = (curr_date - prev_date).days
                
                # Check if approximately weekly (7 days ± tolerance)
                if abs(days_diff - 7) <= self.weekly_date_tolerance:
                    # Check if amounts are similar
                    if self._are_amounts_similar(prev_tx['amount'], tx['amount']):
                        if not recurring:
                            recurring.extend([prev_tx, tx])
                        else:
                            recurring.append(tx)
            
            prev_tx = tx
        
        return recurring if len(recurring) >= 2 else None

    def _are_amounts_similar(self, amount1: float, amount2: float) -> bool:
        """Check if two amounts are within the tolerance percentage."""
        if amount1 == 0 or amount2 == 0:
            return False
        
        diff_percentage = abs((amount1 - amount2) / amount1)
        return diff_percentage <= self.amount_tolerance

def generate_recurring_payments_report(
    recurring_payments: Dict[str, List[Dict[str, Any]]],
    output_path: str
) -> None:
    """
    Generate detailed JSON report and CSV summary of recurring payments.
    
    Args:
        recurring_payments: Dictionary of recurring payment groups
        output_path: Base path for output files (without extension)
    """
    # Generate detailed JSON report
    report = {
        "summary": {
            "total_recurring_groups": len(recurring_payments),
            "recurring_payments": []
        }
    }
    
    # Create CSV summary data
    csv_data = []
    
    for description, transactions in recurring_payments.items():
        amounts = [tx['amount'] for tx in transactions]
        dates = [tx['date'] for tx in transactions]
        
        # Extract frequency from description (e.g., "NETFLIX (Monthly)" -> "Monthly")
        frequency = description.split('(')[-1].strip(')')
        
        # Remove frequency suffix from description for cleaner output
        clean_description = description.split(' (')[0]
        
        # Calculate statistics
        avg_amount = statistics.mean(amounts)
        std_dev = statistics.stdev(amounts) if len(amounts) > 1 else 0
        
        # Add to JSON report
        group_summary = {
            "description": description,
            "transaction_count": len(transactions),
            "average_amount": avg_amount,
            "amount_std_dev": std_dev,
            "first_date": min(dates),
            "last_date": max(dates),
            "transactions": transactions
        }
        report["summary"]["recurring_payments"].append(group_summary)
        
        # Add to CSV data
        csv_data.append({
            "Description": clean_description,
            "Frequency": frequency,
            "Number of Transactions": len(transactions),
            "Average Amount": f"£{abs(avg_amount):.2f}",
            "First Date": min(dates),
            "Last Date": max(dates)
        })
    
    # Save JSON report
    json_path = Path(output_path).with_suffix('.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # Save CSV summary
    csv_path = Path(output_path).with_suffix('.csv')
    df = pd.DataFrame(csv_data)
    
    # Sort by frequency and amount
    df = df.sort_values(['Frequency', 'Average Amount'], ascending=[True, False])
    
    # Write CSV with clean formatting
    df.to_csv(csv_path, index=False) 
