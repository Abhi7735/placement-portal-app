# contains all my database models. I am using Flask-SQLAlchemy ORM to interact with a SQLite database programmatically.
from flask_sqlalchemy import SQLAlchemy   # type: ignore
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore

db = SQLAlchemy()  # create an instance of the SQLAlchemy class to manage database interactions

# ====ADMIN MODEL =====

class Admin(db.Model):
    __tablename__ = 'admin'  # specify the name of the database table for this model

    id= db.column(db.integer, primary_key = True)
    username = db.column(db.string(100), unique= True, nullable= False)
    email = db.column(db.string(100),unique = True, nullable = False)
    password = db.column(db.string(200), nullable = False)
    created_at  = db.column(db.Datetime, default = datetime.utcnow)

    def set_password(self,password):
        self.password = generate_password_hash(password)


    def check_password(self,password):
        return check_password_hash(self.password, password)

    def represent(self):
        return f'<Admin {self.username}>'    
    
    #==== COMPANY MODEL ====
class company(db.model):
        __tablename__ = 'company'

        company_id = db.column(db.integer, primary_key = True)
        company_name = db.column(db.string(100),unique = True, nullable = False)
        email = db.column(db.string(100), unique = True , nullable = False)
        password = db.column(db.string(200), nullable = False)
        hr_contact = db.column(db.string(20),nullable = False)
        website = db.column(db.string(100), nullable = True)
        address = db.column(db.string(200), nullable = True)

        # approval status: pending, Approved, rejected
        approval_status = db.column(db.string(20), default = 'pending')
        is_blacklisted = db.column(db.boolean, default = False)
        created_at = db.column(db.Datetime, default = datetime.utcnow)

        # relationship: one company can create many placement drives
        placement_drives = db.relationship('PlacementDrive', backref = 'company', lazy = True,  cascade = 'all, delete-orphan')

        def set_password(self, password):
            self.password = generate_password_hash(password)
    
        def check_password(self, password):
            return check_password_hash(self.password, password)
    
        def __repr__(self):
            return f'<Company {self.company_name}>'

# ==== STUDENT MODEL ====
class student(db.Model):
    __tablename__ = 'student'

    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    contact  = db.column(db.String(20), nullable=False)

    # profile details
    roll_number = db.column(db.string(50),unique = True, nullable = False)
    department = db.column(db.string(100), nullable = False)
    cgpa = db.column(db.Float, nullable = False)
    grad_year = db.column(db.Integer, nullable = False)
    resume = db.column(db.String(200), nullable = True)  # path to the uploaded resume file
    skills = db.column(db.String(200), nullable = True)  # comma-separated list of skills

    is_blacklisted = db.column(db.boolean, default = False)
    created_at = db.column(db.Datetime, default = datetime.utcnow)
    # relationship: one student can apply to many placement drives
    applications = db.relationship('Application', backref='student', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Student {self.name}>'        
    # ==== PLACEMENT DRIVE MODEL ====
class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'

    drive_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(500), nullable=True)
    eligibility_criteria = db.Column(db.String(500), nullable=True)
    min_cgpa = db.Column(db.Float, nullable=True)
    eligible_departments = db.Column(db.String(200), nullable=True)  # comma-separated list of eligible departments
    
    salary = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    application_deadline = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.String(20), default='active')  # active, closed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship: one placement drive can have many applications
    applications = db.relationship('Application', backref='placement_drive', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<PlacementDrive {self.job_title} at {self.company.company_name}>'    
    # ===== APPLICATION MODEL =====
class Application(db.Model):
    __tablename__ = 'application'

    application_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.drive_id'), nullable=False)
    application_status = db.Column(db.String(20), default='pending')  # pending, shortlisted, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.column(db.string(50),default = 'applied')  # applied, shortlisted, rejected
    cover_letter = db.column(db.text)
    remarks = db.column(db.text)

    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),)

    def __repr__(self):
        return f'<Application {self.application_id}>'
    
 