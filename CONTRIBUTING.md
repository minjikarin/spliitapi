# Contributing to Spliit Python SDK

Thank you for your interest in contributing to the Spliit Python SDK! This guide will help you set up a local development environment and test the SDK locally.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/spliitapi.git
cd spliitapi
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install in Development Mode

Install the package in "editable" mode so changes are reflected immediately:

```bash
pip install -e .
```

This installs the package locally and creates symlinks so any code changes are immediately available.

### 4. Install Development Dependencies

```bash
# Install with all development dependencies
pip install -e .[dev,test]
```

## Testing Your Local Installation

### 1. Verify Installation

```python
# Test in Python REPL
python3
>>> from spliit import Spliit, CATEGORIES
>>> print("SDK imported successfully!")]
```

### 2. Run Unit Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_client.py -v

# Run specific test
python3 -m pytest tests/test_client.py::test_get_group -v
```

### 3. Test with Real API (Optional)

If you have a Spliit group ID, you can test with the real API:

```python
from spliit import Spliit, CATEGORIES

# Replace with your actual group ID
client = Spliit(group_id='your_group_id_here')

try:
    # Test basic functionality
    group = client.get_group()
    print(f"Group: {group['name']}")
    
    participants = client.get_participants()
    print(f"Participants: {list(participants.keys())}")
    
    # Test listing expenses
    expenses = client.list_expenses(limit=5)
    print(f"Found {len(expenses.get('expenses', []))} expenses")
    
except Exception as e:
    print(f"Error: {e}")
```

## Project Structure

```
spliitapi/
├── src/spliit/
│   ├── __init__.py          # Main imports and CATEGORIES
│   ├── client.py            # Spliit client class
│   └── utils.py             # Utility functions
├── tests/
│   ├── conftest.py          # Test configuration
│   └── test_client.py       # Test cases
├── README.md                # Documentation
├── CONTRIBUTING.md          # This file
└── pyproject.toml           # Package configuration

```


## Getting Your Group ID

1. Go to [Spliit.app](https://spliit.app)
2. Open your group
3. Copy the group ID from the URL: `https://spliit.app/groups/YOUR_GROUP_ID_HERE`
