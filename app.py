"""
Demo Application

Shows how the complete pipeline works when properly implemented.
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    """Run demo pipeline"""
    print("Ticket Routing Challenge - Demo Application")
    print()
    print("To run this pipeline, implement the required components:")
    print("  1. load_ticket_data() in data_loader.py")
    print("  2. TicketRouter class in ticket_router.py")
    print("  3. EntityExtractor class in entity_extractor.py")
    print()
    print("Run the tests to verify your implementation:")

if __name__ == "__main__":
    main()

