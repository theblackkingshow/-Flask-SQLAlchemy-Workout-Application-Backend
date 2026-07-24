import unittest

from server.app import app, db
from server.models import Exercise, Workout


class ErrorHandlingTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_invalid_workout_payload_returns_error(self):
        response = self.client.post("/workouts", json={"date": "bad-date"})
        self.assertEqual(response.status_code, 400)

    def test_invalid_exercise_payload_returns_error(self):
        response = self.client.post("/exercises", json={"name": "A"})
        self.assertEqual(response.status_code, 400)

    def test_malformed_json_returns_json_error(self):
        response = self.client.post(
            "/workouts",
            data='{"date":',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
