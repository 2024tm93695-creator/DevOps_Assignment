"""Tests for utility functions: calculations and validations."""

import pytest
from utils.calculations import (
    calculate_calories, 
    calculate_bmi, 
    calculate_subscription_fee,
    get_bmi_category
)
from utils.validations import (
    validate_member_data,
    validate_workout_data,
    validate_exercise_data,
    validate_subscription_data,
    validate_trainer_data
)


class TestCalculateCalories:
    """Test calorimetric calculations."""

    def test_calculate_calories_fat_loss_3day(self):
        """Test calorie calculation for fat loss 3-day program."""
        calories = calculate_calories(80, 180, 30, "Fat Loss (FL) – 3 day")
        assert isinstance(calories, int)
        assert calories > 0
        # Rough validation: should be deficit
        assert calories < (10*80 + 6.25*180 - 5*30 + 5) * 1.2

    def test_calculate_calories_fat_loss_5day(self):
        """Test calorie calculation for fat loss 5-day program."""
        calories = calculate_calories(70, 165, 25, "Fat Loss (FL) – 5 day")
        assert isinstance(calories, int)
        assert calories > 0

    def test_calculate_calories_muscle_gain(self):
        """Test calorie calculation for muscle gain program."""
        calories = calculate_calories(85, 185, 28, "Muscle Gain (MG) – PPL")
        assert isinstance(calories, int)
        assert calories > 0
        # Should be surplus
        bmr = 10*85 + 6.25*185 - 5*28 + 5
        tdee = bmr * 1.55
        assert calories > tdee

    def test_calculate_calories_beginner(self):
        """Test calorie calculation for beginner program."""
        calories = calculate_calories(75, 170, 22, "Beginner (BG)")
        assert isinstance(calories, int)
        assert calories > 0

    def test_calculate_calories_unknown_program(self):
        """Test calorie calculation with unknown program defaults to light activity."""
        calories = calculate_calories(80, 180, 30, "Unknown Program")
        assert isinstance(calories, int)
        assert calories > 0

    @pytest.mark.edge_case
    def test_calculate_calories_extreme_values(self):
        """Test calorie calculation with extreme but valid values."""
        # Very light person
        calories_light = calculate_calories(40, 140, 20, "Beginner (BG)")
        # Very heavy person
        calories_heavy = calculate_calories(150, 200, 50, "Muscle Gain (MG) – PPL")
        assert calories_light > 0
        assert calories_heavy > 0
        assert calories_heavy > calories_light

    def test_calculate_calories_consistency(self):
        """Test that same inputs produce same outputs."""
        calories1 = calculate_calories(80, 180, 30, "Muscle Gain (MG) – PPL")
        calories2 = calculate_calories(80, 180, 30, "Muscle Gain (MG) – PPL")
        assert calories1 == calories2


class TestCalculateBMI:
    """Test BMI calculation."""

    def test_calculate_bmi_normal(self):
        """Test BMI calculation with normal values."""
        bmi = calculate_bmi(70, 180)
        assert isinstance(bmi, float)
        assert 20 < bmi < 26  # Normal BMI range

    def test_calculate_bmi_precision(self):
        """Test BMI is rounded to 2 decimal places."""
        bmi = calculate_bmi(80, 180)
        decimal_places = len(str(bmi).split('.')[-1])
        assert decimal_places <= 2

    @pytest.mark.edge_case
    def test_calculate_bmi_minimal_values(self):
        """Test BMI with minimal valid values."""
        bmi = calculate_bmi(30, 150)
        assert isinstance(bmi, float)
        assert bmi > 0

    def test_calculate_bmi_consistency(self):
        """Test BMI calculation consistency."""
        bmi1 = calculate_bmi(75, 175)
        bmi2 = calculate_bmi(75, 175)
        assert bmi1 == bmi2


class TestBMICategory:
    """Test BMI category classification."""

    def test_bmi_underweight(self):
        """Test BMI classification for underweight."""
        bmi = 17.5
        category = get_bmi_category(bmi)
        assert category == "Underweight"

    def test_bmi_normal_weight(self):
        """Test BMI classification for normal weight."""
        bmi = 22.5
        category = get_bmi_category(bmi)
        assert category == "Normal weight"

    def test_bmi_overweight(self):
        """Test BMI classification for overweight."""
        bmi = 27.5
        category = get_bmi_category(bmi)
        assert category == "Overweight"

    def test_bmi_obese(self):
        """Test BMI classification for obese."""
        bmi = 32.0
        category = get_bmi_category(bmi)
        assert category == "Obese"

    @pytest.mark.edge_case
    def test_bmi_boundary_values(self):
        """Test BMI at exact boundary values."""
        assert get_bmi_category(18.5) == "Normal weight"
        assert get_bmi_category(25.0) == "Overweight"
        assert get_bmi_category(30.0) == "Obese"
        assert get_bmi_category(18.49) == "Underweight"


