"""Define the SQLAlchemy models for workouts, exercises, and workout exercise entries."""

from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates


db = SQLAlchemy()


class Exercise(db.Model):
    """A reusable exercise that can be attached to many workouts."""
    __tablename__ = "exercises"
    __table_args__ = (
        db.CheckConstraint("length(name) >= 2", name="ck_exercise_name_length"),
        db.CheckConstraint("category IN ('Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core', 'Cardio', 'Full Body')", name="ck_exercise_category"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan", overlaps="workouts")
    workouts = db.relationship("Workout", secondary="workout_exercises", back_populates="exercises", overlaps="workout_exercises")

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise AssertionError("Exercise name is required")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise AssertionError("Category is required")
        return value.strip()

    def __repr__(self):
        return f"<Exercise {self.name}>"


class Workout(db.Model):
    """A workout session containing multiple exercises and timing details."""
    __tablename__ = "workouts"
    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
        db.CheckConstraint("length(notes) <= 500", name="ck_workout_notes_length"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan", overlaps="exercises")
    exercises = db.relationship("Exercise", secondary="workout_exercises", back_populates="workouts", overlaps="workout_exercises")

    @validates("date")
    def validate_date(self, key, value):
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError as exc:
                raise AssertionError("Date must be a valid date") from exc
        if isinstance(value, date):
            return value
        raise AssertionError("Date must be a valid date")

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise AssertionError("Duration must be greater than zero")
        return value

    @validates("notes")
    def validate_notes(self, key, value):
        if not value or not value.strip():
            raise AssertionError("Notes are required")
        return value.strip()

    def __repr__(self):
        return f"<Workout {self.id}>"


class WorkoutExercise(db.Model):
    """Link table capturing reps, sets, and duration for an exercise within a workout."""
    __tablename__ = "workout_exercises"
    __table_args__ = (
        db.CheckConstraint("reps > 0", name="ck_workout_exercise_reps_positive"),
        db.CheckConstraint("sets > 0", name="ck_workout_exercise_sets_positive"),
        db.CheckConstraint("duration_seconds >= 0", name="ck_workout_exercise_duration_non_negative"),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False, default=0)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps")
    def validate_reps(self, key, value):
        if value <= 0:
            raise AssertionError("Reps must be greater than zero")
        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if value <= 0:
            raise AssertionError("Sets must be greater than zero")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value < 0:
            raise AssertionError("Duration cannot be negative")
        return value

    def __repr__(self):
        return f"<WorkoutExercise workout_id={self.workout_id} exercise_id={self.exercise_id}>"
