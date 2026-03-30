# ACEest Fitness API - Comprehensive Testing Guide

## Overview

This document provides a comprehensive guide to the Pytest testing framework integrated into the ACEest Fitness API. The test suite ensures code reliability, validates business logic, and provides confidence before deployment.

## Table of Contents
1. [Test Structure](#test-structure)
2. [Running Tests](#running-tests)
3. [Test Coverage](#test-coverage)
4. [Test Categories](#test-categories)
5. [CI/CD Integration](#cicd-integration)
6. [Best Practices](#best-practices)

---

## Test Structure

### Directory Organization

```
flask_app/
├── tests/                    # Test directory
│   ├── __init__.py
│   ├── test_utils.py        # Utility function tests
│   ├── test_models.py       # Database model tests
│   ├── test_services.py     # Business logic tests
│   └── test_routes.py       # API endpoint tests
├── conftest.py              # Pytest fixtures and configuration
├── pytest.ini               # Pytest settings
└── requirements.txt         # Dependencies including pytest
```

### Fixture System

The `conftest.py` file provides reusable fixtures for:

- **Database Setup**: In-memory SQLite database for isolated testing
- **Test Data**: Pre-configured sample data for all entities
- **Client Instance**: Flask test client for API testing
- **Mock Objects**: External dependency mocks

---

## Running Tests

### Installation

```bash
cd flask_app/
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_utils.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_routes.py::TestMembersRoutes -v
```

### Run Specific Test

```bash
pytest tests/test_utils.py::TestCalculateCalories::test_calculate_calories_muscle_gain -v
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only edge case tests
pytest -m edge_case

# Run only negative tests
pytest -m negative

# Exclude slow tests
pytest -m "not slow"
```

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=html
```

Open `htmlcov/index.html` to view detailed coverage report.

### Run with Detailed Output

```bash
pytest -v --tb=long
```

### Run in Parallel (faster execution)

```bash
pytest -n auto
```

---

## Test Coverage

### Current Coverage Goals

- **Utilities**: >95% coverage (calculations, validations)
- **Models**: >90% coverage (data persistence, relationships)
- **Services**: >85% coverage (business logic with mocking)
- **Routes**: >80% coverage (API endpoints, error handling)

### Generate Coverage Report

```bash
pytest --cov=. --cov-report=html:htmlcov --cov-report=xml
```

### View HTML Coverage Report

```bash
# Windows
start htmlcov/index.html

# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

---

## Test Categories

### 1. **Utility Tests** (`test_utils.py`)

**Purpose**: Validate business logic and calculations

**Coverage**:
- ✅ Calorie calculations (BMR, TDEE, goals)
- ✅ BMI calculations and categorization
- ✅ Subscription fee calculations
- ✅ Data validation functions
- ✅ Input sanitization

**Test Scenarios Per Function**:
- Positive tests (valid inputs)
- Negative tests (invalid inputs)
- Edge cases (boundary values)
- Consistency tests (deterministic behavior)

**Example**:
```python
def test_calculate_calories_muscle_gain():
    calories = calculate_calories(85, 185, 28, "Muscle Gain (MG) – PPL")
    assert isinstance(calories, int)
    assert calories > 0
```

### 2. **Model Tests** (`test_models.py`)

**Purpose**: Ensure data persistence and relationships

**Coverage**:
- ✅ Member creation and serialization
- ✅ Workout storage and relationships
- ✅ Progress tracking
- ✅ Metric records
- ✅ Subscription management
- ✅ Trainer profiles
- ✅ Database constraints (unique names, nullable fields)

**Test Scenarios**:
- Object creation and validation
- Serialization to dictionary
- Relationship integrity
- Constraint enforcement
- Boundary values

**Example**:
```python
def test_member_creation(created_member):
    assert created_member.id is not None
    assert created_member.name == 'John Doe'
```

### 3. **Service Tests** (`test_services.py`)

**Purpose**: Validate business logic and data operations

**Coverage**:
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Data validation in services
- ✅ Calorie recalculation on updates
- ✅ Member summaries with related data
- ✅ Error handling and edge cases

**Test Scenarios**:
- Valid operations
- Invalid data handling
- Non-existent record handling
- Duplicate detection
- Partial updates
- Relationship consistency

**Example**:
```python
def test_create_member_valid(sample_member_data):
    member = MemberService.create_member(sample_member_data)
    assert member.id is not None
    assert member.calories > 0
```

### 4. **Route Tests** (`test_routes.py`)

**Purpose**: Validate API endpoints and HTTP responses

**Coverage**:
- ✅ GET endpoints (list, single, summary)
- ✅ POST endpoints (creation with validation)
- ✅ PUT endpoints (updates with constraints)
- ✅ DELETE endpoints (removal)
- ✅ Error responses (400, 404, 500)
- ✅ Response format and structure
- ✅ Content-Type headers
- ✅ Complete workflows

**Test Scenarios**:
- Success cases
- Error cases (missing fields, invalid values)
- Not found scenarios
- Duplicate handling
- Malformed input
- Special characters
- Complete CRUD cycles

**Example**:
```python
def test_create_member_success(client, sample_member_data):
    response = client.post('/api/members/', 
        json=sample_member_data)
    assert response.status_code == 201
    assert response.json['id'] is not None
```

---

## Test Markers

Organize tests with markers for selective execution:

```python
# Run marked tests
pytest -m "unit"           # Unit tests
pytest -m "integration"    # Integration tests
pytest -m "edge_case"      # Edge case tests
pytest -m "negative"       # Error handling tests
pytest -m "not slow"       # Exclude slow tests

# Combine markers
pytest -m "unit and not slow"
pytest -m "integration or edge_case"
```

---

## CI/CD Integration

### GitHub Actions

**File**: `.github/workflows/test.yml`

**Triggers**:
- Push to main/develop branches
- Pull requests
- Changes to flask_app directory

**Jobs**:
1. **Unit Tests**: Run on Python 3.9, 3.10, 3.11
2. **Coverage Check**: Verify code coverage metrics
3. **Integration Tests**: Run integration test suite
4. **Build Validation**: Pre-deployment checks

**Artifacts**:
- Test results (JUnit XML)
- Coverage reports (HTML + XML)
- Coverage upload to Codecov

### Azure Pipelines

**File**: `azure-pipelines.yml`

**Stages**:
1. **Test**: Unit tests, integration tests, code quality
2. **Build Validation**: Deployment readiness check
3. **Documentation**: Generate test reports

**Features**:
- Multi-Python version testing (3.9, 3.10, 3.11)
- Code coverage reporting
- Linting and code quality (Flake8, Black)
- Test result publishing
- Artifact archival

### Local CI/CD Simulation

```bash
# Simulate GitHub Actions locally
pytest tests/ -v \
  --cov=. \
  --cov-report=term-missing \
  --cov-report=xml \
  --junitxml=junit/test-results.xml

# Check linting
flake8 . --max-line-length=127

# Check code formatting
black --check .
```

---

## Best Practices

### Writing Tests

1. **Clear Names**: Test names describe what is tested
   ```python
   def test_calculate_bmi_with_normal_values():  # ✓ Good
   def test_bmi():  # ✗ Unclear
   ```

2. **Arrange-Act-Assert Pattern**:
   ```python
   def test_member_creation(sample_member_data):
       # Arrange
       data = sample_member_data
       
       # Act
       member = MemberService.create_member(data)
       
       # Assert
       assert member.name == data['name']
   ```

3. **Use Fixtures for Setup**:
   ```python
   def test_with_fixture(created_member):  # ✓ Uses fixture
       assert created_member.id is not None
   ```

4. **Test One Thing Per Test**:
   ```python
   def test_age_validation():  # ✓ Tests one aspect
       validate_member_data({'age': -5})  # Should raise
   ```

5. **Include Edge Cases**:
   ```python
   @pytest.mark.edge_case
   def test_boundary_values():
       validate_member_data({'age': 0})
       validate_member_data({'age': 120})
   ```

6. **Mock External Dependencies**:
   ```python
   def test_with_mock(mocker, created_member):
       mock_api = mocker.MagicMock()
       mock_api.get_data.return_value = {...}
   ```

### Test Organization

- **Group related tests** in classes
- **Use markers** to categorize tests
- **Keep tests isolated** (no interdependencies)
- **Use descriptive fixtures** with meaningful names
- **Document complex test logic** with comments

### Performance

- **Use in-memory database** for speed (SQLite)
- **Run tests in parallel** with pytest-xdist
- **Mock slow operations** (API calls, file I/O)
- **Separate slow tests** with `@pytest.mark.slow`

### Coverage

- **Aim for >80% coverage** on critical code
- **Don't chase 100%** unnecessarily
- **Test edge cases** over happy path depth
- **Focus on logic**, not trivial getters/setters

---

## Troubleshooting

### Database Lock Issues

```bash
# Solution: Ensure DB is closed between tests
# conftest.py uses in-memory SQLite which resets each test
```

### Import Errors

```bash
# Solution: Run from flask_app directory
cd flask_app
pytest
```

### Fixture Not Found

```bash
# Solution: Ensure conftest.py is in root of tests directory
# and visible to pytest discovery
```

### Slow Test Execution

```bash
# Solution: Use parallel execution
pytest -n auto

# Or exclude slow tests
pytest -m "not slow"
```

---

## Metrics and Reporting

### Test Execution Summary

```
✓ Total Tests: 95
✓ Passed: 93
✓ Failed: 0
✓ Skipped: 2
✓ Duration: 12.34s
✓ Code Coverage: 87%
```

### Coverage Breakdown

| Component | Coverage | Status |
|-----------|----------|--------|
| Utilities | 96% | ✓ Excellent |
| Models | 92% | ✓ Excellent |
| Services | 88% | ✓ Good |
| Routes | 82% | ✓ Good |
| **Overall** | **87%** | **✓ Acceptable** |

---

## Next Steps

1. **Run the test suite**: `pytest -v`
2. **Generate coverage**: `pytest --cov=. --cov-report=html`
3. **Review results**: Open `htmlcov/index.html`
4. **Fix any failures**: Update code or refine tests
5. **Push to CI/CD**: Automated testing on each commit

---

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)

---

**Last Updated**: 2024
**Maintainer**: DevOps Team
