/**
 * Apple iPhone Studio & Financial Affordability Advisor
 * Vanilla JavaScript Frontend Application (2026 Edition)
 */

let phonesData = [];
let calculatedModels = [];
let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupThemeToggle();
});

/**
 * Initialize application data by fetching phones list from REST API
 */
async function initApp() {
    const phoneGrid = document.getElementById('phoneGrid');
    try {
        const response = await fetch('/api/phones');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const resData = await response.json();
        if (resData.status === 'success') {
            phonesData = resData.data;
            renderShowcase(phonesData);
            populateCompareTable(phonesData);
        } else {
            phoneGrid.innerHTML = `<p class="error-msg">Failed to load phone models.</p>`;
        }
    } catch (err) {
        console.error('Error fetching phone dataset:', err);
        phoneGrid.innerHTML = `
            <div class="loading-spinner">
                <i class="fa-solid fa-triangle-exclamation" style="color: var(--color-danger)"></i>
                <p>Unable to connect to server. Please ensure Python Flask server is running.</p>
            </div>`;
    }
}

/**
 * Render the iPhone Showcase Cards
 */
function renderShowcase(phones) {
    const phoneGrid = document.getElementById('phoneGrid');
    if (!phones || phones.length === 0) {
        phoneGrid.innerHTML = `<div class="loading-spinner"><p>No iPhone models found matching your criteria.</p></div>`;
        return;
    }

    phoneGrid.innerHTML = phones.map(phone => {
        const isGold = phone.rank <= 3; // Flagship gold highlight for iPhone Duo & 18 Pro
        return `
        <div class="phone-card ${isGold ? 'gold-flagship' : ''}">
            <span class="card-badge">${phone.badge || phone.generation}</span>
            <div class="phone-img-wrapper">
                <img src="${phone.image}" alt="${phone.model}" class="phone-img" loading="lazy">
            </div>
            <div class="phone-info-block">
                <h3 class="phone-model">${phone.model}</h3>
                <div class="phone-gen">
                    <i class="fa-solid fa-microchip"></i> ${phone.chipset} &bull; ${phone.generation}
                </div>
                <div class="phone-price-tag">${phone.formatted_price}</div>
                
                <div class="spec-pills">
                    <span class="pill" title="RAM Capacity"><i class="fa-solid fa-memory"></i> ${phone.ram}</span>
                    <span class="pill" title="Battery Capacity"><i class="fa-solid fa-battery-full"></i> ${phone.battery}</span>
                    <span class="pill" title="Display Specs"><i class="fa-solid fa-mobile-screen-button"></i> ${phone.display}</span>
                    <span class="pill" title="Storage Options"><i class="fa-solid fa-hard-drive"></i> ${phone.storage}</span>
                </div>
            </div>
            <div class="card-actions">
                <button class="btn-card" onclick="scrollToCalculator('${phone.model}')">
                    <i class="fa-solid fa-calculator"></i> Check Affordability
                </button>
            </div>
        </div>
        `;
    }).join('');
}

/**
 * Filter & Sort Phone Showcase
 */
function filterShowcase() {
    const searchVal = document.getElementById('searchInput').value.toLowerCase().trim();
    const genVal = document.getElementById('genFilter').value;
    const sortVal = document.getElementById('sortSelect').value;

    let filtered = phonesData.filter(p => {
        const matchesSearch = p.model.toLowerCase().includes(searchVal) || 
                              p.chipset.toLowerCase().includes(searchVal) ||
                              p.generation.toLowerCase().includes(searchVal);
        
        let matchesGen = true;
        if (genVal !== 'all') {
            if (genVal === '17') {
                matchesGen = p.model.toLowerCase().includes('17') || p.model.toLowerCase().includes('air');
            } else if (genVal === '16') {
                matchesGen = p.model.toLowerCase().includes('16');
            } else if (genVal === '15') {
                matchesGen = p.model.toLowerCase().includes('15');
            } else if (genVal === '14') {
                matchesGen = p.model.toLowerCase().includes('14');
            } else if (genVal === '13') {
                matchesGen = p.model.toLowerCase().includes('13') || p.model.toLowerCase().includes('se');
            }
        }

        return matchesSearch && matchesGen;
    });

    if (sortVal === 'price-desc') {
        filtered.sort((a, b) => b.price - a.price);
    } else if (sortVal === 'price-asc') {
        filtered.sort((a, b) => a.price - b.price);
    } else if (sortVal === 'battery') {
        filtered.sort((a, b) => {
            const batA = parseInt(a.battery.replace(/[^0-9]/g, '')) || 0;
            const batB = parseInt(b.battery.replace(/[^0-9]/g, '')) || 0;
            return batB - batA;
        });
    } else {
        filtered.sort((a, b) => a.rank - b.rank);
    }

    renderShowcase(filtered);
}

/**
 * Quick Preset salary & cash application
 */
function applyPreset(salary, cash) {
    document.getElementById('salaryInput').value = salary;
    document.getElementById('cashInput').value = cash;
    document.getElementById('affordabilityForm').dispatchEvent(new Event('submit'));
}

/**
 * Set EMI Tenure Button State
 */
