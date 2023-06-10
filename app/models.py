import uuid

from app import db
from app.logic import get_path

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    token = db.Column(db.LargeBinary, nullable=False)
    
    files = db.relationship("File", back_populates="created_by", cascade="all, delete",
                            foreign_keys="[File.created_by_id]")
    
    def __init__(self, username: str):
        self.username = username
        self.token = uuid.uuid4().bytes
        
class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.LargeBinary, primary_key=True)
    source_path = db.Column(db.Text, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    created_by = db.relationship("User", back_populates="files", foreign_keys=[created_by_id])
    
    def __init__(self, created_by_id: int, file_uuid:uuid.UUID):
        self.created_by_id = created_by_id
        self.source_path = get_path(file_uuid)
        self.id = file_uuid.bytes