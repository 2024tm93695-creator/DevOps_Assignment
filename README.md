# DevOps Assignment — ACEest Fitness API

A Flask-based fitness tracking API with a full DevOps pipeline: GitHub Actions CI/CD and Jenkins BUILD & Quality Gate.

---

## Jenkins BUILD & Quality Gate Integration

Jenkins acts as a **secondary validation layer** — it pulls the latest code from GitHub, performs a clean build, runs linting, unit tests, enforces a 60% coverage quality gate, and builds the Docker image.

### Pipeline Stages (defined in `Jenkinsfile`)

| # | Stage | What it does |
|---|-------|-------------|
| 1 | **Checkout** | Pulls latest code from `main` branch |
| 2 | **Clean Environment** | Removes `__pycache__`, `.pyc`, stale reports |
| 3 | **Install Dependencies** | `pip install -r requirements.txt` + lint tools |
| 4 | **Code Quality** | Flake8 lint + Black format check (parallel) |
| 5 | **Build Validation** | Imports Flask app — confirms it instantiates cleanly |
| 6 | **Unit Tests** | Pytest with coverage HTML + XML + JUnit XML |
| 7 | **Quality Gate** | Fails build if coverage < 60% |
| 8 | **Docker Build** | Builds `aceest-fitness-api:latest` image |

---

### Step 1 — Start Jenkins with Docker

The project ships a ready-to-use Jenkins stack (`docker-compose.jenkins.yml`):

```bash
# Start Jenkins (first boot takes ~2 min to install plugins)
docker-compose -f docker-compose.jenkins.yml up -d

# Watch startup logs
docker logs -f aceest-jenkins
```

Access Jenkins at **http://localhost:8080**
- Username: `admin`
- Password: `admin123`

> Change the password immediately after first login via **Manage Jenkins > Users**.

---

### Step 2 — Verify the Pipeline Job

The init script (`jenkins/init.groovy.d/02-create-pipeline-job.groovy`) automatically creates the **ACEest-Build-Quality-Gate** pipeline job on first boot.

To verify:
1. Open http://localhost:8080
2. You should see the job **ACEest-Build-Quality-Gate** on the dashboard.
3. Click it → **Build Now** to trigger a manual build.

If the job is missing, create it manually (see Step 3).

---

### Step 3 — Manually Create the Pipeline Job (if needed)

1. Click **New Item** on the Jenkins dashboard.
2. Enter name: `ACEest-Build-Quality-Gate`
3. Select **Pipeline** → click **OK**.
4. Under **General**:
   - Check **Discard old builds** → Keep max 10 builds.
5. Under **Build Triggers**:
   - Check **GitHub hook trigger for GITScm polling** (for webhooks).
   - Also check **Poll SCM** with schedule `H/5 * * * *` (fallback polling).
6. Under **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/2024tm93695-creator/DevOps_Assignment.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
   - Check **Lightweight checkout**.
7. Click **Save** → **Build Now**.

---

### Step 4 — Install Required Plugins

Go to **Manage Jenkins > Plugins > Available** and install (or let the Docker init install them from `jenkins/plugins.txt`):

- `Git`, `GitHub`, `GitHub Branch Source`
- `Pipeline`, `Pipeline Stage View`, `Blue Ocean`
- `JUnit`, `HTML Publisher`, `Cobertura`
- `Docker Pipeline`, `Docker Commons`
- `Timestamper`, `Build Timeout`, `Workspace Cleanup`

---

### Step 5 — Configure GitHub Webhook

So Jenkins triggers automatically on every push to `main`:

1. Go to your GitHub repo → **Settings > Webhooks > Add webhook**.
2. Payload URL: `http://<your-jenkins-host>:8080/github-webhook/`
   - For local Jenkins use [ngrok](https://ngrok.com): `ngrok http 8080` then use the HTTPS URL.
3. Content type: `application/json`
4. Events: **Just the push event**.
5. Click **Add webhook**.

In Jenkins, on the job → **Configure** → **Build Triggers** → enable **GitHub hook trigger for GITScm polling**.

---

### Step 6 — Add GitHub Credentials (for private repos)

1. **Manage Jenkins > Credentials > System > Global > Add Credentials**.
2. Kind: **Username with password** (or **Secret text** for a token).
3. Username: your GitHub username.
4. Password: GitHub Personal Access Token (PAT) with `repo` scope.
5. ID: `github-credentials`
6. In the pipeline job SCM config, select these credentials.

---

### Step 7 — Monitor Builds

- **Dashboard**: http://localhost:8080 — see build history and status.
- **Stage View**: Click any build → view per-stage pass/fail.
- **Console Output**: Click a build number → **Console Output** for full logs.
- **Coverage Report**: Published as HTML artifact after Unit Tests stage.
- **Test Results**: JUnit XML results published after Unit Tests stage.

Build status meanings:

| Icon | Status |
|------|--------|
| Blue | Success — all stages passed, quality gate passed |
| Red | Failure — check Quality Gate or test stage |
| Yellow | Unstable — tests ran but some failed |

---

### Quality Gate Details

The **Quality Gate** stage (Stage 7 in `Jenkinsfile`) reads `coverage.xml` after tests and:
- Calculates the overall line coverage percentage.
- **Fails the build** if coverage is below **60%**.
- Prints `QUALITY GATE PASSED` or `QUALITY GATE FAILED` in the console.

To change the threshold, edit `COVERAGE_MIN` in the `Jenkinsfile` environment block:

```groovy
environment {
    COVERAGE_MIN = '60'   // change this value (percentage)
}
```

---

### Project Structure

```
DevOps_Assignment/
├── Jenkinsfile                    # Jenkins pipeline definition (8 stages)
├── Dockerfile                     # Multi-stage Docker build
├── docker-compose.jenkins.yml     # Jenkins server Docker Compose
├── docker-compose.yml             # App Docker Compose
├── jenkins/
│   ├── plugins.txt                # Auto-installed Jenkins plugins
│   └── init.groovy.d/
│       ├── 01-security.groovy     # Admin user + security setup
│       └── 02-create-pipeline-job.groovy  # Auto-creates pipeline job
├── flask_app/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   └── tests/
│       ├── test_models.py
│       ├── test_routes.py
│       ├── test_services.py
│       └── test_utils.py
└── .github/
    └── workflows/
        └── main.yml               # GitHub Actions CI/CD (parallel pipeline)
```

---

### Stopping Jenkins

```bash
docker-compose -f docker-compose.jenkins.yml down

# To also remove all data (full reset):
docker-compose -f docker-compose.jenkins.yml down -v
```
