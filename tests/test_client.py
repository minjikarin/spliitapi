import json
import pytest
from datetime import datetime, UTC, timezone
from spliit import Spliit, CATEGORIES

def test_get_group(mock_requests):
    """Test the get_group method."""
    mock_get, _ = mock_requests
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "group": {
                        "id": "test_group",
                        "name": "Test Group",
                        "participants": [
                            {"id": "user1", "name": "John"},
                            {"id": "user2", "name": "Jane"}
                        ]
                    }
                }
            }
        }
    }]

    client = Spliit(group_id="test_group")
    result = client.get_group()

    assert result["id"] == "test_group"
    assert result["name"] == "Test Group"
    assert len(result["participants"]) == 2
    
    # Verify the API call
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert "groups.get,groups.getDetails" in call_args[0][0]
    assert "batch" in call_args[1]["params"]

def test_get_username_id(mock_requests):
    """Test the get_username_id method."""
    mock_get, _ = mock_requests
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "group": {
                        "participants": [
                            {"id": "user1", "name": "John"},
                            {"id": "user2", "name": "Jane"}
                        ]
                    }
                }
            }
        }
    }]

    client = Spliit(group_id="test_group")
    
    # Test existing user
    assert client.get_username_id("John") == "user1"
    
    # Test non-existent user
    assert client.get_username_id("Bob") is None

def test_get_participants(mock_requests):
    """Test the get_participants method."""
    mock_get, _ = mock_requests
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "group": {
                        "participants": [
                            {"id": "user1", "name": "John"},
                            {"id": "user2", "name": "Jane"}
                        ]
                    }
                }
            }
        }
    }]

    client = Spliit(group_id="test_group")
    participants = client.get_participants()
    
    assert participants == {
        "John": "user1",
        "Jane": "user2"
    }

def test_add_expense(mock_requests):
    """Test the add_expense method."""
    _, mock_post = mock_requests
    mock_post.return_value.content.decode.return_value = "Success"

    client = Spliit(group_id="test_group")
    result = client.add_expense(
        title="Test Expense",
        paid_by="user1",
        paid_for=[("user1", 50), ("user2", 50)],
        amount=1000,
        category=CATEGORIES["Food and Drink"]["Dining Out"]
    )

    assert result == "Success"
    
    # Verify the API call
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert "groups.expenses.create" in call_args[0][0]
    
    # Verify request payload
    json_data = call_args[1]["json"]
    expense_values = json_data["0"]["json"]["expenseFormValues"]
    assert expense_values["title"] == "Test Expense"
    assert expense_values["amount"] == 1000
    assert expense_values["paidBy"] == "user1"
    assert len(expense_values["paidFor"]) == 2
    assert expense_values["category"] == CATEGORIES["Food and Drink"]["Dining Out"]

def test_categories_structure():
    """Test the CATEGORIES constant structure."""
    # Test main categories exist
    expected_categories = {
        "Uncategorized",
        "Entertainment",
        "Food and Drink",
        "Home",
        "Life",
        "Transportation",
        "Utilities"
    }
    assert set(CATEGORIES.keys()) == expected_categories
    
    # Test some specific subcategories
    assert CATEGORIES["Food and Drink"]["Dining Out"] == 8
    assert CATEGORIES["Transportation"]["Car"] == 30
    assert CATEGORIES["Utilities"]["Water"] == 42
    
    # Test value ranges
    all_values = [
        value
        for category in CATEGORIES.values()
        for value in category.values()
    ]
    assert min(all_values) == 0
    assert max(all_values) == 42
    assert len(set(all_values)) == 43  # Check all values are unique

# tests/test_utils.py
from spliit.utils import get_current_timestamp
from datetime import datetime, UTC

def test_get_current_timestamp():
    """Test the get_current_timestamp function."""
    timestamp = get_current_timestamp()
    
    # Verify format
    assert len(timestamp) == 24  # Length of ISO format with milliseconds
    assert timestamp.endswith('Z')  # UTC timezone marker
    assert 'T' in timestamp  # ISO datetime separator
    
    # Verify it can be parsed back to datetime
    dt = datetime.strptime(
        timestamp,
        '%Y-%m-%dT%H:%M:%S.%fZ'
    ).replace(tzinfo=timezone.utc)  # Explicitly attach UTC timezone
    
    assert dt.tzinfo is not None  # Should be timezone-aware
    assert dt.tzinfo == timezone.utc  # Should be UTC specifically

def test_list_expenses(mock_requests):
    """Test the list_expenses method."""
    mock_get, _ = mock_requests
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "expenses": [
                        {"id": "exp1", "title": "Dinner", "amount": 5000},
                        {"id": "exp2", "title": "Groceries", "amount": 3000}
                    ],
                    "nextCursor": 2
                }
            }
        }
    }]

    client = Spliit(group_id="test_group")
    result = client.list_expenses()
    
    assert len(result["expenses"]) == 2
    assert result["expenses"][0]["title"] == "Dinner"
    assert result["nextCursor"] == 2
    
    # Test with pagination
    result_paginated = client.list_expenses(cursor=0, limit=10)
    
    # Verify API calls
    assert mock_get.call_count == 2
    call_args = mock_get.call_args_list[1]
    assert "groups.expenses.list" in call_args[0][0]
    # Verify pagination parameters
    input_data = json.loads(call_args[1]["params"]["input"])
    assert input_data["0"]["json"]["cursor"] == 0
    assert input_data["0"]["json"]["limit"] == 10

