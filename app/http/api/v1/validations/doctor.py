from cerberus import Validator
from datetime import datetime

to_date = lambda s: datetime.strptime(s, "%Y-%m-%d")
to_time_hours = lambda s: datetime.strptime(s, "%H:%M")


def create_doctor_validate(document):

    schema = {
        "name" : {"required": True, "type": "string", "maxlength": 200, "minlength": 4},
        "username" : {"required": True, "type": "string", "maxlength": 60, "minlength": 4},
        "password" : {"required": True, "type": "string", "maxlength": 100, "minlength": 8},
        "gender"  :  {"required": True, "type": "string", 'allowed': ['laki-laki', 'perempuan']},
        "birthdate"  : {"required": True, "type": "datetime","coerce": to_date},
        "work_start_time"  : {"required": True, "type": "datetime","coerce": to_time_hours},
        "work_end_time"  : {"required": True, "type": "datetime","coerce": to_time_hours},
    }

    v = Validator(purge_unknown=True)
    if(v.validate(document, schema) == False):
        return {
            "isError": True,
            "message": v.errors
        }
    return { "isError": False }





def update_doctor_validate(document):
    schema = {
        "name" : {"type": "string", "maxlength": 200, "minlength": 4},
        "username" : { "type": "string", "maxlength": 60, "minlength": 4},
        "password" : { "type": "string", "maxlength": 100, "minlength": 8},
        "gender"  :  { "type": "string", 'allowed': ['laki-laki', 'perempuan']},
        "birthdate"  : {"type": "datetime","coerce": to_date},
        "work_start_time"  : { "type": "datetime","coerce": to_time_hours},
        "work_end_time"  : { "type": "datetime","coerce": to_time_hours},
    }

    v = Validator(purge_unknown=True)
    if(v.validate(document, schema) == False):
        return {
            "isError": True,
            "message": v.errors
        }
    return { "isError": False }
