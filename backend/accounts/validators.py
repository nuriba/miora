import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomPasswordValidator:
    patt = {
        'upper': r'[A-Z]',
        'lower': r'[a-z]',
        'digit': r'\d',
        'special': r'[!@#$%^&*(),.?":{}|<>]'
    }

    def validate(self, pw, user=None):
        if len(pw) < 8:
            raise ValidationError(_('Password ≥ 8 chars'), code='pw_short')
        for name, rgx in self.patt.items():
            if not re.search(rgx, pw):
                raise ValidationError(_(f'Password must contain {name}'), code=f'pw_{name}')

    def get_help_text(self):
        return _('Password ≥8 chars + upper + lower + digit + special') 