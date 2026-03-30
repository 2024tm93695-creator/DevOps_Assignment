// Jenkins init script — runs once on first boot
// Sets up basic security: creates admin user, enables matrix auth
import jenkins.model.*
import hudson.security.*
import jenkins.install.*

def instance = Jenkins.getInstance()

// ── Skip setup wizard ────────────────────────────────────────
instance.setInstallState(InstallState.INITIAL_SETUP_COMPLETED)

// ── Create admin user ────────────────────────────────────────
// Change password via: Manage Jenkins > Users after first login
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount('admin', 'admin123')
instance.setSecurityRealm(hudsonRealm)

// ── Grant admin full permissions ─────────────────────────────
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)

instance.save()
println "✔ Security configured: admin user created"
