import unittest

from server.app import app, db
from server.models import Exercise, Workout


class WorkoutApiTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_create_exercise_and_workout(self):
        response = self.client.post(
            "/exercises",
            json={"name": "Bench Press", "category": "Chest", "equipment_needed": True},
        )
        self.assertEqual(response.status_code, 201)

        workout_response = self.client.post(
            "/workouts",
            json={"date": "2026-07-24", "duration_minutes": 45, "notes": "Upper body focus"},
        )
        self.assertEqual(workout_response.status_code, 201)

    def test_add_exercise_to_workout(self):
        with app.app_context():
            exercise = Exercise(name="Deadlift", category="Legs", equipment_needed=True)
            workout = Workout(date="2026-07-24", duration_minutes=40, notes="Leg day")
            db.session.add_all([exercise, workout])
            db.session.commit()
            exercise_id = exercise.id
            workout_id = workout.id

        response = self.client.post(
            f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
            json={"reps": 8, "sets": 3, "duration_seconds": 60},
        )
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
