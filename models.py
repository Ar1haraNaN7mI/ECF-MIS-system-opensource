from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Inventory Management Models
class DemandPlan(db.Model):
    __tablename__ = 'demand_plan'
    DemandPlanID = db.Column(db.Integer, primary_key=True)
    ItemName = db.Column(db.String(200), nullable=False)
    ForecastQuantity = db.Column(db.Integer, nullable=False)
    PlanDate = db.Column(db.Date, nullable=False)
    
    inventories = db.relationship('Inventory', backref='demand_plan', lazy=True)
    purchase_orders = db.relationship('PurchaseOrder', backref='demand_plan', lazy=True)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    InventoryID = db.Column(db.Integer, primary_key=True)
    ItemName = db.Column(db.String(200), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False, default=0)
    Location = db.Column(db.String(200))
    DemandPlanID = db.Column(db.Integer, db.ForeignKey('demand_plan.DemandPlanID'), nullable=True)
    
    purchase_order_items = db.relationship('PurchaseOrderInventory', backref='inventory', lazy=True)

class Supplier(db.Model):
    __tablename__ = 'supplier'
    SupplierID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    ContactInfo = db.Column(db.String(200))
    Address = db.Column(db.String(500))
    
    purchase_orders = db.relationship('PurchaseOrder', backref='supplier', lazy=True)

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_order'
    PurchaseOrderID = db.Column(db.Integer, primary_key=True)
    OrderDate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    TotalAmount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    Status = db.Column(db.String(50), default='Pending')
    SupplierID = db.Column(db.Integer, db.ForeignKey('supplier.SupplierID'), nullable=False)
    DemandPlanID = db.Column(db.Integer, db.ForeignKey('demand_plan.DemandPlanID'), nullable=True)
    
    inventory_items = db.relationship('PurchaseOrderInventory', backref='purchase_order', lazy=True, cascade='all, delete-orphan')
    financial_records = db.relationship('PurchaseOrderFinancialRecord', backref='purchase_order', lazy=True, cascade='all, delete-orphan')

class PurchaseOrderInventory(db.Model):
    __tablename__ = 'purchase_order_inventory'
    PurchaseOrderID = db.Column(db.Integer, db.ForeignKey('purchase_order.PurchaseOrderID'), primary_key=True)
    InventoryID = db.Column(db.Integer, db.ForeignKey('inventory.InventoryID'), primary_key=True)
    Quantity = db.Column(db.Integer, nullable=False, default=1)

# Financial Management Models
class FinancialRecord(db.Model):
    __tablename__ = 'financial_record'
    FinancialRecordID = db.Column(db.Integer, primary_key=True)
    TransactionDate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    TransactionType = db.Column(db.String(50), nullable=False)  # Income, Expense, Donation, etc.
    AccountCode = db.Column(db.String(50))
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    Description = db.Column(db.Text)
    
    purchase_orders = db.relationship('PurchaseOrderFinancialRecord', backref='financial_record', lazy=True, cascade='all, delete-orphan')
    donations = db.relationship('DonationFinancialRecord', backref='financial_record', lazy=True, cascade='all, delete-orphan')
    payroll_records = db.relationship('PayrollFinancialRecord', backref='financial_record', lazy=True, cascade='all, delete-orphan')

class PurchaseOrderFinancialRecord(db.Model):
    __tablename__ = 'purchase_order_financial_record'
    PurchaseOrderID = db.Column(db.Integer, db.ForeignKey('purchase_order.PurchaseOrderID'), primary_key=True)
    FinancialRecordID = db.Column(db.Integer, db.ForeignKey('financial_record.FinancialRecordID'), primary_key=True)

class PayrollRecord(db.Model):
    __tablename__ = 'payroll_record'
    PayrollRecordID = db.Column(db.Integer, primary_key=True)
    PayPeriod = db.Column(db.String(50), nullable=False)
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    PaymentDate = db.Column(db.Date, nullable=False)
    StaffID = db.Column(db.Integer, db.ForeignKey('staff.StaffID'), nullable=False)
    
    financial_records = db.relationship('PayrollFinancialRecord', backref='payroll_record', lazy=True, cascade='all, delete-orphan')

class PayrollFinancialRecord(db.Model):
    __tablename__ = 'payroll_financial_record'
    PayrollRecordID = db.Column(db.Integer, db.ForeignKey('payroll_record.PayrollRecordID'), primary_key=True)
    FinancialRecordID = db.Column(db.Integer, db.ForeignKey('financial_record.FinancialRecordID'), primary_key=True)

class Expense(db.Model):
    __tablename__ = 'expense'
    ExpenseID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    Type = db.Column(db.String(100), nullable=False)
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    Description = db.Column(db.Text)
    StaffID = db.Column(db.Integer, db.ForeignKey('staff.StaffID'), nullable=True)

