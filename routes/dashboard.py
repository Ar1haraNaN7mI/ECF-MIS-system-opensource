from flask import Blueprint, jsonify, request
from models import db, FinancialRecord, Donation, Donor, Inventory, Staff, Expense
from datetime import datetime, timedelta
from decimal import Decimal
from .utils import success_response, error_response, handle_exceptions

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview', methods=['GET'])
@handle_exceptions
def get_dashboard_overview():
    """Get dashboard overview statistics"""
    # Financial summary
    financial_records = FinancialRecord.query.all()
    total_income = sum(Decimal(str(r.Amount)) for r in financial_records if r.TransactionType in ['Income', 'Donation'] and r.Amount)
    total_expense = sum(Decimal(str(r.Amount)) for r in financial_records if r.TransactionType == 'Expense' and r.Amount)
    
    # Donations
    donations = Donation.query.all()
    total_donations = sum(Decimal(str(d.Amount)) for d in donations if d.Amount)
    donation_count = len(donations)
    
    # Donors
    donor_count = Donor.query.count()
    
    # Inventory
    inventory_items = Inventory.query.all()
    total_inventory_value = len(inventory_items)
    low_stock_items = [i for i in inventory_items if i.Quantity < 10]
    
    # Staff
    active_staff_count = Staff.query.filter(Staff.Status == 'Active').count()
    
    return success_response({
        'financial': {
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'net': float(total_income - total_expense)
        },
        'donations': {
            'total_amount': float(total_donations),
            'count': donation_count
        },
        'donors': {
            'count': donor_count
        },
        'inventory': {
            'total_items': total_inventory_value,
            'low_stock_count': len(low_stock_items)
        },
        'staff': {
            'active_count': active_staff_count
        }
    }, "Dashboard overview retrieved successfully")

@dashboard_bp.route('/financial-trends', methods=['GET'])
@handle_exceptions
def get_financial_trends():
    """Get financial trends over time"""
    days = int(request.args.get('days', 30))
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    records = FinancialRecord.query.filter(
        FinancialRecord.TransactionDate >= start_date
    ).order_by(FinancialRecord.TransactionDate).all()
    
    # Group by date and type
    trends = {}
    for record in records:
        date_str = record.TransactionDate.isoformat() if record.TransactionDate else None
        if not date_str:
            continue
        
        if date_str not in trends:
            trends[date_str] = {'income': 0, 'expense': 0}
        
        amount = float(record.Amount) if record.Amount else 0
        if record.TransactionType in ['Income', 'Donation']:
            trends[date_str]['income'] += amount
        else:
            trends[date_str]['expense'] += amount
    
    return success_response({
        'trends': [{'date': k, **v} for k, v in sorted(trends.items())]
    }, "Financial trends retrieved successfully")

@dashboard_bp.route('/donation-trends', methods=['GET'])
@handle_exceptions
def get_donation_trends():
    """Get donation trends over time"""
    days = int(request.args.get('days', 30))
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    donations = Donation.query.filter(
        Donation.DonationDate >= start_date
    ).order_by(Donation.DonationDate).all()
    
    trends = {}
    for donation in donations:
        date_str = donation.DonationDate.isoformat() if donation.DonationDate else None
        if not date_str:
            continue
        
        if date_str not in trends:
            trends[date_str] = {'count': 0, 'amount': 0}
        
        trends[date_str]['count'] += 1
        trends[date_str]['amount'] += float(donation.Amount) if donation.Amount else 0
    
    return success_response({
        'trends': [{'date': k, **v} for k, v in sorted(trends.items())]
    }, "Donation trends retrieved successfully")

@dashboard_bp.route('/top-donors', methods=['GET'])
@handle_exceptions
def get_top_donors():
    """Get top donors by donation amount"""
    limit = int(request.args.get('limit', 10))
    
    donors = Donor.query.all()
    donor_stats = []
    
    for donor in donors:
        total = sum(float(d.Amount) if d.Amount else 0 for d in donor.donations)
        count = len(donor.donations)
        if total > 0:
            donor_stats.append({
                'id': donor.DonorID,
                'name': donor.Name,
                'total_donations': total,
                'donation_count': count,
                'region': donor.Region,
                'age': donor.Age
            })
    
    donor_stats.sort(key=lambda x: x['total_donations'], reverse=True)
    
    return success_response({
        'top_donors': donor_stats[:limit]
    }, "Top donors retrieved successfully")

@dashboard_bp.route('/expense-breakdown', methods=['GET'])
@handle_exceptions
def get_expense_breakdown():
    """Get expense breakdown by type"""
    expenses = Expense.query.all()
    
    breakdown = {}
    for expense in expenses:
        exp_type = expense.Type or 'Other'
        amount = float(expense.Amount) if expense.Amount else 0
        
        if exp_type not in breakdown:
            breakdown[exp_type] = 0
        
        breakdown[exp_type] += amount
    
    return success_response({
        'breakdown': breakdown
    }, "Expense breakdown retrieved successfully")

