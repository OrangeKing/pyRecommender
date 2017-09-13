from django.core.exceptions import ValidationError

def validate_title(value):
    title = value
    if title == "":
        raise  ValidationError("Not a valid title")
    return title

def validate_location(value):
    location = value
    if " " in location:
        raise  ValidationError("Not a valid location")
    return location
