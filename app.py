import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static')

# Public CDN Image base domains
CDN_BASE = "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/"
CDN_BASE_ALT = "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/"

# iPhone Dataset (Derived from public technical documentation support 108044)
IPHONE_DATASET = [
    {
        "id": "iphone-17-pro-max",
        "model": "iPhone 17 Pro Max",
        "price": 144900,
        "formatted_price": "₹1,44,900",
        "ram": "12 GB",
        "storage": "256GB / 512GB / 1TB / 2TB",
        "battery": "4,832 mAh",
        "chipset": "A19 Pro",
        "display": "6.9-inch Super Retina XDR",
        "generation": "17 Series (2025)",
        "rank": 1,
        "badge": "Cosmic Orange / Deep Blue",
        "image": CDN_BASE + "iphone-16-pro-finish-select-202409-6-9inch-blacktitanium?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Aluminium unibody design, A19 Pro chip, Fusion Ultra Wide, Fusion Main and Fusion Telephoto camera plateau."
    },
    {
        "id": "iphone-17-pro",
        "model": "iPhone 17 Pro",
        "price": 129900,
        "formatted_price": "₹1,29,900",
        "ram": "12 GB",
        "storage": "256GB / 512GB / 1TB",
        "battery": "3,750 mAh",
        "chipset": "A19 Pro",
        "display": "6.3-inch Super Retina XDR",
        "generation": "17 Series (2025)",
        "rank": 2,
        "badge": "Silver Titanium",
        "image": CDN_BASE + "iphone-16-pro-finish-select-202409-6-3inch-whitetitanium?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Aluminium unibody design, Dynamic Island, A19 Pro chip, and triple camera system."
    },
    {
        "id": "iphone-air",
        "model": "iPhone Air",
        "price": 149900,
        "formatted_price": "₹1,49,900",
        "ram": "12 GB",
        "storage": "256GB / 512GB / 1TB",
        "battery": "3,950 mAh",
        "chipset": "A19 Pro",
        "display": "6.5-inch Super Retina XDR (5.6mm)",
        "generation": "17 Series (2025)",
        "rank": 3,
        "badge": "5.6mm Ultra Slim",
        "image": CDN_BASE + "iphone-16-finish-select-202409-6-7inch-teal?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Apple's ultra-slim iPhone Air with 5.6mm thickness, titanium band, and A19 Pro chip."
    },
    {
        "id": "iphone-17",
        "model": "iPhone 17",
        "price": 99900,
        "formatted_price": "₹99,900",
        "ram": "8 GB",
        "storage": "256GB / 512GB",
        "battery": "3,650 mAh",
        "chipset": "A19",
        "display": "6.3-inch ProMotion 120Hz",
        "generation": "17 Series (2025)",
        "rank": 4,
        "badge": "Mist Blue / Sage",
        "image": CDN_BASE + "iphone-16-finish-select-202409-6-1inch-ultramarine?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "120Hz ProMotion display, A19 chip, vertical dual camera system, and Ceramic Shield."
    },
    {
        "id": "iphone-17e",
        "model": "iPhone 17e",
        "price": 79900,
        "formatted_price": "₹79,900",
        "ram": "8 GB",
        "storage": "256GB / 512GB",
        "battery": "3,450 mAh",
        "chipset": "A19",
        "display": "6.1-inch Super Retina XDR",
        "generation": "17 Series (2026)",
        "rank": 5,
        "badge": "Soft Pink",
        "image": CDN_BASE + "iphone-16-finish-select-202409-6-1inch-pink?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "6.1-inch OLED screen, anodised aluminium band, Action button, USB-C, and A19 chip."
    },
    {
        "id": "iphone-16-pro-max",
        "model": "iPhone 16 Pro Max",
        "price": 134900,
        "formatted_price": "₹1,34,900",
        "ram": "8 GB",
        "storage": "256GB / 512GB / 1TB",
        "battery": "4,685 mAh",
        "chipset": "A18 Pro",
        "display": "6.9-inch Super Retina XDR",
        "generation": "16 Series (2024)",
        "rank": 6,
        "badge": "Desert Titanium",
        "image": CDN_BASE + "iphone-16-pro-finish-select-202409-6-9inch-deserttitanium?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Grade 5 Titanium, A18 Pro chip, 4K 120fps Dolby Vision, and Camera Control button."
    },
    {
        "id": "iphone-16-pro",
        "model": "iPhone 16 Pro",
        "price": 119900,
        "formatted_price": "₹1,19,900",
        "ram": "8 GB",
        "storage": "128GB / 256GB / 512GB / 1TB",
        "battery": "3,582 mAh",
        "chipset": "A18 Pro",
        "display": "6.3-inch Super Retina XDR",
        "generation": "16 Series (2024)",
        "rank": 7,
        "badge": "Natural Titanium",
        "image": CDN_BASE + "iphone-16-pro-finish-select-202409-6-3inch-naturaltitanium?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Pro features in 6.3-inch size. Includes A18 Pro, 48MP Fusion camera system, and Camera Control."
    },
    {
        "id": "iphone-16-plus",
        "model": "iPhone 16 Plus",
        "price": 89900,
        "formatted_price": "₹89,900",
        "ram": "8 GB",
        "storage": "128GB / 256GB / 512GB",
        "battery": "4,674 mAh",
        "chipset": "A18",
        "display": "6.7-inch Super Retina XDR",
        "generation": "16 Series (2024)",
        "rank": 8,
        "badge": "Teal Finish",
        "image": CDN_BASE + "iphone-16-finish-select-202409-6-7inch-teal?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Big screen and long battery life with A18 chip, Action button, and Camera Control."
    },
    {
        "id": "iphone-16",
        "model": "iPhone 16",
        "price": 79900,
        "formatted_price": "₹79,900",
        "ram": "8 GB",
        "storage": "128GB / 256GB / 512GB",
        "battery": "3,561 mAh",
        "chipset": "A18",
        "display": "6.1-inch Super Retina XDR",
        "generation": "16 Series (2024)",
        "rank": 9,
        "badge": "Ultramarine",
        "image": CDN_BASE + "iphone-16-finish-select-202409-6-1inch-ultramarine?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "A18 chip, 8GB RAM, Apple Intelligence, and 48MP 2-in-1 Fusion camera system."
    },
    {
        "id": "iphone-16e",
        "model": "iPhone 16e",
        "price": 59900,
        "formatted_price": "₹59,900",
        "ram": "8 GB",
        "storage": "128GB / 256GB / 512GB",
        "battery": "3,400 mAh",
        "chipset": "A18",
        "display": "6.1-inch Super Retina XDR",
        "generation": "16 Series (2025)",
        "rank": 10,
        "badge": "Essential 16",
        "image": CDN_BASE + "iphone-16-finish-select-202409-6-1inch-teal?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "6.1-inch OLED, Action button, A18 chip, and USB-C connectivity."
    },
    {
        "id": "iphone-15-pro-max",
        "model": "iPhone 15 Pro Max",
        "price": 159900,
        "formatted_price": "₹1,59,900",
        "ram": "8 GB",
        "storage": "256GB / 512GB / 1TB",
        "battery": "4,441 mAh",
        "chipset": "A17 Pro",
        "display": "6.7-inch Super Retina XDR",
        "generation": "15 Series (2023)",
        "rank": 11,
        "badge": "Natural Titanium",
        "image": CDN_BASE + "iphone-15-pro-finish-select-202309-6-7inch-naturaltitanium?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Titanium design with A17 Pro chip, Action button, and 5x optical Telephoto camera."
    },
    {
        "id": "iphone-15-pro",
        "model": "iPhone 15 Pro",
        "price": 134900,
        "formatted_price": "₹1,34,900",
        "ram": "8 GB",
        "storage": "128GB / 256GB / 512GB / 1TB",
        "battery": "3,274 mAh",
        "chipset": "A17 Pro",
        "display": "6.1-inch Super Retina XDR",
        "generation": "15 Series (2023)",
        "rank": 12,
        "badge": "Blue Titanium",
        "image": CDN_BASE + "iphone-15-pro-finish-select-202309-6-1inch-bluetitanium?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Lightweight titanium chassis, USB 3 transfer speeds, and console-level A17 Pro gaming."
    },
    {
        "id": "iphone-15-plus",
        "model": "iPhone 15 Plus",
        "price": 73999,
        "formatted_price": "₹73,999",
        "ram": "6 GB",
        "storage": "128GB / 256GB / 512GB",
        "battery": "4,383 mAh",
        "chipset": "A16 Bionic",
        "display": "6.7-inch Super Retina XDR",
        "generation": "15 Series (2023)",
        "rank": 13,
        "badge": "Pink Finish",
        "image": CDN_BASE + "iphone-15-finish-select-202309-6-7inch-pink?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Dynamic Island, 48MP camera, USB-C, and all-day battery life."
    },
    {
        "id": "iphone-15",
        "model": "iPhone 15",
        "price": 55400,
        "formatted_price": "₹55,400",
        "ram": "6 GB",
        "storage": "128GB / 256GB / 512GB",
        "battery": "3,349 mAh",
        "chipset": "A16 Bionic",
        "display": "6.1-inch Super Retina XDR",
        "generation": "15 Series (2023)",
        "rank": 14,
        "badge": "Blue Finish",
        "image": CDN_BASE + "iphone-15-finish-select-202309-6-1inch-blue?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Dynamic Island, 48MP Main camera with 2x Telephoto, color-infused back glass, and USB-C."
    },
    {
        "id": "iphone-14-pro-max",
        "model": "iPhone 14 Pro Max",
        "price": 139900,
        "formatted_price": "₹1,39,900",
        "ram": "6 GB",
        "storage": "128GB / 256GB / 512GB / 1TB",
        "battery": "4,323 mAh",
        "chipset": "A16 Bionic",
        "display": "6.7-inch Super Retina XDR",
        "generation": "14 Series (2022)",
        "rank": 15,
        "badge": "Deep Purple",
        "image": CDN_BASE_ALT + "iphone-14-pro-finish-select-202209-6-7inch-deeppurple?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "First Dynamic Island iPhone, 48MP camera, stainless steel frame, and A16 Bionic."
    },
    {
        "id": "iphone-14-pro",
        "model": "iPhone 14 Pro",
        "price": 129900,
        "formatted_price": "₹1,29,900",
        "ram": "6 GB",
        "storage": "128GB / 256GB / 512GB / 1TB",
        "battery": "3,200 mAh",
        "chipset": "A16 Bionic",
        "display": "6.1-inch Super Retina XDR",
        "generation": "14 Series (2022)",
        "rank": 16,
        "badge": "Gold Finish",
        "image": CDN_BASE_ALT + "iphone-14-pro-finish-select-202209-6-1inch-gold?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Dynamic Island, Always-On display, 48MP Pro camera system, and Crash Detection."
    },
    {
        "id": "iphone-14-plus",
        "model": "iPhone 14 Plus",
        "price": 66999,
        "formatted_price": "₹66,999",
        "ram": "6 GB",
        "storage": "128GB / 256GB / 512GB",
        "battery": "4,325 mAh",
        "chipset": "A15 Bionic",
        "display": "6.7-inch Super Retina XDR",
        "generation": "14 Series (2022)",
        "rank": 17,
        "badge": "Purple Finish",
        "image": CDN_BASE + "iphone-14-finish-select-202209-6-7inch-purple?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Large display, long battery life, Photonic Engine, and dual-camera system."
    },
    {
        "id": "iphone-14",
        "model": "iPhone 14",
        "price": 57900,
        "formatted_price": "₹57,900",
        "ram": "6 GB",
        "storage": "128GB / 256GB / 512GB",
        "battery": "3,279 mAh",
        "chipset": "A15 Bionic",
        "display": "6.1-inch Super Retina XDR",
        "generation": "14 Series (2022)",
        "rank": 18,
        "badge": "Blue Finish",
        "image": CDN_BASE + "iphone-14-finish-select-202209-6-1inch-blue?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "A15 Bionic 5-core GPU, Action mode video stabilization, and emergency SOS via satellite."
    },
    {
        "id": "iphone-13-pro-max",
        "model": "iPhone 13 Pro Max",
        "price": 119900,
        "formatted_price": "₹1,19,900",
        "ram": "6 GB",
        "storage": "128GB / 256GB / 512GB / 1TB",
        "battery": "4,352 mAh",
        "chipset": "A15 Bionic",
        "display": "6.7-inch Super Retina XDR",
        "generation": "13 Series (2021)",
        "rank": 19,
        "badge": "Silver Finish",
        "image": CDN_BASE_ALT + "iphone-13-pro-max-silver-select?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "ProMotion 120Hz display, Cinematic mode, 3x optical zoom, and stainless steel band."
    },
    {
        "id": "iphone-13-pro",
        "model": "iPhone 13 Pro",
        "price": 109900,
        "formatted_price": "₹1,09,900",
        "ram": "6 GB",
        "storage": "128GB / 256GB / 512GB / 1TB",
        "battery": "3,095 mAh",
        "chipset": "A15 Bionic",
        "display": "6.1-inch Super Retina XDR",
        "generation": "13 Series (2021)",
        "rank": 20,
        "badge": "ProMotion 120Hz",
        "image": CDN_BASE_ALT + "iphone-13-pro-family-hero?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Super Retina XDR with ProMotion, macro photography, and Cinematic mode."
    },
    {
        "id": "iphone-13",
        "model": "iPhone 13",
        "price": 39994,
        "formatted_price": "₹39,994",
        "ram": "4 GB",
        "storage": "128GB / 256GB / 512GB",
        "battery": "3,227 mAh",
        "chipset": "A15 Bionic",
        "display": "6.1-inch Super Retina XDR",
        "generation": "13 Series (2021)",
        "rank": 21,
        "badge": "Pink Finish",
        "image": CDN_BASE + "iphone-13-finish-select-202207-pink?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Cinematic mode, A15 Bionic, 128GB base storage, and legendary battery reliability."
    },
    {
        "id": "iphone-13-mini",
        "model": "iPhone 13 mini",
        "price": 49900,
        "formatted_price": "₹49,900",
        "ram": "4 GB",
        "storage": "128GB / 256GB / 512GB",
        "battery": "2,406 mAh",
        "chipset": "A15 Bionic",
        "display": "5.4-inch Super Retina XDR",
        "generation": "13 Series (2021)",
        "rank": 22,
        "badge": "Compact 5.4-inch",
        "image": CDN_BASE_ALT + "iphone-13-mini-pink-select-2021?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Ultra-compact 5.4-inch display, Cinematic mode, dual 12MP cameras, and A15 Bionic."
    },
    {
        "id": "iphone-se-3rd-gen",
        "model": "iPhone SE (3rd generation)",
        "price": 45990,
        "formatted_price": "₹45,990",
        "ram": "4 GB",
        "storage": "64GB / 128GB / 256GB",
        "battery": "2,018 mAh",
        "chipset": "A15 Bionic",
        "display": "4.7-inch Retina HD",
        "generation": "Compact SE (2022)",
        "rank": 23,
        "badge": "Starlight",
        "image": CDN_BASE_ALT + "iphone-se-starlight-select-202203?wid=1000&hei=1000&fmt=jpeg&qlt=95",
        "description": "Classic Touch ID design with A15 Bionic speed, 5G connectivity, and compact pocketable build."
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/phones', methods=['GET'])
def get_phones():
    """Return list of all iPhone models with specs and market prices."""
    return jsonify({
        "status": "success",
        "count": len(IPHONE_DATASET),
        "data": IPHONE_DATASET
    })

@app.route('/api/affordability', methods=['POST'])
def calculate_affordability():
    """
    Calculate phone affordability based on financial guidelines:
    - Monthly Salary
    - Available Cash Savings
    - Preferred EMI Tenure (months)
    """
    payload = request.get_json() or {}
    try:
        monthly_salary = float(payload.get('monthly_salary', 0))
        cash_available = float(payload.get('cash_available', 0))
        emi_tenure_months = int(payload.get('emi_tenure_months', 12))
        if emi_tenure_months <= 0:
            emi_tenure_months = 12
    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "message": "Invalid numeric input values for salary or cash."
        }), 400

    if monthly_salary <= 0:
        return jsonify({
            "status": "error",
            "message": "Monthly salary must be greater than zero."
        }), 400

    analyzed_models = []
    
    for phone in IPHONE_DATASET:
        price = phone['price']
        
        # Scenario A: Full Cash Purchase
        can_buy_in_cash = cash_available >= price
        salary_multiplier = price / monthly_salary
        
        # Scenario B: EMI Purchase
        usable_downpayment = min(cash_available * 0.5, price * 0.3)
        financed_amount = max(0.0, price - usable_downpayment)
        
        monthly_emi = financed_amount / emi_tenure_months
        emi_salary_ratio = (monthly_emi / monthly_salary) * 100.0

        if can_buy_in_cash and salary_multiplier <= 1.5:
            tier = "Zero Burden (Highly Recommended)"
            status_code = "SAFE_CASH"
            badge_color = "success"
            financial_note = f"You can easily buy this phone in cash using existing savings! It costs {salary_multiplier:.1f}x of your monthly salary."
        elif emi_salary_ratio <= 7.0:
            tier = "Zero Burden (Comfortable EMI)"
            status_code = "SAFE_EMI"
            badge_color = "success"
            financial_note = f"Monthly EMI of ₹{monthly_emi:,.0f} is only {emi_salary_ratio:.1f}% of your monthly income (well below safe 10% threshold)."
        elif emi_salary_ratio <= 15.0:
            tier = "Moderate Burden (Manageable EMI)"
            status_code = "MODERATE_EMI"
            badge_color = "warning"
            financial_note = f"Monthly EMI of ₹{monthly_emi:,.0f} takes {emi_salary_ratio:.1f}% of your monthly salary. Keep tenure short."
        else:
            tier = "High Financial Strain (Not Recommended)"
            status_code = "HIGH_BURDEN"
            badge_color = "danger"
            financial_note = f"Monthly EMI of ₹{monthly_emi:,.0f} exceeds {emi_salary_ratio:.1f}% of your salary. Buying this model may stretch your monthly budget."

        analyzed_models.append({
            **phone,
            "can_buy_in_cash": can_buy_in_cash,
            "monthly_emi": round(monthly_emi),
            "formatted_emi": f"₹{round(monthly_emi):,}/mo",
            "down_payment": round(usable_downpayment),
            "formatted_down_payment": f"₹{round(usable_downpayment):,}",
            "emi_salary_ratio": round(emi_salary_ratio, 1),
            "salary_multiplier": round(salary_multiplier, 2),
            "tier": tier,
            "status_code": status_code,
            "badge_color": badge_color,
            "financial_note": financial_note
        })

    safe_models = [p for p in analyzed_models if p['status_code'] in ['SAFE_CASH', 'SAFE_EMI']]
    moderate_models = [p for p in analyzed_models if p['status_code'] == 'MODERATE_EMI']
    high_burden_models = [p for p in analyzed_models if p['status_code'] == 'HIGH_BURDEN']

    top_recommendation = safe_models[0] if safe_models else (moderate_models[0] if moderate_models else None)

    return jsonify({
        "status": "success",
        "inputs": {
            "monthly_salary": monthly_salary,
            "cash_available": cash_available,
            "emi_tenure_months": emi_tenure_months
        },
        "summary": {
            "total_models": len(analyzed_models),
            "zero_burden_count": len(safe_models),
            "moderate_burden_count": len(moderate_models),
            "high_burden_count": len(high_burden_models),
            "top_recommended_model": top_recommendation['model'] if top_recommendation else "None"
        },
        "models": analyzed_models
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f"Starting server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
