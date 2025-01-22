"""
Command-line interface for the transaction validation tool.
"""

import argparse
import logging
from pathlib import Path
from typing import List

from .reconcile import validate_transactions
from .utils import load_transactions, save_validation_report


def setup_logging(verbose: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate JSON transactions against CSV source of truth"
    )
    
    parser.add_argument(
        "csv_file",
        help="Path to CSV file (source of truth) in data directory"
    )
    parser.add_argument(
        "json_file",
        help="Path to JSON file to validate in data directory"
    )
    parser.add_argument(
        "-o", "--output",
        default="validation_report",
        help="Base name for output files (without extension)"
    )
    parser.add_argument(
        "-f", "--fields",
        nargs="+",
        help="Fields to use for matching transactions (default: date and amount)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


def get_data_dir() -> Path:
    """Get the path to the data directory."""
    current_dir = Path(__file__).parent.parent
    return current_dir / "data"


def main() -> None:
    """Main entry point for the validation tool."""
    args = parse_args()
    setup_logging(args.verbose)
    
    try:
        data_dir = get_data_dir()
        
        # Load transaction data
        csv_path = data_dir / args.csv_file
        logging.info("Loading CSV transactions (source of truth) from %s", csv_path)
        csv_data = load_transactions(str(csv_path))
        
        json_path = data_dir / args.json_file
        logging.info("Loading JSON transactions to validate from %s", json_path)
        json_data = load_transactions(str(json_path))
        
        # Perform validation
        logging.info("Validating transactions...")
        validated, missing, extra, discrepancies = validate_transactions(
            csv_data,
            json_data,
            args.fields
        )
        
        # Create reports directory if it doesn't exist
        reports_dir = data_dir.parent / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        # Save results in reports directory
        output_path = reports_dir / args.output
        logging.info("Saving validation report to %s", output_path)
        save_validation_report(
            validated,
            missing,
            extra,
            discrepancies,
            str(output_path)
        )
        
        # Print summary
        print("\nValidation Summary:")
        print(f"Validated Transactions: {len(validated)}")
        print(f"Missing from JSON: {len(missing)}")
        print(f"Extra in JSON: {len(extra)}")
        print(f"Transactions with Discrepancies: {len(discrepancies)}")
        
        logging.info("Validation completed successfully")
        
    except Exception as e:
        logging.error("Error during validation: %s", str(e))
        raise


if __name__ == "__main__":
    main() 
