from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, company, timestamp):
        return (
                six.text_type(company.pk) + six.text_type(timestamp) +
                six.text_type(company.is_registered)
        )


account_activation_token = TokenGenerator()
