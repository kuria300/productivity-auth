from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Exercise, Workout, WorkoutExercise
from app.schemas.tableschema import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema
from marshmallow import ValidationError

exercise_bp=Blueprint('exercise_api', __name__)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
we_schema = WorkoutExerciseSchema()

#fetch exercises
@exercise_bp.route('/exercises', methods=['GET'])
def get_workouts():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

#fetch one 
@exercise_bp.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error':'exercise does not exist'}), 404

    return jsonify(exercise_schema.dump(exercise)), 200

#create 
@exercise_bp.route('/exercises', methods=['POST'])
def post_exercises():
    data=request.get_json()
    try:
        validated_data=exercise_schema.load(data)

        new_exercise = Exercise(
            name=validated_data.get('name'),
            category=validated_data.get('category'),
            equipment_needed=validated_data.get('equipment_needed')
        )
        db.session.add(new_exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(new_exercise)),201
    except ValidationError as err:
        return jsonify({'errors':err.messages}), 400


#delete one
@exercise_bp.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error':'exercise does not exist'}), 404

    db.session.delete(exercise)
    db.session.commit()

    return '', 204

@exercise_bp.route('/workouts/<int:w_id>/exercises/<int:e_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(w_id, e_id):
    data=request.get_json()
    try:
        if not data:
            return jsonify({'error':'no data available'})
        validated_data = we_schema.load(data)
        
        new_link = WorkoutExercise(
        reps=validated_data.get('reps'),
        sets=validated_data.get('sets'),
        duration_seconds=validated_data.get('duration_seconds'),
        workout_id=w_id,
        exercise_id=e_id
        )
        
        db.session.add(new_link)
        db.session.commit()
        return jsonify(we_schema.dump(new_link)), 201
    except ValidationError as err:
        return jsonify({'errors':err.messages}), 400

