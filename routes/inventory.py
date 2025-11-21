from flask import Blueprint, request, jsonify
from models import db, Inventory, DemandPlan, Supplier, PurchaseOrder, PurchaseOrderInventory, FinancialRecord, PurchaseOrderFinancialRecord
from datetime import datetime
from decimal import Decimal
from .utils import success_response, error_response, handle_exceptions, validate_json

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/items', methods=['GET'])
def get_inventory_items():
    """Get all inventory items"""
    items = Inventory.query.all()
    
    return jsonify([{
        'id': i.InventoryID,
        'item_name': i.ItemName,
        'quantity': i.Quantity,
        'location': i.Location,
        'demand_plan_id': i.DemandPlanID
    } for i in items])

@inventory_bp.route('/items', methods=['POST'])
def create_inventory_item():
    """Create a new inventory item"""
    data = request.json
    
    item = Inventory(
        ItemName=data.get('item_name'),
        Quantity=data.get('quantity', 0),
        Location=data.get('location'),
        DemandPlanID=data.get('demand_plan_id')
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({'id': item.InventoryID, 'message': 'Inventory item created successfully'}), 201

@inventory_bp.route('/items/<int:item_id>', methods=['GET'])
@handle_exceptions
def get_inventory_item(item_id):
    """Get a single inventory item"""
    item = Inventory.query.get_or_404(item_id)
    
    return success_response({
        'id': item.InventoryID,
        'item_name': item.ItemName,
        'quantity': item.Quantity,
        'location': item.Location,
        'demand_plan_id': item.DemandPlanID
    }, "Inventory item retrieved successfully")

@inventory_bp.route('/items/<int:item_id>', methods=['PUT'])
@validate_json
@handle_exceptions
def update_inventory_item(item_id):
    """Update an inventory item"""
    item = Inventory.query.get_or_404(item_id)
    data = request.json
    
    if 'item_name' in data:
        item.ItemName = data['item_name']
    if 'quantity' in data:
        item.Quantity = data['quantity']
    if 'location' in data:
        item.Location = data['location']
    
    db.session.commit()
    
    return success_response({
        'id': item.InventoryID,
        'item_name': item.ItemName,
        'quantity': item.Quantity,
        'location': item.Location
    }, "Inventory item updated successfully")

@inventory_bp.route('/demand-plans', methods=['GET'])
def get_demand_plans():
    """Get all demand plans"""
    plans = DemandPlan.query.order_by(DemandPlan.PlanDate.desc()).all()
    
    return jsonify([{
        'id': p.DemandPlanID,
        'item_name': p.ItemName,
        'forecast_quantity': p.ForecastQuantity,
        'plan_date': p.PlanDate.isoformat() if p.PlanDate else None
    } for p in plans])

@inventory_bp.route('/demand-plans', methods=['POST'])
def create_demand_plan():
    """Create a new demand plan"""
    data = request.json
    
    plan = DemandPlan(
        ItemName=data.get('item_name'),
        ForecastQuantity=data.get('forecast_quantity', 0),
        PlanDate=datetime.strptime(data['plan_date'], '%Y-%m-%d').date() if data.get('plan_date') else datetime.utcnow().date()
    )
    
    db.session.add(plan)
    db.session.commit()
    
    return jsonify({'id': plan.DemandPlanID, 'message': 'Demand plan created successfully'}), 201

@inventory_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    """Get all suppliers"""
    suppliers = Supplier.query.all()
    
    return jsonify([{
        'id': s.SupplierID,
        'name': s.Name,
        'contact_info': s.ContactInfo,
        'address': s.Address
    } for s in suppliers])

@inventory_bp.route('/suppliers', methods=['POST'])
@validate_json
@handle_exceptions
def create_supplier():
    """Create a new supplier"""
    data = request.json
    
    supplier = Supplier(
        Name=data.get('name'),
        ContactInfo=data.get('contact_info'),
        Address=data.get('address')
    )
    
    db.session.add(supplier)
    db.session.commit()
    
    return success_response({
        'id': supplier.SupplierID,
        'name': supplier.Name,
        'contact_info': supplier.ContactInfo,
        'address': supplier.Address
    }, "Supplier created successfully", 201)

@inventory_bp.route('/suppliers/<int:supplier_id>', methods=['GET'])
@handle_exceptions
def get_supplier(supplier_id):
    """Get a single supplier"""
    supplier = Supplier.query.get_or_404(supplier_id)
    
    return success_response({
        'id': supplier.SupplierID,
        'name': supplier.Name,
        'contact_info': supplier.ContactInfo,
        'address': supplier.Address
    }, "Supplier retrieved successfully")

@inventory_bp.route('/suppliers/<int:supplier_id>', methods=['PUT'])
@validate_json
@handle_exceptions
def update_supplier(supplier_id):
    """Update a supplier"""
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.json
    
    if 'name' in data:
        supplier.Name = data['name']
    if 'contact_info' in data:
        supplier.ContactInfo = data['contact_info']
    if 'address' in data:
        supplier.Address = data['address']
    
    db.session.commit()
    
    return success_response({
        'id': supplier.SupplierID,
        'name': supplier.Name,
        'contact_info': supplier.ContactInfo,
        'address': supplier.Address
    }, "Supplier updated successfully")

@inventory_bp.route('/purchase-orders', methods=['GET'])
def get_purchase_orders():
    """Get all purchase orders"""
    status = request.args.get('status')
    
    query = PurchaseOrder.query
    
    if status:
        query = query.filter(PurchaseOrder.Status == status)
    
    orders = query.order_by(PurchaseOrder.OrderDate.desc()).all()
    
    return jsonify([{
        'id': po.PurchaseOrderID,
        'order_date': po.OrderDate.isoformat() if po.OrderDate else None,
        'total_amount': float(po.TotalAmount) if po.TotalAmount else 0,
        'status': po.Status,
        'supplier_id': po.SupplierID,
        'supplier_name': po.supplier.Name if po.supplier else None,
        'demand_plan_id': po.DemandPlanID,
        'items': [{
            'inventory_id': poi.InventoryID,
            'item_name': poi.inventory.ItemName if poi.inventory else None,
            'quantity': poi.Quantity
        } for poi in po.inventory_items]
    } for po in orders])

@inventory_bp.route('/purchase-orders', methods=['POST'])
def create_purchase_order():
    """Create a new purchase order"""
    data = request.json
    
    order = PurchaseOrder(
        OrderDate=datetime.strptime(data['order_date'], '%Y-%m-%d').date() if data.get('order_date') else datetime.utcnow().date(),
        TotalAmount=Decimal(str(data.get('total_amount', 0))),
        Status=data.get('status', 'Pending'),
        SupplierID=data.get('supplier_id'),
        DemandPlanID=data.get('demand_plan_id')
    )
    
    db.session.add(order)
    db.session.flush()
    
    # Add inventory items
    items = data.get('items', [])
    for item_data in items:
        poi = PurchaseOrderInventory(
            PurchaseOrderID=order.PurchaseOrderID,
            InventoryID=item_data['inventory_id'],
            Quantity=item_data.get('quantity', 1)
        )
        db.session.add(poi)
    
    # Create financial record
    if order.TotalAmount:
        financial_record = FinancialRecord(
            TransactionDate=order.OrderDate,
            TransactionType='Expense',
            Amount=order.TotalAmount,
            Description=f'Purchase Order #{order.PurchaseOrderID}'
        )
        db.session.add(financial_record)
        db.session.flush()
        
        pofr = PurchaseOrderFinancialRecord(
            PurchaseOrderID=order.PurchaseOrderID,
            FinancialRecordID=financial_record.FinancialRecordID
        )
        db.session.add(pofr)
    
    db.session.commit()
    
    return jsonify({'id': order.PurchaseOrderID, 'message': 'Purchase order created successfully'}), 201

