from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Location
from .serializers import *
from authentications.permissions import *
from rest_framework.permissions import IsAuthenticated
from authentications.models import *

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
    

# View to all recoreded locations
class LocationList(APIView):
    permission_classes = [permissions.AllowAny] 
    def get(self, request, format=None):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response({
            "message": "Locations retrieved successfully",
            "locations": serializer.data
        }, status=status.HTTP_200_OK)
    


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
    
 
class TrackReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        report = Report.objects.get(id=pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data)
    

# class ReportApproveView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk, format=None):
#         report = Report.objects.get(id=pk)
#         action = request.data.get('action')
#         viewers = request.data.get('viewers', None)

#         if action not in ['approve', 'rollback']:
#             return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

#         if action == 'approve':
#             if report.status in ['pending', 'rollback', 'approved'] and request.user.role.name == Role.verifier:
#                 report.status = 'processing'
#                 report.verified_by = request.user
#             elif report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.approver:
#                 report.status = 'processing'
#                 report.approved_by = request.user
#             elif report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.header:
#                 if viewers is None:
#                     return Response({'error': 'Viewers are required for header approval'}, status=status.HTTP_400_BAD_REQUEST)
#                 report.status = 'approved'
#                 report.forwarded_by = request.user
#                 viewers_users = User.objects.filter(id__in=viewers)
#                 minister_user = User.objects.get(role__name='minister')  # Fetch the minister
#                 report.viewed_by.set(viewers_users)
#                 report.forwarded_to = minister_user
#             else:
#                 return Response({'error': f'Invalid action for your role {request.user.role.name} or report status {report.status}'}, status=status.HTTP_400_BAD_REQUEST)
#         elif action == 'rollback':
#             if report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.header:
#                 report.status = 'rollback'
#                 report.forwarded_by = None
#                 report.approved_by = None
#             elif report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.approver:
#                 report.status = 'rollback'
#                 report.approved_by = None
#                 report.verified_by = None
#             elif report.status in ['processing', 'approved', 'rollback'] and request.user.role.name == Role.verifier:
#                 report.status = 'rollback'
#                 report.verified_by = None
#             else:
#                 return Response({'error': f'Invalid action for your role {request.user.role.name} or report status {report.status}'}, status=status.HTTP_400_BAD_REQUEST)

#         report.save()
#         return Response({'message': f'User with role {request.user.role.name} has {action}d report with id {report.id}.'})
    


class ReportApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        report = Report.objects.get(id=pk)
        action = request.data.get('action')
        viewers = request.data.get('viewers', None)
        comment_text = request.data.get('comment', None)

        if action not in ['approve', 'rollback']:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'approve':
            if comment_text:  # If comment is provided
                Comment.objects.create(commented_by=request.user, report=report, comment=comment_text)
            if report.status in ['pending', 'rollback', 'approved'] and request.user.role.name == Role.verifier:
                report.status = 'processing'
                report.verified_by = request.user
            elif report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.approver:
                report.status = 'processing'
                report.approved_by = request.user
            elif report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.header:
                if viewers is None:
                    return Response({'error': 'Viewers are required for header approval'}, status=status.HTTP_400_BAD_REQUEST)
                report.status = 'approved'
                report.forwarded_by = request.user
                viewers_users = User.objects.filter(id__in=viewers)
                minister_user = User.objects.get(role__name='minister')  # Fetch the minister
                report.viewed_by.set(viewers_users)
                report.forwarded_to = minister_user
            else:
                return Response({'error': f'Invalid action for your role {request.user.role.name} or report status {report.status}'}, status=status.HTTP_400_BAD_REQUEST)
        elif action == 'rollback':
            if comment_text is None:
                return Response({'error': 'Comment is required for rollback action'}, status=status.HTTP_400_BAD_REQUEST)
            Comment.objects.create(commented_by=request.user, report=report, comment=comment_text)
            if report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.header:
                report.status = 'rollback'
                report.forwarded_by = None
                report.approved_by = None
                report.viewed_by.clear()
                report.forwarded_to = None
            elif report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.approver:
                report.status = 'rollback'
                report.approved_by = None
                report.verified_by = None
            elif report.status in ['processing', 'approved', 'rollback'] and request.user.role.name == Role.verifier:
                report.status = 'rollback'
                report.verified_by = None
            else:
                return Response({'error': f'Invalid action for your role {request.user.role.name} or report status {report.status}'}, status=status.HTTP_400_BAD_REQUEST)

        report.save()
        return Response({'message': f'User with role {request.user.role.name} has {action}d report with id {report.id}.'})
    

class ViewReportCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        report = Report.objects.get(id=pk)
        comments = report.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)