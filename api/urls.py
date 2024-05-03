from django.urls import path
from . import views

urlpatterns = [
    path('api/vendors/', views.VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<vendor_id>/', views.VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
    path('api/vendors/<vendor_id>/performance/', views.VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    
    path('api/purchase_orders/', views.PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<po_id>/', views.PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('api/purchase_orders/<int:pk>/acknowledge/', views.PurchaseOrderAcknowledgeAPIView.as_view(), name='purchase-order-acknowledge'),
    
]
