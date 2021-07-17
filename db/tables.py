
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

"""
from SQLAlchemy import create_engine
from SQLAlchemy.ext.declarative import declarative_base
from SQLAlchemy import Column, Integer, String, DateTime
from SQLAlchemy.orm import sessionmaker
"""

# engine ==========================================
engine=create_engine("mysql+pymysql://root:root@localhost:3306/training_score")
Base=declarative_base(bind=engine)

# table definition ================================
class Calculation(Base):
    __tablename__="calculation" 
    dt_start = Column(DateTime, primary_key=True)
    user_name = Column(String, primary_key=True)
    type = Column(String)
    ans_num = Column(Integer)
    correct_num = Column(Integer)
    duration = Column(Integer)

# session controller ==============================
class SessionManager():
    def __init__(self):
        SessionClass = sessionmaker(bind=engine)
        self.ses = SessionClass() # session
        return None
    
    def calc_insert(self, data):
        self.ses.add(Calculation(
            dt_start=data["dt_start"],
            user_name=data["user_name"],
            type=data["type"],
            ans_num=data["ans_num"],
            correct_num=data["correct_num"],
            duration=data["duration"]
        ))
        self.ses.commit()
        return None



if __name__ == '__main__':
    import datetime
    import time
    test_data = {
        "dt_start": None,
        "user_name": "insert_test",
        "type": "test",
        "ans_num": int(9999),
        "correct_num": int(9999),
        "duration": int(999)
    }
    sm = SessionManager()
    try:
        while True:
            test_data["dt_start"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sm.calc_insert(data=test_data)
            print("insert: {}".format(test_data))
            time.sleep(3)
    except:
        # delete test records ====
        print("\ndelete all test data: user_name={}".format(test_data["user_name"]))
        sm.ses.query(Calculation).filter(
            Calculation.user_name==test_data["user_name"]
        ).delete()
        sm.ses.commit()
        del sm
