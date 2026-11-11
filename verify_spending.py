import json
from collections import defaultdict

def analyze_citations(data):
    """Analyzes a list of spending data entries to identify potential citation issues."""
    errors = defaultdict(list)
    total_spending = 0
    reported_spending = 0

    for entry in data:
        # Simulate checking for missing source or inconsistent figures
        if not entry.get('source'):
            errors['missing_source'].append(entry)
        if entry.get('reported_amount') is not None and entry.get('actual_amount') is not None:
            if abs(entry['reported_amount'] - entry['actual_amount']) > entry['actual_amount'] * 0.05: # 5% tolerance
                errors['inconsistent_figures'].append(entry)
        elif entry.get('reported_amount') is None and entry.get('actual_amount') is not None:
            errors['missing_reported_amount'].append(entry)
        elif entry.get('reported_amount') is not None and entry.get('actual_amount') is None:
            errors['missing_actual_amount'].append(entry)

        # Accumulate totals for a broader check
        if entry.get('actual_amount') is not None:
            total_spending += entry['actual_amount']
        if entry.get('reported_amount') is not None:
            reported_spending += entry['reported_amount']

    # Check for overall discrepancy between reported and actual totals
    if abs(reported_spending - total_spending) > total_spending * 0.02: # 2% tolerance for overall sum
        errors['overall_discrepancy'] = {
            'total_actual': total_spending,
            'total_reported': reported_spending
        }

    return errors

if __name__ == "__main__":
    # Sample data representing official spending figures and their citations.
    # In a real scenario, this would come from a database or API.
    spending_data = [
        {
            "project": "Highway Construction",
            "ministry": "Transportation",
            "actual_amount": 1500000000,
            "reported_amount": 1480000000,
            "source": "Ministry of Transportation Annual Report 2022"
        },
        {
            "project": "Hospital Renovation",
            "ministry": "Health",
            "actual_amount": 750000000,
            "reported_amount": 750000000,
            "source": "Health Ministry Budget Statement"
        },
        {
            "project": "Education Initiative",
            "ministry": "Education",
            "actual_amount": 1200000000,
            "reported_amount": 1100000000, # Significant difference
            "source": "Education Ministry Project Overview"
        },
        {
            "project": "Defense Procurement",
            "ministry": "Defense",
            "actual_amount": 3000000000,
            "reported_amount": 3000000000,
            # Missing source for this entry
        },
        {
            "project": "Infrastructure Upgrade",
            "ministry": "Infrastructure",
            "actual_amount": 900000000,
            "reported_amount": None, # Reported amount missing
            "source": "Infrastructure Ministry Report"
        },
        {
            "project": "Research Grant",
            "ministry": "Science",
            "actual_amount": None, # Actual amount missing
            "reported_amount": 50000000,
            "source": "Science Fund Announcement"
        }
    ]

    print("Analyzing spending data for citation integrity...")
    citation_errors = analyze_citations(spending_data)

    print("\n--- Citation Error Report ---")
    if not citation_errors:
        print("No significant citation issues found.")
    else:
        for error_type, details in citation_errors.items():
            print(f"\nError Type: {error_type.replace('_', ' ').title()}")
            if error_type == 'overall_discrepancy':
                print(f"  Total Actual: {details['total_actual']:,} | Total Reported: {details['total_reported']:,}")
            else:
                for item in details:
                    print(f"  - Project: {item.get('project', 'N/A')}, Ministry: {item.get('ministry', 'N/A')}")

    print("\nAnalysis complete.")
