Spliit Python SDK
==================

A Python SDK for interacting with the Spliit API. Spliit is an open-source expense sharing application that helps you split bills and track shared expenses with friends, family, or colleagues.

Installation
------------

This SDK requires Python 3.7+. You can install it directly with pip:

.. code:: sh

    pip install spliit

For development or local installation, you can also install from requirements:

.. code:: sh

    # Install core dependencies
    pip install -r requirements.txt
    
    # For development (includes testing tools)
    pip install -r requirements-dev.txt

Getting Started
---------------

To make your first API call, you'll need a Spliit group ID. You can find this in the URL when viewing your group on `Spliit <https://spliit.app>`__.

.. code:: py

    from spliit import Spliit, CATEGORIES

    # Initialize the client with your group ID
    client = Spliit(group_id='your_group_id_here')

    try:
        # Get group information
        group = client.get_group()
        print(f"Group: {group['name']}")
        
        # List all expenses
        expenses = client.list_expenses()
        print(f"Found {len(expenses['expenses'])} expenses")
        
    except Exception as error:
        print(f"Error: {error}")

Examples
--------

You can find comprehensive examples for all supported operations in the sections below.

Initialization
--------------

The client can be initialized with a group ID:

.. code:: py

    from spliit import Spliit
    
    # Initialize with group ID
    client = Spliit(group_id='your_group_id_here')

Your group ID can be found in the URL when viewing your group on Spliit (e.g., `https://spliit.app/groups/your_group_id_here`).

Documentation
-------------

This SDK provides comprehensive access to Spliit's expense management features:

- `Group Information <#group-operations>`__ - Get group details and participants
- `Expense Management <#expense-operations>`__ - Full CRUD operations for expenses
- `Categories <#categories>`__ - Predefined expense categories

Group Operations
----------------

Get Group Information
~~~~~~~~~~~~~~~~~~~~~

.. code:: py

    # Get basic group information
    group = client.get_group()
    print(f"Group: {group['name']}")
    print(f"Currency: {group['currency']}")

Get Participants
~~~~~~~~~~~~~~~~

.. code:: py

    # Get all participants
    participants = client.get_participants()
    for name, participant_id in participants.items():
        print(f"{name}: {participant_id}")
    
    # Get specific participant ID by name
    john_id = client.get_username_id("John")
    if john_id:
        print(f"John's ID: {john_id}")

Update Group
~~~~~~~~~~~~

.. code:: py

    # Update group name, currency, and description
    result = client.update_group(
        name="Updated Group Name",
        currency="EUR",
        information="Trip to Europe - Updated from Python SDK"
    )
    print(f"Group updated: {result}")
    
    # Update participants (replaces all participants)
    result = client.update_group(
        participants=["Alice", "Bob", "Charlie", "David"]
    )
    
    # Update only specific fields - others remain unchanged
    result = client.update_group(
        name="New Name Only",
        information="Just updating the description"
    )

Expense Operations
------------------

List Expenses
~~~~~~~~~~~~~

.. code:: py

    # Get all expenses
    expenses = client.list_expenses()
    print(f"Total expenses: {len(expenses['expenses'])}")
    
    # Get expenses with pagination
    expenses = client.list_expenses(limit=10, cursor=0)
    for expense in expenses['expenses']:
        print(f"{expense['title']}: ${expense['amount']/100:.2f}")

Get Single Expense
~~~~~~~~~~~~~~~~~~

.. code:: py

    # Get specific expense by ID
    expense = client.get_expense('expense_id_here')
    expense_data = expense['expense']
    print(f"Title: {expense_data['title']}")
    print(f"Amount: ${expense_data['amount']/100:.2f}")
    print(f"Paid by: {expense_data['paidBy']}")

Create Expense
~~~~~~~~~~~~~~

.. code:: py

    from spliit import CATEGORIES
    
    # Get participant IDs
    participants = client.get_participants()
    john_id = participants["John"]
    jane_id = participants["Jane"]
    
    # Create a new expense
    result = client.add_expense(
        title="Dinner at Restaurant",
        paid_by=john_id,
        paid_for=[
            (john_id, 50),    # John pays 50% 
            (jane_id, 50)     # Jane pays 50%
        ],
        amount=5000,  # $50.00 (amount in cents)
        category=CATEGORIES['Food and Drink']['Dining Out']
    )
    print(f"Expense created: {result}")

