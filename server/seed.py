#!/usr/bin/env python3
import os
import sys
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.app import app
from server.models import Exercise, Workout, WorkoutExercise, db


with app.app_context():
    db.drop_all()
    db.create_all()

    chest_press = Exercise(name="Bench Press", category="Chest", equipment_needed=True)
    squat = Exercise(name="Back Squat", category="Legs", equipment_needed=True)
    row = Exercise(name="Bent Over Row", category="Back", equipment_needed=True)
    plank = Exercise(name="Plank", category="Core", equipment_needed=False)

    workout_one = Workout(date=date(2026, 7, 24), duration_minutes=45, notes="Upper body focus")
    workout_two = Workout(date=date(2026, 7, 25), duration_minutes=60, notes="Lower body strength")

    db.session.add_all([chest_press, squat, row, plank, workout_one, workout_two])
    db.session.commit()

    db.session.add_all(
        [
            WorkoutExercise(workout_id=workout_one.id, exercise_id=chest_press.id, reps=10, sets=3, duration_seconds=90),
            WorkoutExercise(workout_id=workout_one.id, exercise_id=row.id, reps=12, sets=3, duration_seconds=60),
            WorkoutExercise(workout_id=workout_two.id, exercise_id=squat.id, reps=8, sets=4, duration_seconds=120),
            WorkoutExercise(workout_id=workout_two.id, exercise_id=plank.id, reps=1, sets=3, duration_seconds=60),
        ]
    )
    db.session.commit()
