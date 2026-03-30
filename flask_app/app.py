from flask import Flask
from flask_cors import CORS
from config import Config
from models.database import init_db
# Import models after db init
from routes.members import members_bp
from routes.workouts import workouts_bp
from routes.subscriptions import subscriptions_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
init_db(app)

# Import models after db init
from models import member, progress, workout, metric, trainer, subscription

# Register blueprints
app.register_blueprint(members_bp, url_prefix='/api/members')
app.register_blueprint(workouts_bp, url_prefix='/api/workouts')
app.register_blueprint(subscriptions_bp, url_prefix='/api/subscriptions')

@app.route('/')
def index():
    return {"message": "ACEest Fitness API"}

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)