Update Expense
~~~~~~~~~~~~~~

.. code:: py

    # Update expense - only provide fields you want to change
    result = client.update_expense(
        expense_id='expense_id_here',
        title="Updated Dinner Title",
        amount=6000,  # $60.00
        expense_date="2025-06-12T00:00:00.000Z"
    )
    print(f"Expense updated: {result}")
    
    # Update who paid and splitting
    result = client.update_expense(
        expense_id='expense_id_here',
        paid_by=jane_id,
        paid_for=[
            (john_id, 30),
            (jane_id, 70)
        ],
        split_mode="EVENLY",
        is_reimbursement=False
    )

Delete Expense
~~~~~~~~~~~~~~

.. code:: py

    # Delete an expense
    result = client.delete_expense('expense_id_here')
    print(f"Expense deleted: {result}")


Error Handling
--------------

All methods raise exceptions for HTTP errors:

.. code:: py

    try:
        expense = client.get_expense('invalid_expense_id')
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

Complete Example
----------------

Here's a complete example showing common operations:

.. code:: py

    from spliit import Spliit, CATEGORIES
    
    def main():
        # Initialize client
        client = Spliit(group_id='your_group_id_here')
        
        try:
            # Get group info
            group = client.get_group()
            print(f"Managing expenses for: {group['name']}")
            
            # Update group if needed
            if group['name'] == "Old Group Name":
                client.update_group(name="Updated Group Name")
                print("Group name updated!")
            
            # Get participants
            participants = client.get_participants()
            print(f"Participants: {list(participants.keys())}")
            
            # Create expense
            if len(participants) >= 2:
                names = list(participants.keys())
                payer_id = participants[names[0]]
                
                # Split evenly between all participants
                split_amount = 100 // len(participants)
                paid_for = [
                    (participant_id, split_amount) 
                    for participant_id in participants.values()
                ]
                
                result = client.add_expense(
                    title="Group Dinner",
                    paid_by=payer_id,
                    paid_for=paid_for,
                    amount=8500,  # $85.00
                    category=CATEGORIES['Food and Drink']['Dining Out']
                )
                print("Expense created successfully!")
            
            # List recent expenses
            expenses = client.list_expenses(limit=5)
            print(f"\\nRecent expenses:")
            for expense in expenses['expenses']:
                amount_dollars = expense['amount'] / 100
                print(f"- {expense['title']}: ${amount_dollars:.2f}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    if __name__ == "__main__":
        main()

List of Supported Endpoints
----------------------------

.. code:: py

    # Group Information
    client.get_group()
    client.get_participants()
    client.get_username_id('participant_name')
    client.update_group(name='New Name', currency='EUR', information='Description', participants=['Alice', 'Bob'])
    
    # Expense Management
    client.list_expenses()
    client.list_expenses(limit=20, cursor=0)
    client.get_expense('expense_id')
    client.add_expense(title='...', paid_by='...', paid_for=[...], amount=1000, category=0)
    client.update_expense('expense_id', title='...', amount=1200, expense_date='2025-06-12T00:00:00.000Z')
    client.delete_expense('expense_id')

API Coverage
------------

This SDK currently covers the following Spliit API endpoints:

**Groups (3/5 endpoints):**
- ✅ `groups.get` - Get group information
- ✅ `groups.getDetails` - Get detailed group information
- ✅ `groups.update` - Update group settings
- ❌ `groups.list` - List groups
- ❌ `groups.create` - Create new group

**Group Expenses (4/4 endpoints):**
- ✅ `groups.expenses.list` - List expenses with pagination
- ✅ `groups.expenses.get` - Get single expense
- ✅ `groups.expenses.create` - Create new expense
- ✅ `groups.expenses.update` - Update expense
- ✅ `groups.expenses.delete` - Delete expense

**Not Yet Supported:**
- Group balances and statistics
- Group activities

Contributing
------------

Want to contribute? This project is open source and welcomes contributions. Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request
