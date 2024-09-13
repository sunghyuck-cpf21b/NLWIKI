from database import SessionLocal
from models import *

from sqlalchemy import and_

import datetime

from PIL import Image

from passlib.context import CryptContext

db = SessionLocal()

def img_maker():
    width, height = 100, 100

    background_color = (0,0,0)

    image = Image.new('RGB', (width, height), background_color)

    image.save('now_image.png')
    print('image saved')

def img_editor():
    image = Image.open('domain/jff/DP/now_image.png')
    pixels = image.load()
    pixels[50,50] = (0,0,0)
    image.save('test_img.png')


def occ_date_fix():
    data = db.query(Post).filter(and_(Post.category=='논란', Post.occ_date==None)).all()
    data.occ_date = datetime.date(2024,9,12)
    db.add(data)
    db.commit()