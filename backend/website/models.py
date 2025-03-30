from . import db
from flask_login import UserMixin
import datetime as dt


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    User_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False)
    Role = db.Column(db.String, nullable=False)

    customer = db.relationship('Customers', backref='user', uselist=False)
    professional = db.relationship('Service_Professionals', backref='user', uselist=False)
d
    def __init__(self, Name, Email, Password, Role):
        self.Name = Name
        self.Email = Email 
        self.Password =Password
        self.Role = Role


class Customers(db.Model):
    __tablename__ = 'Customers'
    Customer_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    User_id = db.Column(db.Integer, db.ForeignKey('Users.User_id', ondelete="CASCADE"), nullable=False)
    Name = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False, unique=True)
    Contact = db.Column(db.String, nullable=True)
    City = db.Column(db.String, nullable=True)
    Locality = db.Column(db.String, nullable=True)
    Is_Flagged = db.Column(db.Boolean, default=False)

    def __init__(self, User_id, Name, Email, Contact, City, Locality):
        self.User_id = User_id
        self.Name = Name
        self.Email = Email
        self.Contact = Contact
        self.City = City
        self.Locality = Locality


class Service_Professionals(db.Model):
    __tablename__ = 'Service_Professionals'
    Professional_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    User_id = db.Column(db.Integer, db.ForeignKey('Users.User_id', ondelete="CASCADE"), nullable=False)
    Name = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False, unique=True)
    Service_Type = db.Column(db.Integer, db.ForeignKey('Services.Service_id', ondelete="CASCADE"), nullable=True) 
    Experience = db.Column(db.String, default="0", nullable=True)
    Contact = db.Column(db.String, nullable=True)
    Description = db.Column(db.String, nullable=True)
    City = db.Column(db.String, nullable=True)
    Locality = db.Column(db.String, nullable=True)
    Status = db.Column(db.Boolean, default=False)
    Is_Flagged = db.Column(db.Boolean, default=False)

    def __init__(self, User_id, Name, Email, Service_Type, Experience, Contact, Description, City, Locality):
        self.User_id = User_id
        self.Name = Name
        self.Email = Email
        self.Service_Type = Service_Type
        self.Experience = Experience
        self.Contact = Contact
        self.Description = Description
        self.City = City
        self.Locality = Locality


class Services(db.Model):
    __tablename__ = 'Services'
    Service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Service_type = db.Column(db.String, nullable=False)
    Price_range = db.Column(db.String, nullable=False)
    Duration = db.Column(db.String, nullable=False)
    Description = db.Column(db.String, nullable=False)

    service_professionals = db.relationship('Service_Professionals', backref='service', lazy=True)


class Service_Requests(db.Model):
    __tablename__ = 'Service_Requests'
    Request_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    Customer_id = db.Column(db.Integer, db.ForeignKey('Customers.Customer_id'), nullable=False)
    Service_id = db.Column(db.Integer, db.ForeignKey('Services.Service_id'), nullable=False)
    Professional_id = db.Column(db.Integer, db.ForeignKey('Service_Professionals.Professional_id'), nullable=False)
    Address = db.Column(db.String, nullable=False)
    Start_date = db.Column(db.Date, nullable=False)
    End_date = db.Column(db.Date, nullable=True)
    Status = db.Column(db.String, default="pending", nullable=False)
    Action = db.Column(db.String, default="open", nullable=False)

    customer = db.relationship('Customers', backref='service_requests')
    service = db.relationship('Services', backref='service_requests')
    professional = db.relationship('Service_Professionals', backref='service_requests')


class Reviews(db.Model):
    __tablename__ = 'Reviews'
    Review_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    Customer_id = db.Column(db.Integer, db.ForeignKey('Customers.Customer_id'), nullable=False)
    Professional_id = db.Column(db.Integer, db.ForeignKey('Service_Professionals.Professional_id'), nullable=False)
    Request_id = db.Column(db.Integer, db.ForeignKey('Service_Requests.Request_id'), nullable=False)
    Ratings = db.Column(db.Integer, nullable=False)
    Comment = db.Column(db.String)

    service_request = db.relationship('Service_Requests', backref='review', uselist=False)
    customer = db.relationship('Customers', backref='reviews')
    professional = db.relationship('Service_Professionals', backref='reviews')

    def __init__(self, Request_id, Customer_id, Professional_id, Ratings, Comment=None):
        self.Request_id = Request_id
        self.Customer_id = Customer_id
        self.Professional_id = Professional_id
        self.Ratings = Ratings
        self.Comment = Comment
