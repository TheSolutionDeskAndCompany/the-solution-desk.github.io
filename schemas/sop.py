from marshmallow import fields, validate
from models.sop import SOP
from schemas import ma

class SOPSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SOP
        load_instance = True
        include_fk = True
    
    title = fields.String(required=True, validate=validate.Length(min=3, max=100))
    content = fields.String(required=True, validate=validate.Length(min=10))
    category = fields.String(validate=validate.Length(max=50))
    project_id = fields.Integer(allow_none=True)
