from datetime import datetime
from enum import Enum
from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

def validate_dog_age(age):
    """
    犬の年齢を検証するスタンドアロン関数
    
    Args:
        age: 検証する年齢（整数）
        
    Returns:
        int: 有効な年齢
        
    Raises:
        ValueError: 年齢が無効な場合
    """
    if age is None:
        raise ValueError("Age cannot be None")
    
    if not isinstance(age, int):
        raise ValueError("Age must be an integer")
    
    if age < 0 or age > 20:
        raise ValueError(f"Dog age must be between 0 and 20 years, got {age}")
    
    return age

# Define an Enum for dog status
class AdoptionStatus(Enum):
    AVAILABLE = 'Available'
    ADOPTED = 'Adopted'
    PENDING = 'Pending'

class Dog(BaseModel):
    __tablename__ = 'dogs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.id'))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    description = db.Column(db.Text)
    
    # Adoption status
    status = db.Column(db.Enum(AdoptionStatus), default=AdoptionStatus.AVAILABLE)
    intake_date = db.Column(db.DateTime, default=datetime.now)
    adoption_date = db.Column(db.DateTime, nullable=True)
    
    @validates('name')
    def validate_name(self, key, name):
        return self.validate_string_length('Dog name', name, min_length=2)
    
    @validates('gender')
    def validate_gender(self, key, gender):
        if gender not in ['Male', 'Female', 'Unknown']:
            raise ValueError("Gender must be 'Male', 'Female', or 'Unknown'")
        return gender
    
    @validates('age')
    def validate_age(self, key, age):
        """
        年齢を検証する関数
        年齢が0から20の間であることを確認し、範囲外の場合はエラーをスローする
        """
        return validate_dog_age(age)
    
    @validates('description')
    def validate_description(self, key, description):
        if description is not None:
            return self.validate_string_length('Description', description, min_length=10, allow_none=True)
        return description
    
    def __repr__(self):
        return f'<Dog {self.name}, ID: {self.id}, Status: {self.status.value}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'breed': self.breed.name if self.breed else None,
            'age': self.age,
            'gender': self.gender,
            'description': self.description,
            'status': self.status.name if self.status else 'UNKNOWN'
        }