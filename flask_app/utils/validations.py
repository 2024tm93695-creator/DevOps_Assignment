from datetime import datetime, date

def validate_member_data(data, update=False):
    required_fields = ['name', 'age', 'height', 'weight', 'program', 'target_weight', 'target_adherence']
    
    if not update:
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
    
    if 'name' in data and (not isinstance(data['name'], str) or len(data['name'].strip()) == 0):
        raise ValueError("Name must be a non-empty string")
    
    if 'age' in data and (not isinstance(data['age'], int) or data['age'] < 0 or data['age'] > 120):
        raise ValueError("Age must be an integer between 0 and 120")
    
    if 'height' in data and (not isinstance(data['height'], (int, float)) or data['height'] <= 0):
        raise ValueError("Height must be a positive number")
    
    if 'weight' in data and (not isinstance(data['weight'], (int, float)) or data['weight'] <= 0):
        raise ValueError("Weight must be a positive number")
    
    if 'target_weight' in data and (not isinstance(data['target_weight'], (int, float)) or data['target_weight'] <= 0):
        raise ValueError("Target weight must be a positive number")
    
    if 'target_adherence' in data and (not isinstance(data['target_adherence'], int) or not (0 <= data['target_adherence'] <= 100)):
        raise ValueError("Target adherence must be an integer between 0 and 100")

def validate_workout_data(data, update=False):
    required_fields = ['client_name', 'date', 'workout_type', 'duration_min']
    
    if not update:
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
    
    if 'client_name' in data and not isinstance(data['client_name'], str):
        raise ValueError("Client name must be a string")
    
    if 'date' in data:
        try:
            if isinstance(data['date'], str):
                datetime.fromisoformat(data['date'])
            elif not isinstance(data['date'], date):
                raise ValueError("Invalid date format")
        except:
            raise ValueError("Date must be in ISO format (YYYY-MM-DD)")
    
    if 'duration_min' in data and (not isinstance(data['duration_min'], int) or data['duration_min'] <= 0):
        raise ValueError("Duration must be a positive integer")

def validate_exercise_data(data):
    required_fields = ['name', 'sets', 'reps']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    if not isinstance(data['name'], str) or len(data['name'].strip()) == 0:
        raise ValueError("Exercise name must be a non-empty string")
    
    if not isinstance(data['sets'], int) or data['sets'] <= 0:
        raise ValueError("Sets must be a positive integer")
    
    if not isinstance(data['reps'], int) or data['reps'] <= 0:
        raise ValueError("Reps must be a positive integer")
    
    if 'weight' in data and data['weight'] is not None and (not isinstance(data['weight'], (int, float)) or data['weight'] < 0):
        raise ValueError("Weight must be a non-negative number")

def validate_subscription_data(data, update=False):
    required_fields = ['client_name', 'plan_name', 'start_date', 'end_date']
    
    if not update:
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
    
    if 'client_name' in data and (not isinstance(data['client_name'], str) or len(data['client_name'].strip()) == 0):
        raise ValueError("Client name must be a non-empty string")
    
    if 'plan_name' in data and not isinstance(data['plan_name'], str):
        raise ValueError("Plan name must be a string")
    
    start_date = None
    end_date = None
    
    for date_field in ['start_date', 'end_date']:
        if date_field in data:
            try:
                if isinstance(data[date_field], str):
                    temp_date = datetime.fromisoformat(data[date_field]).date()
                    if date_field == 'start_date':
                        start_date = temp_date
                    else:
                        end_date = temp_date
                elif isinstance(data[date_field], date):
                    if date_field == 'start_date':
                        start_date = data[date_field]
                    else:
                        end_date = data[date_field]
                else:
                    raise ValueError(f"Invalid {date_field} format")
            except:
                raise ValueError(f"{date_field} must be in ISO format (YYYY-MM-DD)")
    
    # Check that end_date is not before start_date
    if start_date and end_date and end_date < start_date:
        raise ValueError("End date must be after or equal to start date")

def validate_trainer_data(data, update=False):
    if not update and 'name' not in data:
        raise ValueError("Missing required field: name")
    
    if 'name' in data and (not isinstance(data['name'], str) or len(data['name'].strip()) == 0):
        raise ValueError("Name must be a non-empty string")
    
    if 'experience_years' in data and data['experience_years'] is not None:
        if not isinstance(data['experience_years'], int) or data['experience_years'] < 0:
            raise ValueError("Experience years must be a non-negative integer")
    
    if 'email' in data and data['email']:
        # Basic email validation
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            raise ValueError("Invalid email format")