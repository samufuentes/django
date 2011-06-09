from decimal import Decimal

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.unittest import TestCase
from django import test


class TestFieldWithValidators(TestCase):
    def test_all_errors_get_reported(self):
        field = forms.CharField(
            validators=[validators.validate_integer, validators.validate_email]
        )
        self.assertRaises(ValidationError, field.clean, 'not int nor mail')
        try:
            field.clean('not int nor mail')
        except ValidationError, e:
            self.assertEqual(2, len(e.messages))

class DecimalFieldTests(test.TestCase):
    def test_validate(self):
        f = forms.DecimalField(max_digits=10, decimal_places=1)
        try:
            f.validate(Decimal('1E+2'))  # Ensure that scientific notation with positive exponent is accepted (#15775)
            f.validate(Decimal('1E-1'))
            f.validate(Decimal('100'))
        except ValidationError:
            self.fail("Validation is not working properly")
        self.assertRaises(ValidationError, f.validate, Decimal('1E-2'))