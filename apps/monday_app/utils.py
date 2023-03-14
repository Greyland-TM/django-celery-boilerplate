import requests
import json
import os

# LEADS BOARD COLUMNS
def get_leads_board_columns(customer, columns):
    """
    This function is responsible for returning the column values for the leads board
    If I you want to sync more fields from the monday.com ledas board, add them here
    """

    print('Getting leads board columns...')
    evaluated_column_values = {}
    for data in columns:
        data_id = data['id']
        if data['title'] == 'Phone':
            evaluated_column_values[data_id] = str(customer.phone)
        elif data['title'] == 'Email':
            evaluated_column_values[data_id] = {"email": customer.email, "text": customer.email}
        elif data['title'] == 'app_2 ID':
            evaluated_column_values[data_id] = str(customer.pk)

    return evaluated_column_values

# CUSTOMERS BOARD COLUMNS
def get_customers_board_columns(customer, columns):
    print('Getting customers board columns...')
    evaluated_column_values = {}
    for data in columns:
        data_id = data['id']
        if data['title'] == 'Phone':
            evaluated_column_values[data_id] = str(customer.phone)
        elif data['title'] == 'Email':
            evaluated_column_values[data_id] = {"email": customer.email, "text": customer.email}
        elif data['title'] == 'app_2 ID':
            evaluated_column_values[data_id] = str(customer.pk)

    return evaluated_column_values

# UPDATE MONDAY ENTRY
def update_monday_entry(customer, board_id, url, headers, item_id, new_column_values):
    update_item_query = """
    mutation ($board_id: Int!, $item_id: Int!, $column_values: JSON!) {
        change_multiple_column_values(board_id: $board_id, item_id: $item_id, column_values: $column_values) {
            id
        }
    }
    """
    variables = {
        "board_id": board_id,
        "item_id": int(item_id),
        "column_values": json.dumps(new_column_values)
    }
    response = requests.post(url, headers=headers, json={"query": update_item_query, "variables": variables})
    response.raise_for_status()
    data = response.json()
    
    if response['data']['errors']:
        print('errors: ', response['data']['errors'])
        return False
    return True

# CREATE NEW MONDAY ENTRY
def create_monday_entry(customer, board_id, url, headers, new_column_values):
    lead_insertion_query = """
    mutation ($board_id: Int!, $item_name: String!, $column_values: JSON!) {
        create_item(board_id: $board_id, item_name: $item_name, column_values: $column_values) {
            id
        }
    }
    """
    variables = {
        "board_id": board_id,
        "item_name": f'{customer.first_name} {customer.last_name}',
        "column_values": json.dumps(new_column_values)
    }
    response = requests.post(url, headers=headers, json={"query": lead_insertion_query, "variables": variables})
    response.raise_for_status()
    data = response.json()
    monday_id = data["data"]["create_item"]["id"]
    customer.monday_id = monday_id
    customer.save(sync_monday=False)
    print(f'monday_id: {monday_id} - Save this to the customer model')
    return monday_id
