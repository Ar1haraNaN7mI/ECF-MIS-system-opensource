from flask import Blueprint, request, jsonify
from models import db, Staff, Attendance, Schedule, PerformanceReview, PayrollRecord
from datetime import datetime
from decimal import Decimal
from .utils import success_response, error_response, handle_exceptions, validate_json

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff', methods=['GET'])
def get_staff():
    """Get all staff members"""
    status = request.args.get('status')
    role = request.args.get('role')
    
    query = Staff.query
    
    if status:
        query = query.filter(Staff.Status == status)
    if role:
        query = query.filter(Staff.Role == role)
    
    staff_list = query.all()
    
    return jsonify([{
        'id': s.StaffID,
        'name': s.Name,
        'role': s.Role,
        'contact_info': s.ContactInfo,
        'status': s.Status
    } for s in staff_list])

@staff_bp.route('/staff', methods=['POST'])
@validate_json
@handle_exceptions
def create_staff():
    """Create a new staff member"""
    data = request.json
    
    staff = Staff(
        Name=data.get('name'),
        Role=data.get('role'),
        ContactInfo=data.get('contact_info'),
        Status=data.get('status', 'Active')
    )
    
    db.session.add(staff)
    db.session.commit()
    
    return success_response({
        'id': staff.StaffID,
        'name': staff.Name,
        'role': staff.Role,
        'status': staff.Status
    }, "Staff member created successfully", 201)

@staff_bp.route('/staff/<int:staff_id>', methods=['GET'])
@handle_exceptions
def get_staff_member(staff_id):
    """Get a single staff member"""
    staff = Staff.query.get_or_404(staff_id)
    
    return success_response({
        'id': staff.StaffID,
        'name': staff.Name,
        'role': staff.Role,
        'contact_info': staff.ContactInfo,
        'status': staff.Status
    }, "Staff member retrieved successfully")

@staff_bp.route('/staff/<int:staff_id>', methods=['PUT'])
@validate_json
@handle_exceptions
def update_staff(staff_id):
    """Update a staff member"""
    staff = Staff.query.get_or_404(staff_id)
    data = request.json
    
    if 'name' in data:
        staff.Name = data['name']
    if 'role' in data:
        staff.Role = data['role']
    if 'contact_info' in data:
        staff.ContactInfo = data['contact_info']
    if 'status' in data:
        staff.Status = data['status']
    
    db.session.commit()
    
    return success_response({
        'id': staff.StaffID,
        'name': staff.Name,
        'role': staff.Role,
        'status': staff.Status
    }, "Staff member updated successfully")

