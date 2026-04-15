from app import create_app
from app.extensions import db
from app.models import Exercise, Workout, WorkoutExercise
from faker import Faker
import random
from datetime import date

fake=Faker()
app=create_app()

with app.app_context():
    # Clear existing data first
    db.session.query(WorkoutExercise).delete()
    db.session.query(Exercise).delete()
    db.session.query(Workout).delete()

    gym_exercises = [
    "Bench Press", "Squat", "Deadlift", "Shoulder Press", 
    "Bicep Curl", "Tricep Dip", "Lunges", "Plank", 
    "Pull Up", "Push Up", "Leg Press", "Lat Pulldown"
     ] 

    #exercises
    exercises=[]
    for _ in range(10):
        ex = Exercise(
            name = fake.unique.word(ext_word_list=tuple(gym_exercises)),
            category=random.choice(["Strength", "Cardio", "Calisthenics"]),
            equipment_needed=random.choice([True, False])
        )
        exercises.append(ex)
        db.session.add(ex)
        
    #workouts
    workouts=[]
    for _ in range(5):
        w = Workout(
            date=fake.date_this_month(before_today=True, after_today=False),
            duration_minutes=random.randint(30, 90),
            notes=fake.sentence()
        )
        workouts.append(w)
        db.session.add(w)
    
    db.session.commit()

    for w in workouts:

        # add 3 to workouts
        for ex in random.sample(exercises, 3):

            link = WorkoutExercise(
                workout=w, 
                exercise=ex,
                reps=random.randint(8, 12),
                sets=3, 
                duration_seconds=900
            )
            db.session.add(link)


        
    db.session.commit()
    print('seeding done')