def test_get_expense(mock_requests):
    """Test the get_expense method."""
    mock_get, _ = mock_requests
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "expense": {
                        "id": "exp1",
                        "title": "Test Expense",
                        "amount": 1000,
                        "paidBy": "user1",
                        "category": 8
                    }
                }
            }
        }
    }]

    client = Spliit(group_id="test_group")
    result = client.get_expense("exp1")
    
    assert result["expense"]["id"] == "exp1"
    assert result["expense"]["title"] == "Test Expense"
    assert result["expense"]["amount"] == 1000
    
    # Verify API call
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert "groups.expenses.get" in call_args[0][0]
    input_data = json.loads(call_args[1]["params"]["input"])
    assert input_data["0"]["json"]["expenseId"] == "exp1"

def test_update_expense(mock_requests):
    """Test the update_expense method."""
    mock_get, mock_post = mock_requests
    # Mock get_expense response
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "expense": {
                        "id": "exp1",
                        "title": "Old Title",
                        "amount": 1000,
                        "paidBy": {"id": "user1", "name": "User 1"},
                        "categoryId": 8,
                        "expenseDate": "2024-01-01T12:00:00.000Z",
                        "splitMode": "EVENLY",
                        "isReimbursement": False,
                        "paidFor": [{"participantId": "user1", "shares": 100, "expenseId": "exp1"}],
                        "notes": ""
                    }
                }
            }
        }
    }]
    mock_post.return_value.content.decode.return_value = "Updated"

    client = Spliit(group_id="test_group")
    result = client.update_expense(
        expense_id="exp1",
        title="New Title",
        amount=1500
    )
    
    assert result == "Updated"
    
    # Verify API calls
    mock_get.assert_called_once()
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert "groups.expenses.update" in call_args[0][0]
    
    # Verify request payload
    json_data = call_args[1]["json"]
    assert json_data["0"]["json"]["expenseId"] == "exp1"
    expense_values = json_data["0"]["json"]["expenseFormValues"]
    assert expense_values["title"] == "New Title"
    assert expense_values["amount"] == 1500
    # Check that meta field is included
    assert "meta" in json_data["0"]
    assert json_data["0"]["meta"]["values"]["expenseFormValues.expenseDate"] == ["Date"]

def test_delete_expense(mock_requests):
    """Test the delete_expense method."""
    _, mock_post = mock_requests
    mock_post.return_value.content.decode.return_value = "Deleted"

    client = Spliit(group_id="test_group")
    result = client.delete_expense("exp1")
    
    assert result == "Deleted"
    
    # Verify API call
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert "groups.expenses.delete" in call_args[0][0]
    
    # Verify request payload
    json_data = call_args[1]["json"]
    assert json_data["0"]["json"]["expenseId"] == "exp1"
    assert json_data["0"]["json"]["groupId"] == "test_group"

def test_update_group(mock_requests):
    """Test the update_group method."""
    mock_get, mock_post = mock_requests
    # Mock get_group response
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "group": {
                        "id": "test_group",
                        "name": "Old Group Name",
                        "currency": "USD",
                        "participants": [
                            {"id": "user1", "name": "John"},
                            {"id": "user2", "name": "Jane"}
                        ]
                    }
                }
            }
        }
    }]
    mock_post.return_value.content.decode.return_value = "Updated"

    client = Spliit(group_id="test_group")
    result = client.update_group(
        name="New Group Name",
        currency="EUR",
        information="Updated from Python SDK"
    )
    
    assert result == "Updated"
    
    # Verify API calls
    mock_get.assert_called_once()
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert "groups.update" in call_args[0][0]
    
    # Verify request payload
    json_data = call_args[1]["json"]
    assert json_data["0"]["json"]["groupId"] == "test_group"
    group_values = json_data["0"]["json"]["groupFormValues"]
    assert group_values["name"] == "New Group Name"
    assert group_values["currency"] == "EUR"
    assert group_values["information"] == "Updated from Python SDK"
    # Should preserve existing participants
    assert len(group_values["participants"]) == 2

