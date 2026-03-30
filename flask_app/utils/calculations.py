def calculate_calories(weight, height, age, program):
    """Calculate daily calorie needs based on member data and program"""
    # Basic BMR calculation using Mifflin-St Jeor equation
    # For simplicity, assuming male formula: BMR = 10*weight + 6.25*height - 5*age + 5
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    
    # Activity factor based on program
    program_factors = {
        "Fat Loss (FL) – 3 day": 1.2,  # Light activity
        "Fat Loss (FL) – 5 day": 1.375,  # Moderate activity
        "Muscle Gain (MG) – PPL": 1.55,  # Very active
        "Beginner (BG)": 1.2,  # Light activity
    }
    
    activity_factor = program_factors.get(program, 1.2)
    tdee = bmr * activity_factor
    
    # Adjust for goals
    if "Fat Loss" in program:
        return int(tdee - 500)  # Deficit for fat loss
    elif "Muscle Gain" in program:
        return int(tdee + 300)  # Surplus for muscle gain
    else:
        return int(tdee)  # Maintenance

def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (cm)"""
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def calculate_subscription_fee(plan_name):
    """Calculate subscription fee based on plan"""
    plan_fees = {
        "Basic": 50.0,
        "Premium": 80.0,
        "VIP": 120.0,
        "Student": 30.0,
        "Senior": 40.0,
    }
    return plan_fees.get(plan_name, 50.0)

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"