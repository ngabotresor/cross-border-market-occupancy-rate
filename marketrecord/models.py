from django.db import models
from authentications.models import User

class Location(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'location'

    def __str__(self):
        return self.name

class Market(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='markets')

    class Meta:
        db_table = 'market'

    def __str__(self):
        return self.name

class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('rollbacked', 'Rollbacked'),
    ]
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='reports')
    season = models.CharField(max_length=255)
    year = models.IntegerField()
    created_by = models.ForeignKey('authentications.User', on_delete=models.CASCADE, related_name='reports_created')
    verified_by = models.ForeignKey('authentications.User', on_delete=models.CASCADE, related_name='reports_verified', null=True, blank=True)
    approved_by = models.ForeignKey('authentications.User', on_delete=models.CASCADE, related_name='reports_approved', null=True, blank=True)
    forwarded_by = models.ForeignKey('authentications.User', on_delete=models.CASCADE, related_name='reports_forwarded', null=True, blank=True)
    viewed_by = models.ManyToManyField('authentications.User', related_name='reports_viewed', blank=True)
    forwarded_to = models.ForeignKey('authentications.User', on_delete=models.CASCADE, related_name='reports_forwarded_to', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'report'
        unique_together = ['market', 'season', 'year']

    def __str__(self):
        return f"{self.market} - {self.season} - {self.year}"

class ReportRecord(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='records')
    component_name = models.CharField(max_length=255)
    component_description = models.TextField()
    total_number_places_available = models.IntegerField()
    number_places_rented = models.IntegerField()
    occupancy_rate = models.FloatField(default=0)
    observation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'report_record'

    def __str__(self):
        return f"{self.report} - {self.component} - {self.status}"
    
    def save(self, *args, **kwargs):
        if self.total_number_places_available > 0:
            self.occupancy_rate = (self.number_places_rented / self.total_number_places_available) * 100
        else:
            self.occupancy_rate = 0
        super().save(*args, **kwargs)


class Comment(models.Model):
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
