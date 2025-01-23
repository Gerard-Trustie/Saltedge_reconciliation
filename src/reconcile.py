"""
Main reconciliation logic for matching and processing transactions.
"""

from typing import Dict, List, Any, Tuple, Optional
from .utils import normalize_transaction


def find_json_match(
    csv_transaction: Dict[str, Any],
    json_transactions: List[Dict[str, Any]],
    match_fields: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Find a matching JSON transaction for a given CSV transaction.
    
    Args:
        csv_transaction: Transaction from CSV (source of truth)
        json_transactions: List of transactions from JSON to validate
        match_fields: Fields to use for matching (default: date and amount)
    
    Returns:
        Matching JSON transaction or None
    """
    # Always match on date and amount
    match_fields = ["date", "amount"]
    
    for json_tx in json_transactions:
        matches = True
        
        # Compare date and amount
        csv_amount = csv_transaction.get("amount", 0)
        json_amount = json_tx.get("amount", 0)
        
        # Strict amount comparison including sign
        if (csv_transaction.get("date") != json_tx.get("date") or
            abs(csv_amount - json_amount) > 0.01 or  # Check magnitude within tolerance
            (csv_amount * json_amount < 0)):  # Check if signs are different
            matches = False
            continue
        
        if matches:
            # Add debug logging
            print(f"Match found:")
            print(f"CSV amount: {csv_amount}")
            print(f"JSON amount: {json_amount}")
            return json_tx
    
    return None


def get_field_discrepancies(
    csv_tx: Dict[str, Any], json_tx: Dict[str, Any]
) -> List[str]:
    """
    Identify discrepancies between CSV and JSON transaction fields.
    """
    discrepancies = []
    
    # Compare normalized fields
    if abs(csv_tx.get("amount", 0) - json_tx.get("amount", 0)) > 0.01:
        discrepancies.append("amount")
    
    if csv_tx.get("date") != json_tx.get("date"):
        discrepancies.append("date")
    
    return discrepancies


def validate_transactions(
    csv_data: List[Dict[str, Any]],
    json_data: List[Dict[str, Any]],
    match_fields: Optional[List[str]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Tuple[Dict[str, Any], Dict[str, Any], List[str]]]]:
    """
    Validate JSON transactions against CSV transactions (source of truth).
    
    Args:
        csv_data: List of transactions from CSV (source of truth)
        json_data: List of transactions from JSON to validate
        match_fields: Fields to use for matching
    
    Returns:
        Tuple of (
            validated_transactions,  # CSV transactions with matching JSON entries
            missing_from_json,      # CSV transactions not found in JSON
            extra_in_json,          # JSON transactions not matching any CSV entry
            discrepancies          # Tuples of (csv_tx, json_tx, discrepant_fields)
        )
    """
    validated = []
    missing_from_json = []
    remaining_json = json_data.copy()
    discrepancies = []
    
    # For each CSV transaction (source of truth)
    for csv_tx in csv_data:
        # Try to find matching JSON transaction
        json_match = find_json_match(csv_tx, remaining_json, match_fields)
        
        if json_match:
            # Remove from remaining JSON transactions
            remaining_json.remove(json_match)
            
            # Check for discrepancies in other fields
            discrepant_fields = get_field_discrepancies(csv_tx, json_match)
            
            if discrepant_fields:
                discrepancies.append((csv_tx, json_match, discrepant_fields))
            else:
                validated.append(csv_tx)
        else:
            missing_from_json.append(csv_tx)
    
    # Any remaining JSON transactions are extra
    extra_in_json = remaining_json
    
    return validated, missing_from_json, extra_in_json, discrepancies
