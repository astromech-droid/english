# Generated by Django 4.1.7 on 2023-03-19 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("gym", "0010_phrasegroup_past_simple_alter_phrasegroup_base"),
    ]

    operations = [
        migrations.AddField(
            model_name="phrasegroup",
            name="past_participle",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="past_participle",
                to="gym.phrase",
            ),
        ),
        migrations.AddField(
            model_name="phrasegroup",
            name="present_participle",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="present_participle",
                to="gym.phrase",
            ),
        ),
        migrations.AddField(
            model_name="phrasegroup",
            name="third_person_singular",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="third_person_singular",
                to="gym.phrase",
            ),
        ),
    ]
