"""
Helper functions for loading, saving and processing transaction data.
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

import pandas as pd


def normalize_transaction(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize transaction data by cleaning and standardizing fields.
    
    Args:
        transaction: Raw transaction dictionary
    
    Returns:
        Normalized transaction dictionary with standardized fields
    """
    normalized = {}
    
    # Handle amount/value fields
    if "Value" in transaction:  # CSV field
        try:
            # Remove currency symbol if present and convert to float
            value_str = str(transaction["Value"]).strip().replace("£", "").replace(",", "")
            normalized["amount"] = float(value_str)
        except (ValueError, TypeError):
            normalized["amount"] = 0.0
    elif "amount" in transaction:  # JSON field
        try:
            normalized["amount"] = float(str(transaction["amount"]).strip().replace(",", ""))
        except (ValueError, TypeError):
            normalized["amount"] = 0.0
    
    # Handle date fields
    if "Date" in transaction:  # CSV field (capital D)
        date_str = str(transaction["Date"]).strip()
        try:
            # Parse dd mmm yyyy format (e.g., "19 Jan 2025")
            date_obj = datetime.strptime(date_str, "%d %b %Y")
            normalized["date"] = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            normalized["date"] = None
    elif "made_on" in transaction:  # JSON field
        date_str = str(transaction["made_on"]).strip()
        try:
            # JSON dates are in YYYY-MM-DD format
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            normalized["date"] = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            normalized["date"] = None
    
    # Store original fields for reference
    normalized["original_data"] = transaction
    
    return normalized


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Load and normalize transactions from CSV or JSON file.
    """
    path = Path(file_path)
    
    if path.suffix == ".csv":
        transactions = _load_csv(path)
    elif path.suffix == ".json":
        transactions = _load_json(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")
    
    # Normalize each transaction
    return [normalize_transaction(tx) for tx in transactions]


def _load_csv(file_path: Path) -> List[Dict[str, Any]]:
    """Load transactions from CSV file."""
    transactions = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append(dict(row))
    return transactions


def _load_json(file_path: Path) -> List[Dict[str, Any]]:
    """Load transactions from JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data: List[Dict[str, Any]] = json.load(f)
        return data


def save_validation_report(
    validated: List[Dict[str, Any]],
    missing_from_json: List[Dict[str, Any]],
    extra_in_json: List[Dict[str, Any]],
    discrepancies: List[Tuple[Dict[str, Any], Dict[str, Any], List[str]]],
    output_path: str
) -> None:
    """
    Save validation results to CSV and JSON files.
    
    Args:
        validated: CSV transactions with matching JSON entries
        missing_from_json: CSV transactions not found in JSON
        extra_in_json: JSON transactions not matching any CSV entry
        discrepancies: List of (csv_tx, json_tx, discrepant_fields) tuples
        output_path: Base path for output files
    """
    report = {
        "summary": {
            "total_validated": len(validated),
            "total_missing_from_json": len(missing_from_json),
            "total_extra_in_json": len(extra_in_json),
            "total_discrepancies": len(discrepancies),
        },
        "validated_transactions": validated,
        "missing_from_json": missing_from_json,
        "extra_in_json": extra_in_json,
        "transactions_with_discrepancies": [
            {
                "csv_transaction": csv_tx,
                "json_transaction": json_tx,
                "discrepant_fields": fields
            }
            for csv_tx, json_tx, fields in discrepancies
        ]
    }
    
    # Save JSON report
    json_path = Path(output_path).with_suffix('.json')
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    
    # Save CSV summary
    csv_path = Path(output_path).with_suffix('.csv')
    df = pd.DataFrame([{
        "Category": "Validated Transactions",
        "Count": len(validated)
    }, {
        "Category": "Missing from JSON",
        "Count": len(missing_from_json)
    }, {
        "Category": "Extra in JSON",
        "Count": len(extra_in_json)
    }, {
        "Category": "Transactions with Discrepancies",
        "Count": len(discrepancies)
    }])
    
    df.to_csv(csv_path, index=False)
