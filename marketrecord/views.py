from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Location
from .serializers import *
from authentications.permissions import *
from rest_framework.permissions import IsAuthenticated
from authentications.models import *
from django.shortcuts import get_object_or_404

class ComponentUpdate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk, format=None):
        market = Component.objects.get(pk=pk)
        serializer = ComponentSerializer(market, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Component updated successfully",
                "component": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Failed to update component",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
class ComponentCreate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser] 

    def post(self, request, format=None):
        serializer = ComponentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Component created successfully',
                'components': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Component creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
# View to all recoreded Component
class ComponentList(APIView):
    permission_classes = [permissions.IsAuthenticated] 
    def get(self, request, format=None):
        component = Component.objects.all()
        serializer = ComponentSerializer(component, many=True)
        return Response({
            "message": "component retrieved successfully",
            "components": serializer.data
        }, status=status.HTTP_200_OK)
            
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
    

class LocationDelete(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk, format=None):
        location = get_object_or_404(Location, pk=pk)
        location.delete()
        return Response({
            "message": "Location deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    

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
    


class MarketUpdate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk, format=None):
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Market updated successfully",
                "market": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Failed to update market",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class MarketDelete(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk, format=None):
        market = Market.objects.get(pk=pk)
        market.delete()
        return Response({
            "message": "Market deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    

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
    
# view to list markets in a user location
class UserLocationMarketList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        markets = Market.objects.filter(location=user.location)
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
    

# View to allow a creator to update a report
class ReportUpdate(APIView):
    permission_classes = [IsAuthenticated, IsCreatorUser]

    def put(self, request, pk, format=None):
        report = Report.objects.get(id=pk)
        serializer = ReportSerializer(report, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            report.status = 'rollback_to_be_signed'
            report.save()
            return Response({
                "message": "Report updated successfully",
                "report": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Failed to update report",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

#view to allow a user to only see the report that has the market with the same location as the user
class UserLocationReportList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        reports = Report.objects.filter(market__location=user.location)
        serializer = ReportSerializer(reports, many=True)
        return Response({
            "message": "Reports retrieved successfully",
            "reports": serializer.data
        }, status=status.HTTP_200_OK)
    
# a view to allow an admin to view all reports in the system
class AllReportList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, format=None):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response({
            "message": "Reports retrieved successfully",
            "reports": serializer.data
        }, status=status.HTTP_200_OK)
    

# view to list your own reports(reported that you created)

class UserReportList(APIView):
    permission_classes = [IsAuthenticated, IsCreatorUser]
    def get(self, request, format=None):
        user = request.user
        reports = Report.objects.filter(created_by=user)
        serializer = ReportSerializer(reports, many=True)
        return Response({
            "message": "Reports retrieved successfully",
            "reports": serializer.data
        }, status=status.HTTP_200_OK)
     
 
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
    


# class ReportApproveView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk, format=None):
#         report = Report.objects.get(id=pk)
#         action = request.data.get('action')
#         viewers = request.data.get('viewers', None)
#         comment_text = request.data.get('comment', None)

#         if action not in ['approve', 'rollback']:
#             return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

#         if action == 'approve':
#             if comment_text:  # If comment is provided
#                 Comment.objects.create(commented_by=request.user, report=report, comment=comment_text)
#             if report.status in ['pending', 'rollback'] and request.user.role.name == Role.verifier:
#                 report.status = 'processing'
#                 report.verified_by = request.user
#                 report.verified_at = datetime.now()
#             elif report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.approver:
#                 report.status = 'processing'
#                 report.approved_by = request.user
#                 report.approved_at = datetime.now()
#             elif report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.header:
#                 if viewers is None:
#                     return Response({'error': 'Viewers are required for header approval'}, status=status.HTTP_400_BAD_REQUEST)
#                 report.status = 'approved'
#                 report.forwarded_by = request.user
#                 viewers_users = User.objects.filter(id__in=viewers)
#                 minister_user = User.objects.get(role__name='minister')  # Fetch the minister
#                 report.viewed_by.set(viewers_users)
#                 report.forwarded_to = minister_user
#                 report.forwarded_at = datetime.now()
#             else:
#                 return Response({'error': f'Invalid action for your role {request.user.role.name} or report status {report.status}'}, status=status.HTTP_400_BAD_REQUEST)
#         elif action == 'rollback':
#             if comment_text is None:
#                 return Response({'error': 'Comment is required for rollback action'}, status=status.HTTP_400_BAD_REQUEST)
#             Comment.objects.create(commented_by=request.user, report=report, comment=comment_text)
#             if report.status in ['processing', 'rollback', 'approved'] and request.user.role.name == Role.header:
#                 report.status = 'rollback'
#                 report.forwarded_by = None
#                 report.approved_by = None
#                 report.viewed_by.clear()
#                 report.forwarded_to = None
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
            if report.status in ['pending', 'rollback_to_be_signed'] and request.user.role.name == Role.verifier:
                report.status = 'verified'
                report.verified_by = request.user
                report.verified_at = datetime.now()
            elif report.status in ['verified'] and request.user.role.name == Role.approver:
                report.status = 'approved'
                report.approved_by = request.user
                report.approved_at = datetime.now()
            elif report.status in ['approved'] and request.user.role.name == Role.header:
                if viewers is None:
                    return Response({'error': 'Viewers are required for header approval'}, status=status.HTTP_400_BAD_REQUEST)
                report.status = 'forwarded'
                report.forwarded_by = request.user
                viewers_users = User.objects.filter(id__in=viewers)
                minister_user = User.objects.get(role__name='minister')  # Fetch the minister
                report.viewed_by.set(viewers_users)
                report.forwarded_to = minister_user
                report.forwarded_at = datetime.now()
            else:
                return Response({'error': f'Invalid action for your role {request.user.role.name} or report status {report.status}'}, status=status.HTTP_400_BAD_REQUEST)
            report.save()
            return Response({'message': f'User with role {request.user.role.name} has {action}d report with id {report.id}.'})
        elif action == 'rollback':
            if comment_text is None:
                return Response({'error': 'Comment is required for rollback action'}, status=status.HTTP_400_BAD_REQUEST)
            Comment.objects.create(commented_by=request.user, report=report, comment=comment_text)
            if report.status in ['pending','verified', 'approved']:
                report.status = 'rollback'
                report.verified_by = None
                report.verified_at = None
                report.approved_by = None
                report.approved_at = None
                report.forwarded_by = None
                report.forwarded_at = None
                report.viewed_by.clear()
                report.forwarded_to = None
            else:
                return Response({'error': f'Invalid action for your role {request.user.role.name} or report status {report.status}'}, status=status.HTTP_400_BAD_REQUEST)

            report.save()
            return Response({'message': f'User with role {request.user.role.name} has {action}d report with id {report.id}.'})
        



# a view to allow minister to view all reports that have been forwarded to him

class MinisterReportList(APIView):
    permission_classes = [IsAuthenticated, IsMinisterUser]
    def get(self, request, format=None):
        reports = Report.objects.filter(forwarded_to=request.user)
        serializer = ReportSerializer(reports, many=True)
        return Response({
            "message": "Reports retrieved successfully",
            "reports": serializer.data
        }, status=status.HTTP_200_OK)
    

# a view to allow viewer to view all reports that have been forwarded to him
class ViewerReportList(APIView):
    permission_classes = [IsAuthenticated, IsViewerUser]
    def get(self, request, format=None):
        reports = Report.objects.filter(viewed_by=request.user)
        serializer = ReportSerializer(reports, many=True)
        return Response({
            "message": "Reports retrieved successfully",
            "reports": serializer.data
        }, status=status.HTTP_200_OK)
        
    

class ViewReportCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        report = Report.objects.get(id=pk)
        comments = report.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)