from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
import re


"""
    Validator Added To check user password based on some criteria
"""


class CustomPasswordValidator(BaseValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(limit_value=object, *args, **kwargs)
        self.regex = re.compile(r"\d")

    def __call__(self, value):
        if len(value) < 8:
            raise ValidationError(
                "Password Should have 8 character at least",
                code=self.code,
            )

        if value.isdigit():
            raise ValidationError(
                "Password Shouldnt be numeric only",
                code=self.code,
            )


"""
    Mobile Validator added based on pattern needed for mobile field
"""


class MobileValidator(BaseValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(limit_value=object, *args, **kwargs)
        self.regex = re.compile(r"9\d{9}")

    def __call__(self, value) -> None:
        if not re.fullmatch(self.regex, value):
            raise ValidationError(
                "Mobile Number is not valid",
                code=self.code,
            )
