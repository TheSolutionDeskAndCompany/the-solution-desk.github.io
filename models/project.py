from datetime import datetime
from app import db

class Project(db.Model):
    """Project model for portfolio projects"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    long_description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    demo_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    download_url = db.Column(db.String(200))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'
    
    @classmethod
    def get_all(cls, featured_only=False):
        """Get all projects, optionally filtered by featured status"""
        query = cls.query
        if featured_only:
            query = query.filter_by(is_featured=True)
        return query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_slug(cls, slug):
        """Get a project by its slug"""
        return cls.query.filter_by(slug=slug).first()
    
    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'long_description': self.long_description,
            'image_url': self.image_url,
            'demo_url': self.demo_url,
            'github_url': self.github_url,
            'download_url': self.download_url,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
    def serialize(self):
        """Alias for to_dict for API consistency"""
        return self.to_dict()
