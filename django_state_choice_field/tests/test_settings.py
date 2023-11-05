from pathlib import Path

SECRET_KEY = "kPFh0pNINnZX14liOPnFtnKAzpmJJVSy"

BASE_DIR = Path(__file__).resolve().parent.parent
TEST_DIR = BASE_DIR / "tests"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    "django_state_choice_field",
    "django_state_choice_field.tests",
]

USE_TZ = False
