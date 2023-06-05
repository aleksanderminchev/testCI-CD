from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from api.auth import token_auth
from models.user import User
from models.teacher import Teacher,Referral

class ReferralSchema(ma.SQLAlchemySchema):
    class Meta:
        model= Referral
        ordered = True
    id=ma.Integer(dump_only=True)
    created_at=ma.DateTime(dump_only=True)
    last_updated=ma.DateTime(dump_only=True)
    referred_id=ma.Integer(required=True,load_only=True)
    referral_amount=ma.Float(dump_only=True)
    referrer_id=ma.Integer(required=True,load_only=True)
    referred=ma.Integer(dump_only=True)
    referrer=ma.Integer(dump_only=True)

class AddReferral(ma.SQLAlchemySchema):
    class Meta:
        model=Referral
        ordered=True
    id=ma.Integer(dump_only=True)
    created_at=ma.DateTime(dump_only=True)
    last_updated=ma.DateTime(dump_only=True)
    referral_amount=ma.Float()
    referred_id=ma.Integer(required=True,load_only=True)
    referrer_id=ma.Integer(required=True,load_only=True)
    referred=ma.Integer(dump_only=True)
    referrer=ma.Integer(dump_only=True)
    paid=ma.Boolean(dump_only=True)
    
    @validates('referrer_id')
    def validate_referrer_id(self,value):
        teacher= Teacher.get_teacher_by_id(value)
        if teacher is None:
            raise ValidationError('Teacher does not exist for referring')

    @validates('referred_id')
    def validate_referred_id(self,value):
        teacher= Teacher.get_teacher_by_id(value)
        refferall=Referral.query.filter_by(referred_id=value).first()
        if teacher is None:
            raise ValidationError('Teacher does not exist for referring')
        elif refferall is not None:
            raise ValidationError('Teacher has already been referred by someone else')
    @validates_schema
    def validate_teacher_ids_are_not_same(self, data, **kwargs):
        reffered_id= data['reffered_id']
        refferer_id=data['refferer_id']
        if refferer_id==reffered_id:
            raise ValidationError('A teacher cannot referre themselves')
class UpdateReferralsSchema(ReferralSchema):
    class Meta:
        model= Referral
        ordered = True
    id=ma.Integer(required=True)
    referral=ma.String(required=True)
    @validates("id")
    def validate_referral_id(self,value):
       if Referral.get_referral_by_id(value) is None:
           raise ValidationError("No referral was found")