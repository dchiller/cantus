# Generated by Django 4.2.7 on 2024-01-25 22:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cantusdata", "0002_remove_chant_concordances_delete_concordance"),
    ]

    operations = [
        migrations.AddField(
            model_name="chant",
            name="differentiae_database",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
