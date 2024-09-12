from database import SessionLocal
from models import *

import datetime

from PIL import Image

from passlib.context import CryptContext

db = SessionLocal()

def img_maker():
    width, height = 100, 100

    background_color = (0,0,0)

    image = Image.new('RGB', (width, height), background_color)

    image.save('test_img.png')

def img_editor():
    image = Image.open('domain/jff/DP/now_image.png')
    pixels = image.load()
    pixels[50,50] = (0,0,0)
    image.save('test_img.png')


