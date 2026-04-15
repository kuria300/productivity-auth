from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Exercise, Workout
from app.schemas.tableschema import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema
from marshmallow import ValidationError

workout_bp=Blueprint('workout_api', __name__)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
#for many entries
exercises_schema = ExerciseSchema(many=True)
we_schema = WorkoutExerciseSchema()

#fetch workouts
@workout_bp.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

#create workout
@workout_bp.route('/workouts', methods=['POST'])
def post_workouts():
    data=request.get_json()
    try:
        validated_data=workout_schema.load(data)

        new_workout = Workout(
            date=validated_data.get('date'),
            duration_minutes=validated_data.get('duration_minutes'),
            notes=validated_data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()

        return jsonify(workout_schema.dump(new_workout)),201
    except ValidationError as err:
        return jsonify({'errors':err.messages}), 400

#get one workout
@workout_bp.route('/workouts/<int:id>', methods=['GET'])
def get_one_workout(id):
    workout=Workout.query.filter_by(id=id).first()

    return jsonify(workout_schema.dump(workout)), 200

#delete one
@workout_bp.route('/workouts/<int:id>', methods=['DELETE'])
def delete_one_workout(id):
    #cascade deletes all data from child too
    workout = Workout.query.get(id)
    db.session.delete(workout)
    db.session.commit() 
    return '', 204



