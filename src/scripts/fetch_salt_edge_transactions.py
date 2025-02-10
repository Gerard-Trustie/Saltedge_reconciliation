import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from src.utils.salt_edge import SaltEdgeClient

def main():
    # Find and load environment variables
    env_path = find_dotenv()
    print(f"Loading .env from: {env_path}")
    load_dotenv(env_path, override=True)  # Force reload
    
    # Get credentials from environment variables
    app_id = os.getenv('APP_ID')
    secret = os.getenv('SECRET')
    connection_id = os.getenv('CONNECTION_ID')
    
    if not all([app_id, secret, connection_id]):
        raise ValueError("Missing required environment variables. Please check your .env file.")

    print(f"Using connection ID: {connection_id}")  # Debug print

    # Initialize the client
    client = SaltEdgeClient(app_id, secret)

    try:
        # Fetch transactions
        print("Fetching transactions...")
        transactions = client.get_transactions(connection_id)
        
        # Save to JSON file
        output_file = "transactions.json"
        client.save_transactions_to_json(transactions, output_file)
        print(f"Successfully saved transactions to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 
