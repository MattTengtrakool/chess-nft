import pyrebase
from configs import *

firebase=pyrebase.initialize_app(fbconfig)
db = firebase.database()

def get_position(position):
    return db.child("Positions").child(position).get().val()

def add_position(position, address):
    if not get_position(position):
        data = {"Position":position, "Address":address}
        db.child("Positions").child(position).set(data)
        return True
    return False

def get_id():
    return db.child("id").get().val()

def add_id():
    pre_id = get_id()
    if not pre_id:
        db.child("id").child("id").set(0)
        return 0

    db.child("id").child("id").set(str(int(pre_id['id']) + 1))
    return int(pre_id['id'])
        
        


# data ={"Position":"1234", "Address":"abc89sd"}
# # db.child("Positions").child(data["Position"]).set(data)
# print(db.child("Positions").child("1234").get().val()['Address'])
# print(add_position("2546", "0xjfkdlahfjd"))
