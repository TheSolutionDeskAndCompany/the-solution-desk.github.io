from marshmallow import fields, validate
from models.kpi import KPI
from schemas import ma

class KPISchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KPI
        load_instance = True
        include_fk = True
    
    name = fields.String(required=True, validate=validate.Length(min=3, max=100))
    description = fields.String(required=True, validate=validate.Length(min=10))
    target_value = fields.Float(required=True)
    current_value = fields.Float(required=True)
    project_id = fields.Integer(required=True)
