from cerberus import Validator
from datetime import datetime

to_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M")


def create_appointment_validate(document):

    schema = {
        "patient_id" : {"required": True, "type": "integer"},
        "doctor_id" : {"required": True, "type": "integer"},
        "datetime"  : {"required": True, "type": "datetime","coerce": to_datetime},
        "status"  :  {"required": True, "type": "string", 'allowed': ['IN_QUEUE', 'DONE', 'CANCELLED']},
        "diagnose"  :  {"type": "string"},
        "notes"  :  {"type": "string"},
    }

    v = Validator(purge_unknown=True)
    if(v.validate(document, schema) == False):
        return {
            "isError": True,
            "message": v.errors
        }
    return { "isError": False }





def update_appointment_validate(document):
    schema = {
        "patient_id" : {"type": "integer"},
        "doctor_id" : {"type": "integer"},
        "datetime"  : {"type": "datetime","coerce": to_datetime},
        "status"  :  {"type": "string", 'allowed': ['IN_QUEUE', 'DONE', 'CANCELLED']},
        "diagnose"  :  {"type": "string"},
        "notes"  :  {"type": "string"},
    }

    v = Validator(purge_unknown=True)
    if(v.validate(document, schema) == False):
        return {
            "isError": True,
            "message": v.errors
        }
    return { "isError": False }
