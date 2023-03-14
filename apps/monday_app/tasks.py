from boilerplate_django_celery.celery import app
from apps.monday_app.utils import (
    get_leads_board_columns, 
    get_customers_board_columns,
    create_monday_entry, 
    update_monday_entry
)
import requests
import json
import os

@app.task
def save_to_monday(customer_pk, board_type, is_new, package_pk=None, customer_monday_id=None):
    from apps.accounts.models import Customer
    """
    This is the main task responsible for syncing the customer details to monday.com
    It is all functional and adding a new lead to monday.com is working.
    pass in "leads", "customers" or "packages" as the board_type as the first argument
    """

    try:
        # Get customer details
        customer = Customer.objects.get(pk=customer_pk) 
        customer_full_name = f'{customer.first_name} {customer.last_name}'
        print(f"Attempting to update monday.com board...")
        print(f"Customer: {customer_full_name}, email: {customer.email}, pk: {customer.pk}, board_type: {board_type}")

        # Make monday headers & url
        url = os.environ.get('MONDAY_API_URL')
        if board_type == 'lead':
            board_id_env = os.environ.get('MONDAY_LEADS_BOARD_ID')
        elif board_type == 'customer':
            board_id_env = os.environ.get('MONDAY_CUSTOMERS_BOARD_ID')
        elif board_type == 'package':
            board_id_env = os.environ.get('MONDAY_PACKAGES_BOARD_ID')
        else:
            print('Invalid board type provided!') # TODO - Error handling
        board_id = int(board_id_env)
        monday_api_key = os.environ.get(
            "MONDAY_API_KEY"
        ) 
        headers = {"Authorization": monday_api_key}

        # Get monday board details
        monday_query_string = 'query {{boards (ids: {}) {{owners {{id}} columns {{id title type}} }} }}'.format(board_id)
        request_json = {"query": monday_query_string}
        response = requests.get(url, headers=headers, json=request_json)
        response.raise_for_status()
        data = response.json()
        board = data["data"]["boards"][0]
        columns = board["columns"]

        # Set up which columns to modify
        if board_type == 'lead':
            new_column_values = get_leads_board_columns(customer, columns)
        elif board_type == 'customer':
            new_column_values = get_customers_board_columns(customer, columns)

        # Create or update the contact on monday.com
        if is_new:
            monday_id = create_monday_entry(customer, board_id, url, headers, new_column_values)
        else:
            monday_id = update_monday_entry(customer, board_id, url, headers, customer.monday_id, new_column_values)

        # Check if contact was created / handle errors
        if not monday_id:
            print('ERROR: Failed to create/update contact on monday.com')
            return False
        
        print(f'Successfully synced {customer} to Monday.com {board_type} board...')
        return monday_id
    except Exception as e:
        # TODO - Error handling
        print(f"\nERROR: {e}")
        return False
