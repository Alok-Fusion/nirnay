"""
NIRNAY — Data Generation Configuration
=======================================
All reference data, constants, and distribution parameters for synthetic
Indian banking data generation. This is the single source of truth for
every generator module.

Author: NIRNAY Data Engineering Team
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# REPRODUCIBILITY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEED = 42

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VOLUME CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NUM_CUSTOMERS = 1000
NUM_MERCHANTS = 500
NUM_TRANSACTIONS = 50000
NUM_SCAM_PATTERNS = 200
RECIPIENTS_PER_CUSTOMER = (3, 12)  # (min, max)
SUSPICIOUS_RATIO = 0.05            # 5% of transactions flagged

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATE RANGES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATA_START_DATE = "2025-01-01"
DATA_END_DATE = "2026-06-30"
CUSTOMER_SINCE_START = "2016-01-01"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INDIAN NAMES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MALE_FIRST_NAMES = [
    "Aarav", "Abhishek", "Aditya", "Ajay", "Akash", "Amit", "Anand", "Anil",
    "Ankit", "Arjun", "Ashish", "Deepak", "Dev", "Dhruv", "Gaurav", "Harsh",
    "Hemant", "Ishaan", "Jayesh", "Karan", "Kartik", "Kunal", "Lalit", "Manish",
    "Mohit", "Naveen", "Nikhil", "Pankaj", "Pranav", "Raj", "Rahul", "Rajesh",
    "Rakesh", "Ravi", "Rohan", "Rohit", "Sachin", "Sahil", "Sanjay", "Shivam",
    "Siddharth", "Sunil", "Suresh", "Tarun", "Varun", "Vijay", "Vikram",
    "Vinod", "Vishal", "Vivek", "Yash", "Yuvraj", "Manoj", "Pradeep",
    "Ramesh", "Sandeep", "Tushar", "Uday", "Aman", "Bharat",
]

FEMALE_FIRST_NAMES = [
    "Aisha", "Ananya", "Anjali", "Archana", "Bhavna", "Chitra", "Deepa",
    "Divya", "Gauri", "Isha", "Jyoti", "Kavya", "Kriti", "Lakshmi", "Madhuri",
    "Meera", "Megha", "Nandini", "Neha", "Nisha", "Pallavi", "Pooja", "Priya",
    "Rashmi", "Riya", "Sakshi", "Sapna", "Seema", "Shreya", "Simran", "Sneha",
    "Sonal", "Srishti", "Sunita", "Swati", "Tanvi", "Tara", "Uma", "Vandana",
    "Vidya", "Yamini", "Aditi", "Arundhati", "Diya", "Harini", "Ira", "Juhi",
    "Kiara", "Lavanya", "Mira", "Nikita", "Padma", "Radha", "Sanya", "Trisha",
]

LAST_NAMES = [
    "Agarwal", "Banerjee", "Bhat", "Bose", "Chatterjee", "Chopra", "Das",
    "Deshmukh", "Dutta", "Ghosh", "Gupta", "Iyer", "Jain", "Joshi", "Kapoor",
    "Khan", "Krishnamurthy", "Kumar", "Malhotra", "Mehta", "Mishra", "Mukherjee",
    "Nair", "Pandey", "Patel", "Pillai", "Rajput", "Rao", "Reddy", "Roy",
    "Saxena", "Shah", "Sharma", "Singh", "Sinha", "Srivastava", "Thakur",
    "Tiwari", "Varma", "Verma", "Yadav", "Menon", "Kaur", "Sethi", "Ahuja",
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INDIAN CITIES (city, state, pincode_prefix, latitude, longitude)
# Weights reflect population / digital banking penetration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CITIES = [
    {"city": "Mumbai",          "state": "Maharashtra",       "pin": "400", "lat": 19.076, "lon": 72.877},
    {"city": "Delhi",           "state": "Delhi",             "pin": "110", "lat": 28.704, "lon": 77.102},
    {"city": "Bangalore",       "state": "Karnataka",         "pin": "560", "lat": 12.971, "lon": 77.594},
    {"city": "Hyderabad",       "state": "Telangana",         "pin": "500", "lat": 17.385, "lon": 78.486},
    {"city": "Chennai",         "state": "Tamil Nadu",        "pin": "600", "lat": 13.082, "lon": 80.270},
    {"city": "Kolkata",         "state": "West Bengal",       "pin": "700", "lat": 22.572, "lon": 88.363},
    {"city": "Pune",            "state": "Maharashtra",       "pin": "411", "lat": 18.520, "lon": 73.856},
    {"city": "Ahmedabad",       "state": "Gujarat",           "pin": "380", "lat": 23.022, "lon": 72.571},
    {"city": "Jaipur",          "state": "Rajasthan",         "pin": "302", "lat": 26.912, "lon": 75.787},
    {"city": "Lucknow",         "state": "Uttar Pradesh",     "pin": "226", "lat": 26.846, "lon": 80.946},
    {"city": "Chandigarh",      "state": "Chandigarh",        "pin": "160", "lat": 30.733, "lon": 76.779},
    {"city": "Bhopal",          "state": "Madhya Pradesh",    "pin": "462", "lat": 23.259, "lon": 77.412},
    {"city": "Indore",          "state": "Madhya Pradesh",    "pin": "452", "lat": 22.719, "lon": 75.857},
    {"city": "Nagpur",          "state": "Maharashtra",       "pin": "440", "lat": 21.145, "lon": 79.088},
    {"city": "Kochi",           "state": "Kerala",            "pin": "682", "lat": 9.931,  "lon": 76.267},
    {"city": "Coimbatore",      "state": "Tamil Nadu",        "pin": "641", "lat": 11.016, "lon": 76.955},
    {"city": "Visakhapatnam",   "state": "Andhra Pradesh",    "pin": "530", "lat": 17.686, "lon": 83.218},
    {"city": "Patna",           "state": "Bihar",             "pin": "800", "lat": 25.612, "lon": 85.144},
    {"city": "Surat",           "state": "Gujarat",           "pin": "395", "lat": 21.170, "lon": 72.831},
    {"city": "Noida",           "state": "Uttar Pradesh",     "pin": "201", "lat": 28.535, "lon": 77.391},
    {"city": "Gurgaon",         "state": "Haryana",           "pin": "122", "lat": 28.459, "lon": 77.026},
    {"city": "Thiruvananthapuram","state": "Kerala",           "pin": "695", "lat": 8.524,  "lon": 76.936},
    {"city": "Dehradun",        "state": "Uttarakhand",       "pin": "248", "lat": 30.316, "lon": 78.032},
    {"city": "Mangalore",       "state": "Karnataka",         "pin": "575", "lat": 12.914, "lon": 74.856},
    {"city": "Vadodara",        "state": "Gujarat",           "pin": "390", "lat": 22.307, "lon": 73.181},
]
CITY_WEIGHTS = [
    0.14, 0.13, 0.12, 0.08, 0.07, 0.06, 0.06, 0.04, 0.03, 0.03,
    0.02, 0.02, 0.02, 0.02, 0.02, 0.015, 0.015, 0.01, 0.015, 0.02,
    0.02, 0.01, 0.01, 0.005, 0.005,
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INDIAN BANKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BANKS = [
    {"name": "State Bank of India", "short": "SBI",       "ifsc": "SBIN0"},
    {"name": "HDFC Bank",           "short": "HDFC",      "ifsc": "HDFC0"},
    {"name": "ICICI Bank",          "short": "ICICI",     "ifsc": "ICIC0"},
    {"name": "Axis Bank",           "short": "Axis",      "ifsc": "UTIB0"},
    {"name": "Kotak Mahindra Bank", "short": "Kotak",     "ifsc": "KKBK0"},
    {"name": "Punjab National Bank","short": "PNB",       "ifsc": "PUNB0"},
    {"name": "Bank of Baroda",      "short": "BOB",       "ifsc": "BARB0"},
    {"name": "Canara Bank",         "short": "Canara",    "ifsc": "CNRB0"},
    {"name": "Union Bank of India", "short": "UBI",       "ifsc": "UBIN0"},
    {"name": "IndusInd Bank",       "short": "IndusInd",  "ifsc": "INDB0"},
    {"name": "Yes Bank",            "short": "Yes",       "ifsc": "YESB0"},
    {"name": "IDBI Bank",           "short": "IDBI",      "ifsc": "IBKL0"},
]
BANK_WEIGHTS = [0.18, 0.16, 0.14, 0.10, 0.08, 0.07, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# OCCUPATIONS (title, employment_type, annual_income_range, weight)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OCCUPATIONS = [
    {"title": "Software Engineer",    "type": "Salaried",      "min": 500000,  "max": 3500000,  "weight": 0.12},
    {"title": "Data Scientist",       "type": "Salaried",      "min": 700000,  "max": 4000000,  "weight": 0.04},
    {"title": "Business Analyst",     "type": "Salaried",      "min": 500000,  "max": 2500000,  "weight": 0.05},
    {"title": "Doctor",               "type": "Self-Employed", "min": 800000,  "max": 5000000,  "weight": 0.04},
    {"title": "Chartered Accountant", "type": "Self-Employed", "min": 600000,  "max": 3500000,  "weight": 0.04},
    {"title": "Teacher",              "type": "Salaried",      "min": 300000,  "max": 1200000,  "weight": 0.06},
    {"title": "Government Officer",   "type": "Salaried",      "min": 400000,  "max": 1800000,  "weight": 0.06},
    {"title": "Bank Employee",        "type": "Salaried",      "min": 400000,  "max": 2000000,  "weight": 0.03},
    {"title": "Lawyer",               "type": "Self-Employed", "min": 500000,  "max": 4000000,  "weight": 0.03},
    {"title": "Business Owner",       "type": "Self-Employed", "min": 400000,  "max": 8000000,  "weight": 0.10},
    {"title": "Freelancer",           "type": "Freelance",     "min": 300000,  "max": 3000000,  "weight": 0.05},
    {"title": "Marketing Manager",    "type": "Salaried",      "min": 500000,  "max": 2500000,  "weight": 0.04},
    {"title": "Sales Executive",      "type": "Salaried",      "min": 300000,  "max": 1500000,  "weight": 0.05},
    {"title": "Civil Engineer",       "type": "Salaried",      "min": 400000,  "max": 2000000,  "weight": 0.04},
    {"title": "Architect",            "type": "Self-Employed", "min": 500000,  "max": 3000000,  "weight": 0.02},
    {"title": "Pharmacist",           "type": "Salaried",      "min": 300000,  "max": 1200000,  "weight": 0.03},
    {"title": "Retired",              "type": "Retired",       "min": 200000,  "max": 1000000,  "weight": 0.05},
    {"title": "Student",              "type": "Student",       "min": 0,       "max": 200000,   "weight": 0.04},
    {"title": "Homemaker",            "type": "Homemaker",     "min": 0,       "max": 100000,   "weight": 0.03},
    {"title": "Consultant",           "type": "Self-Employed", "min": 600000,  "max": 5000000,  "weight": 0.04},
    {"title": "Shop Owner",           "type": "Self-Employed", "min": 200000,  "max": 1500000,  "weight": 0.04},
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TRANSACTION CATEGORIES (amount in INR)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRANSACTION_CATEGORIES = {
    "Food & Dining":   {"min": 50,    "max": 3000,   "mean": 450,   "std": 400,   "weight": 0.18},
    "Fuel":            {"min": 200,   "max": 5000,   "mean": 1500,  "std": 800,   "weight": 0.05},
    "Shopping":        {"min": 200,   "max": 25000,  "mean": 2500,  "std": 3000,  "weight": 0.12},
    "Healthcare":      {"min": 200,   "max": 50000,  "mean": 3000,  "std": 5000,  "weight": 0.04},
    "Travel":          {"min": 500,   "max": 50000,  "mean": 5000,  "std": 8000,  "weight": 0.04},
    "Investment":      {"min": 1000,  "max": 200000, "mean": 25000, "std": 30000, "weight": 0.05},
    "Insurance":       {"min": 1000,  "max": 50000,  "mean": 10000, "std": 8000,  "weight": 0.03},
    "Education":       {"min": 1000,  "max": 100000, "mean": 15000, "std": 15000, "weight": 0.03},
    "EMI":             {"min": 2000,  "max": 50000,  "mean": 12000, "std": 8000,  "weight": 0.06},
    "Utilities":       {"min": 100,   "max": 10000,  "mean": 2000,  "std": 1500,  "weight": 0.10},
    "Entertainment":   {"min": 100,   "max": 5000,   "mean": 800,   "std": 700,   "weight": 0.05},
    "Rent":            {"min": 5000,  "max": 50000,  "mean": 15000, "std": 8000,  "weight": 0.05},
    "Salary":          {"min": 15000, "max": 500000, "mean": 50000, "std": 40000, "weight": 0.04},
    "Transfer":        {"min": 500,   "max": 100000, "mean": 10000, "std": 15000, "weight": 0.10},
    "Subscription":    {"min": 99,    "max": 2000,   "mean": 500,   "std": 300,   "weight": 0.06},
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAYMENT CHANNELS & DEVICE TYPES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAYMENT_CHANNELS = ["UPI", "NEFT", "IMPS", "RTGS", "Debit Card", "Net Banking", "Auto Debit"]
PAYMENT_CHANNEL_WEIGHTS = [0.55, 0.10, 0.12, 0.03, 0.10, 0.05, 0.05]

DEVICE_TYPES = ["Android", "iOS", "Desktop", "Tablet"]
DEVICE_WEIGHTS = [0.55, 0.25, 0.15, 0.05]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MERCHANTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MERCHANT_CATEGORIES = [
    "Restaurant", "Grocery", "Fuel Station", "E-commerce", "Fashion",
    "Electronics", "Healthcare", "Hospital", "Pharmacy", "Travel Agency",
    "Hotel", "Airlines", "Insurance", "Mutual Fund", "Stock Broker",
    "Education Institute", "Coaching", "Streaming Service", "Gaming",
    "Utility Provider", "Telecom", "Real Estate", "Jewellery",
    "Automobile", "Home Decor", "Gym & Fitness", "Salon & Spa",
    "Supermarket", "Cloud Kitchen", "Cab Service",
]

MERCHANT_NAMES_BY_CATEGORY = {
    "Restaurant":          ["Swiggy", "Zomato", "Dominos", "McDonalds", "Pizza Hut", "Haldirams", "Barbeque Nation", "Mainland China", "Saravana Bhavan", "Paradise Biryani"],
    "Grocery":             ["BigBasket", "Blinkit", "DMart", "Reliance Fresh", "More Supermarket", "Star Bazaar", "Natures Basket", "JioMart", "Zepto"],
    "Fuel Station":        ["Indian Oil", "Bharat Petroleum", "Hindustan Petroleum", "Shell India", "Reliance Petroleum"],
    "E-commerce":          ["Amazon India", "Flipkart", "Myntra", "Meesho", "Snapdeal", "Tata CLiQ", "Ajio", "Nykaa"],
    "Fashion":             ["Zara India", "H&M India", "Westside", "Pantaloons", "Max Fashion", "FabIndia", "Allen Solly", "Van Heusen"],
    "Electronics":         ["Croma", "Reliance Digital", "Vijay Sales", "Samsung Store", "Apple India", "Mi Store"],
    "Healthcare":          ["Apollo Pharmacy", "MedPlus", "Practo", "1mg", "PharmEasy", "Tata Health"],
    "Hospital":            ["Apollo Hospital", "Fortis Healthcare", "Max Hospital", "Manipal Hospital", "Narayana Health"],
    "Pharmacy":            ["Apollo Pharmacy", "MedPlus Pharmacy", "Netmeds", "1mg Pharmacy"],
    "Travel Agency":       ["MakeMyTrip", "Goibibo", "Yatra", "Cleartrip", "EaseMyTrip", "ixigo"],
    "Hotel":               ["OYO Rooms", "Taj Hotels", "ITC Hotels", "Marriott India", "Hyatt India", "Lemon Tree"],
    "Airlines":            ["IndiGo", "Air India", "SpiceJet", "Vistara", "AirAsia India", "Akasa Air"],
    "Insurance":           ["LIC India", "HDFC Life", "ICICI Prudential", "SBI Life", "Max Life Insurance", "Star Health"],
    "Mutual Fund":         ["SBI Mutual Fund", "HDFC AMC", "ICICI Prudential MF", "Axis Mutual Fund", "Kotak AMC", "Zerodha Coin"],
    "Stock Broker":        ["Zerodha", "Groww", "Upstox", "Angel One", "5paisa", "ICICI Direct"],
    "Education Institute": ["BYJU'S", "Unacademy", "Coursera India", "Udemy", "Vedantu", "Simplilearn"],
    "Coaching":            ["Allen Career", "FIITJEE", "Aakash Institute", "Physics Wallah"],
    "Streaming Service":   ["Netflix India", "Amazon Prime Video", "Disney+ Hotstar", "Sony LIV", "Spotify India", "JioCinema"],
    "Gaming":              ["Steam India", "PlayStation Store", "Google Play Games", "Xbox India"],
    "Utility Provider":    ["Tata Power", "BSES Rajdhani", "Mahanagar Gas", "Adani Gas", "Jio Fiber", "MSEDCL"],
    "Telecom":             ["Jio", "Airtel", "Vodafone Idea", "BSNL"],
    "Real Estate":         ["MagicBricks", "99acres", "NoBroker", "Housing.com"],
    "Jewellery":           ["Tanishq", "Kalyan Jewellers", "Malabar Gold", "PC Jewellers", "Senco Gold"],
    "Automobile":          ["Maruti Suzuki", "Tata Motors", "Hero MotoCorp", "TVS Motor", "Hyundai India"],
    "Home Decor":          ["IKEA India", "Urban Ladder", "Pepperfry", "HomeTown"],
    "Gym & Fitness":       ["Cult.fit", "Golds Gym India", "Anytime Fitness"],
    "Salon & Spa":         ["Lakme Salon", "VLCC", "Naturals Salon", "Jawed Habib"],
    "Supermarket":         ["Reliance Smart", "Spencer's", "Spar India", "HyperCITY"],
    "Cloud Kitchen":       ["Faasos", "Box8", "Rebel Foods", "EatSure", "Licious"],
    "Cab Service":         ["Uber India", "Ola Cabs", "Rapido", "BluSmart"],
}

# Category to transaction category mapping
MERCHANT_TO_TXN_CATEGORY = {
    "Restaurant": "Food & Dining", "Grocery": "Food & Dining", "Cloud Kitchen": "Food & Dining",
    "Fuel Station": "Fuel", "Cab Service": "Travel",
    "E-commerce": "Shopping", "Fashion": "Shopping", "Electronics": "Shopping",
    "Jewellery": "Shopping", "Supermarket": "Shopping", "Home Decor": "Shopping",
    "Healthcare": "Healthcare", "Hospital": "Healthcare", "Pharmacy": "Healthcare",
    "Travel Agency": "Travel", "Hotel": "Travel", "Airlines": "Travel",
    "Insurance": "Insurance", "Mutual Fund": "Investment", "Stock Broker": "Investment",
    "Education Institute": "Education", "Coaching": "Education",
    "Streaming Service": "Subscription", "Gaming": "Entertainment",
    "Utility Provider": "Utilities", "Telecom": "Utilities",
    "Real Estate": "Rent", "Automobile": "Shopping",
    "Gym & Fitness": "Subscription", "Salon & Spa": "Entertainment",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RELATIONSHIP & RECIPIENT TYPES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RELATIONSHIP_TYPES = ["Family", "Friend", "Colleague", "Business", "Merchant", "Landlord", "Unknown"]
RELATIONSHIP_WEIGHTS = [0.25, 0.20, 0.10, 0.15, 0.10, 0.05, 0.15]
RECIPIENT_TYPES = ["Individual", "Business", "Merchant"]
RECIPIENT_TYPE_WEIGHTS = [0.65, 0.20, 0.15]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DEMOGRAPHIC ENUMS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACCOUNT_TYPES = ["Savings", "Current", "Salary"]
ACCOUNT_TYPE_WEIGHTS = [0.55, 0.15, 0.30]

EDUCATION_LEVELS = ["High School", "Undergraduate", "Graduate", "Post Graduate", "PhD", "Diploma"]
EDUCATION_WEIGHTS = [0.10, 0.25, 0.30, 0.25, 0.03, 0.07]

MARITAL_STATUS = ["Single", "Married", "Divorced", "Widowed"]
MARITAL_WEIGHTS = [0.35, 0.50, 0.10, 0.05]

KYC_STATUS = ["Verified", "Pending", "Partially Verified", "Expired"]
KYC_WEIGHTS = [0.82, 0.07, 0.06, 0.05]

RISK_PROFILES = ["Conservative", "Moderate", "Aggressive"]
RISK_PROFILE_WEIGHTS = [0.40, 0.40, 0.20]

LANGUAGES = ["English", "Hindi", "Tamil", "Telugu", "Kannada", "Malayalam", "Bengali", "Marathi", "Gujarati"]
LANGUAGE_WEIGHTS = [0.30, 0.30, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05, 0.04]

TRANSACTION_STATUSES = ["Completed", "Pending", "Failed", "Cancelled", "Reversed"]
TRANSACTION_STATUS_WEIGHTS = [0.88, 0.04, 0.03, 0.03, 0.02]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RISK & SCAM CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]

RISK_TYPES = [
    "New Recipient", "Large Amount", "Late Night", "Behavior Deviation",
    "Device Change", "Location Change", "Investment Scam", "Crypto Scam",
    "Deepfake Scam", "Impersonation Scam", "Romance Scam", "Lottery Scam",
    "Emergency Scam", "Money Mule", "Fake Bank Officer",
]

SCAM_CATEGORIES = [
    "Investment Scam", "Impersonation Scam", "Romance Scam", "Tech Support Scam",
    "Lottery Scam", "Advance Fee Scam", "Crypto Scam", "Deepfake Scam",
    "Emergency Scam", "Money Mule", "Fake Bank Officer", "Job Scam",
    "Charity Scam", "Phishing",
]

MERCHANT_RISK_LEVELS = ["Low", "Medium", "High"]
MERCHANT_RISK_WEIGHTS = [0.82, 0.13, 0.05]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SCAM PATTERN TEMPLATES (used to generate 200+ patterns)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCAM_TEMPLATES = {
    "Investment Scam": [
        {"name": "Guaranteed Returns Scheme",          "desc": "Promises fixed {pct}% monthly returns on investment with zero risk. Uses fake testimonials and fabricated portfolio screenshots.",                    "sig": "large_amount|new_recipient|investment_category|urgency_language"},
        {"name": "Stock Market Tips Fraud",             "desc": "Offers insider stock tips for a fee, claiming guaranteed profits from upcoming market movements.",                                                   "sig": "recurring_small_payments|new_recipient|increasing_amounts"},
        {"name": "Forex Trading Scam",                  "desc": "Promises extraordinary returns through forex trading platform that is actually a Ponzi scheme.",                                                    "sig": "large_amount|foreign_platform|new_recipient|urgency"},
        {"name": "Mutual Fund Impersonation",           "desc": "Impersonates legitimate mutual fund companies offering exclusive high-return schemes not available to public.",                                      "sig": "impersonation|large_amount|urgency|official_branding"},
        {"name": "Gold Investment Fraud",               "desc": "Offers below-market gold prices with guaranteed buyback at premium rates after a lock-in period.",                                                  "sig": "large_amount|new_recipient|unrealistic_returns"},
        {"name": "Property Investment Scheme",          "desc": "Promotes fake real estate investment with promises of {pct}x returns within months.",                                                               "sig": "very_large_amount|new_recipient|real_estate_keywords"},
        {"name": "IPO Allocation Scam",                 "desc": "Claims guaranteed IPO allotment in upcoming high-demand offerings for an upfront processing fee.",                                                  "sig": "advance_fee|urgency|official_impersonation"},
        {"name": "Fixed Deposit Fraud",                 "desc": "Offers FD rates significantly above market rate from supposedly reputed banks through unauthorized agents.",                                         "sig": "large_amount|unrealistic_rates|bank_impersonation"},
        {"name": "Chit Fund Ponzi",                     "desc": "Operates as a chit fund scheme paying early investors from new member contributions until collapse.",                                                "sig": "recurring_payments|community_pressure|increasing_amounts"},
        {"name": "Binary Options Trading",              "desc": "Promotes binary options trading platform showing fabricated wins to lure larger deposits.",                                                          "sig": "escalating_deposits|new_platform|foreign_recipient"},
        {"name": "Cryptocurrency Mining Pool",          "desc": "Fake cloud mining operation promising daily returns from cryptocurrency mining hardware investments.",                                                "sig": "crypto_keywords|recurring_returns|new_recipient"},
        {"name": "Agriculture Investment Scheme",       "desc": "Promises high returns from agricultural land or produce investment schemes that don't actually exist.",                                              "sig": "rural_targeting|large_amount|seasonal_promises"},
        {"name": "Startup Investment Fraud",            "desc": "Solicits investment in fake startups with fabricated valuations and exit strategies.",                                                               "sig": "large_amount|startup_keywords|urgency|fake_documents"},
        {"name": "Ponzi Scheme Classic",                "desc": "Multi-level investment scheme where returns to existing investors are funded by new investor deposits.",                                              "sig": "recruitment_pressure|regular_payments|increasing_contribution"},
        {"name": "Commodity Trading Scam",              "desc": "Fake commodity trading platform showing manipulated profits to encourage larger deposits.",                                                          "sig": "escalating_amounts|trading_keywords|new_platform"},
    ],
    "Impersonation Scam": [
        {"name": "Bank Manager Call",                   "desc": "Caller impersonates bank manager claiming account issues requiring immediate payment to 'secure' the account.",                                      "sig": "phone_initiated|urgency|bank_keywords|new_recipient"},
        {"name": "RBI Officer Fraud",                   "desc": "Impersonates Reserve Bank of India officer threatening account freeze unless 'compliance fee' is paid immediately.",                                 "sig": "government_impersonation|threat|urgency|large_amount"},
        {"name": "Income Tax Notice Scam",              "desc": "Sends fake income tax notice via SMS/WhatsApp demanding immediate payment to avoid penalties and arrest.",                                           "sig": "tax_keywords|threat_of_arrest|urgency|government_impersonation"},
        {"name": "Police Impersonation",                "desc": "Caller claims to be police officer saying victim's Aadhaar/PAN is linked to criminal activity, demands payment to clear records.",                  "sig": "authority_impersonation|threat|fear|immediate_payment"},
        {"name": "Telecom Provider Fraud",              "desc": "Impersonates telecom company claiming SIM will be deactivated unless KYC update fee is paid.",                                                      "sig": "telecom_keywords|urgency|small_amount|deactivation_threat"},
        {"name": "Electricity Board Scam",              "desc": "Threatens immediate power disconnection unless outstanding bill is paid to specified account within hours.",                                          "sig": "utility_impersonation|threat|urgency|alternate_account"},
        {"name": "Insurance Company Fraud",             "desc": "Impersonates insurance company offering maturity bonus payout after paying 'processing charges'.",                                                   "sig": "insurance_keywords|advance_fee|official_documents"},
        {"name": "Courier Company Scam",                "desc": "Claims package held at customs requiring payment of duties to a personal account to release delivery.",                                              "sig": "customs_keywords|advance_fee|personal_account"},
        {"name": "Hospital Emergency Call",             "desc": "Caller claims relative is in hospital emergency room and needs immediate payment for life-saving treatment.",                                        "sig": "emotional_pressure|urgency|family_keywords|new_recipient"},
        {"name": "Government Subsidy Fraud",            "desc": "Promises government subsidy or scheme benefit after paying 'registration fee' to unauthorized account.",                                             "sig": "government_scheme|advance_fee|official_language"},
        {"name": "EPFO Impersonation",                  "desc": "Impersonates EPFO official offering early PF withdrawal after paying a 'processing fee'.",                                                          "sig": "epfo_keywords|advance_fee|official_impersonation"},
        {"name": "Passport Office Scam",                "desc": "Claims passport renewal requires urgent fee payment to avoid cancellation.",                                                                        "sig": "government_impersonation|urgency|document_threat"},
    ],
    "Romance Scam": [
        {"name": "Online Dating Fund Request",          "desc": "After weeks of online relationship building, partner requests money for emergency medical treatment abroad.",                                         "sig": "relationship_buildup|emotional_appeal|foreign_recipient|medical_emergency"},
        {"name": "Military Deployment Scam",            "desc": "Claims to be deployed military officer needing funds for 'leave approval' or 'satellite phone charges'.",                                           "sig": "military_keywords|emotional_attachment|recurring_requests"},
        {"name": "Visa and Travel Romance",             "desc": "Online partner claims they need funds for visa and travel to visit the victim in India.",                                                            "sig": "travel_keywords|escalating_amounts|emotional_pressure"},
        {"name": "Business Emergency Romance",          "desc": "Long-distance partner claims business emergency and needs urgent loan that will be returned with interest.",                                         "sig": "business_emergency|romantic_context|large_amount|repayment_promise"},
        {"name": "Gift Card Romance Scam",              "desc": "Partner requests gift cards instead of direct transfer, claiming they can only accept this form of payment.",                                        "sig": "gift_card_purchase|romantic_context|multiple_small_amounts"},
        {"name": "Inheritance Romance Fraud",            "desc": "Partner claims large inheritance locked in foreign bank requiring 'legal fees' to access.",                                                         "sig": "inheritance_story|escalating_fees|foreign_context"},
        {"name": "Medical Emergency Romance",           "desc": "Partner or partner's family member suddenly needs expensive surgery, requests immediate financial help.",                                             "sig": "medical_urgency|emotional_manipulation|large_amount"},
        {"name": "Stranded Abroad Romance",             "desc": "Claims to be stranded in foreign country with stolen passport and wallet, needs emergency funds.",                                                   "sig": "emergency_abroad|emotional_appeal|immediate_transfer"},
    ],
    "Tech Support Scam": [
        {"name": "Microsoft Support Fraud",             "desc": "Cold call claiming Windows virus detected, requests remote access and payment for 'cleanup service'.",                                              "sig": "remote_access|tech_keywords|foreign_call|escalating_fees"},
        {"name": "Antivirus Renewal Scam",              "desc": "Fake antivirus expiry notification directing to payment page for unnecessary renewal.",                                                              "sig": "phishing_link|tech_keywords|recurring_charge"},
        {"name": "ISP Technical Issue",                 "desc": "Impersonates internet provider claiming technical issue requiring payment for 'router upgrade'.",                                                   "sig": "telecom_impersonation|tech_keywords|advance_payment"},
        {"name": "Apple ID Lock Scam",                  "desc": "Claims Apple ID has been compromised and requires payment to 'verify identity' and unlock account.",                                                "sig": "brand_impersonation|urgency|identity_verification"},
        {"name": "Google Account Recovery",             "desc": "Fake notification about Google account breach requesting payment for 'security verification'.",                                                      "sig": "brand_impersonation|phishing|security_keywords"},
        {"name": "Bank App Update Fraud",               "desc": "Claims mobile banking app needs urgent security update, directs to fake page collecting credentials and payment.",                                   "sig": "bank_impersonation|app_update|credential_theft"},
    ],
    "Lottery Scam": [
        {"name": "WhatsApp Lottery Winner",             "desc": "Random WhatsApp message claiming user won international lottery, requires 'tax payment' to release winnings.",                                       "sig": "unsolicited_message|lottery_keywords|advance_fee|foreign_recipient"},
        {"name": "KBC Prize Fraud",                     "desc": "Claims victim selected for KBC (Kaun Banega Crorepati) prize, demands processing fee for prize money.",                                             "sig": "tv_show_impersonation|advance_fee|official_documents"},
        {"name": "Amazon Lucky Draw",                   "desc": "Fake notification of Amazon lucky draw winning, requires payment for shipping and handling of prize.",                                               "sig": "brand_impersonation|advance_fee|phishing_link"},
        {"name": "Government Lucky Draw",               "desc": "Claims government-sponsored lucky draw selection, demands registration fee to claim prize.",                                                        "sig": "government_impersonation|advance_fee|official_language"},
        {"name": "SIM Card Lucky Draw",                 "desc": "Text message claiming mobile number selected for telecom company lucky draw with cash prize.",                                                      "sig": "telecom_impersonation|advance_fee|sms_phishing"},
        {"name": "International Sweepstakes",           "desc": "Email claiming selection for international sweepstakes, requires upfront tax payment in cryptocurrency.",                                            "sig": "foreign_lottery|crypto_payment|advance_fee"},
    ],
    "Advance Fee Scam": [
        {"name": "Loan Approval Fee Fraud",             "desc": "Offers pre-approved personal loan at low interest, requires upfront 'processing fee' before disbursement.",                                         "sig": "loan_keywords|advance_fee|too_good_terms|new_recipient"},
        {"name": "Job Offer Processing Fee",            "desc": "Fake job offer from reputed company requiring registration/training fee before joining date.",                                                      "sig": "job_keywords|advance_fee|company_impersonation"},
        {"name": "Flat Booking Advance",                "desc": "Requests advance booking amount for non-existent affordable housing in prime location.",                                                            "sig": "real_estate_keywords|large_advance|urgency|limited_availability"},
        {"name": "Visa Processing Fee",                 "desc": "Fake immigration consultant demanding upfront visa processing fees with guaranteed approval.",                                                      "sig": "visa_keywords|advance_fee|government_impersonation"},
        {"name": "Scholarship Fee Fraud",               "desc": "Claims student selected for prestigious scholarship requiring 'administrative fee' to process.",                                                    "sig": "education_keywords|advance_fee|official_impersonation"},
        {"name": "Car Loan Pre-Processing",             "desc": "Offers instant car loan approval with low EMI but requires upfront insurance and processing charges.",                                              "sig": "vehicle_loan|advance_fee|official_documents"},
    ],
    "Crypto Scam": [
        {"name": "Crypto Doubling Scheme",              "desc": "Promises to double cryptocurrency investment within 24 hours using 'proprietary AI trading algorithm'.",                                            "sig": "crypto_keywords|unrealistic_returns|urgency|ai_claims"},
        {"name": "Fake Crypto Exchange",                "desc": "Directs to fraudulent cryptocurrency exchange that accepts deposits but blocks all withdrawals.",                                                    "sig": "crypto_exchange|deposits_only|fake_platform"},
        {"name": "NFT Investment Fraud",                "desc": "Promotes worthless NFTs as guaranteed appreciating digital art investments with celebrity endorsements.",                                             "sig": "nft_keywords|celebrity_impersonation|large_amount"},
        {"name": "DeFi Yield Farming Scam",             "desc": "Promises extremely high APY through decentralized finance protocol that is actually a rug-pull scheme.",                                            "sig": "defi_keywords|unrealistic_apy|smart_contract_risk"},
        {"name": "Bitcoin ATM Scam",                    "desc": "Instructs victim to deposit cash at Bitcoin ATM and send cryptocurrency to 'secure' wallet controlled by scammer.",                                 "sig": "crypto_keywords|cash_conversion|urgency|authority_impersonation"},
        {"name": "Crypto Recovery Scam",                "desc": "Targets previous crypto scam victims, offering recovery services for an upfront fee.",                                                              "sig": "recovery_promise|advance_fee|targeting_victims"},
        {"name": "Pump and Dump Token",                 "desc": "Promotes unknown cryptocurrency token with coordinated social media hype before founders dump holdings.",                                           "sig": "obscure_token|social_media_push|urgency|fomo"},
        {"name": "Fake Airdrop Scam",                   "desc": "Claims free cryptocurrency airdrop requiring 'gas fee' payment or wallet connection to malicious site.",                                           "sig": "free_crypto|advance_fee|phishing_link"},
    ],
    "Deepfake Scam": [
        {"name": "CEO Video Call Fraud",                "desc": "Uses deepfake technology to impersonate company CEO in video call instructing urgent fund transfer to vendor.",                                      "sig": "deepfake_video|authority_impersonation|large_amount|urgency"},
        {"name": "Family Member Video Scam",            "desc": "Deepfake video call impersonating family member requesting emergency funds for accident or legal trouble.",                                          "sig": "deepfake_video|family_impersonation|emotional_urgency|new_recipient"},
        {"name": "Celebrity Endorsement Deepfake",      "desc": "Deepfake video of celebrity endorsing investment scheme to establish credibility for fraud.",                                                        "sig": "deepfake_video|celebrity_impersonation|investment_scam"},
        {"name": "Friend Voice Clone",                  "desc": "AI-generated voice clone of friend requesting urgent loan via phone call.",                                                                         "sig": "voice_clone|friend_impersonation|urgency|new_account"},
        {"name": "Boss Impersonation Call",             "desc": "AI voice clone of workplace boss instructing confidential urgent payment to new vendor.",                                                            "sig": "voice_clone|authority_impersonation|confidentiality|urgency"},
        {"name": "Relative Kidnapping Hoax",            "desc": "Uses voice cloning to simulate kidnapped relative's voice demanding ransom payment.",                                                               "sig": "voice_clone|ransom|extreme_urgency|emotional_manipulation"},
    ],
    "Emergency Scam": [
        {"name": "Accident Emergency Fraud",            "desc": "Caller claims relative involved in serious accident and needs immediate hospital payment before treatment.",                                         "sig": "medical_emergency|family_context|urgency|new_recipient"},
        {"name": "Arrest Threat Scam",                  "desc": "Claims family member arrested and needs bail money transferred immediately to avoid jail.",                                                          "sig": "legal_emergency|family_context|urgency|threat"},
        {"name": "Stranded Traveller Fraud",            "desc": "Claims friend or relative stranded in remote location with no money or phone, needs immediate help.",                                               "sig": "travel_emergency|friend_family|urgency|unverifiable"},
        {"name": "Fire or Flood Emergency",             "desc": "Claims home destroyed by fire/flood and needs immediate financial assistance for shelter and food.",                                                 "sig": "natural_disaster|emotional_appeal|urgency"},
        {"name": "College Fee Emergency",               "desc": "Claims child's college admission at risk unless fee is paid within hours to specific account.",                                                     "sig": "education_emergency|time_pressure|parental_anxiety"},
    ],
    "Money Mule": [
        {"name": "Work From Home Reshipping",           "desc": "Offers work-from-home job receiving and forwarding packages or money transfers, making victim an unwitting money mule.",                            "sig": "job_offer|forwarding_pattern|multiple_small_transactions"},
        {"name": "Payment Processing Job",              "desc": "Recruits victim as 'payment processor' receiving funds in personal account and forwarding to other accounts.",                                      "sig": "job_offer|rapid_forwarding|multiple_recipients"},
        {"name": "Crypto Exchange Assistant",            "desc": "Asks victim to convert cash to crypto and transfer to specified wallets as a 'side job'.",                                                         "sig": "crypto_conversion|rapid_turnover|commission_based"},
    ],
    "Fake Bank Officer": [
        {"name": "KYC Update Fraud",                    "desc": "Calls as bank officer claiming KYC update required immediately or account will be frozen, collects details and money.",                             "sig": "kyc_keywords|bank_impersonation|urgency|account_freeze_threat"},
        {"name": "Credit Card Upgrade Scam",            "desc": "Offers premium credit card upgrade requiring 'activation fee' and collects full card details.",                                                     "sig": "credit_card_keywords|upgrade_offer|advance_fee|data_theft"},
        {"name": "Loan Closure Scam",                   "desc": "Claims outstanding loan requires immediate closure payment to avoid legal action, provides fake loan details.",                                     "sig": "loan_keywords|legal_threat|urgency|fake_account"},
        {"name": "Account Verification Fraud",          "desc": "Sends OTP and asks customer to share for 'verification', then uses it to authorize fraudulent transaction.",                                        "sig": "otp_request|social_engineering|bank_impersonation"},
        {"name": "Reward Points Redemption",            "desc": "Claims accumulated reward points expiring today, guides through fake redemption process that initiates transfer.",                                   "sig": "reward_keywords|urgency|bank_impersonation|guided_process"},
        {"name": "Debit Card Block Alert",              "desc": "Fake alert that debit card will be blocked unless user calls given number and pays 'renewal fee'.",                                                 "sig": "card_block_threat|urgency|advance_fee|bank_impersonation"},
    ],
    "Job Scam": [
        {"name": "Data Entry Job Fraud",                "desc": "Offers high-paying data entry job requiring upfront registration and software purchase fee.",                                                       "sig": "job_keywords|advance_fee|unrealistic_salary"},
        {"name": "Part-time Social Media Job",          "desc": "Promises payment for liking/sharing social media posts, requires initial 'task activation' payment.",                                               "sig": "social_media|small_advance|escalating_tasks"},
        {"name": "Foreign Job Placement",               "desc": "Fake recruitment agency offering Gulf/European jobs with visa sponsorship after paying placement fee.",                                             "sig": "foreign_job|advance_fee|visa_promise|agency_impersonation"},
        {"name": "App Review Task Scam",                "desc": "Telegram-based task scam asking users to rate apps for money, requiring escalating 'investment' amounts.",                                          "sig": "telegram_based|escalating_deposits|task_based"},
    ],
    "Charity Scam": [
        {"name": "Fake Disaster Relief",                "desc": "Solicits donations for fabricated or real disaster using fake charity organization and emotional imagery.",                                          "sig": "charity_keywords|emotional_appeal|unverified_org"},
        {"name": "Child Education Charity",             "desc": "Fake NGO collecting funds for child education with no actual beneficiaries.",                                                                       "sig": "charity_keywords|emotional_appeal|recurring_donation"},
        {"name": "Temple Donation Fraud",               "desc": "Impersonates religious institution collecting donations for temple renovation or festival.",                                                        "sig": "religious_keywords|impersonation|community_trust"},
    ],
    "Phishing": [
        {"name": "Bank SMS Phishing",                   "desc": "SMS with link to fake banking site that captures credentials and initiates unauthorized transfers.",                                                "sig": "sms_link|bank_impersonation|credential_theft"},
        {"name": "UPI Collect Request Fraud",           "desc": "Sends UPI collect request disguised as refund or cashback, tricking user into approving payment.",                                                  "sig": "upi_collect|refund_disguise|social_engineering"},
        {"name": "Email Invoice Phishing",              "desc": "Sends fake invoice from known vendor with modified bank account details for payment.",                                                              "sig": "email_phishing|invoice_fraud|account_substitution"},
        {"name": "QR Code Payment Fraud",               "desc": "Provides QR code claiming to receive payment but actually initiates a debit from victim's account.",                                               "sig": "qr_code|reverse_payment|social_engineering"},
    ],
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONVERSATION TEMPLATES (for AI agent conversations)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT_QUESTIONS = [
    "Can you tell me how you know the recipient of this transfer?",
    "How did you first learn about this investment opportunity?",
    "Has anyone asked you to keep this transaction confidential?",
    "Did someone contact you by phone, WhatsApp, or social media about this?",
    "Were you told to act urgently or that the offer is time-limited?",
    "Have you independently verified the recipient's identity?",
    "Is this amount typical for your usual transactions?",
    "Have you received any communication claiming to be from your bank recently?",
    "Were you asked to share any OTP or banking credentials?",
    "Do you personally know the person you are sending money to?",
    "Has someone offered you guaranteed returns on this investment?",
    "Were you shown screenshots or testimonials of other people's profits?",
    "Is someone guiding you through this transaction on a phone call right now?",
    "Have you verified this opportunity through any official channels?",
    "Are you making this transfer of your own free will without any pressure?",
]

SAFE_RESPONSES = [
    "Yes, they are my {relation} and I have known them for {years} years.",
    "This is a regular monthly payment I always make.",
    "I have verified everything through official channels.",
    "No one contacted me. I initiated this myself.",
    "This is my usual {category} expense.",
    "I have been transacting with this recipient for a long time.",
    "No, there is no urgency. I am doing this at my convenience.",
]

SUSPICIOUS_RESPONSES = [
    "Someone called me and told me to do this urgently.",
    "I saw an ad on social media promising high returns.",
    "They said my account will be blocked if I don't pay now.",
    "I met them online a few weeks ago.",
    "They asked me not to tell anyone about this opportunity.",
    "I was told to transfer first and they will send back double.",
    "An officer from the bank called and asked me to make this payment.",
    "I need to send this money quickly or the offer expires.",
    "They showed me screenshots of other people earning huge profits.",
    "I received a message saying I won a prize.",
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TRANSACTION REMARKS TEMPLATES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NORMAL_REMARKS = {
    "Food & Dining":   ["Lunch", "Dinner", "Grocery shopping", "Online food order", "Restaurant bill", "Coffee", "Snacks"],
    "Fuel":            ["Petrol refill", "Diesel refill", "CNG refill", "Fuel for car", "Bike fuel"],
    "Shopping":        ["Online purchase", "Clothing", "Electronics", "Gadget purchase", "Home appliance", "Gift shopping"],
    "Healthcare":      ["Doctor consultation", "Medicine purchase", "Lab tests", "Health checkup", "Dental treatment"],
    "Travel":          ["Flight booking", "Hotel booking", "Train ticket", "Cab fare", "Bus ticket", "Trip expenses"],
    "Investment":      ["SIP investment", "Mutual fund", "Stock purchase", "FD deposit", "Gold investment"],
    "Insurance":       ["Premium payment", "Insurance renewal", "Health insurance", "Vehicle insurance"],
    "Education":       ["Course fee", "Tuition fee", "Exam fee", "Book purchase", "Online course"],
    "EMI":             ["Home loan EMI", "Car loan EMI", "Personal loan EMI", "Education loan EMI"],
    "Utilities":       ["Electricity bill", "Water bill", "Gas bill", "Internet bill", "Mobile recharge"],
    "Entertainment":   ["Movie tickets", "Concert tickets", "Gaming purchase", "Streaming subscription"],
    "Rent":            ["Monthly rent", "House rent", "Office rent", "PG rent"],
    "Salary":          ["Monthly salary", "Salary credit", "Bonus", "Incentive"],
    "Transfer":        ["Personal transfer", "Family support", "Sent to friend", "Bill split", "Repayment"],
    "Subscription":    ["Netflix", "Spotify", "Amazon Prime", "Gym membership", "Magazine subscription"],
}

SCAM_REMARKS = [
    "Investment in guaranteed returns scheme - promised {pct}% monthly returns",
    "Processing fee for lottery prize of Rs {amount}",
    "Urgent KYC update fee as advised by bank officer",
    "Account verification payment to avoid account freeze",
    "Registration fee for high-paying work from home job",
    "Emergency medical funds for friend",
    "Crypto trading deposit - guaranteed doubling in 24 hours",
    "Advance fee for pre-approved personal loan at 2% interest",
    "Tax payment to avoid legal notice and arrest",
    "Insurance maturity bonus processing charges",
    "Gift for online friend - emergency situation",
    "Custom duty payment for international prize delivery",
    "Security deposit for exclusive crypto trading group",
    "Visa processing fee for overseas job placement",
    "Platform activation fee for binary options trading",
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RISK SCORE THRESHOLDS (matches architecture document)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RISK_THRESHOLDS = {
    "Low":      (0, 30),
    "Medium":   (31, 50),
    "High":     (51, 90),
    "Critical": (91, 100),
}
