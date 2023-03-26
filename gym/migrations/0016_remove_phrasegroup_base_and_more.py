# Generated by Django 4.1.7 on 2023-03-26 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("gym", "0015_paverb"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="phrasegroup",
            name="base",
        ),
        migrations.RemoveField(
            model_name="phrasegroup",
            name="past_participle",
        ),
        migrations.RemoveField(
            model_name="phrasegroup",
            name="past_simple",
        ),
        migrations.RemoveField(
            model_name="phrasegroup",
            name="present_participle",
        ),
        migrations.RemoveField(
            model_name="phrasegroup",
            name="third_person_singular",
        ),
        migrations.CreateModel(
            name="PhraseThirdPersonSingular",
            fields=[
                (
                    "phrase_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="gym.phrase",
                    ),
                ),
                (
                    "phrase_group",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="third_person_singular",
                        to="gym.phrase",
                    ),
                ),
            ],
            bases=("gym.phrase",),
        ),
        migrations.CreateModel(
            name="PhrasePresentParticiple",
            fields=[
                (
                    "phrase_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="gym.phrase",
                    ),
                ),
                (
                    "phrase_group",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="present_participle",
                        to="gym.phrase",
                    ),
                ),
            ],
            bases=("gym.phrase",),
        ),
        migrations.CreateModel(
            name="PhrasePastSimple",
            fields=[
                (
                    "phrase_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="gym.phrase",
                    ),
                ),
                (
                    "phrase_group",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="past_simple",
                        to="gym.phrase",
                    ),
                ),
            ],
            bases=("gym.phrase",),
        ),
        migrations.CreateModel(
            name="PhrasePastParticiple",
            fields=[
                (
                    "phrase_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="gym.phrase",
                    ),
                ),
                (
                    "phrase_group",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="past_participle",
                        to="gym.phrase",
                    ),
                ),
            ],
            bases=("gym.phrase",),
        ),
        migrations.CreateModel(
            name="PhraseBase",
            fields=[
                (
                    "phrase_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="gym.phrase",
                    ),
                ),
                (
                    "phrase_group",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="base",
                        to="gym.phrase",
                    ),
                ),
            ],
            bases=("gym.phrase",),
        ),
    ]
