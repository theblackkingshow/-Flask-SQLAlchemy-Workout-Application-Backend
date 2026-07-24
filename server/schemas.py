"""Marshmallow schemas for validating and serializing workout API payloads."""

from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    category = fields.Str(required=True, validate=validate.OneOf(["Chest", "Back", "Legs", "Shoulders", "Arms", "Core", "Cardio", "Full Body"]))
    equipment_needed = fields.Bool(required=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(required=True, validate=validate.Range(min=1))
    sets = fields.Int(required=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(required=True, validate=validate.Range(min=0))


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)
    exercises = fields.List(fields.Nested(ExerciseSchema), dump_only=True)
