from database import SessionLocal
from models import *



def comment_counter(comments):
    comment_num = len(comments)
    subcomment_num = 0
    for c in comments:
        subcomment_num += len(c.subcomments)
    return comment_num + subcomment_num

def post_list_maker(db_data: list): # 조건에 맞게 불러온 데이터베이스 테이블을 가공하는 함수
    result = []
    for i in db_data:
        temp_dict = {
            'id': i.id,
            'category': i.category,
            'subject': i.subject,
            'total_comments': comment_counter(i.comments),
            'creator': i.user.username,
            'create_date': i.create_date
        }
        result.append(temp_dict)
    return result