# Generated by Django 4.1.7 on 2023-03-19 04:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gym", "0012_beverb"),
    ]

    operations = [
        migrations.AddField(
            model_name="beverb",
            name="tense",
            field=models.CharField(
                choices=[
                    ("PRT_SMP", "現在"),
                    ("PRT_CON", "現在進行"),
                    ("PST_SMP", "過去"),
                    ("FTR_SMP", "未来"),
                ],
                max_length=7,
                null=True,
            ),
        ),
    ]
