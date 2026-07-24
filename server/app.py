"""Flask application and API routes for the workout tracking backend."""

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from server.errors import error_response
from server.models import Exercise, Workout, WorkoutExercise, db
from server.schemas import ExerciseSchema, WorkoutExerciseSchema, WorkoutSchema

app = Flask(__name__)
# Store the app configuration in one place so the database and JSON behavior are consistent.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False

app.json.sort_keys = False

migrate = Migrate(app, db)
db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


@app.route("/", methods=["GET"])
def home():
    return make_response(
        jsonify(
            {
                "message": "Workout API is running",
                "status": "ok",
                "endpoints": [
                    "GET /workouts",
                    "GET /workouts/<id>",
                    "POST /workouts",
                    "DELETE /workouts/<id>",
                    "GET /exercises",
                    "GET /exercises/<id>",
                    "POST /exercises",
                    "DELETE /exercises/<id>",
                    "POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises",
                ],
            }
        ),
        200,
    )


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    try:
        payload = workout_schema.load(data)
    except ValidationError as exc:
        return error_response("Invalid workout payload", 400)

    workout = Workout(**payload)
    try:
        db.session.add(workout)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        return make_response(jsonify({"error": str(exc)}), 400)

    return make_response(jsonify(workout_schema.dump(workout)), 201)


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout deleted"}), 200)


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    try:
        payload = exercise_schema.load(data)
    except ValidationError as exc:
        return error_response("Invalid exercise payload", 400)

    exercise = Exercise(**payload)
    try:
        db.session.add(exercise)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        return make_response(jsonify({"error": str(exc)}), 400)

    return make_response(jsonify(exercise_schema.dump(exercise)), 201)


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise deleted"}), 200)


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_workout_exercise(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    data = request.get_json() or {}
    payload = {
        "workout_id": workout.id,
        "exercise_id": exercise.id,
        **data,
    }
    try:
        validated_payload = workout_exercise_schema.load(payload)
    except ValidationError as exc:
        return error_response("Invalid workout exercise payload", 400)

    existing = WorkoutExercise.query.filter_by(workout_id=workout.id, exercise_id=exercise.id).first()
    if existing:
        return make_response(jsonify({"error": "Exercise already added to workout"}), 400)

    workout_exercise = WorkoutExercise(**validated_payload)
    try:
        db.session.add(workout_exercise)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        return make_response(jsonify({"error": str(exc)}), 400)

    return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
