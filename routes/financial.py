from flask import Blueprint, request, jsonify
from models import db, FinancialRecord, PurchaseOrder, PayrollRecord, Expense, PurchaseOrderFinancialRecord, PayrollFinancialRecord
from datetime import datetime
from decimal import Decimal
from .utils import success_response, error_response, handle_exceptions, validate_json

financial_bp = Blueprint('financial', __name__)

@financial_bp.route('/records', methods=['GET'])
@handle_exceptions
def get_financial_records():
    """Get all financial records with optional filters"""
    transaction_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = FinancialRecord.query
    
    if transaction_type:
        query = query.filter(FinancialRecord.TransactionType == transaction_type)
    if start_date:
        try:
            query = query.filter(FinancialRecord.TransactionDate >= datetime.strptime(start_date, '%Y-%m-%d').date())
        except ValueError:
            return error_response("Invalid start_date format. Use YYYY-MM-DD", 400)
    if end_date:
        try:
            query = query.filter(FinancialRecord.TransactionDate <= datetime.strptime(end_date, '%Y-%m-%d').date())
        except ValueError:
            return error_response("Invalid end_date format. Use YYYY-MM-DD", 400)
    
    records = query.order_by(FinancialRecord.TransactionDate.desc()).all()
    
    data = [{
        'id': r.FinancialRecordID,
        'date': r.TransactionDate.isoformat() if r.TransactionDate else None,
        'type': r.TransactionType,
        'amount': float(r.Amount) if r.Amount else 0,
        'account_code': r.AccountCode,
        'description': r.Description
    } for r in records]
    
    return success_response(data, "Financial records retrieved successfully")

@financial_bp.route('/records', methods=['POST'])
@validate_json
@handle_exceptions
def create_financial_record():
    """Create a new financial record"""
    data = request.json
    
    if not data.get('amount'):
        return error_response("Amount is required", 400)
    
    try:
        record = FinancialRecord(
            TransactionDate=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else datetime.utcnow().date(),
            TransactionType=data.get('type', 'Expense'),
            AccountCode=data.get('account_code'),
            Amount=Decimal(str(data.get('amount', 0))),
            Description=data.get('description')
        )
        
        db.session.add(record)
        db.session.commit()
        
        return success_response({
            'id': record.FinancialRecordID,
            'date': record.TransactionDate.isoformat() if record.TransactionDate else None,
            'type': record.TransactionType,
            'amount': float(record.Amount) if record.Amount else 0
        }, "Financial record created successfully", 201)
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)

@financial_bp.route('/summary', methods=['GET'])
def get_financial_summary():
    """Get financial summary by type"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = FinancialRecord.query
    
    if start_date:
        query = query.filter(FinancialRecord.TransactionDate >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(FinancialRecord.TransactionDate <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    records = query.all()
    
    summary = {}
    total_income = Decimal('0')
    total_expense = Decimal('0')
    
    for record in records:
        amount = Decimal(str(record.Amount)) if record.Amount else Decimal('0')
        trans_type = record.TransactionType
        
        if trans_type not in summary:
            summary[trans_type] = Decimal('0')
        
        summary[trans_type] += amount
        
        if trans_type in ['Income', 'Donation']:
            total_income += amount
        else:
            total_expense += amount
    
    return jsonify({
        'by_type': {k: float(v) for k, v in summary.items()},
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'net': float(total_income - total_expense)
    })

@financial_bp.route('/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses"""
    expenses = Expense.query.order_by(Expense.Date.desc()).all()
    
    return jsonify([{
        'id': e.ExpenseID,
        'date': e.Date.isoformat() if e.Date else None,
        'type': e.Type,
        'amount': float(e.Amount) if e.Amount else 0,
        'description': e.Description,
        'staff_id': e.StaffID
    } for e in expenses])

@financial_bp.route('/records/<int:record_id>', methods=['GET'])
@handle_exceptions
def get_financial_record(record_id):
    """Get a single financial record"""
    record = FinancialRecord.query.get_or_404(record_id)
    
    return success_response({
        'id': record.FinancialRecordID,
        'date': record.TransactionDate.isoformat() if record.TransactionDate else None,
        'type': record.TransactionType,
        'amount': float(record.Amount) if record.Amount else 0,
        'account_code': record.AccountCode,
        'description': record.Description
    }, "Financial record retrieved successfully")

@financial_bp.route('/records/<int:record_id>', methods=['PUT'])
@validate_json
@handle_exceptions
def update_financial_record(record_id):
    """Update a financial record"""
    record = FinancialRecord.query.get_or_404(record_id)
    data = request.json
    
    if 'date' in data:
        try:
            record.TransactionDate = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return error_response("Invalid date format. Use YYYY-MM-DD", 400)
    if 'type' in data:
        record.TransactionType = data['type']
    if 'amount' in data:
        record.Amount = Decimal(str(data['amount']))
    if 'account_code' in data:
        record.AccountCode = data['account_code']
    if 'description' in data:
        record.Description = data['description']
    
    db.session.commit()
    
    return success_response({
        'id': record.FinancialRecordID,
        'date': record.TransactionDate.isoformat() if record.TransactionDate else None,
        'type': record.TransactionType,
        'amount': float(record.Amount) if record.Amount else 0
    }, "Financial record updated successfully")

@financial_bp.route('/expenses', methods=['POST'])
@validate_json
@handle_exceptions
def create_expense():
    """Create a new expense"""
    data = request.json
    
    try:
        expense = Expense(
            Date=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else datetime.utcnow().date(),
            Type=data.get('type', 'Other'),
            Amount=Decimal(str(data.get('amount', 0))),
            Description=data.get('description'),
            StaffID=data.get('staff_id')
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return success_response({
            'id': expense.ExpenseID,
            'date': expense.Date.isoformat() if expense.Date else None,
            'type': expense.Type,
            'amount': float(expense.Amount) if expense.Amount else 0
        }, "Expense created successfully", 201)
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)

