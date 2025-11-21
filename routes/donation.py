from flask import Blueprint, request, jsonify
from models import db, Donation, Donor, Gift, FinancialRecord, DonationFinancialRecord
from datetime import datetime
from decimal import Decimal
from .utils import success_response, error_response, handle_exceptions, validate_json

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/donations', methods=['GET'])
def get_donations():
    """Get all donations"""
    status = request.args.get('status')
    donor_id = request.args.get('donor_id')
    
    query = Donation.query
    
    if status:
        query = query.filter(Donation.Status == status)
    if donor_id:
        query = query.filter(Donation.DonorID == int(donor_id))
    
    donations = query.order_by(Donation.DonationDate.desc()).all()
    
    return jsonify([{
        'id': d.DonationID,
        'type': d.DonationType,
        'status': d.Status,
        'amount': float(d.Amount) if d.Amount else 0,
        'date': d.DonationDate.isoformat() if d.DonationDate else None,
        'donor_id': d.DonorID,
        'donor_name': d.donor.Name if d.donor else None,
        'staff_id': d.StaffID,
        'gift_id': d.GiftID
    } for d in donations])

@donation_bp.route('/donations', methods=['POST'])
@validate_json
@handle_exceptions
def create_donation():
    """Create a new donation"""
    data = request.json
    
    try:
        donation = Donation(
            DonationType=data.get('type', 'Monetary'),
            Status=data.get('status', 'Pending'),
            Amount=Decimal(str(data.get('amount', 0))),
            DonationDate=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else datetime.utcnow().date(),
            DonorID=data.get('donor_id'),
            StaffID=data.get('staff_id'),
            GiftID=data.get('gift_id')
        )
        
        db.session.add(donation)
        db.session.flush()
        
        # Create financial record for monetary donations
        if donation.DonationType == 'Monetary' and donation.Amount:
            financial_record = FinancialRecord(
                TransactionDate=donation.DonationDate,
                TransactionType='Donation',
                Amount=donation.Amount,
                Description=f'Donation from donor {donation.DonorID}'
            )
            db.session.add(financial_record)
            db.session.flush()
            
            donation_financial = DonationFinancialRecord(
                DonationID=donation.DonationID,
                FinancialRecordID=financial_record.FinancialRecordID
            )
            db.session.add(donation_financial)
        
        db.session.commit()
        
        return success_response({
            'id': donation.DonationID,
            'type': donation.DonationType,
            'amount': float(donation.Amount) if donation.Amount else 0,
            'date': donation.DonationDate.isoformat() if donation.DonationDate else None
        }, "Donation created successfully", 201)
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)

@donation_bp.route('/donations/<int:donation_id>', methods=['GET'])
@handle_exceptions
def get_donation(donation_id):
    """Get a single donation"""
    donation = Donation.query.get_or_404(donation_id)
    
    return success_response({
        'id': donation.DonationID,
        'type': donation.DonationType,
        'status': donation.Status,
        'amount': float(donation.Amount) if donation.Amount else 0,
        'date': donation.DonationDate.isoformat() if donation.DonationDate else None,
        'donor_id': donation.DonorID,
        'staff_id': donation.StaffID,
        'gift_id': donation.GiftID
    }, "Donation retrieved successfully")

@donation_bp.route('/donations/<int:donation_id>', methods=['PUT'])
@validate_json
@handle_exceptions
def update_donation(donation_id):
    """Update a donation"""
    donation = Donation.query.get_or_404(donation_id)
    data = request.json
    
    if 'type' in data:
        donation.DonationType = data['type']
    if 'status' in data:
        donation.Status = data['status']
    if 'amount' in data:
        donation.Amount = Decimal(str(data['amount']))
    if 'date' in data:
        try:
            donation.DonationDate = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return error_response("Invalid date format. Use YYYY-MM-DD", 400)
    if 'donor_id' in data:
        donation.DonorID = data['donor_id']
    if 'staff_id' in data:
        donation.StaffID = data['staff_id']
    
    db.session.commit()
    
    return success_response({
        'id': donation.DonationID,
        'type': donation.DonationType,
        'status': donation.Status,
        'amount': float(donation.Amount) if donation.Amount else 0
    }, "Donation updated successfully")

