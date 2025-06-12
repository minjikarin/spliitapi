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
# Install core dependencies only
pip install -r requirements.txt

# OR install development dependencies (includes testing tools)
pip install -r requirements-dev.txt
```

## Testing Your Local Installation

### 1. Verify Installation

```python
# Test in Python REPL
python3
>>> from spliit import Spliit, CATEGORIES
>>> print("SDK imported successfully!")
>>> print(f"Available categories: {len(CATEGORIES)}")
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

## Local Development Workflow

### 1. Making Changes

After making code changes:

```bash
# No need to reinstall - changes are automatically reflected
# Just run tests to verify
python3 -m pytest tests/test_client.py -v
```

### 2. Adding New Features

When adding new methods:

1. **Add the method to `src/spliit/client.py`**
2. **Add tests to `tests/test_client.py`**
3. **Update documentation in `README.md`**
4. **Run tests to ensure everything works**

```bash
# Example workflow
# 1. Edit src/spliit/client.py
# 2. Add tests
# 3. Run tests
python3 -m pytest tests/test_client.py::test_your_new_method -v
```

### 3. Testing Different Scenarios

```python
# Create a test script: test_local.py
from spliit import Spliit, CATEGORIES

def test_local_development():
    """Test script for local development."""
    print("Testing Spliit SDK locally...")
    
    # Test categories
    print(f"Food categories: {CATEGORIES['Food and Drink']}")
    
    # Test client initialization
    client = Spliit(group_id='test_id')
    print("Client created successfully!")
    
    # Add your specific tests here
    
if __name__ == "__main__":
    test_local_development()
```

Run your test script:
```bash
python3 test_local.py
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
├── pyproject.toml           # Package configuration
└── LICENSE                  # License file
```

## Common Development Tasks

### Adding a New API Endpoint

1. **Study the API endpoint structure** from the Spliit API documentation
2. **Add method to `client.py`**:
   ```python
   def new_method(self, param1: str, param2: Optional[int] = None) -> Dict:
       """Description of what this method does."""
       params = {"batch": "1"}
       json_data = {
           "0": {
               "json": {
                   "groupId": self.group_id,
                   "param1": param1,
                   "param2": param2
               }
           }
       }
       
       response = requests.post(
           f"{self.base_url}/endpoint.path",
           params=params,
           json=json_data
       )
       response.raise_for_status()
       return response.json()[0]["result"]["data"]["json"]
   ```

3. **Add comprehensive tests**:
   ```python
   def test_new_method(mock_requests):
       """Test the new_method."""
       mock_get, mock_post = mock_requests
       mock_post.return_value.json.return_value = [{"result": {"data": {"json": "success"}}}]
       
       client = Spliit(group_id="test_group")
       result = client.new_method("test_param")
       
       assert result == "success"
       mock_post.assert_called_once()
   ```

4. **Update README.md** with usage examples

### Debugging Issues

1. **Check import errors**:
   ```bash
   python3 -c "from spliit import Spliit; print('Import successful')"
   ```

2. **Reinstall in development mode**:
   ```bash
   pip install -e . --force-reinstall
   ```

3. **Check test failures**:
   ```bash
   python3 -m pytest tests/ -v --tb=short
   ```

## Running Different Test Scenarios

### Mock Testing (Default)
```bash
# Uses mocked HTTP responses
python3 -m pytest tests/test_client.py -v
```

### Integration Testing
```bash
# Create integration_test.py for real API testing
python3 integration_test.py
```

### Performance Testing
```bash
# Test with larger datasets
python3 -c "
from spliit import Spliit
import time

start = time.time()
client = Spliit(group_id='test')
# Add performance tests here
print(f'Completed in {time.time() - start:.2f}s')
"
```

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'spliit'**
   ```bash
   pip install -e .
   ```

2. **Tests failing after changes**
   ```bash
   pip install -e . --force-reinstall
   python3 -m pytest tests/ -v
   ```

3. **Python path issues**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

### Getting Your Group ID

1. Go to [Spliit.app](https://spliit.app)
2. Open your group
3. Copy the group ID from the URL: `https://spliit.app/groups/YOUR_GROUP_ID_HERE`

## Best Practices

1. **Always write tests** for new functionality
2. **Follow existing code patterns** for consistency
3. **Update documentation** when adding features
4. **Test with real API calls** when possible
5. **Handle errors gracefully** with proper exceptions
6. **Use type hints** for better code clarity

## Submitting Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and test**:
   ```bash
   python3 -m pytest tests/ -v
   ```

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

4. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Need Help?

If you encounter any issues during development:

1. Check the test files for usage examples
2. Review the existing code patterns in `client.py`
3. Look at the Spliit API documentation
4. Open an issue on the GitHub repository

Happy coding! 🚀