def test_update_group_participants(mock_requests):
    """Test the update_group method with participant changes."""
    mock_get, mock_post = mock_requests
    # Mock get_group response
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "group": {
                        "id": "test_group",
                        "name": "Test Group",
                        "currency": "USD",
                        "participants": [
                            {"id": "user1", "name": "John"},
                            {"id": "user2", "name": "Jane"}
                        ]
                    }
                }
            }
        }
    }]
    mock_post.return_value.content.decode.return_value = "Updated"

    client = Spliit(group_id="test_group")
    result = client.update_group(
        participants=["Alice", "Bob", "Charlie"]
    )
    
    assert result == "Updated"
    
    # Verify request payload
    call_args = mock_post.call_args
    json_data = call_args[1]["json"]
    group_values = json_data["0"]["json"]["groupFormValues"]
    
    # Should update participants
    assert len(group_values["participants"]) == 3
    participant_names = [p["name"] for p in group_values["participants"]]
    assert participant_names == ["Alice", "Bob", "Charlie"]
    
    # Should preserve existing name and currency
    assert group_values["name"] == "Test Group"
    assert group_values["currency"] == "USD"

def test_update_group_information_only(mock_requests):
    """Test updating only the information field."""
    mock_get, mock_post = mock_requests
    # Mock get_group response with existing information
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "group": {
                        "id": "test_group",
                        "name": "Test Group",
                        "currency": "USD",
                        "information": "Old description",
                        "participants": [
                            {"id": "user1", "name": "John"}
                        ]
                    }
                }
            }
        }
    }]
    mock_post.return_value.content.decode.return_value = "Updated"

    client = Spliit(group_id="test_group")
    result = client.update_group(information="New description from API")
    
    assert result == "Updated"
    
    # Verify request payload
    call_args = mock_post.call_args
    json_data = call_args[1]["json"]
    group_values = json_data["0"]["json"]["groupFormValues"]
    
    # Should update only information
    assert group_values["information"] == "New description from API"
    # Should preserve existing fields
    assert group_values["name"] == "Test Group"
    assert group_values["currency"] == "USD"
    assert len(group_values["participants"]) == 1

def test_update_expense_format_exact(mock_requests):
    """Test that update_expense generates the exact API format."""
    mock_get, mock_post = mock_requests
    # Mock get_expense response
    mock_get.return_value.json.return_value = [{
        "result": {
            "data": {
                "json": {
                    "expense": {
                        "id": "KkUUY78C",
                        "title": "Old Title",
                        "amount": 5000,
                        "paidBy": "5xt0dyVY9H877UmxqIBvM",
                        "category": 7,
                        "expenseDate": "2025-06-11T00:00:00.000Z",
                        "splitMode": "EVENLY",
                        "isReimbursement": False,
                        "paidFor": [
                            {"participant": "5xt0dyVY9H877UmxqIBvM", "shares": 100}
                        ]
                    }
                }
            }
        }
    }]
    mock_post.return_value.content.decode.return_value = "Updated"

    client = Spliit(group_id="mlJlb")
    result = client.update_expense(
        expense_id="KkUUY78C",
        title="Dinner at Restaurant",
        category=8,
        amount=7000,
        expense_date="2025-06-12T00:00:00.000Z",
        paid_for=[
            ("5xt0dyVY9H877UmxqIBvM", 50),
            ("Xk19w47KWFRrtmV2tV17f", 50)
        ]
    )
    
    assert result == "Updated"
    
    # Verify the exact payload format
    call_args = mock_post.call_args
    json_data = call_args[1]["json"]
    
    expected_structure = {
        "0": {
            "json": {
                "expenseId": "KkUUY78C",
                "groupId": "mlJlb",
                "expenseFormValues": {
                    "expenseDate": "2025-06-12T00:00:00.000Z",
                    "title": "Dinner at Restaurant",
                    "category": 8,
                    "amount": 7000,
                    "paidBy": "5xt0dyVY9H877UmxqIBvM",
                    "paidFor": [
                        {
                            "participant": "5xt0dyVY9H877UmxqIBvM",
                            "shares": 50
                        },
                        {
                            "participant": "Xk19w47KWFRrtmV2tV17f",
                            "shares": 50
                        }
                    ],
                    "splitMode": "EVENLY",
                    "saveDefaultSplittingOptions": False,
                    "isReimbursement": False
                }
            },
            "meta": {
                "values": {
                    "expenseFormValues.expenseDate": ["Date"]
                }
            }
        }
    }
    
    # Check key fields match the expected structure
    assert json_data["0"]["json"]["expenseId"] == expected_structure["0"]["json"]["expenseId"]
    assert json_data["0"]["json"]["groupId"] == expected_structure["0"]["json"]["groupId"]
    
    expense_values = json_data["0"]["json"]["expenseFormValues"]
    expected_values = expected_structure["0"]["json"]["expenseFormValues"]
    
    assert expense_values["expenseDate"] == expected_values["expenseDate"]
    assert expense_values["title"] == expected_values["title"]
    assert expense_values["category"] == expected_values["category"]
    assert expense_values["amount"] == expected_values["amount"]
    assert expense_values["splitMode"] == expected_values["splitMode"]
    assert expense_values["saveDefaultSplittingOptions"] == expected_values["saveDefaultSplittingOptions"]
    assert expense_values["isReimbursement"] == expected_values["isReimbursement"]
    assert expense_values["paidFor"] == expected_values["paidFor"]
    
    # Check meta structure
    assert json_data["0"]["meta"]["values"]["expenseFormValues.expenseDate"] == ["Date"]
