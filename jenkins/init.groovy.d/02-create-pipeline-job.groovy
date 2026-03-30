// Jenkins init script — creates the ACEest pipeline job automatically
import jenkins.model.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import hudson.plugins.git.*
import hudson.triggers.*

def instance = Jenkins.getInstance()

// ── Job configuration ────────────────────────────────────────
def jobName        = 'ACEest-Build-Quality-Gate'
def repoUrl        = 'https://github.com/2024tm93695-creator/DevOps_Assignment.git'
def branch         = '*/main'
def jenkinsfilePath = 'Jenkinsfile'

// Skip if job already exists
if (instance.getItem(jobName)) {
    println "✔ Pipeline job '${jobName}' already exists — skipping"
    return
}

// ── Create Pipeline job ──────────────────────────────────────
def job = instance.createProject(WorkflowJob, jobName)
job.setDescription('ACEest Fitness API — BUILD & Quality Gate pipeline')

// Configure SCM (Git) to use the repo Jenkinsfile
def gitSCM = new GitSCM(
    GitSCM.createRepoList(repoUrl, null),
    [new BranchSpec(branch)],
    false, [], null, null, []
)

def flowDefinition = new CpsScmFlowDefinition(gitSCM, jenkinsfilePath)
flowDefinition.setLightweight(true)
job.setDefinition(flowDefinition)

// ── Build Triggers — Poll SCM every 5 min (fallback if webhook not set) ──
job.addTrigger(new SCMTrigger('H/5 * * * *'))

// ── Discard old builds ───────────────────────────────────────
job.setBuildDiscarder(
    new hudson.tasks.LogRotator(-1, 10, -1, -1)
)

job.save()
instance.save()

println "✔ Pipeline job '${jobName}' created successfully"
println "   Repo   : ${repoUrl}"
println "   Branch : ${branch}"
