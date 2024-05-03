from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
import uuid
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class VendorManager(BaseUserManager):
    def create_user(self, email, vendor_code, password=None):
        if not email:
            raise ValueError("Email address is required")
        user = self.model(
            email=self.normalize_email(email),
            vendor_code=vendor_code,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, vendor_code, password):
        user = self.create_user(email, vendor_code, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def generate_uuid():
    return str(uuid.uuid4())

class Vendor(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    vendor_code = models.CharField(max_length=100, default=generate_uuid)
    name = models.CharField(max_length=100)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
    contact_details = models.TextField()
    address = models.TextField()
    last_login = models.DateTimeField(verbose_name='last_login', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['vendor_code']

    objects = VendorManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def update_performance_metrics(self):
        # Calculate On-Time Delivery Rate
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            on_time_pos = completed_pos.filter(delivery_date__lte=timezone.now()).count()
            self.on_time_delivery_rate = (on_time_pos / total_completed_pos) * 100
        else:
            self.on_time_delivery_rate = 0.0

        # Calculate Quality Rating Average
        self.quality_rating_avg = completed_pos.aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] or 0.0

        # Calculate Average Response Time
        completed_pos_with_ack = completed_pos.filter(acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos_with_ack]
        self.average_response_time = sum(response_times) / len(response_times) if response_times else 0.0

        # Calculate Fulfilment Rate
        successful_fulfilled_pos = completed_pos.exclude(quality_rating__lt=0).count()
        self.fulfillment_rate = (successful_fulfilled_pos / total_completed_pos) * 100 if total_completed_pos > 0 else 0.0

        self.save()


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number


@receiver(pre_save, sender=PurchaseOrder)
def generate_unique_po_number(sender, instance, **kwargs):
    if not instance.po_number:
        # Generate a unique po_number if not provided
        instance.po_number = str(uuid.uuid4().hex)[:12]  # Use a portion of UUID as po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"

    # class Meta:
    #     unique_together = ['vendor', 'date']
