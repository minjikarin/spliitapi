# Spliit Python SDK

A Python SDK for interacting with the Spliit API. Spliit is an open-source expense sharing application that helps you split bills and track shared expenses with friends, family, or colleagues.

## Installation

This SDK requires Python 3.7+. You can install it directly with pip:

```bash
pip install spliit
```

For local development, you can install the package with optional dependencies:

```bash
# Install for basic usage (production)
pip install .

```

## Getting Started

To make your first API call, you'll need a Spliit group ID. You can find this in the URL when viewing your group on [Spliit](https://spliit.app).

```python
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
```

## Examples

You can find comprehensive examples for all supported operations in the sections below.

## Initialization

The client can be initialized with a group ID:

```python
from spliit import Spliit

# Initialize with group ID
client = Spliit(group_id='your_group_id_here')
```

Your group ID can be found in the URL when viewing your group on Spliit (e.g., `https://spliit.app/groups/your_group_id_here`).


## Group Operations

### Get Group Information

```python
# Get basic group information
group = client.get_group()
print(f"Group: {group['name']}")
print(f"Currency: {group['currency']}")
```

### Get Participants

```python
# Get all participants
participants = client.get_participants()
for name, participant_id in participants.items():
    print(f"{name}: {participant_id}")

# Get specific participant ID by name
john_id = client.get_username_id("John")
if john_id:
    print(f"John's ID: {john_id}")
```

### Update Group

```python
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
```

## Expense Operations

### List Expenses

```python
# Get all expenses
expenses = client.list_expenses()
print(f"Total expenses: {len(expenses['expenses'])}")

# Get expenses with pagination
expenses = client.list_expenses(limit=10, cursor=0)
for expense in expenses['expenses']:
    print(f"{expense['title']}: ${expense['amount']/100:.2f}")
```

### Get Single Expense

```python
# Get specific expense by ID
expense = client.get_expense('expense_id_here')
expense_data = expense['expense']
print(f"Title: {expense_data['title']}")
print(f"Amount: ${expense_data['amount']/100:.2f}")
print(f"Paid by: {expense_data['paidBy']}")
```

### Create Expense

```python
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
```

### Update Expense

```python
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
        (john_id, 50),
        (jane_id, 50)
    ],
    split_mode="EVENLY",
    is_reimbursement=False
)
```

### Delete Expense

```python
# Delete an expense
result = client.delete_expense('expense_id_here')
print(f"Expense deleted: {result}")
```
