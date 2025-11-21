const API_BASE = '/api';

let charts = {};

// Navigation
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const section = btn.dataset.section;
        switchSection(section);
    });
});

function switchSection(section) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

    document.getElementById(section).classList.add('active');
    document.querySelector(`[data-section="${section}"]`).classList.add('active');

    loadSectionData(section);
}

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        const parent = btn.closest('.section');

        parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        parent.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

        btn.classList.add('active');
        parent.querySelector(`#${tab}-tab`).classList.add('active');

        loadTabData(tab);
    });
});

// Load section data
function loadSectionData(section) {
    switch (section) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'financial':
            loadFinancialRecords();
            break;
        case 'donation':
            loadDonations();
            break;
        case 'inventory':
            loadInventory();
            break;
        case 'staff':
            loadStaff();
            break;
    }
}

function loadTabData(tab) {
    switch (tab) {
        case 'donations':
            loadDonations();
            break;
        case 'donors':
            loadDonors();
            break;
        case 'demographics':
            loadDemographics();
            break;
        case 'items':
            loadInventoryItems();
            break;
        case 'suppliers':
            loadSuppliers();
            break;
        case 'orders':
            loadPurchaseOrders();
            break;
        case 'staff-list':
            loadStaff();
            break;
        case 'attendance':
            loadAttendance();
            break;
        case 'schedules':
            loadSchedules();
            break;
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const [overview, financialTrends, donationTrends, expenseBreakdown, demographics, topDonors] = await Promise.all([
            fetchAPI(`${API_BASE}/dashboard/overview`),
            fetchAPI(`${API_BASE}/dashboard/financial-trends?days=30`),
            fetchAPI(`${API_BASE}/dashboard/donation-trends?days=30`),
            fetchAPI(`${API_BASE}/dashboard/expense-breakdown`),
            fetchAPI(`${API_BASE}/donation/demographics`),
            fetchAPI(`${API_BASE}/dashboard/top-donors?limit=10`)
        ]);

        // Update stats
        document.getElementById('total-income').textContent = `$${overview.financial.total_income.toLocaleString()}`;
        document.getElementById('total-expense').textContent = `$${overview.financial.total_expense.toLocaleString()}`;
        document.getElementById('net-income').textContent = `$${overview.financial.net.toLocaleString()}`;
        document.getElementById('total-donations').textContent = `$${overview.donations.total_amount.toLocaleString()}`;
        document.getElementById('donor-count').textContent = overview.donors.count;
        document.getElementById('active-staff').textContent = overview.staff.active_count;

        // Financial trends chart
        renderFinancialTrendsChart(financialTrends.trends || []);

        // Donation trends chart
        renderDonationTrendsChart(donationTrends.trends || []);

        // Expense breakdown chart
        renderExpenseBreakdownChart(expenseBreakdown.breakdown || {});

        // Demographics charts
        renderDonorAgeChart(demographics.age_groups || {});
        renderDonorRegionChart(demographics.regions || {});

        // Top donors chart
        renderTopDonorsChart(topDonors.top_donors || []);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function renderFinancialTrendsChart(data) {
    const ctx = document.getElementById('financial-trend-chart');
    if (charts.financialTrends) charts.financialTrends.destroy();

    charts.financialTrends = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: 'Income',
                data: data.map(d => d.income),
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1
            }, {
                label: 'Expense',
                data: data.map(d => d.expense),
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

function renderDonationTrendsChart(data) {
    const ctx = document.getElementById('donation-trend-chart');
    if (charts.donationTrends) charts.donationTrends.destroy();

    charts.donationTrends = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: 'Donation Amount',
                data: data.map(d => d.amount),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

function renderExpenseBreakdownChart(data) {
    const ctx = document.getElementById('expense-breakdown-chart');
    if (charts.expenseBreakdown) charts.expenseBreakdown.destroy();

    charts.expenseBreakdown = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

function renderDonorAgeChart(data) {
    const ctx = document.getElementById('donor-age-chart');
    if (charts.donorAge) charts.donorAge.destroy();

    charts.donorAge = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

function renderDonorRegionChart(data) {
    const ctx = document.getElementById('donor-region-chart');
    if (charts.donorRegion) charts.donorRegion.destroy();

    charts.donorRegion = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Number of Donors',
                data: Object.values(data),
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

function renderTopDonorsChart(data) {
    const ctx = document.getElementById('top-donors-chart');
    if (charts.topDonors) charts.topDonors.destroy();

    charts.topDonors = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.name),
            datasets: [{
                label: 'Total Donations',
                data: data.map(d => d.total_donations),
                backgroundColor: 'rgba(153, 102, 255, 0.5)',
                borderColor: 'rgb(153, 102, 255)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

// Helper function to handle API responses
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, options);
        const result = await response.json();

        if (result.success === false) {
            throw new Error(result.message || 'Request failed');
        }

        return result.data || result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Financial Management
async function loadFinancialRecords() {
    try {
        const startDate = document.getElementById('financial-start-date').value;
        const endDate = document.getElementById('financial-end-date').value;

        let url = `${API_BASE}/financial/records`;
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        if (params.toString()) url += '?' + params.toString();

        const data = await fetchAPI(url);
        const records = Array.isArray(data) ? data : [];

        const tbody = document.querySelector('#financial-table tbody');
        tbody.innerHTML = records.map(record => `
            <tr>
                <td>${record.date || ''}</td>
                <td>${record.type || ''}</td>
                <td>$${(record.amount || 0).toLocaleString()}</td>
                <td>${record.account_code || ''}</td>
                <td>${record.description || ''}</td>
                <td>
                    <button class="btn btn-secondary" onclick="editFinancialRecord(${record.id})">Edit</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading financial records:', error);
        alert('Failed to load financial records: ' + error.message);
    }
}

// Donation Management
async function loadDonations() {
    try {
        const data = await fetchAPI(`${API_BASE}/donation/donations`);
        const donations = Array.isArray(data) ? data : [];

        const tbody = document.querySelector('#donations-table tbody');
        tbody.innerHTML = donations.map(donation => `
            <tr>
                <td>${donation.date || ''}</td>
                <td>${donation.type || ''}</td>
                <td>$${(donation.amount || 0).toLocaleString()}</td>
                <td>${donation.status || ''}</td>
                <td>${donation.donor_name || ''}</td>
                <td>
                    <button class="btn btn-secondary" onclick="editDonation(${donation.id})">Edit</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading donations:', error);
    }
}

async function loadDonors() {
    try {
        const data = await fetchAPI(`${API_BASE}/donation/donors`);
        const donors = Array.isArray(data) ? data : [];

        const tbody = document.querySelector('#donors-table tbody');
        tbody.innerHTML = donors.map(donor => `
            <tr>
                <td>${donor.name || ''}</td>
                <td>${donor.contact_info || ''}</td>
                <td>${donor.age || ''}</td>
                <td>${donor.region || ''}</td>
                <td>${donor.registration_date || ''}</td>
                <td>$${(donor.total_donations || 0).toLocaleString()}</td>
                <td>
                    <button class="btn btn-secondary" onclick="editDonor(${donor.id})">Edit</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading donors:', error);
    }
}

async function loadDemographics() {
    try {
        const data = await fetchAPI(`${API_BASE}/donation/demographics`);

        const ageCtx = document.getElementById('demographics-age-chart');
        if (charts.demographicsAge) charts.demographicsAge.destroy();
        charts.demographicsAge = new Chart(ageCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(data.age_groups),
                datasets: [{
                    data: Object.values(data.age_groups),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 206, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(153, 102, 255, 0.5)'
                    ]
                }]
            },
            options: { responsive: true }
        });

        const regionCtx = document.getElementById('demographics-region-chart');
        if (charts.demographicsRegion) charts.demographicsRegion.destroy();
        charts.demographicsRegion = new Chart(regionCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(data.regions),
                datasets: [{
                    label: 'Number of Donors',
                    data: Object.values(data.regions),
                    backgroundColor: 'rgba(75, 192, 192, 0.5)'
                }]
            },
            options: { responsive: true }
        });
    } catch (error) {
        console.error('Error loading demographics:', error);
    }
}

// Inventory Management
async function loadInventoryItems() {
    try {
        const data = await fetchAPI(`${API_BASE}/inventory/items`);
        const items = Array.isArray(data) ? data : [];

        const tbody = document.querySelector('#inventory-table tbody');
        tbody.innerHTML = items.map(item => `
            <tr>
                <td>${item.item_name || ''}</td>
                <td>${item.quantity || 0}</td>
                <td>${item.location || ''}</td>
                <td>
                    <button class="btn btn-secondary" onclick="editInventoryItem(${item.id})">Edit</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading inventory:', error);
    }
}

async function loadSuppliers() {
    try {
        const data = await fetchAPI(`${API_BASE}/inventory/suppliers`);
        const suppliers = Array.isArray(data) ? data : [];

        const tbody = document.querySelector('#suppliers-table tbody');
        tbody.innerHTML = suppliers.map(supplier => `
            <tr>
                <td>${supplier.name || ''}</td>
                <td>${supplier.contact_info || ''}</td>
                <td>${supplier.address || ''}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading suppliers:', error);
    }
}

async function loadPurchaseOrders() {
    try {
        const data = await fetchAPI(`${API_BASE}/inventory/purchase-orders`);
        const orders = Array.isArray(data) ? data : [];

        const tbody = document.querySelector('#orders-table tbody');
        tbody.innerHTML = orders.map(order => `
            <tr>
                <td>${order.order_date || ''}</td>
                <td>${order.supplier_name || ''}</td>
                <td>$${(order.total_amount || 0).toLocaleString()}</td>
                <td>${order.status || ''}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading purchase orders:', error);
    }
}

function loadInventory() {
    loadInventoryItems();
}

// Staff Management
async function loadStaff() {
    try {
        const data = await fetchAPI(`${API_BASE}/staff/staff`);
        const staffList = Array.isArray(data) ? data : [];

        const tbody = document.querySelector('#staff-table tbody');
        tbody.innerHTML = staffList.map(staff => `
            <tr>
                <td>${staff.name || ''}</td>
                <td>${staff.role || ''}</td>
                <td>${staff.contact_info || ''}</td>
                <td>${staff.status || ''}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading staff:', error);
    }
}

async function loadAttendance() {
    try {
        const data = await fetchAPI(`${API_BASE}/staff/attendance`);
        const attendanceList = Array.isArray(data) ? data : [];

        const tbody = document.querySelector('#attendance-table tbody');
        tbody.innerHTML = attendanceList.map(attendance => `
            <tr>
                <td>${attendance.date || ''}</td>
                <td>${attendance.staff_name || ''}</td>
                <td>${attendance.check_in || ''}</td>
                <td>${attendance.check_out || ''}</td>
                <td>${attendance.status || ''}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading attendance:', error);
    }
}

async function loadSchedules() {
    try {
        const data = await fetchAPI(`${API_BASE}/staff/schedules`);
        const schedules = Array.isArray(data) ? data : [];

        const tbody = document.querySelector('#schedules-table tbody');
        tbody.innerHTML = schedules.map(schedule => `
            <tr>
                <td>${schedule.shift_date || ''}</td>
                <td>${schedule.staff_name || ''}</td>
                <td>${schedule.shift_type || ''}</td>
                <td>${schedule.field || ''}</td>
                <td>${schedule.hours || 0}</td>
                <td>${schedule.location || ''}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading schedules:', error);
    }
}

// Modal functions
function showModal(content) {
    document.getElementById('modal-body').innerHTML = content;
    document.getElementById('modal-overlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modal-overlay').classList.remove('active');
}

function showAddFinancialModal() {
    const content = `
        <h2>Add Financial Record</h2>
        <form onsubmit="addFinancialRecord(event)">
            <div class="form-group">
                <label>Date</label>
                <input type="date" name="date" required>
            </div>
            <div class="form-group">
                <label>Type</label>
                <select name="type" required>
                    <option value="Income">Income</option>
                    <option value="Expense">Expense</option>
                    <option value="Donation">Donation</option>
                </select>
            </div>
            <div class="form-group">
                <label>Amount</label>
                <input type="number" step="0.01" name="amount" required>
            </div>
            <div class="form-group">
                <label>Account Code</label>
                <input type="text" name="account_code">
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea name="description"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    `;
    showModal(content);
}

function showAddDonationModal() {
    const content = `
        <h2>Add Donation</h2>
        <form onsubmit="addDonation(event)">
            <div class="form-group">
                <label>Date</label>
                <input type="date" name="date" required>
            </div>
            <div class="form-group">
                <label>Type</label>
                <select name="type" required>
                    <option value="Monetary">Monetary</option>
                    <option value="Gift">Gift</option>
                </select>
            </div>
            <div class="form-group">
                <label>Amount</label>
                <input type="number" step="0.01" name="amount" required>
            </div>
            <div class="form-group">
                <label>Donor ID</label>
                <input type="number" name="donor_id" required>
            </div>
            <div class="form-group">
                <label>Status</label>
                <select name="status">
                    <option value="Pending">Pending</option>
                    <option value="Completed">Completed</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    `;
    showModal(content);
}

function showAddDonorModal() {
    const content = `
        <h2>Add Donor</h2>
        <form onsubmit="addDonor(event)">
            <div class="form-group">
                <label>Name</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>Contact Info</label>
                <input type="text" name="contact_info">
            </div>
            <div class="form-group">
                <label>Age</label>
                <input type="number" name="age">
            </div>
            <div class="form-group">
                <label>Region</label>
                <input type="text" name="region">
            </div>
            <div class="form-group">
                <label>Registration Date</label>
                <input type="date" name="registration_date">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    `;
    showModal(content);
}

function showAddInventoryModal() {
    const content = `
        <h2>Add Inventory Item</h2>
        <form onsubmit="addInventoryItem(event)">
            <div class="form-group">
                <label>Item Name</label>
                <input type="text" name="item_name" required>
            </div>
            <div class="form-group">
                <label>Quantity</label>
                <input type="number" name="quantity" value="0" required>
            </div>
            <div class="form-group">
                <label>Location</label>
                <input type="text" name="location">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    `;
    showModal(content);
}

async function editInventoryItem(itemId) {
    try {
        const data = await fetchAPI(`${API_BASE}/inventory/items/${itemId}`);

        const content = `
            <h2>Edit Inventory Item</h2>
            <form onsubmit="updateInventoryItem(event, ${itemId})">
                <div class="form-group">
                    <label>Item Name</label>
                    <input type="text" name="item_name" value="${data.item_name || ''}" required>
                </div>
                <div class="form-group">
                    <label>Quantity</label>
                    <input type="number" name="quantity" value="${data.quantity || 0}" required>
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" name="location" value="${data.location || ''}">
                </div>
                <button type="submit" class="btn btn-primary">Update</button>
            </form>
        `;
        showModal(content);
    } catch (error) {
        console.error('Error loading inventory item:', error);
        alert('Failed to load inventory item: ' + error.message);
    }
}

async function updateInventoryItem(event, itemId) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    data.quantity = parseInt(data.quantity);

    try {
        await fetchAPI(`${API_BASE}/inventory/items/${itemId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        closeModal();
        loadInventoryItems();
        alert('Inventory item updated successfully!');
    } catch (error) {
        console.error('Error updating inventory item:', error);
        alert('Failed to update: ' + error.message);
    }
}

function showAddSupplierModal() {
    const content = `
        <h2>Add Supplier</h2>
        <form onsubmit="addSupplier(event)">
            <div class="form-group">
                <label>Name</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>Contact Info</label>
                <input type="text" name="contact_info">
            </div>
            <div class="form-group">
                <label>Address</label>
                <input type="text" name="address">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    `;
    showModal(content);
}

function showAddPurchaseOrderModal() {
    const content = `
        <h2>Create Purchase Order</h2>
        <form onsubmit="addPurchaseOrder(event)">
            <div class="form-group">
                <label>Order Date</label>
                <input type="date" name="order_date" required>
            </div>
            <div class="form-group">
                <label>Supplier ID</label>
                <input type="number" name="supplier_id" required>
            </div>
            <div class="form-group">
                <label>Total Amount</label>
                <input type="number" step="0.01" name="total_amount" required>
            </div>
            <div class="form-group">
                <label>Status</label>
                <select name="status">
                    <option value="Pending">Pending</option>
                    <option value="Completed">Completed</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    `;
    showModal(content);
}

function showAddStaffModal() {
    const content = `
        <h2>Add Staff</h2>
        <form onsubmit="addStaff(event)">
            <div class="form-group">
                <label>Name</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>Role</label>
                <input type="text" name="role">
            </div>
            <div class="form-group">
                <label>Contact Info</label>
                <input type="text" name="contact_info">
            </div>
            <div class="form-group">
                <label>Status</label>
                <select name="status">
                    <option value="Active">Active</option>
                    <option value="Inactive">Inactive</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    `;
    showModal(content);
}

// Form submission handlers
async function addFinancialRecord(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    try {
        const result = await fetchAPI(`${API_BASE}/financial/records`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        closeModal();
        loadFinancialRecords();
        alert('Financial record added successfully!');
    } catch (error) {
        console.error('Error adding financial record:', error);
        alert('Failed to add: ' + error.message);
    }
}

async function addDonation(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    data.donor_id = parseInt(data.donor_id);
    data.amount = parseFloat(data.amount);

    try {
        await fetchAPI(`${API_BASE}/donation/donations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        closeModal();
        loadDonations();
        alert('Donation added successfully!');
    } catch (error) {
        console.error('Error adding donation:', error);
        alert('Failed to add: ' + error.message);
    }
}

async function addDonor(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    if (data.age) data.age = parseInt(data.age);

    try {
        await fetchAPI(`${API_BASE}/donation/donors`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        closeModal();
        loadDonors();
        alert('Donor added successfully!');
    } catch (error) {
        console.error('Error adding donor:', error);
        alert('Failed to add: ' + error.message);
    }
}

async function addInventoryItem(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    data.quantity = parseInt(data.quantity);

    try {
        await fetchAPI(`${API_BASE}/inventory/items`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        closeModal();
        loadInventoryItems();
        alert('Inventory item added successfully!');
    } catch (error) {
        console.error('Error adding inventory item:', error);
        alert('Failed to add: ' + error.message);
    }
}

async function addSupplier(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    try {
        await fetchAPI(`${API_BASE}/inventory/suppliers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        closeModal();
        loadSuppliers();
        alert('Supplier added successfully!');
    } catch (error) {
        console.error('Error adding supplier:', error);
        alert('Failed to add: ' + error.message);
    }
}

async function addPurchaseOrder(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    data.supplier_id = parseInt(data.supplier_id);
    data.total_amount = parseFloat(data.total_amount);
    data.items = [];

    try {
        await fetchAPI(`${API_BASE}/inventory/purchase-orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        closeModal();
        loadPurchaseOrders();
        alert('Purchase order created successfully!');
    } catch (error) {
        console.error('Error adding purchase order:', error);
        alert('Failed to add: ' + error.message);
    }
}

async function addStaff(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    try {
        await fetchAPI(`${API_BASE}/staff/staff`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        closeModal();
        loadStaff();
        alert('Staff added successfully!');
    } catch (error) {
        console.error('Error adding staff:', error);
        alert('Failed to add: ' + error.message);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});