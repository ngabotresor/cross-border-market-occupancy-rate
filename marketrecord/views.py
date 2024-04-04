from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Location
from .serializers import *
from authentications.permissions import *
from rest_framework.permissions import IsAuthenticated
from authentications.models import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q, Avg 
from django.utils import timezone
from django.db.models.functions import Coalesce

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
    permission_classes = [IsAuthenticated]
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
                #send email to approver
                subject = 'A new report has been verified'
                message = f'Report {report.id} has been verified by {request.user.first_name} {request.user.last_name}.'
                email_from = settings.EMAIL_HOST_USER
                users_same_location = User.objects.filter(
                    location=report.created_by.location,
                    role__in=[1,3,4,5]
                )
                recipient_list = [user.email for user in users_same_location]
                send_mail(subject, message, email_from, recipient_list)
            elif report.status in ['verified'] and request.user.role.name == Role.approver:
                report.status = 'approved'
                report.approved_by = request.user
                report.approved_at = datetime.now()
                #send email to users with roles verifier, approver and header
                subject = 'A new report has been approved'
                message = f'Report {report.id} has been approved by {request.user.first_name} {request.user.last_name}.'
                email_from = settings.EMAIL_HOST_USER
                users_same_location = User.objects.filter(
                    location=report.created_by.location,
                    role__in=[1,3,4,5]
                )
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
                #send email to verifier, approver, header, and minister
                subject = 'A new report has been forwarded'
                message = f'Report {report.id} has been forwarded by {request.user.first_name} {request.user.last_name}.'
                email_from = settings.EMAIL_HOST_USER

                # Get all users with the same location as the user who created the report and who are verifiers, approvers, or headers
                # and all users who are ministers, regardless of location
                users_to_notify = User.objects.filter(
                Q(location=report.created_by.location, role__in=[1,3,4,5]) |
                Q(role=6) |
                Q(id__in=viewers_users)  
                 )
                recipient_list = [user.email for user in users_to_notify]

                send_mail(subject, message, email_from, recipient_list)

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
                #send email to the creator of the report
                subject = 'A report has been rollbacked'
                message = f'Report {report.id} has been rollbacked by {request.user.first_name} {request.user.last_name}.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [report.created_by.email]
                send_mail(subject, message, email_from, recipient_list)

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
    
    

# view to show the occupancy rate of a report in every market for a selected year


# class MarketOccupancyRateView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminOrMinisterOrViewerUser]
#     def get(self, request, year=None, format=None):
#         # If a year is not specified, use the current year
#         if year is None:
#             year = timezone.now().year

#         # Get the average occupancy rate for each market for the specified year
#         markets = Market.objects.annotate(
#             avg_occupancy_rate=Coalesce(Avg(
#                 'reports__records__occupancy_rate',
#                 filter=Q(reports__year=year)
#             ), 0.0)  # Make 0 a float
#         )

#         # Prepare data for Response
#         data = [
#             {"market": market.name, "average_occupancy_rate": market.avg_occupancy_rate}
#             for market in markets
#         ]

#         return Response(data)

# view to show the occupancy rate of a report in every market for a selected year
class MarketOccupancyRateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrMinisterOrViewerUser]
    def get(self, request, year=None, format=None):
        # If a year is not specified, use the current year
        if year is None:
            year = timezone.now().year

        # Get the average occupancy rate for each market for the specified year
        markets = Market.objects.annotate(
            avg_occupancy_rate=Coalesce(Avg(
                'reports__records__occupancy_rate',
                filter=Q(reports__year=year)
            ), 0.0)  # Make 0 a float
        )

        # Prepare data for Response
        data = [
            {"market": market.name, "average_occupancy_rate": market.avg_occupancy_rate, "year": year}
            for market in markets
        ]

        return Response(data)

# class SeasonOccupancyRateView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminOrMinisterOrViewerUser]
#     def get(self, request, format=None):
#         # Get the year and market_id from the query parameters (if they exist)
#         year = request.query_params.get('year')
#         market_id = request.query_params.get('market_id')

#         # Start with all reports
#         reports = Report.objects.all()

#         # If a year is specified, filter by year
#         if year is not None:
#             reports = reports.filter(year=year)

#         # If a market is specified, filter by market
#         if market_id is not None:
#             reports = reports.filter(market_id=market_id)

#         # List of all seasons
#         all_seasons = ['Spring', 'Summer', 'Autumn', 'Winter']

#         # Calculate the average occupancy rate for each season
#         data = []
#         for season in all_seasons:
#             avg_occupancy_rate = reports.filter(season=season).aggregate(avg_occupancy_rate=Avg('records__occupancy_rate'))['avg_occupancy_rate']
#             data.append({
#                 'season': season,
#                 'avg_occupancy_rate': avg_occupancy_rate if avg_occupancy_rate is not None else 0
#             })

#         return Response(data)


# Season Occupancy rate
class SeasonOccupancyRateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrMinisterOrViewerUser]
    def get(self, request, format=None):
        # Get the year and market_id from the query parameters (if they exist)
        year = request.query_params.get('year')
        market_id = request.query_params.get('market_id')

        # Start with all reports
        reports = Report.objects.all()

        # If a year is specified, filter by year
        if year is not None:
            reports = reports.filter(year=year)

        # If a market is specified, filter by market
        if market_id is not None:
            reports = reports.filter(market_id=market_id)

        # List of all seasons
        all_seasons = ['Spring', 'Summer', 'Autumn', 'Winter']

        # Calculate the average occupancy rate for each season
        data = []
        for season in all_seasons:
            avg_occupancy_rate = reports.filter(season=season).aggregate(avg_occupancy_rate=Avg('records__occupancy_rate'))['avg_occupancy_rate']
            data.append({
                'season': season,
                'avg_occupancy_rate': avg_occupancy_rate if avg_occupancy_rate is not None else 0,
                'year': year,
                'market': Market.objects.get(id=market_id).name if market_id else 'All markets'
            })

        return Response(data)