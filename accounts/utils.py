from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.six import text_type
text_type = str


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


account_activation_token = AppTokenGenerator()
