from marshmallow import fields, validate
from models.idea import Idea
from schemas import ma

class IdeaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Idea
        load_instance = True
        include_fk = True
    
    title = fields.String(required=True, validate=validate.Length(min=3, max=100))
    description = fields.String(required=True, validate=validate.Length(min=10))
    project_id = fields.Integer(allow_none=True)
