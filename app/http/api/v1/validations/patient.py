from cerberus import Validator
from datetime import datetime

to_date = lambda s: datetime.strptime(s, "%Y-%m-%d")
to_time_hours = lambda s: datetime.strptime(s, "%H:%M")

def create_patient_validate(document):

    schema = {
        "name" : {"required": True, "type": "string", "maxlength": 200, "minlength": 4},
        "address" : {"required": True, "type": "string", "maxlength": 200, "minlength": 4},
        "no_ktp" : {"required": True, "type": "string", "maxlength": 100, "minlength": 4},
        "gender"  :  {"required": True, "type": "string", 'allowed': ['laki-laki', 'perempuan']},
        "birthdate"  : {"required": True, "type": "datetime","coerce": to_date}
    }

    v = Validator(purge_unknown=True)
    if(v.validate(document, schema) == False):
        return {
            "isError": True,
            "message": v.errors
        }
    return { "isError": False }


def update_patient_validate(document):
    schema = {
        "name" : { "type": "string", "maxlength": 200, "minlength": 4},
        "address" : { "type": "string", "maxlength": 200, "minlength": 4},
        "no_ktp" : { "type": "string", "maxlength": 100, "minlength": 4},
        "gender"  :  { "type": "string", 'allowed': ['laki-laki', 'perempuan']},
        "birthdate"  : { "type": "datetime","coerce": to_date}
    }

    v = Validator(purge_unknown=True)
    if(v.validate(document, schema) == False):
        return {
            "isError": True,
            "message": v.errors
        }
    return { "isError": False }


