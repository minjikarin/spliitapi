#!/usr/bin/env python3
"""
Example usage of the Spliit Python SDK for local testing.
Replace 'your_group_id_here' with your actual Spliit group ID.
"""

from spliit import Spliit, CATEGORIES

def main():
    # Replace with your actual group ID from Spliit
    group_id = "your_group_id_here"
    client = Spliit(group_id=group_id)
    
    try:
        print("🚀 Testing Spliit Python SDK locally...")
        
        # Test 1: Get group information
        print("\n📋 Getting group information...")
        group = client.get_group()
        print(f"Group: {group['name']}")
        print(f"Currency: {group['currency']}")
        if 'information' in group:
            print(f"Description: {group['information']}")
        
        # Test 2: Get participants
        print("\n👥 Getting participants...")
        participants = client.get_participants()
        print(f"Participants: {list(participants.keys())}")
        
        # Test 3: Update group (optional - uncomment to test)
        # print("\n✏️  Updating group...")
        # result = client.update_group(
        #     information="Updated from Python SDK - Local Test"
        # )
        # print(f"Update result: {result}")
        
        # Test 3a: Update expense (optional - uncomment to test)
        # if expenses.get('expenses') and len(expenses['expenses']) > 0:
        #     expense_id = expenses['expenses'][0]['id']
        #     print(f"\n✏️  Updating expense {expense_id}...")
        #     result = client.update_expense(
        #         expense_id=expense_id,
        #         title="Updated from Python SDK"
        #     )
        #     print(f"Update result: {result}")
        
        # Test 4: List expenses
        print("\n💰 Listing recent expenses...")
        expenses = client.list_expenses(limit=5)
        if expenses.get('expenses'):
            for expense in expenses['expenses']:
                amount_dollars = expense['amount'] / 100
                print(f"- {expense['title']}: ${amount_dollars:.2f}")
        else:
            print("No expenses found")
        
        # Test 5: Show available categories
        print("\n📂 Available expense categories:")
        for category_name, subcategories in CATEGORIES.items():
            print(f"- {category_name}: {len(subcategories)} subcategories")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure to:")
        print("1. Replace 'your_group_id_here' with your actual group ID")
        print("2. Check your internet connection")
        print("3. Verify the group ID is correct")

if __name__ == "__main__":
    main()