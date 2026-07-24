# Workout Application Backend

This project implements a Flask + SQLAlchemy + Marshmallow API for tracking workouts and reusable exercises.

## Installation

```bash
pipenv install
pipenv shell
```

## Database setup

```bash
flask --app server.app db init
flask --app server.app db migrate -m "Initial migration"
flask --app server.app db upgrade head
python server/seed.py
```

## Run the app

```bash
flask --app server.app run
```

## API health check

Visit the root route to confirm the service is up:

```bash
GET /
```

## Resetting the database

To reseed the database from scratch, run:

```bash
python server/seed.py
```

## Endpoints

- GET /workouts - list all workouts
- GET /workouts/<id> - retrieve a workout by id
- POST /workouts - create a new workout
- DELETE /workouts/<id> - delete a workout and its linked workout exercises
- GET /exercises - list all exercises
- GET /exercises/<id> - retrieve an exercise by id
- POST /exercises - create a new exercise
- DELETE /exercises/<id> - delete an exercise and its linked workout exercises
- POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - add an exercise to a workout
