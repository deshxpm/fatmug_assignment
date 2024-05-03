
Vendor Management System (VMS)

Welcome to the Vendor Management System (VMS) project! This README provides essential information on setting up and using the VMS API endpoints.

Table of Contents
    Installation
    Usage
    API Endpoints
    Contributing
    License
    Installation
    Follow these steps to set up the Vendor Management System on your local machine:

Clone the Repository:
    git clone https://github.com/yourusername/vendor-management-system.git

Navigate to the Project Directory:
    cd vendor-management-system
    Create a Virtual Environment:
    python -m venv venv
Activate the Virtual Environment:
    On Windows:
    venv\Scripts\activate

On macOS/Linux:
    source venv/bin/activate
    Install Dependencies:

pip install -r requirements.txt

Apply Migrations:
    python manage.py migrate

Start the Development Server:
python manage.py runserver

Usage
The Vendor Management System provides APIs for managing vendors and purchase orders. Use these APIs to perform CRUD operations on vendors and purchase orders, and to retrieve performance metrics for vendors.

API Endpoints
    Vendors
        List/Create Vendors:
        GET /api/vendors/
        POST /api/vendors/
        Retrieve/Update/Delete Vendor:
        GET /api/vendors/{vendor_id}/
        PUT /api/vendors/{vendor_id}/
        DELETE /api/vendors/{vendor_id}/
        Retrieve Vendor Performance Metrics:
        GET /api/vendors/{vendor_id}/performance/

    Purchase Orders
        List/Create Purchase Orders:
        GET /api/purchase_orders/
        POST /api/purchase_orders/
        Retrieve/Update/Delete Purchase Order:
        GET /api/purchase_orders/{po_id}/
        PUT /api/purchase_orders/{po_id}/
        DELETE /api/purchase_orders/{po_id}/
        Acknowledge Purchase Order:
        POST /api/purchase_orders/{po_id}/acknowledge/

Contributing
Contributions to the Vendor Management System are welcome! Follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature/your-feature-name).
Create a new Pull Request.