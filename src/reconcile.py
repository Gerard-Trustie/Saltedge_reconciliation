"""
Main reconciliation logic for matching and processing transactions.
"""

from typing import Dict, List, Any


def reconcile_transactions(
    source_data: List[Dict[str, Any]], target_data: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Reconcile transactions between two data sources.

    Args:
        source_data: List of transaction dictionaries from source system
        target_data: List of transaction dictionaries from target system

    Returns:
        List of reconciled transactions with matching status
    """
    reconciled = []

    for source_tx in source_data:
        match = None
        for target_tx in target_data:
            if _is_matching_transaction(source_tx, target_tx):
                match = target_tx
                break

        reconciled.append(
            {
                "source_transaction": source_tx,
                "target_transaction": match,
                "status": "matched" if match else "unmatched",
            }
        )

    return reconciled


def _is_matching_transaction(source_tx: Dict[str, Any], target_tx: Dict[str, Any]) -> bool:
    """
    Compare two transactions to determine if they match.

    Args:
        source_tx: Transaction from source system
        target_tx: Transaction from target system

    Returns:
        Boolean indicating if transactions match
    """
    # Add your matching logic here
    # Example: Match on amount and date
    return source_tx.get("amount") == target_tx.get("amount") and source_tx.get(
        "date"
    ) == target_tx.get("date")
