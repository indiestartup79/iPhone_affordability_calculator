# 📱 iPhone Affordability Calculator & Apple Studio Showcase

A modern, responsive web application built with **Python Flask** (RESTful JSON APIs) and **Vanilla JavaScript / HTML5 / CSS3** (Frontend). 

This project showcases the complete lineup of official Apple iPhone models—sourced directly from [Apple Support Article 108044](https://support.apple.com/en-in/108044)—and features a **Smart Financial Affordability Advisor** that helps buyers determine which iPhone model they can comfortably afford without financial strain.

---

## ✨ Features

- 🍎 **Complete Official Apple Catalog**: Sourced directly from Apple Support Article 108044 (iPhone 17 series, iPhone Air, iPhone 16 series, 15 series, 14 series, 13 series, and iPhone SE).
- 🖼️ **Official Apple Store CDN Renders**: 100% authentic product imagery served directly from `store.storeimages.cdn-apple.com`.
- 💰 **Smart Financial Affordability Advisor**:
  - **1-Click Salary Presets**: Test `₹50k`, `₹1 Lakh`, and `₹2 Lakh` monthly income scenarios instantly.
  - **Safe 10% EMI Limit Metric**: Calculates maximum monthly EMI threshold (10% of net monthly income).
  - **Color-Coded Status Tiers**:
    - 🟢 **Zero Financial Burden**: Cash purchase or monthly EMI $\le$ 7% of income.
    - 🟡 **Moderate Stretch**: Monthly EMI between 7% and 15% of income.
    - 🔴 **High Financial Burden**: Monthly EMI > 15% of income (not recommended).
- 🔍 **Dynamic Filtering & Sorting**: Filter by generation/series, search by model/chipset, and sort by Price or Battery capacity (mAh).
- 📊 **Spec Matrix Comparison**: Side-by-side spec viewer (RAM, Storage, Battery, Display, Chipset).
- 🎨 **Apple Metallic Dark Design**: Glassmorphism navigation bar, responsive flex/grid layouts, and dark/light theme toggle.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, Flask (RESTful JSON APIs)
- **Frontend**: Vanilla JavaScript (ES6+ Fetch API), HTML5, CSS3 (Flexbox & CSS Grid)
- **Data File**: `Apple_phones.txt` (Structured text document containing specs, pricing, and model details)

---

## 📁 Project Structure

```text
Test_News/
├── app.py                  # Main Flask application & REST API routes
├── Apple_phones.txt        # Structured text file with official Apple phone specs & prices
├── requirements.txt        # Python dependencies (flask)
├── .gitignore              # Git ignore configuration
├── README.md               # Project documentation
├── templates/
│   └── index.html          # HTML5 single-page application template
└── static/
    ├── css/
    │   └── styles.css      # Apple-inspired CSS stylesheet & responsive styles
    └── js/
        └── app.js          # Vanilla JS frontend application logic & REST API client
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.8 or higher installed on your system.

### 1. Clone the repository
```bash
git clone https://github.com/indiestartup79/iPhone_affordability_calculator.git
cd iPhone_affordability_calculator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python3 app.py
```

### 4. Open in browser
Navigate to **`http://127.0.0.1:5050`** in your web browser.

> **Custom Port Note**: You can specify a custom port by setting the `PORT` environment variable:
> ```bash
> PORT=8080 python3 app.py
> ```

---

## 📡 RESTful JSON APIs

### 1. `GET /api/phones`
Returns the complete dataset of official Apple iPhone models with pricing, specifications, and image URLs.

**Sample Response**:
```json
{
  "status": "success",
  "count": 23,
  "data": [
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
      "badge": "Desert Titanium",
      "image": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-finish-select-202409-6-9inch-deserttitanium?wid=1000&hei=1000&fmt=jpeg&qlt=95"
    }
  ]
}
```

### 2. `POST /api/affordability`
Calculates affordability tiers for all models based on user input.

**Request Payload**:
```json
{
  "monthly_salary": 75000,
  "cash_available": 40000,
  "emi_tenure_months": 12
}
```

**Sample Response**:
```json
{
  "status": "success",
  "inputs": {
    "monthly_salary": 75000,
    "cash_available": 40000,
    "emi_tenure_months": 12
  },
  "summary": {
    "total_models": 23,
    "zero_burden_count": 8,
    "moderate_burden_count": 6,
    "high_burden_count": 9,
    "top_recommended_model": "iPhone 16"
  },
  "models": [...]
}
```

---

## 🧮 Financial Methodology & Rules Used

The financial calculations adhere to standard financial planning principles:

1. **50/30/20 Rule**: Discretionary luxury purchases (like smartphones) belong to the 30% "Wants" category and should never drain emergency savings or essential funds.
2. **10% Income EMI Threshold**: Total monthly phone EMI should not exceed **10% to 15% of net monthly income**.
3. **1.5x Income Rule**: Total smartphone cost should not exceed **1.5x your monthly net income**.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
