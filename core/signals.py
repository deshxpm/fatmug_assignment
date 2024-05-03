# from django.db.models import Count, Sum, Avg, F
import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Vendor, PurchaseOrder, HistoricalPerformance

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Vendor)
def create_historical_performance(sender, instance, created, **kwargs):
    if not created:
        logger.info(f"Vendor instance updated: {instance}")
        # Update HistoricalPerformance if Vendor is updated (e.g., performance metrics changed)
        HistoricalPerformance.objects.create(
            vendor=instance,
            date=instance.last_login,  # Use a relevant date field (e.g., last_login) as the date for historical record
            on_time_delivery_rate=instance.on_time_delivery_rate,
            quality_rating_avg=instance.quality_rating_avg,
            average_response_time=instance.average_response_time,
            fulfillment_rate=instance.fulfillment_rate
        )

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics_on_po_completion(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        instance.vendor.update_performance_metrics()

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time_on_acknowledgment(sender, instance, created, **kwargs):
    if instance.acknowledgment_date:
        instance.vendor.update_performance_metrics()


# @receiver(post_save, sender=PurchaseOrder)
# def update_performance_metrics(sender, instance, created, **kwargs):
#     vendor = instance.vendor

#     if instance.status == 'completed':
#         # Calculate on-time delivery rate
#         total_completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
#         on_time_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=instance.delivery_date).count()
#         if total_completed_pos > 0:
#             vendor.on_time_delivery_rate = (on_time_pos / total_completed_pos) * 100

#         # Calculate quality rating average
#         completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
#         total_completed_pos = completed_pos.count()
#         if total_completed_pos > 0:
#             quality_rating_avg = completed_pos.aggregate(avg_quality=Avg('quality_rating'))['avg_quality']
#             vendor.quality_rating_avg = quality_rating_avg

#     if instance.acknowledgment_date is not None:
#         # Calculate average response time
#         completed_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
#         total_completed_pos = completed_pos.count()
#         if total_completed_pos > 0:
#             response_times = completed_pos.annotate(response_time=F('acknowledgment_date') - F('issue_date')).aggregate(avg_response=Avg('response_time'))['avg_response']
#             vendor.average_response_time = response_times.total_seconds() if response_times else 0

#     # Calculate fulfilment rate
#     completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
#     total_completed_pos = completed_pos.count()
#     successful_fulfilled_pos = completed_pos.exclude(quality_rating__lt=0).count()  # Adjust condition based on issues
#     if total_completed_pos > 0:
#         vendor.fulfillment_rate = (successful_fulfilled_pos / total_completed_pos) * 100

#     # Update the vendor instance in the database
#     vendor.save()
