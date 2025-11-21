"""
Initialize database with sample data
Run this script to populate the database with realistic sample data
"""
from app import app, db
from models import (
    Staff, Donor, Donation, Gift, FinancialRecord, Inventory, Supplier,
    PurchaseOrder, PurchaseOrderInventory, Expense, Attendance, Schedule,
    PerformanceReview, DemandPlan, PayrollRecord
)
from datetime import datetime, timedelta
from decimal import Decimal
import random

def init_data():
    """Initialize database with sample data"""
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        print("Creating sample data...")
        
        # 1. Create Staff
        staff_members = [
            Staff(Name="John Smith", Role="Manager", ContactInfo="john.smith@eldercare.org", Status="Active"),
            Staff(Name="Sarah Johnson", Role="Nurse", ContactInfo="sarah.j@eldercare.org", Status="Active"),
            Staff(Name="Michael Chen", Role="Caregiver", ContactInfo="michael.chen@eldercare.org", Status="Active"),
            Staff(Name="Emily Davis", Role="Administrator", ContactInfo="emily.davis@eldercare.org", Status="Active"),
            Staff(Name="David Wilson", Role="Nurse", ContactInfo="david.wilson@eldercare.org", Status="Active"),
            Staff(Name="Lisa Anderson", Role="Caregiver", ContactInfo="lisa.a@eldercare.org", Status="Active"),
        ]
        for staff in staff_members:
            db.session.add(staff)
        db.session.commit()
        print(f"Created {len(staff_members)} staff members")
        
        # 2. Create Donors
        donors = [
            Donor(Name="Robert Brown", ContactInfo="robert.brown@email.com", RegistrationDate=datetime(2023, 1, 15).date(), Age=65, Region="North"),
            Donor(Name="Mary White", ContactInfo="mary.white@email.com", RegistrationDate=datetime(2023, 2, 20).date(), Age=72, Region="South"),
            Donor(Name="James Taylor", ContactInfo="james.taylor@email.com", RegistrationDate=datetime(2023, 3, 10).date(), Age=58, Region="East"),
            Donor(Name="Patricia Martinez", ContactInfo="patricia.m@email.com", RegistrationDate=datetime(2023, 4, 5).date(), Age=68, Region="West"),
            Donor(Name="William Lee", ContactInfo="william.lee@email.com", RegistrationDate=datetime(2023, 5, 12).date(), Age=75, Region="North"),
            Donor(Name="Jennifer Garcia", ContactInfo="jennifer.g@email.com", RegistrationDate=datetime(2023, 6, 18).date(), Age=62, Region="South"),
            Donor(Name="Richard Miller", ContactInfo="richard.m@email.com", RegistrationDate=datetime(2023, 7, 22).date(), Age=70, Region="East"),
            Donor(Name="Susan Davis", ContactInfo="susan.davis@email.com", RegistrationDate=datetime(2023, 8, 8).date(), Age=55, Region="West"),
            Donor(Name="Joseph Rodriguez", ContactInfo="joseph.r@email.com", RegistrationDate=datetime(2023, 9, 14).date(), Age=80, Region="North"),
            Donor(Name="Nancy Wilson", ContactInfo="nancy.wilson@email.com", RegistrationDate=datetime(2023, 10, 25).date(), Age=67, Region="South"),
        ]
        for donor in donors:
            db.session.add(donor)
        db.session.commit()
        print(f"Created {len(donors)} donors")
        
        # 3. Create Donations
        donation_types = ["Monetary", "Gift"]
        statuses = ["Completed", "Pending"]
        staff_ids = [s.StaffID for s in staff_members]
        donor_ids = [d.DonorID for d in donors]
        
        donations = []
        for i in range(30):
            donation_date = datetime.now().date() - timedelta(days=random.randint(0, 180))
            amount = Decimal(str(random.randint(100, 5000)))
            donation = Donation(
                DonationType=random.choice(donation_types),
                Status=random.choice(statuses),
                Amount=amount if random.choice(donation_types) == "Monetary" else Decimal('0'),
                DonationDate=donation_date,
                DonorID=random.choice(donor_ids),
                StaffID=random.choice(staff_ids) if random.random() > 0.3 else None
            )
            donations.append(donation)
            db.session.add(donation)
            
            # Create financial record for monetary donations
            if donation.DonationType == "Monetary" and donation.Amount:
                financial_record = FinancialRecord(
                    TransactionDate=donation.DonationDate,
                    TransactionType="Donation",
                    Amount=donation.Amount,
                    Description=f"Donation from donor {donation.DonorID}"
                )
                db.session.add(financial_record)
                db.session.flush()
                
                from models import DonationFinancialRecord
                donation_financial = DonationFinancialRecord(
                    DonationID=donation.DonationID,
                    FinancialRecordID=financial_record.FinancialRecordID
                )
                db.session.add(donation_financial)
        
        db.session.commit()
        print(f"Created {len(donations)} donations")
        
        # 4. Create Inventory Items
        inventory_items = [
            Inventory(ItemName="Medical Supplies - Bandages", Quantity=500, Location="Warehouse A"),
            Inventory(ItemName="Medical Supplies - Gloves", Quantity=1000, Location="Warehouse A"),
            Inventory(ItemName="Food - Canned Goods", Quantity=200, Location="Warehouse B"),
            Inventory(ItemName="Food - Rice", Quantity=150, Location="Warehouse B"),
            Inventory(ItemName="Equipment - Wheelchairs", Quantity=25, Location="Storage Room"),
            Inventory(ItemName="Equipment - Walkers", Quantity=30, Location="Storage Room"),
            Inventory(ItemName="Hygiene Products - Soap", Quantity=300, Location="Warehouse A"),
            Inventory(ItemName="Hygiene Products - Shampoo", Quantity=250, Location="Warehouse A"),
            Inventory(ItemName="Clothing - Blankets", Quantity=100, Location="Warehouse C"),
            Inventory(ItemName="Clothing - Socks", Quantity=500, Location="Warehouse C"),
        ]
        for item in inventory_items:
            db.session.add(item)
        db.session.commit()
        print(f"Created {len(inventory_items)} inventory items")
        
        # 5. Create Suppliers
        suppliers = [
            Supplier(Name="MedSupply Co.", ContactInfo="contact@medsupply.com", Address="123 Medical St, City"),
            Supplier(Name="Food Distributors Inc.", ContactInfo="sales@fooddist.com", Address="456 Food Ave, City"),
            Supplier(Name="Equipment Solutions Ltd.", ContactInfo="info@equipsol.com", Address="789 Equipment Blvd, City"),
            Supplier(Name="Hygiene Products Corp.", ContactInfo="orders@hygienepro.com", Address="321 Hygiene Rd, City"),
        ]
        for supplier in suppliers:
            db.session.add(supplier)
        db.session.commit()
        print(f"Created {len(suppliers)} suppliers")
        
        # 6. Create Demand Plans
        demand_plans = [
            DemandPlan(ItemName="Medical Supplies - Bandages", ForecastQuantity=600, PlanDate=datetime.now().date() + timedelta(days=30)),
            DemandPlan(ItemName="Food - Canned Goods", ForecastQuantity=250, PlanDate=datetime.now().date() + timedelta(days=30)),
            DemandPlan(ItemName="Equipment - Wheelchairs", ForecastQuantity=30, PlanDate=datetime.now().date() + timedelta(days=60)),
        ]
        for plan in demand_plans:
            db.session.add(plan)
        db.session.commit()
        print(f"Created {len(demand_plans)} demand plans")
        
        # 7. Create Purchase Orders
        supplier_ids = [s.SupplierID for s in suppliers]
        inventory_ids = [i.InventoryID for i in inventory_items]
        
        purchase_orders = []
        for i in range(10):
            order_date = datetime.now().date() - timedelta(days=random.randint(0, 90))
            total_amount = Decimal(str(random.randint(500, 5000)))
            po = PurchaseOrder(
                OrderDate=order_date,
                TotalAmount=total_amount,
                Status=random.choice(["Completed", "Pending", "Processing"]),
                SupplierID=random.choice(supplier_ids),
                DemandPlanID=random.choice([p.DemandPlanID for p in demand_plans]) if random.random() > 0.5 else None
            )
            db.session.add(po)
            db.session.flush()
            
            # Add inventory items to purchase order
            num_items = random.randint(1, 3)
            selected_items = random.sample(inventory_ids, min(num_items, len(inventory_items)))
            for inv_id in selected_items:
                poi = PurchaseOrderInventory(
                    PurchaseOrderID=po.PurchaseOrderID,
                    InventoryID=inv_id,
                    Quantity=random.randint(10, 100)
                )
                db.session.add(poi)
            
            # Create financial record
            financial_record = FinancialRecord(
                TransactionDate=order_date,
                TransactionType="Expense",
                Amount=total_amount,
                Description=f"Purchase Order #{po.PurchaseOrderID}"
            )
            db.session.add(financial_record)
            db.session.flush()
            
            from models import PurchaseOrderFinancialRecord
            pofr = PurchaseOrderFinancialRecord(
                PurchaseOrderID=po.PurchaseOrderID,
                FinancialRecordID=financial_record.FinancialRecordID
            )
            db.session.add(pofr)
            
            purchase_orders.append(po)
        
        db.session.commit()
        print(f"Created {len(purchase_orders)} purchase orders")
        
        # 8. Create Expenses
        expense_types = ["Utilities", "Rent", "Maintenance", "Transportation", "Other"]
        for i in range(20):
            expense_date = datetime.now().date() - timedelta(days=random.randint(0, 120))
            expense = Expense(
                Date=expense_date,
                Type=random.choice(expense_types),
                Amount=Decimal(str(random.randint(50, 2000))),
                Description=f"{random.choice(expense_types)} expense",
                StaffID=random.choice(staff_ids) if random.random() > 0.4 else None
            )
            db.session.add(expense)
        db.session.commit()
        print("Created 20 expenses")
        
        # 9. Create Payroll Records
        for staff in staff_members:
            for month in range(1, 13):
                payroll_date = datetime(2024, month, 15).date()
                payroll = PayrollRecord(
                    PayPeriod=f"2024-{month:02d}",
                    Amount=Decimal(str(random.randint(3000, 6000))),
                    PaymentDate=payroll_date,
                    StaffID=staff.StaffID
                )
                db.session.add(payroll)
                db.session.flush()
                
                # Create financial record
                financial_record = FinancialRecord(
                    TransactionDate=payroll_date,
                    TransactionType="Expense",
                    Amount=payroll.Amount,
                    Description=f"Payroll for {payroll.PayPeriod}"
                )
                db.session.add(financial_record)
                db.session.flush()
                
                from models import PayrollFinancialRecord
                pfr = PayrollFinancialRecord(
                    PayrollRecordID=payroll.PayrollRecordID,
                    FinancialRecordID=financial_record.FinancialRecordID
                )
                db.session.add(pfr)
        
        db.session.commit()
        print("Created payroll records")
        
        # 10. Create Attendance Records
        for staff in staff_members:
            for day in range(30):
                attendance_date = datetime.now().date() - timedelta(days=day)
                if attendance_date.weekday() < 5:  # Weekdays only
                    attendance = Attendance(
                        Date=attendance_date,
                        CheckIn=datetime.strptime(f"{random.randint(7, 9)}:{random.randint(0, 59):02d}", "%H:%M").time(),
                        CheckOut=datetime.strptime(f"{random.randint(16, 18)}:{random.randint(0, 59):02d}", "%H:%M").time(),
                        Status="Present",
                        StaffID=staff.StaffID
                    )
                    db.session.add(attendance)
        db.session.commit()
        print("Created attendance records")
        
        # 11. Create Schedules
        shift_types = ["Morning", "Afternoon", "Night"]
        fields = ["Nursing", "Caregiving", "Administration", "Support"]
        locations = ["Main Facility", "Branch A", "Branch B", "Home Care"]
        
        for staff in staff_members:
            for week in range(4):
                schedule_date = datetime.now().date() + timedelta(days=week*7 + random.randint(0, 6))
                schedule = Schedule(
                    ShiftDate=schedule_date,
                    ShiftType=random.choice(shift_types),
                    Field=random.choice(fields),
                    Hours=Decimal(str(random.choice([4, 6, 8]))),
                    Location=random.choice(locations),
                    StaffID=staff.StaffID
                )
                db.session.add(schedule)
        db.session.commit()
        print("Created schedules")
        
        # 12. Create Performance Reviews
        for staff in staff_members:
            review_date = datetime.now().date() - timedelta(days=random.randint(30, 180))
            review = PerformanceReview(
                ReviewDate=review_date,
                Score=Decimal(str(random.randint(70, 100))),
                Comments=f"Performance review for {staff.Name}. Overall satisfactory performance.",
                StaffID=staff.StaffID
            )
            db.session.add(review)
        db.session.commit()
        print("Created performance reviews")
        
        # 13. Create Additional Financial Records
        for i in range(15):
            record_date = datetime.now().date() - timedelta(days=random.randint(0, 150))
            record_type = random.choice(["Income", "Expense"])
            amount = Decimal(str(random.randint(100, 3000)))
            
            financial_record = FinancialRecord(
                TransactionDate=record_date,
                TransactionType=record_type,
                AccountCode=f"ACC{random.randint(1000, 9999)}",
                Amount=amount,
                Description=f"{record_type} transaction - {random.choice(['Service', 'Grant', 'Donation', 'Operating'])}"
            )
            db.session.add(financial_record)
        db.session.commit()
        print("Created additional financial records")
        
        print("\n" + "="*50)
        print("Data initialization completed successfully!")
        print("="*50)
        print(f"\nSummary:")
        print(f"- Staff Members: {len(staff_members)}")
        print(f"- Donors: {len(donors)}")
        print(f"- Donations: {len(donations)}")
        print(f"- Inventory Items: {len(inventory_items)}")
        print(f"- Suppliers: {len(suppliers)}")
        print(f"- Purchase Orders: {len(purchase_orders)}")
        print(f"- Expenses: 20")
        print(f"- Payroll Records: {len(staff_members) * 12}")
        print(f"- Attendance Records: Multiple")
        print(f"- Schedules: Multiple")
        print(f"- Performance Reviews: {len(staff_members)}")

if __name__ == '__main__':
    init_data()

