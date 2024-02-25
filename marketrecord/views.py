from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Location
from .serializers import *
from authentications.permissions import *
from rest_framework.permissions import IsAuthenticated

class LocationCreate(APIView):
    permission_classes = [permissions.AllowAny] 

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Location created successfully',
                'location': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Location creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    


# Records markets for a specific location 
class MarketCreate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request, format=None):
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Market created successfully",
                "market": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to create market",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

# View to all recoreded markets

class MarketList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, format=None):
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True)
        return Response({
            "message": "Markets retrieved successfully",
            "markets": serializer.data
        }, status=status.HTTP_200_OK)
    
#Crate a report
class ReportCreate(APIView):
    permission_classes = [IsAuthenticated, IsCreatorUser]
    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({
                "message": "Report created successfully",
                "report": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to create report",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
