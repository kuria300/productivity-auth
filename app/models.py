from app.extensions import db

class Exercise(db.Model):
    __tablename__='exercises'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    category=db.Column(db.String())
    equipment_needed=db.Column(db.Boolean)

    workout_link=db.relationship('WorkoutExercise', back_populates='exercise', cascade='delete, delete-orphan')

    def __repr__(self):
        return f'Exercise=(name={self.name}, category={self.category})'


class Workout(db.Model):
    __tablename__='workouts'

    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date)
    duration_minutes=db.Column(db.Integer)
    notes=db.Column(db.Text)

    exercise_link=db.relationship('WorkoutExercise', back_populates='workout', cascade='delete, delete-orphan')

    def __repr__(self):
        return f'Workout=(date={self.data}, notes={self.notes})'


class WorkoutExercise(db.Model):
    __tablename__='WorkoutExercises'

    id=db.Column(db.Integer, primary_key=True)
    reps=db.Column(db.Integer)
    sets=db.Column(db.Integer)
    duration_seconds=db.Column(db.Integer)

    workout_id=db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id=db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    workout=db.relationship('Workout', back_populates='exercise_link')
    exercise=db.relationship('Exercise', back_populates='workout_link')

