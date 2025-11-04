from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

# Database model for product items

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False) # most hashing algorithms produce 60 character strings
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'${self.budget:,}'
        else:
            return f'${self.budget}'
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self, item_obj):
        return item_obj in self.items

    # This is a one-to-many relationship with the Item model
    items = db.relationship('Item', backref='owned_user', lazy=True) 
    # backref is a simple way to also declare a new property on the Item model that references the User who owns the item
    # lazy=True means that SQLAlchemy will load the data from the database in one go


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id')) # This is a foreign key that references the id column of the User table
    
    def __repr__(self):
        return f'Item {self.name}'
    
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

