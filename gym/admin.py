from django.contrib import admin

from .models import BeVerb, PaVerb, Phrase, PhraseGroup, Subject, Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "sentence_type", "tense", "text")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "personal_pronoun")


@admin.register(BeVerb)
class BeVerbAdmin(admin.ModelAdmin):
    list_display = ("id", "personal_pronoun", "tense", "text")


@admin.register(PaVerb)
class PaVerbAdmin(admin.ModelAdmin):
    list_display = ("id", "personal_pronoun", "tense", "text")


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ("id", "english", "japanese", "verb_form")


@admin.register(PhraseGroup)
class PhraseGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "base",
        "past_simple",
        "present_participle",
        "past_participle",
        "third_person_singular",
    )
