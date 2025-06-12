import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import requests

from .utils import format_expense_payload

@dataclass
class Spliit:
    """Client for interacting with the Spliit API."""
    
    group_id: str
    base_url: str = "https://spliit.app/api/trpc"
    
    def get_group(self) -> Dict:
        """Get group details."""
        params_input = {
            "0": {"json": {"groupId": self.group_id}},
            "1": {"json": {"groupId": self.group_id}}
        }
        
        params = {
            "batch": "1",
            "input": json.dumps(params_input)
        }
        
        response = requests.get(
            f"{self.base_url}/groups.get,groups.getDetails",
            params=params
        )
        response.raise_for_status()
        return response.json()[0]["result"]["data"]["json"]["group"]
    
    def get_username_id(self, name: str) -> Optional[str]:
        """Get participant ID by name."""
        group = self.get_group()
        for participant in group["participants"]:
            if name == participant["name"]:
                return participant["id"]
        return None
    
    def get_participants(self) -> Dict[str, str]:
        """Get all participants with their IDs."""
        group = self.get_group()
        return {
            participant["name"]: participant["id"]
            for participant in group["participants"]
        }
    
    def add_expense(
        self,
        title: str,
        paid_by: str,
        paid_for: List[Tuple[str, int]],
        amount: int = 1300,
        category: int = 0
    ) -> str:
        """Add a new expense to the group."""
        params = {"batch": "1"}
        
        json_data = format_expense_payload(
            self.group_id,
            title,
            paid_by,
            paid_for,
            amount,
            category
        )
        
        response = requests.post(
            f"{self.base_url}/groups.expenses.create",
            params=params,
            json=json_data
        )
        response.raise_for_status()
        return response.content.decode()
    
    def list_expenses(self, cursor: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """List expenses in the group with optional pagination."""
        input_json = {"groupId": self.group_id}
        if cursor is not None:
            input_json["cursor"] = cursor
        if limit is not None:
            input_json["limit"] = limit
            
        params = {
            "batch": "1",
            "input": json.dumps({"0": {"json": input_json}})
        }
        
        response = requests.get(
            f"{self.base_url}/groups.expenses.list",
            params=params
        )
        response.raise_for_status()
        return response.json()[0]["result"]["data"]["json"]
    
    def get_expense(self, expense_id: str) -> Dict:
        """Get a specific expense by ID."""
        params = {
            "batch": "1",
            "input": json.dumps({
                "0": {
                    "json": {
                        "groupId": self.group_id,
                        "expenseId": expense_id
                    }
                }
            })
        }
        
        response = requests.get(
            f"{self.base_url}/groups.expenses.get",
            params=params
        )
        response.raise_for_status()
        return response.json()[0]["result"]["data"]["json"]
    
    def update_expense(
        self,
        expense_id: str,
        title: Optional[str] = None,
        paid_by: Optional[str] = None,
        paid_for: Optional[List[Tuple[str, int]]] = None,
        amount: Optional[int] = None,
        category: Optional[int] = None,
        expense_date: Optional[str] = None,
        split_mode: Optional[str] = None,
        is_reimbursement: Optional[bool] = None
    ) -> str:
        """Update an existing expense."""
        # Get current expense to merge with updates
        current_expense = self.get_expense(expense_id)
        expense_data = current_expense["expense"]
        
        # Extract paidBy ID from the response (it's an object with id field)
        current_paid_by = expense_data["paidBy"]["id"] if isinstance(expense_data["paidBy"], dict) else expense_data["paidBy"]
        
        # Build updated expense form values
        expense_form_values = {
            "expenseDate": expense_date if expense_date is not None else expense_data["expenseDate"],
            "title": title if title is not None else expense_data["title"],
            "category": category if category is not None else expense_data["categoryId"],
            "amount": amount if amount is not None else expense_data["amount"],
            "paidBy": paid_by if paid_by is not None else current_paid_by,
            "splitMode": split_mode if split_mode is not None else expense_data.get("splitMode", "EVENLY"),
            "saveDefaultSplittingOptions": False,
            "isReimbursement": is_reimbursement if is_reimbursement is not None else expense_data.get("isReimbursement", False)
        }
        
        # Handle paid_for update
        if paid_for is not None:
            expense_form_values["paidFor"] = [
                {"participant": participant_id, "shares": shares}
                for participant_id, shares in paid_for
            ]
        else:
            # Convert the paidFor format from API response to update format
            expense_form_values["paidFor"] = [
                {"participant": item["participantId"], "shares": item["shares"]}
                for item in expense_data["paidFor"]
            ]
        
        params = {"batch": "1"}
        json_data = {
            "0": {
                "json": {
                    "expenseId": expense_id,
                    "groupId": self.group_id,
                    "expenseFormValues": expense_form_values
                },
                "meta": {
                    "values": {
                        "expenseFormValues.expenseDate": ["Date"]
                    }
                }
            }
        }
        
        response = requests.post(
            f"{self.base_url}/groups.expenses.update",
            params=params,
            json=json_data
        )
        response.raise_for_status()
        return response.content.decode()
    
    def delete_expense(self, expense_id: str) -> str:
        """Delete an expense from the group."""
        params = {"batch": "1"}
        json_data = {
            "0": {
                "json": {
                    "expenseId": expense_id,
                    "groupId": self.group_id
                }
            }
        }
        
        response = requests.post(
            f"{self.base_url}/groups.expenses.delete",
            params=params,
            json=json_data
        )
        response.raise_for_status()
        return response.content.decode()
    
    def update_group(
        self,
        name: Optional[str] = None,
        currency: Optional[str] = None,
        information: Optional[str] = None,
        participants: Optional[List[str]] = None
    ) -> str:
        """Update group details."""
        # Get current group data to merge with updates
        current_group = self.get_group()
        
        # Build updated group form values
        group_form_values = {
            "name": name if name is not None else current_group["name"],
            "currency": currency if currency is not None else current_group["currency"]
        }
        
        # Add information field if provided or preserve existing
        if information is not None:
            group_form_values["information"] = information
        elif "information" in current_group:
            group_form_values["information"] = current_group["information"]
        
        # Handle participants update
        if participants is not None:
            group_form_values["participants"] = [{"name": name} for name in participants]
        else:
            group_form_values["participants"] = current_group["participants"]
        
        params = {"batch": "1"}
        json_data = {
            "0": {
                "json": {
                    "groupId": self.group_id,
                    "groupFormValues": group_form_values
                }
            }
        }
        
        response = requests.post(
            f"{self.base_url}/groups.update",
            params=params,
            json=json_data
        )
        response.raise_for_status()
        return response.content.decode()