# Generated by Django 2.2.10 on 2020-02-13 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0003_user_gdpr_fields")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_password_change_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Last password change date"
            ),
        )
    ]