class TestSubscriptionFee:
    """Test subscription fee calculation."""

    def test_subscription_fee_basic(self):
        """Test fee for basic plan."""
        fee = calculate_subscription_fee("Basic")
        assert fee == 50.0

    def test_subscription_fee_premium(self):
        """Test fee for premium plan."""
        fee = calculate_subscription_fee("Premium")
        assert fee == 80.0

    def test_subscription_fee_vip(self):
        """Test fee for VIP plan."""
        fee = calculate_subscription_fee("VIP")
        assert fee == 120.0

    def test_subscription_fee_student(self):
        """Test fee for student plan."""
        fee = calculate_subscription_fee("Student")
        assert fee == 30.0

    def test_subscription_fee_senior(self):
        """Test fee for senior plan."""
        fee = calculate_subscription_fee("Senior")
        assert fee == 40.0

    def test_subscription_fee_unknown_defaults_to_basic(self):
        """Test that unknown plan defaults to basic fee."""
        fee = calculate_subscription_fee("UnknownPlan")
        assert fee == 50.0

    @pytest.mark.edge_case
    def test_subscription_fee_empty_string(self):
        """Test fee calculation with empty string."""
        fee = calculate_subscription_fee("")
        assert fee == 50.0


class TestValidateMemberData:
    """Test member data validation."""

    def test_validate_member_data_valid(self, sample_member_data):
        """Test validation passes for valid data."""
        # Should not raise any exception
        validate_member_data(sample_member_data)

    @pytest.mark.negative
    def test_validate_member_data_missing_required_field(self):
        """Test validation fails for missing required field."""
        data = {
            'name': 'John',
            'age': 30,
            'height': 180.0
            # Missing weight, program, target_weight, target_adherence
        }
        with pytest.raises(ValueError, match="Missing required field"):
            validate_member_data(data)

    @pytest.mark.negative
    def test_validate_member_data_invalid_name_empty(self):
        """Test validation fails for empty name."""
        data = {
            'name': '',
            'age': 30,
            'height': 180.0,
            'weight': 80.0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 80
        }
        with pytest.raises(ValueError, match="Name must be"):
            validate_member_data(data)

    @pytest.mark.negative
    def test_validate_member_data_invalid_name_type(self):
        """Test validation fails for non-string name."""
        data = {
            'name': 123,
            'age': 30,
            'height': 180.0,
            'weight': 80.0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 80
        }
        with pytest.raises(ValueError, match="Name must be"):
            validate_member_data(data)

    @pytest.mark.negative
    def test_validate_member_data_invalid_age_negative(self):
        """Test validation fails for negative age."""
        data = {
            'name': 'John',
            'age': -5,
            'height': 180.0,
            'weight': 80.0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 80
        }
        with pytest.raises(ValueError, match="Age must be"):
            validate_member_data(data)

    @pytest.mark.negative
    def test_validate_member_data_invalid_age_over_120(self):
        """Test validation fails for age over 120."""
        data = {
            'name': 'John',
            'age': 150,
            'height': 180.0,
            'weight': 80.0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 80
        }
        with pytest.raises(ValueError, match="Age must be"):
            validate_member_data(data)

    @pytest.mark.negative
    def test_validate_member_data_invalid_height_zero(self):
        """Test validation fails for zero height."""
        data = {
            'name': 'John',
            'age': 30,
            'height': 0,
            'weight': 80.0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 80
        }
        with pytest.raises(ValueError, match="Height must be"):
            validate_member_data(data)

    @pytest.mark.negative
    def test_validate_member_data_invalid_weight_zero(self):
        """Test validation fails for zero weight."""
        data = {
            'name': 'John',
            'age': 30,
            'height': 180.0,
            'weight': 0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 80
        }
        with pytest.raises(ValueError, match="Weight must be"):
            validate_member_data(data)

    @pytest.mark.negative
    def test_validate_member_data_invalid_adherence_over_100(self):
        """Test validation fails for adherence over 100."""
        data = {
            'name': 'John',
            'age': 30,
            'height': 180.0,
            'weight': 80.0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 150
        }
        with pytest.raises(ValueError, match="Target adherence must be"):
            validate_member_data(data)

    def test_validate_member_data_update_mode(self):
        """Test validation in update mode allows partial data."""
        data = {'name': 'Updated Name'}
        # Should not raise, as update mode is lenient
        validate_member_data(data, update=True)

    @pytest.mark.edge_case
    def test_validate_member_data_boundary_values(self):
        """Test validation with boundary values."""
        data = {
            'name': 'A',  # Minimum name length
            'age': 0,      # Minimum age
            'height': 0.1,  # Minimum height
            'weight': 0.1,  # Minimum weight
            'program': 'Beginner (BG)',
            'target_weight': 50.0,
            'target_adherence': 0  # Minimum adherence
        }
        validate_member_data(data)


