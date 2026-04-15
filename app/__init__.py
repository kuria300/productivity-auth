from flask import Flask
from .extensions import db, migrate, ma
from dotenv import load_dotenv
from app.models import Exercise, Workout, WorkoutExercise
from app.routes.exercise_detail import exercise_bp
from app.routes.workout_detail import workout_bp

load_dotenv()
from config import Config

def create_app():
    
    app=Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app=app)
    migrate.init_app(app, db)
    ma.init_app(app)

    app.register_blueprint(workout_bp)
    app.register_blueprint(exercise_bp)

    return app