# Donation Management Models
class Donor(db.Model):
    __tablename__ = 'donor'
    DonorID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    ContactInfo = db.Column(db.String(200))
    RegistrationDate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    Age = db.Column(db.Integer)
    Region = db.Column(db.String(100))
    
    donations = db.relationship('Donation', backref='donor', lazy=True)

class Gift(db.Model):
    __tablename__ = 'gift'
    GiftID = db.Column(db.Integer, primary_key=True)
    GiftType = db.Column(db.String(100), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False, default=1)
    DistributionDate = db.Column(db.Date)
    
    donations = db.relationship('Donation', backref='gift', lazy=True)

class Donation(db.Model):
    __tablename__ = 'donation'
    DonationID = db.Column(db.Integer, primary_key=True)
    DonationType = db.Column(db.String(50), nullable=False)  # Monetary, Gift, etc.
    Status = db.Column(db.String(50), default='Pending')
    Amount = db.Column(db.Numeric(10, 2), default=0)
    DonationDate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    DonorID = db.Column(db.Integer, db.ForeignKey('donor.DonorID'), nullable=False)
    StaffID = db.Column(db.Integer, db.ForeignKey('staff.StaffID'), nullable=True)
    GiftID = db.Column(db.Integer, db.ForeignKey('gift.GiftID'), nullable=True)
    
    financial_records = db.relationship('DonationFinancialRecord', backref='donation', lazy=True, cascade='all, delete-orphan')

class DonationFinancialRecord(db.Model):
    __tablename__ = 'donation_financial_record'
    DonationID = db.Column(db.Integer, db.ForeignKey('donation.DonationID'), primary_key=True)
    FinancialRecordID = db.Column(db.Integer, db.ForeignKey('financial_record.FinancialRecordID'), primary_key=True)

# Staff and User Management Models
class Staff(db.Model):
    __tablename__ = 'staff'
    StaffID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Role = db.Column(db.String(100))
    ContactInfo = db.Column(db.String(200))
    Status = db.Column(db.String(50), default='Active')
    
    payroll_records = db.relationship('PayrollRecord', backref='staff', lazy=True)
    expenses = db.relationship('Expense', backref='staff', lazy=True)
    donations = db.relationship('Donation', backref='staff', lazy=True)
    attendance_records = db.relationship('Attendance', backref='staff', lazy=True)
    schedules = db.relationship('Schedule', backref='staff', lazy=True)
    performance_reviews = db.relationship('PerformanceReview', backref='staff', lazy=True)
    user = db.relationship('User', backref='staff', uselist=False, lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    AttendanceID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    CheckIn = db.Column(db.Time)
    CheckOut = db.Column(db.Time)
    Status = db.Column(db.String(50), default='Present')
    StaffID = db.Column(db.Integer, db.ForeignKey('staff.StaffID'), nullable=False)

class Schedule(db.Model):
    __tablename__ = 'schedule'
    ScheduleID = db.Column(db.Integer, primary_key=True)
    ShiftDate = db.Column(db.Date, nullable=False)
    ShiftType = db.Column(db.String(50))
    Field = db.Column(db.String(100))
    Hours = db.Column(db.Numeric(4, 2))
    Location = db.Column(db.String(200))
    StaffID = db.Column(db.Integer, db.ForeignKey('staff.StaffID'), nullable=False)

class PerformanceReview(db.Model):
    __tablename__ = 'performance_review'
    PerformanceReviewID = db.Column(db.Integer, primary_key=True)
    ReviewDate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    Score = db.Column(db.Numeric(5, 2))
    Comments = db.Column(db.Text)
    StaffID = db.Column(db.Integer, db.ForeignKey('staff.StaffID'), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    StaffID = db.Column(db.Integer, db.ForeignKey('staff.StaffID'), nullable=True)
    
    roles = db.relationship('UserRole', backref='user', lazy=True, cascade='all, delete-orphan')

class Role(db.Model):
    __tablename__ = 'role'
    RoleID = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(100), unique=True, nullable=False)
    
    users = db.relationship('UserRole', backref='role', lazy=True, cascade='all, delete-orphan')
    permissions = db.relationship('RolePermission', backref='role', lazy=True, cascade='all, delete-orphan')

class Permission(db.Model):
    __tablename__ = 'permission'
    PermissionID = db.Column(db.Integer, primary_key=True)
    PermissionName = db.Column(db.String(100), unique=True, nullable=False)
    
    roles = db.relationship('RolePermission', backref='permission', lazy=True, cascade='all, delete-orphan')

class UserRole(db.Model):
    __tablename__ = 'user_role'
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), primary_key=True)
    RoleID = db.Column(db.Integer, db.ForeignKey('role.RoleID'), primary_key=True)

class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    RoleID = db.Column(db.Integer, db.ForeignKey('role.RoleID'), primary_key=True)
    PermissionID = db.Column(db.Integer, db.ForeignKey('permission.PermissionID'), primary_key=True)