class TestValidateWorkoutData:
    """Test workout data validation."""

    def test_validate_workout_data_valid(self, sample_workout_data):
        """Test validation passes for valid workout data."""
        validate_workout_data(sample_workout_data)

    @pytest.mark.negative
    def test_validate_workout_data_missing_field(self):
        """Test validation fails for missing required field."""
        data = {
            'client_name': 'John',
            'date': '2024-01-15'
            # Missing workout_type and duration_min
        }
        with pytest.raises(ValueError, match="Missing required field"):
            validate_workout_data(data)

    @pytest.mark.negative
    def test_validate_workout_data_invalid_date_format(self):
        """Test validation fails for invalid date format."""
        data = {
            'client_name': 'John',
            'date': '15-01-2024',  # Invalid format
            'workout_type': 'Chest',
            'duration_min': 60
        }
        with pytest.raises(ValueError, match="Date must be"):
            validate_workout_data(data)

    @pytest.mark.negative
    def test_validate_workout_data_invalid_duration_zero(self):
        """Test validation fails for zero duration."""
        data = {
            'client_name': 'John',
            'date': '2024-01-15',
            'workout_type': 'Chest',
            'duration_min': 0
        }
        with pytest.raises(ValueError, match="Duration must be"):
            validate_workout_data(data)

    def test_validate_workout_data_update_mode(self):
        """Test validation in update mode allows partial data."""
        data = {'client_name': 'Updated Name'}
        validate_workout_data(data, update=True)


class TestValidateExerciseData:
    """Test exercise data validation."""

    def test_validate_exercise_data_valid(self, sample_exercise_data):
        """Test validation passes for valid exercise data."""
        validate_exercise_data(sample_exercise_data)

    @pytest.mark.negative
    def test_validate_exercise_data_missing_field(self):
        """Test validation fails for missing required field."""
        data = {
            'name': 'Bench Press',
            'sets': 4
            # Missing reps
        }
        with pytest.raises(ValueError, match="Missing required field"):
            validate_exercise_data(data)

    @pytest.mark.negative
    def test_validate_exercise_data_invalid_name_empty(self):
        """Test validation fails for empty exercise name."""
        data = {
            'name': '',
            'sets': 4,
            'reps': 8
        }
        with pytest.raises(ValueError, match="Exercise name must be"):
            validate_exercise_data(data)

    @pytest.mark.negative
    def test_validate_exercise_data_invalid_sets_zero(self):
        """Test validation fails for zero sets."""
        data = {
            'name': 'Bench Press',
            'sets': 0,
            'reps': 8
        }
        with pytest.raises(ValueError, match="Sets must be"):
            validate_exercise_data(data)

    @pytest.mark.negative
    def test_validate_exercise_data_invalid_reps_negative(self):
        """Test validation fails for negative reps."""
        data = {
            'name': 'Bench Press',
            'sets': 4,
            'reps': -5
        }
        with pytest.raises(ValueError, match="Reps must be"):
            validate_exercise_data(data)

    @pytest.mark.negative
    def test_validate_exercise_data_invalid_weight_negative(self):
        """Test validation fails for negative weight."""
        data = {
            'name': 'Bench Press',
            'sets': 4,
            'reps': 8,
            'weight': -10.0
        }
        with pytest.raises(ValueError, match="Weight must be"):
            validate_exercise_data(data)

    def test_validate_exercise_data_valid_weight_none(self):
        """Test validation passes when weight is None."""
        data = {
            'name': 'Push-ups',
            'sets': 3,
            'reps': 15,
            'weight': None
        }
        validate_exercise_data(data)