@staff_bp.route('/attendance', methods=['GET'])
def get_attendance():
    """Get attendance records"""
    staff_id = request.args.get('staff_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Attendance.query
    
    if staff_id:
        query = query.filter(Attendance.StaffID == int(staff_id))
    if start_date:
        query = query.filter(Attendance.Date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Attendance.Date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    records = query.order_by(Attendance.Date.desc()).all()
    
    return jsonify([{
        'id': a.AttendanceID,
        'date': a.Date.isoformat() if a.Date else None,
        'check_in': str(a.CheckIn) if a.CheckIn else None,
        'check_out': str(a.CheckOut) if a.CheckOut else None,
        'status': a.Status,
        'staff_id': a.StaffID,
        'staff_name': a.staff.Name if a.staff else None
    } for a in records])

@staff_bp.route('/attendance', methods=['POST'])
@validate_json
@handle_exceptions
def create_attendance():
    """Create a new attendance record"""
    data = request.json
    
    try:
        attendance = Attendance(
            Date=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else datetime.utcnow().date(),
            CheckIn=datetime.strptime(data['check_in'], '%H:%M:%S').time() if data.get('check_in') else None,
            CheckOut=datetime.strptime(data['check_out'], '%H:%M:%S').time() if data.get('check_out') else None,
            Status=data.get('status', 'Present'),
            StaffID=data.get('staff_id')
        )
        
        db.session.add(attendance)
        db.session.commit()
        
        return success_response({
            'id': attendance.AttendanceID,
            'date': attendance.Date.isoformat() if attendance.Date else None,
            'status': attendance.Status
        }, "Attendance record created successfully", 201)
    except ValueError as e:
        return error_response(f"Invalid date/time format: {str(e)}", 400)

@staff_bp.route('/schedules', methods=['GET'])
def get_schedules():
    """Get staff schedules"""
    staff_id = request.args.get('staff_id')
    
    query = Schedule.query
    
    if staff_id:
        query = query.filter(Schedule.StaffID == int(staff_id))
    
    schedules = query.order_by(Schedule.ShiftDate.desc()).all()
    
    return jsonify([{
        'id': s.ScheduleID,
        'shift_date': s.ShiftDate.isoformat() if s.ShiftDate else None,
        'shift_type': s.ShiftType,
        'field': s.Field,
        'hours': float(s.Hours) if s.Hours else 0,
        'location': s.Location,
        'staff_id': s.StaffID,
        'staff_name': s.staff.Name if s.staff else None
    } for s in schedules])

@staff_bp.route('/schedules', methods=['POST'])
@validate_json
@handle_exceptions
def create_schedule():
    """Create a new schedule"""
    data = request.json
    
    try:
        schedule = Schedule(
            ShiftDate=datetime.strptime(data['shift_date'], '%Y-%m-%d').date() if data.get('shift_date') else datetime.utcnow().date(),
            ShiftType=data.get('shift_type'),
            Field=data.get('field'),
            Hours=Decimal(str(data.get('hours', 0))) if data.get('hours') else None,
            Location=data.get('location'),
            StaffID=data.get('staff_id')
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        return success_response({
            'id': schedule.ScheduleID,
            'shift_date': schedule.ShiftDate.isoformat() if schedule.ShiftDate else None,
            'shift_type': schedule.ShiftType
        }, "Schedule created successfully", 201)
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)

@staff_bp.route('/performance-reviews', methods=['GET'])
def get_performance_reviews():
    """Get performance reviews"""
    staff_id = request.args.get('staff_id')
    
    query = PerformanceReview.query
    
    if staff_id:
        query = query.filter(PerformanceReview.StaffID == int(staff_id))
    
    reviews = query.order_by(PerformanceReview.ReviewDate.desc()).all()
    
    return jsonify([{
        'id': pr.PerformanceReviewID,
        'review_date': pr.ReviewDate.isoformat() if pr.ReviewDate else None,
        'score': float(pr.Score) if pr.Score else 0,
        'comments': pr.Comments,
        'staff_id': pr.StaffID,
        'staff_name': pr.staff.Name if pr.staff else None
    } for pr in reviews])

@staff_bp.route('/performance-reviews', methods=['POST'])
def create_performance_review():
    """Create a new performance review"""
    data = request.json
    
    review = PerformanceReview(
        ReviewDate=datetime.strptime(data['review_date'], '%Y-%m-%d').date() if data.get('review_date') else datetime.utcnow().date(),
        Score=Decimal(str(data.get('score', 0))) if data.get('score') else None,
        Comments=data.get('comments'),
        StaffID=data.get('staff_id')
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({'id': review.PerformanceReviewID, 'message': 'Performance review created successfully'}), 201

@staff_bp.route('/payroll', methods=['GET'])
def get_payroll():
    """Get payroll records"""
    staff_id = request.args.get('staff_id')
    
    query = PayrollRecord.query
    
    if staff_id:
        query = query.filter(PayrollRecord.StaffID == int(staff_id))
    
    records = query.order_by(PayrollRecord.PaymentDate.desc()).all()
    
    return jsonify([{
        'id': pr.PayrollRecordID,
        'pay_period': pr.PayPeriod,
        'amount': float(pr.Amount) if pr.Amount else 0,
        'payment_date': pr.PaymentDate.isoformat() if pr.PaymentDate else None,
        'staff_id': pr.StaffID,
        'staff_name': pr.staff.Name if pr.staff else None
    } for pr in records])

@staff_bp.route('/payroll', methods=['POST'])
def create_payroll():
    """Create a new payroll record"""
    data = request.json
    
    payroll = PayrollRecord(
        PayPeriod=data.get('pay_period'),
        Amount=Decimal(str(data.get('amount', 0))),
        PaymentDate=datetime.strptime(data['payment_date'], '%Y-%m-%d').date() if data.get('payment_date') else datetime.utcnow().date(),
        StaffID=data.get('staff_id')
    )
    
    db.session.add(payroll)
    
    # Create financial record
    from models import FinancialRecord, PayrollFinancialRecord
    financial_record = FinancialRecord(
        TransactionDate=payroll.PaymentDate,
        TransactionType='Expense',
        Amount=payroll.Amount,
        Description=f'Payroll for {payroll.PayPeriod}'
    )
    db.session.add(financial_record)
    db.session.flush()
    
    pfr = PayrollFinancialRecord(
        PayrollRecordID=payroll.PayrollRecordID,
        FinancialRecordID=financial_record.FinancialRecordID
    )
    db.session.add(pfr)
    
    db.session.commit()
    
    return jsonify({'id': payroll.PayrollRecordID, 'message': 'Payroll record created successfully'}), 201



