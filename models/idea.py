from datetime import datetime
from app import db

class Idea(db.Model):
    """Idea model for project ideas and concepts"""
    __tablename__ = 'ideas'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='new')  # new, in_progress, completed, archived
    priority = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Idea {self.title}>'
    
    @classmethod
    def get_all(cls, status=None):
        """Get all ideas, optionally filtered by status"""
        query = cls.query
        if status:
            query = query.filter_by(status=status)
        return query.order_by(cls.priority.desc(), cls.created_at.desc()).all()
    
    def serialize(self):
        """Convert idea to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
