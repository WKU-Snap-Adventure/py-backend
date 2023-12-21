from app import db

class BagItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_name = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, user_id, item_name, count):
        self.user_id = user_id
        self.item_name = item_name
        self.count = count