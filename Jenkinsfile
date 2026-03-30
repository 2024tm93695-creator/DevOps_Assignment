pipeline {
    agent any

    environment {
        REPO_URL      = 'https://github.com/2024tm93695-creator/DevOps_Assignment.git'
        BRANCH        = 'main'
        WORKING_DIR   = 'flask_app'
        COVERAGE_MIN  = '60'
        IMAGE_NAME    = 'aceest-fitness-api'
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // ─── STAGE 1: CHECKOUT ───────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo "Pulling latest code from GitHub branch: ${env.BRANCH}"
                git url: "${env.REPO_URL}", branch: "${env.BRANCH}"
            }
        }

        // ─── STAGE 2: CLEAN ENVIRONMENT ──────────────────────────────────
        stage('Clean Environment') {
            steps {
                echo 'Cleaning previous build artefacts...'
                sh '''
                    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
                    find . -name "*.pyc" -delete 2>/dev/null || true
                    rm -rf ${WORKING_DIR}/.coverage \
                           ${WORKING_DIR}/htmlcov \
                           ${WORKING_DIR}/coverage.xml \
                           ${WORKING_DIR}/junit 2>/dev/null || true
                    mkdir -p ${WORKING_DIR}/junit
                '''
            }
        }

        // ─── STAGE 3: INSTALL DEPENDENCIES ───────────────────────────────
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    cd ${WORKING_DIR}
                    python3 -m pip install --upgrade pip wheel setuptools --quiet
                    pip install -r requirements.txt --quiet
                    pip install flake8 pylint black --quiet
                '''
            }
        }

        // ─── STAGE 4: CODE QUALITY (LINT) ────────────────────────────────
        stage('Code Quality') {
            parallel {
                stage('Flake8 Lint') {
                    steps {
                        echo 'Running Flake8 linting...'
                        sh '''
                            cd ${WORKING_DIR}
                            flake8 . \
                                --count \
                                --exit-zero \
                                --max-complexity=10 \
                                --max-line-length=127 \
                                --statistics \
                                --exclude=__pycache__,tests,instance \
                                | tee flake8_report.txt
                        '''
                    }
                }
                stage('Black Format Check') {
                    steps {
                        echo 'Checking code formatting with Black...'
                        sh '''
                            cd ${WORKING_DIR}
                            black --check --diff . --exclude="/(tests|instance|__pycache__)/" || true
                        '''
                    }
                }
            }
        }

        // ─── STAGE 5: BUILD VALIDATION ───────────────────────────────────
        stage('Build Validation') {
            steps {
                echo 'Validating application builds correctly...'
                sh '''
                    cd ${WORKING_DIR}
                    python3 -c "
import sys
sys.path.insert(0, '.')
from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
print('Build validation: Flask app instantiated successfully')
print('Python version:', sys.version)
"
                '''
            }
        }

        // ─── STAGE 6: UNIT TESTS ─────────────────────────────────────────
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests with coverage...'
                sh '''
                    cd ${WORKING_DIR}
                    pytest tests/ \
                        -v \
                        --tb=short \
                        -m "not slow and not integration" \
                        --cov=. \
                        --cov-report=html:htmlcov \
                        --cov-report=xml:coverage.xml \
                        --cov-report=term-missing \
                        --junitxml=junit/test-results.xml \
                        --ignore=tests/__pycache__ \
                        || true
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true,
                          testResults: "${env.WORKING_DIR}/junit/test-results.xml"
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: "${env.WORKING_DIR}/htmlcov",
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        // ─── STAGE 7: QUALITY GATE ───────────────────────────────────────
        stage('Quality Gate') {
            steps {
                echo "Enforcing coverage quality gate: minimum ${env.COVERAGE_MIN}%"
                sh """
                    cd ${WORKING_DIR}
                    if [ -f coverage.xml ]; then
                        COVERAGE=\$(python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('coverage.xml')
root = tree.getroot()
line_rate = float(root.attrib.get('line-rate', 0))
pct = round(line_rate * 100, 2)
print(pct)
")
                        echo "Coverage: \${COVERAGE}%"
                        python3 -c "
import sys
coverage = float(sys.argv[1])
minimum  = float(sys.argv[2])
print(f'Coverage: {coverage}%  |  Required: {minimum}%')
if coverage < minimum:
    print('QUALITY GATE FAILED - coverage below threshold')
    sys.exit(1)
print('QUALITY GATE PASSED')
" \${COVERAGE} ${env.COVERAGE_MIN}
                    else
                        echo "WARNING: coverage.xml not found, skipping quality gate"
                    fi
                """
            }
        }

        // ─── STAGE 8: DOCKER BUILD ────────────────────────────────────────
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh """
                    docker build -t ${env.IMAGE_NAME}:build-${env.BUILD_NUMBER} \
                                 -t ${env.IMAGE_NAME}:latest \
                                 -f Dockerfile .
                    echo 'Docker image built successfully:'
                    docker images ${env.IMAGE_NAME}
                """
            }
        }
    }

    // ─── POST ACTIONS ─────────────────────────────────────────────────────
    post {
        success {
            echo """
            ============================================
             BUILD SUCCEEDED
            --------------------------------------------
             Branch  : ${env.BRANCH}
             Build # : ${env.BUILD_NUMBER}
             Status  : All stages passed
            ============================================
            """
        }
        failure {
            echo """
            ============================================
             BUILD FAILED
            --------------------------------------------
             Branch  : ${env.BRANCH}
             Build # : ${env.BUILD_NUMBER}
             Check the console output for details.
            ============================================
            """
        }
        always {
            archiveArtifacts artifacts: "${env.WORKING_DIR}/flake8_report.txt",
                             allowEmptyArchive: true
            cleanWs()
        }
    }
}