function setTenure(months) {
    document.getElementById('tenureInput').value = months;
    document.querySelectorAll('.tenure-btn').forEach(btn => {
        if (parseInt(btn.getAttribute('data-months')) === months) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

function scrollToCalculator(modelName) {
    const calcSec = document.getElementById('calculator');
    calcSec.scrollIntoView({ behavior: 'smooth' });
}

async function calculateAffordability(event) {
    event.preventDefault();
    
    const salary = parseFloat(document.getElementById('salaryInput').value) || 0;
    const cash = parseFloat(document.getElementById('cashInput').value) || 0;
    const tenure = parseInt(document.getElementById('tenureInput').value) || 12;

    const payload = {
        monthly_salary: salary,
        cash_available: cash,
        emi_tenure_months: tenure
    };

    try {
        const response = await fetch('/api/affordability', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const result = await response.json();

        if (result.status === 'success') {
            displayCalculatorResults(result);
        }
    } catch (err) {
        console.error('Error calculating affordability:', err);
        alert('Could not perform financial calculation. Please check your inputs.');
    }
}

function displayCalculatorResults(data) {
    const resultsContainer = document.getElementById('calculatorResults');
    resultsContainer.classList.remove('hidden');

    const safeLimit = Math.round(data.inputs.monthly_salary * 0.10);

    document.getElementById('resIncome').innerText = `₹${data.inputs.monthly_salary.toLocaleString('en-IN')}`;
    document.getElementById('resCash').innerText = `₹${data.inputs.cash_available.toLocaleString('en-IN')}`;
    document.getElementById('resSafeEmiLimit').innerText = `₹${safeLimit.toLocaleString('en-IN')}/mo`;

    document.getElementById('countAll').innerText = data.summary.total_models;
    document.getElementById('countSafe').innerText = data.summary.zero_burden_count;
    document.getElementById('countModerate').innerText = data.summary.moderate_burden_count;
    document.getElementById('countHigh').innerText = data.summary.high_burden_count;

    calculatedModels = data.models;
    currentFilter = 'all';
    
    document.querySelectorAll('.tab-btn').forEach((btn, idx) => {
        btn.classList.toggle('active', idx === 0);
    });

    renderAffordabilityGrid(calculatedModels);
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

function filterResults(category) {
    currentFilter = category;
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    event.currentTarget.classList.add('active');

    let filtered = calculatedModels;
    if (category === 'SAFE') {
        filtered = calculatedModels.filter(m => m.status_code === 'SAFE_CASH' || m.status_code === 'SAFE_EMI');
    } else if (category === 'MODERATE') {
        filtered = calculatedModels.filter(m => m.status_code === 'MODERATE_EMI');
    } else if (category === 'HIGH') {
        filtered = calculatedModels.filter(m => m.status_code === 'HIGH_BURDEN');
    }

    renderAffordabilityGrid(filtered);
}

function renderAffordabilityGrid(models) {
    const grid = document.getElementById('affordabilityGrid');

    if (!models || models.length === 0) {
        grid.innerHTML = `<div class="loading-spinner"><p>No iPhone models found in this affordability tier.</p></div>`;
        return;
    }

    grid.innerHTML = models.map(m => {
        let borderClass = 'border-success';
        if (m.badge_color === 'warning') borderClass = 'border-warning';
        if (m.badge_color === 'danger') borderClass = 'border-danger';

        return `
            <div class="afford-card ${borderClass}">
                <div>
                    <div class="afford-header">
                        <h3 class="afford-model">${m.model}</h3>
                        <span class="afford-price">${m.formatted_price}</span>
                    </div>
                    <span class="tier-badge ${m.badge_color}">
                        <i class="fa-solid ${m.badge_color === 'danger' ? 'fa-triangle-exclamation' : 'fa-circle-check'}"></i> ${m.tier}
                    </span>

                    <div class="afford-metrics">
                        <div class="metric-item">
                            <span class="metric-label">Monthly EMI</span>
                            <span class="metric-val" style="color: ${m.badge_color === 'danger' ? 'var(--color-danger)' : 'var(--text-primary)'}">
                                ${m.can_buy_in_cash ? '₹0 (In Cash)' : m.formatted_emi}
                            </span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-label">% of Income</span>
                            <span class="metric-val" style="color: ${m.badge_color === 'danger' ? 'var(--color-danger)' : 'var(--accent-blue)'}">
                                ${m.can_buy_in_cash ? '0%' : m.emi_salary_ratio + '%'}
                            </span>
                        </div>
                    </div>

                    <div class="afford-note">
                        <i class="fa-solid fa-lightbulb" style="color: var(--accent-blue)"></i> ${m.financial_note}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function populateCompareTable(phones) {
    const tbody = document.getElementById('compareTableBody');
    tbody.innerHTML = phones.map(p => `
        <tr>
            <td><strong>${p.model}</strong></td>
            <td><strong style="color: var(--accent-blue)">${p.formatted_price}</strong></td>
            <td>${p.ram}</td>
            <td>${p.storage}</td>
            <td>${p.battery}</td>
            <td>${p.chipset}</td>
            <td>${p.display}</td>
        </tr>
    `).join('');
}

function openCompareModal() {
    document.getElementById('compareModal').classList.add('open');
}

function closeCompareModal() {
    document.getElementById('compareModal').classList.remove('open');
}

function setupThemeToggle() {
    const btn = document.getElementById('themeToggleBtn');
    btn.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        btn.innerHTML = isLight ? `<i class="fa-solid fa-sun"></i>` : `<i class="fa-solid fa-moon"></i>`;
    });
}
