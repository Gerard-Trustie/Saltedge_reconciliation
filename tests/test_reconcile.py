"""
Unit tests for reconciliation logic.
"""
import pytest
from src.reconcile import reconcile_transactions, _is_matching_transaction

def test_matching_transactions():
    source_tx = {"amount": 100.00, "date": "2024-03-20"}
    target_tx = {"amount": 100.00, "date": "2024-03-20"}
    
    assert _is_matching_transaction(source_tx, target_tx) == True

def test_non_matching_transactions():
    source_tx = {"amount": 100.00, "date": "2024-03-20"}
    target_tx = {"amount": 200.00, "date": "2024-03-20"}
    
    assert _is_matching_transaction(source_tx, target_tx) == False

def test_reconcile_transactions():
    source_data = [
        {"amount": 100.00, "date": "2024-03-20"},
        {"amount": 200.00, "date": "2024-03-21"}
    ]
    target_data = [
        {"amount": 100.00, "date": "2024-03-20"}
    ]
    
    results = reconcile_transactions(source_data, target_data)
    
    assert len(results) == 2
    assert results[0]["status"] == "matched"
    assert results[1]["status"] == "unmatched" 
