from django.core.exceptions import ValidationError
from django.utils.timezone import localdate


def validate_date(validated_data):
    """Validates date of product launching date"""
    if localdate() < validated_data:
        raise ValidationError(
            "The date must be less or equal to the current date."
        )
