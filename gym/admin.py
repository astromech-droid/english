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


@admin.register(PhraseGroup)
class PhraseGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "base",
        "past_simple",
        "past_participle",
        "present_participle",
        "third_person_singular",
    )

    def base(self, object):
        return object.base.english

    def past_simple(self, object):
        return object.past_simple

    def past_participle(self, object):
        return object.past_participle

    def present_participle(self, object):
        return object.present_participle

    def third_person_singular(self, object):
        return object.third_person_singular


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ("id", "english", "japanese")
