from django.contrib.auth.admin import User
from django.conf import settings
from django.core.management import call_command
from django.db import migrations

import orders


def load_fixture(apps, schema_editor):
    call_command("loaddata", "fixture_users.json", app_label="orders")


def reverse_func(apps, schema_editor):
    print("reverse")


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_func),
    ]
