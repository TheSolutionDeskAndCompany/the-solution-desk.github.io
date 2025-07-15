from datetime import datetime
from app import db

class SOP(db.Model):
    """Standard Operating Procedure model"""
    __tablename__ = 'sops'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    version = db.Column(db.String(10), default='1.0')
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SOP {self.title}>'
    
    @classmethod
    def get_all(cls, category=None):
        """Get all SOPs, optionally filtered by category"""
        query = cls.query
        if category:
            query = query.filter_by(category=category)
        return query.order_by(cls.title).all()
    
    def serialize(self):
        """Convert SOP to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'version': self.version,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
