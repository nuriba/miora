from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


def validate_measurement(value):
    """Validate body measurement values."""
    if value <= 0:
        raise ValidationError('Measurement must be positive')
    if value > 300:
        raise ValidationError('Measurement seems unrealistic (> 300cm)')


def validate_hex_color(value):
    """Validate hex color code."""
    if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
        raise ValidationError('Invalid hex color format')


def validate_size_code(value):
    """Validate garment size code."""
    valid_sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    if value.upper() not in valid_sizes:
        # Check for numeric sizes (0-50)
        try:
            size_num = int(value)
            if size_num < 0 or size_num > 50:
                raise ValidationError('Invalid size')
        except ValueError:
            raise ValidationError(f'Size must be one of {valid_sizes} or a number 0-50')


phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)