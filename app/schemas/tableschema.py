from app.extensions import ma
from marshmallow import fields, validate


class ExerciseSchema(ma.Schema):
    id=fields.Integer(dump_only=True)
    name=fields.String(required=True, validate=validate.Length(min=2, max=100))
    category=fields.String(validate=validate.OneOf(["Strength", "Cardio", "Calisthenics"]))
    equipment_needed=fields.Boolean(required=True)


class WorkoutExerciseSchema(ma.Schema):
    id =fields.Integer(dump_only=True)
    reps=fields.Integer(validate=validate.Range(min=1,error="Reps must be at least 1"))
    sets=fields.Integer(validate=validate.Range(min=1,error="Sets must be at least 1"))
    duration_seconds =fields.Integer(validate=validate.Range(min=1, error='Durstion must be at least 1'))
    
    # which workout and which exercise are being connected
    workout_id = fields.Int(load_only=True)
    exercise_id = fields.Int(load_only=True)
    
    #When you view a workout, you get a list of every exercise in it.
    exercise=fields.Nested(ExerciseSchema, only=("name", "category"), dump_only=True)

class WorkoutSchema(ma.Schema):
    id=fields.Integer(dump_only=True)
    date=fields.Date(required=True)
    duration_minutes= fields.Integer(validate=validate.Range(min=1))
    notes=fields.String(validate=validate.Length(max=500))

    # a workout has many exercises
    exercise_link=fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

