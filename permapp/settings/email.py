from .base import read_env, validate_env_email


env = read_env()

EMAIL_CONFIG = env.email_url("EMAIL_SERVER_URL")
vars().update(EMAIL_CONFIG)

DEFAULT_FROM_EMAIL = env.str("FROM_EMAIL")
validate_env_email(DEFAULT_FROM_EMAIL, "FROM_EMAIL")

SERVER_EMAIL = env.str("SERVER_EMAIL")
validate_env_email(SERVER_EMAIL, "SERVER_EMAIL")

for email in env.list("EMAILS_ADMIN"):
    validate_env_email(email, "EMAILS_ADMIN")
ADMINS = [(email, email) for email in env("EMAILS_ADMIN")]
MANAGERS = ADMINS

EMAILS_CCI = env.list("EMAILS_CCI")
for email in EMAILS_CCI:
    validate_env_email(email, "EMAILS_CCI")
