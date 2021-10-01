from cerberus import Validator

def auth_login_validate(document):
    schema = {
        "username" : {"required": True},
        "password" : {"required": True},
    }

    v = Validator(purge_unknown=True)
    if(v.validate(document, schema) == False):
        return {
            "isError": True,
            "message": v.errors
        }
    return { "isError": False }

