from datetime import datetime
from app import db

class Project(db.Model):
    """项目模型"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    files = db.relationship('ProjectFile', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'file_count': len(self.files) if self.files else 0
        }

class ProjectFile(db.Model):
    """项目文件模型"""
    __tablename__ = 'project_files'
    
    id = db.Column(db.Integer, primary_key=True)
    original_name = db.Column(db.String(500), nullable=False)
    stored_name = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))  # excel, image, pdf, etc.
    file_size = db.Column(db.Integer)  # 字节
    mime_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'original_name': self.original_name,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'description': self.description,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'project_id': self.project_id,
            'download_url': f'/api/files/{self.id}/download'
        }