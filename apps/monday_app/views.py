from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# from apps.accounts.models import Customer, Employee
import requests
import os

# Create your views here.
class ProcessModayWebhook(APIView):
    """Process webhook from monday.com"""
    def post(self, request, board_type):
        print('IN THE REQUEST...')
        
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
        webhook_query = """
            webhooks(board_id: $board_id){
                id
                event
                board_id
                config
            }
        """

        variables = {
            "board_id": board_id
        }

        response = requests.post(url, headers=headers, json={"query": webhook_query, "variables": variables})
        return Response(
            status=status.HTTP_200_OK, data={"ok": True, "message": "Webhook processed"}
        )