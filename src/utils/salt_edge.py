import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SaltEdgeClient:
    def __init__(self, app_id: str, secret: str):
        self.base_url = "https://www.saltedge.com/api/v5"
        self.headers = {
            "app-id": app_id,
            "secret": secret,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def check_connection(self, connection_id: str) -> Dict:
        """
        Check if the connection is active and valid.
        
        Args:
            connection_id: The Salt Edge connection ID
            
        Returns:
            Connection information dictionary
        """
        url = f"{self.base_url}/connections/{connection_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to check connection: {str(e)}")

    def get_transactions(
        self,
        connection_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch transactions from Salt Edge API and return as JSON.
        
        Args:
            connection_id: The Salt Edge connection ID
            from_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            to_date: End date in YYYY-MM-DD format (default: today)
        
        Returns:
            List of transaction dictionaries
            
        Todo:
            * Remove hardcoded CONNECTION_ID from environment variables
            * Use passed connection_id parameter instead of environment variable
            * Make date range configurable (currently hardcoded to 365 days)
            * Add error handling for specific API error responses
            * Add retry logic for failed requests
        """
        # First check if the connection is valid
        try:
            self.check_connection(connection_id)
        except Exception as e:
            raise Exception(f"Invalid connection: {str(e)}")

        # Set default date range if not provided
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        if not from_date:
            from_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        url = f"{self.base_url}/transactions"
        params = {
            "connection_id": connection_id,
            "from_date": from_date,
            "to_date": to_date
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch transactions: {str(e)}")

    def save_transactions_to_json(
        self,
        transactions: List[Dict],
        output_file: str
    ) -> None:
        """
        Save transactions to a JSON file.
        
        Args:
            transactions: List of transaction dictionaries
            output_file: Path to save the JSON file
        """
        with open(output_file, 'w') as f:
            json.dump(transactions, f, indent=2) 
