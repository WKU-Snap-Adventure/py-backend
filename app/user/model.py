from app import db, bc, jwt

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(50), nullable=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')
    
    @password.setter
    def password(self, password):
        self.password_hash = bc.generate_password_hash(password).decode('utf-8')

    def __init__(self, username, password, nickname):
        self.username = username
        self.password = password
        self.nickname = nickname
    
    def check_password(self, password):
        return bc.check_password_hash(self.password_hash, password)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

# Not working
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
