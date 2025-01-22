"""
Helper functions for loading, saving and processing transaction data.
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Load transactions from CSV or JSON file.

    Args:
        file_path: Path to the transaction file

    Returns:
        List of transaction dictionaries
    """
    path = Path(file_path)

    if path.suffix == ".csv":
        return _load_csv(path)
    if path.suffix == ".json":
        return _load_json(path)
    raise ValueError(f"Unsupported file format: {path.suffix}")


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


def save_results(results: List[Dict[str, Any]], output_path: str) -> None:
    """
    Save reconciliation results to JSON file.

    Args:
        results: List of reconciled transactions
        output_path: Path to save results
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
