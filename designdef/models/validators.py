from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError


def validate_dash_array(value):
    values = value.split()
    try:
        values = map(int, values)
    except ValueError as e:
        raise ValidationError(e)
    for v in values:
        if v < 1:
            raise ValidationError("A dash array must only contain positive integers.")


def validate_shape_ctype(value):
    from .element_type import MapElementType

    ctype = ContentType.objects.get_for_id(value)
    if ctype not in MapElementType.list_usable_shape_ctypes():
        raise ValidationError(f"The content type '{ctype}' is not a usable shape type")
