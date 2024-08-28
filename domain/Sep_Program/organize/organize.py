from database import SessionLocal, Base
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Exercise
import datetime

db = SessionLocal()

def exercise_replace(date: datetime.date, index: int, db: Session, create: bool):
    '''
    create: if you want to create exercise, argument 'create' should be True \n
    use before create data \n
    use after delete data
    '''

    order_add = 1 if create else -1
    exercises = db.query(Exercise).filter(and_(Exercise.date == date, Exercise.order >= index)).order_by(Exercise.order).all()
    if not exercises:
        return
    if create:
        exercises = list(reversed(exercises))
    print('exercise db')
    if exercises:
        for exercise in exercises:
            print(exercise.order)
            exercise.order += order_add
            print(exercise.order)
            db.add(exercise)
            db.commit()
        print('commit!!')


def exercise_reorder(date: datetime.date, db: Session):
    data = db.query(Exercise).filter_by(date=date).all()
    for i, e in enumerate(data):
        e.order = i
        db.add(e)
        db.commit()