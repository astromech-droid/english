# Generated by Django 4.1.7 on 2023-03-26 06:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gym", "0016_remove_phrasegroup_base_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="phrase",
            name="verb_form",
        ),
        migrations.AddField(
            model_name="phrasebase",
            name="verb_form",
            field=models.CharField(
                choices=[
                    ("BASE", "基本形"),
                    ("PASM", "過去形"),
                    ("PAPA", "過去分詞"),
                    ("PRPA", "現在分詞"),
                    ("THPS", "三人称単数"),
                ],
                default="BASE",
                editable=False,
                max_length=4,
            ),
        ),
        migrations.AddField(
            model_name="phrasepastparticiple",
            name="verb_form",
            field=models.CharField(
                choices=[
                    ("BASE", "基本形"),
                    ("PASM", "過去形"),
                    ("PAPA", "過去分詞"),
                    ("PRPA", "現在分詞"),
                    ("THPS", "三人称単数"),
                ],
                default="PRPA",
                editable=False,
                max_length=4,
            ),
        ),
        migrations.AddField(
            model_name="phrasepastsimple",
            name="verb_form",
            field=models.CharField(
                choices=[
                    ("BASE", "基本形"),
                    ("PASM", "過去形"),
                    ("PAPA", "過去分詞"),
                    ("PRPA", "現在分詞"),
                    ("THPS", "三人称単数"),
                ],
                default="PASM",
                editable=False,
                max_length=4,
            ),
        ),
        migrations.AddField(
            model_name="phrasepresentparticiple",
            name="verb_form",
            field=models.CharField(
                choices=[
                    ("BASE", "基本形"),
                    ("PASM", "過去形"),
                    ("PAPA", "過去分詞"),
                    ("PRPA", "現在分詞"),
                    ("THPS", "三人称単数"),
                ],
                default="PRPA",
                editable=False,
                max_length=4,
            ),
        ),
        migrations.AddField(
            model_name="phrasethirdpersonsingular",
            name="verb_form",
            field=models.CharField(
                choices=[
                    ("BASE", "基本形"),
                    ("PASM", "過去形"),
                    ("PAPA", "過去分詞"),
                    ("PRPA", "現在分詞"),
                    ("THPS", "三人称単数"),
                ],
                default="THPS",
                editable=False,
                max_length=4,
            ),
        ),
    ]
