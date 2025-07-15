from datetime import datetime
from app import db

class KPI(db.Model):
    """Key Performance Indicator model"""
    __tablename__ = 'kpis'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    target_value = db.Column(db.Float)
    current_value = db.Column(db.Float, default=0)
    unit = db.Column(db.String(20))
    category = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<KPI {self.title}>'
    
    @classmethod
    def get_all(cls, category=None):
        """Get all KPIs, optionally filtered by category"""
        query = cls.query
        if category:
            query = query.filter_by(category=category)
        return query.order_by(cls.title).all()
    
    def progress_percentage(self):
        """Calculate the progress percentage"""
        if self.target_value and self.target_value > 0:
            return min(100, max(0, (self.current_value / self.target_value) * 100))
        return 0
    
    def serialize(self):
        """Convert KPI to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
            'category': self.category,
            'progress_percentage': self.progress_percentage(),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