class TestValidateSubscriptionData:
    """Test subscription data validation."""

    def test_validate_subscription_data_valid(self, sample_subscription_data):
        """Test validation passes for valid subscription data."""
        validate_subscription_data(sample_subscription_data)

    @pytest.mark.negative
    def test_validate_subscription_data_missing_field(self):
        """Test validation fails for missing required field."""
        data = {
            'client_name': 'John',
            'plan_name': 'Basic'
            # Missing start_date and end_date
        }
        with pytest.raises(ValueError, match="Missing required field"):
            validate_subscription_data(data)

    @pytest.mark.negative
    def test_validate_subscription_data_invalid_client_name_type(self):
        """Test validation fails for non-string client name."""
        data = {
            'client_name': 123,
            'plan_name': 'Basic',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        }
        with pytest.raises(ValueError, match="Client name must be"):
            validate_subscription_data(data)

    @pytest.mark.negative
    def test_validate_subscription_data_invalid_plan_name_type(self):
        """Test validation fails for non-string plan name."""
        data = {
            'client_name': 'John',
            'plan_name': 123,
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        }
        with pytest.raises(ValueError, match="Plan name must be"):
            validate_subscription_data(data)

    @pytest.mark.negative
    def test_validate_subscription_data_invalid_start_date_format(self):
        """Test validation fails for invalid start date format."""
        data = {
            'client_name': 'John',
            'plan_name': 'Basic',
            'start_date': '01-01-2024',  # Invalid format
            'end_date': '2024-12-31'
        }
        with pytest.raises(ValueError, match="start_date must be"):
            validate_subscription_data(data)

    @pytest.mark.negative
    def test_validate_subscription_data_invalid_end_date_type(self):
        """Test validation fails for non-date end date."""
        data = {
            'client_name': 'John',
            'plan_name': 'Basic',
            'start_date': '2024-01-01',
            'end_date': 12345  # Invalid type
        }
        with pytest.raises(ValueError, match="end_date must be"):
            validate_subscription_data(data)

    def test_validate_subscription_data_update_mode(self):
        """Test validation in update mode allows partial data."""
        data = {'plan_name': 'Premium'}
        validate_subscription_data(data, update=True)


class TestValidateTrainerData:
    """Test trainer data validation."""

    def test_validate_trainer_data_valid(self):
        """Test validation passes for valid trainer data."""
        data = {
            'name': 'John Smith',
            'specialization': 'Strength Training',
            'experience_years': 10,
            'email': 'john@example.com'
        }
        validate_trainer_data(data)

    @pytest.mark.negative
    def test_validate_trainer_data_missing_name(self):
        """Test validation fails for missing name in create mode."""
        data = {
            'specialization': 'Fitness',
            'experience_years': 5,
            'email': 'trainer@example.com'
        }
        with pytest.raises(ValueError, match="Missing required field"):
            validate_trainer_data(data)

    @pytest.mark.negative
    def test_validate_trainer_data_invalid_name_empty(self):
        """Test validation fails for empty name."""
        data = {
            'name': '',
            'specialization': 'Fitness',
            'experience_years': 5,
            'email': 'trainer@example.com'
        }
        with pytest.raises(ValueError, match="Name must be"):
            validate_trainer_data(data)

    @pytest.mark.negative
    def test_validate_trainer_data_invalid_experience_negative(self):
        """Test validation fails for negative experience years."""
        data = {
            'name': 'John Smith',
            'specialization': 'Fitness',
            'experience_years': -2,
            'email': 'john@example.com'
        }
        with pytest.raises(ValueError, match="Experience years must be"):
            validate_trainer_data(data)

    @pytest.mark.negative
    def test_validate_trainer_data_invalid_email_format(self):
        """Test validation fails for invalid email format."""
        data = {
            'name': 'John Smith',
            'specialization': 'Fitness',
            'experience_years': 5,
            'email': 'invalid-email'
        }
        with pytest.raises(ValueError, match="Invalid email format"):
            validate_trainer_data(data)

    def test_validate_trainer_data_update_mode(self):
        """Test validation in update mode allows partial data."""
        data = {'experience_years': 8}
        validate_trainer_data(data, update=True)

    def test_validate_trainer_data_optional_fields(self):
        """Test validation passes with optional fields omitted."""
        data = {
            'name': 'Jane Doe',
            'specialization': None,
            'experience_years': None,
            'email': None
        }
        validate_trainer_data(data)
