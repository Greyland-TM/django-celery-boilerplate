from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from apps.accounts.models import Customer
# from .models import ProfilePackage
from .utils import create_service_package, update_service_package

# Create your views here.
class ProfilePackage(APIView):
    """CRUD operations for social media ads"""

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        """Post request for making a new add"""
        package = request.data['packages'][0]
        customer_pk = request.data['customer_pk']
        try:
            customer = Customer.objects.get(pk=customer_pk)
            print('customer: ', customer)
            # create_service_package(package, customer_pk)
        except Exception as error:
            print(f"\nError: {error}")
            
        return Response(
            status=status.HTTP_200_OK, data={"ok": True, "message": "Packages Created"}
        )
