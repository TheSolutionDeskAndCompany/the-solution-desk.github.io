from marshmallow import fields, validate, validates, ValidationError
from models.project import Project
from schemas import ma

class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True
        include_fk = True
    
    title = fields.String(required=True, validate=validate.Length(min=3, max=100))
    description = fields.String(required=True, validate=validate.Length(min=10))
    github_url = fields.URL(allow_none=True)
    demo_url = fields.URL(allow_none=True)
    download_url = fields.String(allow_none=True)
    
    @validates('title')
    def validate_title(self, title):
        # Custom validation example - check if title already exists on creation
        if self.context.get('create_mode', False):
            existing = Project.query.filter_by(title=title).first()
            if existing:
                raise ValidationError(f'Project with title "{title}" already exists')
        return title
