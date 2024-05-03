from rest_framework import generics
from rest_framework.response import Response
from core.models import *
from .serializers import *

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_url_kwarg = 'vendor_id'

    def retrieve(self, request, *args, **kwargs):
        # try:
        instance = self.get_object()
        instance.update_performance_metrics()  # Update performance metrics before serialization
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        # except Vendor.DoesNotExist:
        #     return Response({"error": "Vendor not found"}, status=404)
        # except Exception as e:
        #     return Response({"error": str(e)}, status=500)
    
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    # Override perform_create to set vendor automatically based on user
    def perform_create(self, serializer):
        serializer.save()#(vendor=self.request.user.vendor)  # Assuming vendor is associated with user

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

class PurchaseOrderAcknowledgeAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderAcknowledgeSerializer
