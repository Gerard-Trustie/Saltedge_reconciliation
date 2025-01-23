"""
Command-line interface for recurring payments detection.
"""

import argparse
import logging
import statistics
from pathlib import Path

from .utils import load_transactions
from .recurring_payments import RecurringPaymentDetector, generate_recurring_payments_report


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
        description="Identify recurring payments in transaction data"
    )
    
    parser.add_argument(
        "json_file",
        help="Path to JSON transaction file in data directory"
    )
    parser.add_argument(
        "-o", "--output",
        default="recurring_payments_report",
        help="Base name for output files (without extension)"
    )
    parser.add_argument(
        "--monthly-tolerance",
        type=int,
        default=3,
        help="Tolerance in days for monthly patterns (default: 3)"
    )
    parser.add_argument(
        "--weekly-tolerance",
        type=int,
        default=1,
        help="Tolerance in days for weekly patterns (default: 1)"
    )
    parser.add_argument(
        "--amount-tolerance",
        type=float,
        default=0.05,
        help="Tolerance percentage for amount variations (default: 0.05 = 5%%)"
    )
    parser.add_argument(
        "--description-similarity",
        type=float,
        default=0.85,
        help="Minimum similarity ratio for descriptions (default: 0.85)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


def main() -> None:
    """Main entry point for recurring payments detection."""
    args = parse_args()
    setup_logging(args.verbose)
    
    try:
        # Get data directory
        data_dir = Path(__file__).parent.parent / "data"
        reports_dir = data_dir.parent / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        # Load transaction data
        json_path = data_dir / args.json_file
        logging.info("Loading transactions from %s", json_path)
        transactions = load_transactions(str(json_path))
        
        # Create detector with configured tolerances
        detector = RecurringPaymentDetector(
            monthly_date_tolerance=args.monthly_tolerance,
            weekly_date_tolerance=args.weekly_tolerance,
            amount_tolerance=args.amount_tolerance,
            description_similarity=args.description_similarity
        )
        
        # Find recurring payments
        logging.info("Analyzing transactions for recurring patterns...")
        recurring_payments = detector.find_recurring_payments(transactions)
        
        # Generate report
        output_path = reports_dir / f"{args.output}.json"
        logging.info("Saving recurring payments report to %s", output_path)
        generate_recurring_payments_report(recurring_payments, str(output_path))
        
        # Print summary
        print("\nRecurring Payments Summary:")
        print(f"Total recurring payment groups: {len(recurring_payments)}")
        for desc, txs in recurring_payments.items():
            print(f"\n{desc}:")
            print(f"  Number of transactions: {len(txs)}")
            print(f"  Average amount: £{abs(statistics.mean(tx['amount'] for tx in txs)):.2f}")
        
        logging.info("Analysis completed successfully")
        
    except Exception as e:
        logging.error("Error during analysis: %s", str(e))
        raise


if __name__ == "__main__":
    main() 
