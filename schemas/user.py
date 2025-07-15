from marshmallow import fields, validate, validates, ValidationError
from models.user import User, RoleEnum
from schemas import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)
        
    email = fields.Email(required=True)
    role = fields.String(validate=validate.OneOf([r.value for r in RoleEnum]))
    password = fields.String(load_only=True, validate=validate.Length(min=8), required=True)
    
    @validates('email')
    def validate_email(self, email):
        if self.context.get('create_mode', False):
            existing = User.query.filter_by(email=email).first()
            if existing:
                raise ValidationError('Email is already registered')
        return email