@donation_bp.route('/donors', methods=['GET'])
def get_donors():
    """Get all donors"""
    region = request.args.get('region')
    
    query = Donor.query
    
    if region:
        query = query.filter(Donor.Region == region)
    
    donors = query.order_by(Donor.RegistrationDate.desc()).all()
    
    return jsonify([{
        'id': d.DonorID,
        'name': d.Name,
        'contact_info': d.ContactInfo,
        'registration_date': d.RegistrationDate.isoformat() if d.RegistrationDate else None,
        'age': d.Age,
        'region': d.Region,
        'total_donations': sum(float(don.Amount) if don.Amount else 0 for don in d.donations)
    } for d in donors])

@donation_bp.route('/donors', methods=['POST'])
@validate_json
@handle_exceptions
def create_donor():
    """Create a new donor"""
    data = request.json
    
    try:
        donor = Donor(
            Name=data.get('name'),
            ContactInfo=data.get('contact_info'),
            RegistrationDate=datetime.strptime(data['registration_date'], '%Y-%m-%d').date() if data.get('registration_date') else datetime.utcnow().date(),
            Age=data.get('age'),
            Region=data.get('region')
        )
        
        db.session.add(donor)
        db.session.commit()
        
        return success_response({
            'id': donor.DonorID,
            'name': donor.Name,
            'age': donor.Age,
            'region': donor.Region
        }, "Donor created successfully", 201)
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)

@donation_bp.route('/donors/<int:donor_id>', methods=['GET'])
@handle_exceptions
def get_donor(donor_id):
    """Get a single donor"""
    donor = Donor.query.get_or_404(donor_id)
    
    return success_response({
        'id': donor.DonorID,
        'name': donor.Name,
        'contact_info': donor.ContactInfo,
        'registration_date': donor.RegistrationDate.isoformat() if donor.RegistrationDate else None,
        'age': donor.Age,
        'region': donor.Region
    }, "Donor retrieved successfully")

@donation_bp.route('/donors/<int:donor_id>', methods=['PUT'])
@validate_json
@handle_exceptions
def update_donor(donor_id):
    """Update a donor"""
    donor = Donor.query.get_or_404(donor_id)
    data = request.json
    
    if 'name' in data:
        donor.Name = data['name']
    if 'contact_info' in data:
        donor.ContactInfo = data['contact_info']
    if 'age' in data:
        donor.Age = data['age']
    if 'region' in data:
        donor.Region = data['region']
    if 'registration_date' in data:
        try:
            donor.RegistrationDate = datetime.strptime(data['registration_date'], '%Y-%m-%d').date()
        except ValueError:
            return error_response("Invalid date format. Use YYYY-MM-DD", 400)
    
    db.session.commit()
    
    return success_response({
        'id': donor.DonorID,
        'name': donor.Name,
        'age': donor.Age,
        'region': donor.Region
    }, "Donor updated successfully")

@donation_bp.route('/demographics', methods=['GET'])
def get_donor_demographics():
    """Get donor demographics statistics"""
    donors = Donor.query.all()
    
    # Age groups
    age_groups = {'0-25': 0, '26-40': 0, '41-60': 0, '61+': 0, 'Unknown': 0}
    
    # Regions
    regions = {}
    
    for donor in donors:
        # Age grouping
        if donor.Age:
            if donor.Age <= 25:
                age_groups['0-25'] += 1
            elif donor.Age <= 40:
                age_groups['26-40'] += 1
            elif donor.Age <= 60:
                age_groups['41-60'] += 1
            else:
                age_groups['61+'] += 1
        else:
            age_groups['Unknown'] += 1
        
        # Region grouping
        region = donor.Region or 'Unknown'
        regions[region] = regions.get(region, 0) + 1
    
    return jsonify({
        'age_groups': age_groups,
        'regions': regions,
        'total_donors': len(donors)
    })

@donation_bp.route('/gifts', methods=['GET'])
def get_gifts():
    """Get all gifts"""
    gifts = Gift.query.all()
    
    return jsonify([{
        'id': g.GiftID,
        'type': g.GiftType,
        'quantity': g.Quantity,
        'distribution_date': g.DistributionDate.isoformat() if g.DistributionDate else None
    } for g in gifts])

@donation_bp.route('/gifts', methods=['POST'])
def create_gift():
    """Create a new gift"""
    data = request.json
    
    gift = Gift(
        GiftType=data.get('type'),
        Quantity=data.get('quantity', 1),
        DistributionDate=datetime.strptime(data['distribution_date'], '%Y-%m-%d').date() if data.get('distribution_date') else None
    )
    
    db.session.add(gift)
    db.session.commit()
    
    return jsonify({'id': gift.GiftID, 'message': 'Gift created successfully'}), 201




