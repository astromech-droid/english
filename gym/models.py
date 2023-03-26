from django.db import models


class PersonalPronoun(models.TextChoices):
    FIRST_PERSON_SINGULAR = "FPS", "一人称単数"
    FIRST_PERSON_PLURAL = "FPP", "一人称複数"
    SECOND_PERSON_SINGULAR = "SPS", "二人称単数"
    SECOND_PERSON_PLURAL = "SPP", "二人称複数"
    THIRD_PERSON_SINGULAR = "TPS", "三人称単数"
    THIRD_PERSON_PLURAL = "TPP", "三人称複数"


class Subject(models.Model):
    personal_pronoun = models.CharField(max_length=3, choices=PersonalPronoun.choices)
    text = models.CharField(max_length=4)

    def __str__(self):
        return self.text


class Tense(models.TextChoices):
    PRESENT_SIMPLE = "PRT_SMP", "現在"
    PRESENT_CONTINUOUS = "PRT_CON", "現在進行"
    # PRESENT_PERFECT = "PRT_PFT", "現在完了"
    # PRESENT_PERFECT_CONTINUOUS = "PRT_PCN", "現在完了"
    PAST_SIMPLE = "PST_SMP", "過去"
    # PAST_CONTINUOUS = "PST_CON", "過去進行"
    # PAST_PERFECT = "PST_PFT", "過去完了"
    # PAST_PERFECT_CONTINUOUS = "PST_PCN", "過去完了"
    FUTURE_SIMPLE = "FTR_SMP", "未来"
    # FUTURE_CONTINUOUS = "FTR_CON", "未来進行"
    # FUTURE_PERFECT = "FTR_PFT", "未来完了"
    # FUTURE_PERFECT_CONTINUOUS = "FTR_PCN", "未来完了"


class SentenceType(models.TextChoices):
    POSITIVE = "POS", "肯定文"
    NEGATIVE = "NEG", "否定文"
    QUESTION = "QUE", "疑問文"


class Template(models.Model):
    sentence_type = models.CharField(max_length=3, choices=SentenceType.choices)
    tense = models.CharField(max_length=7, choices=Tense.choices)
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class VerbForm(models.TextChoices):
    BASE = "BASE", "基本形"
    PAST_SIMPLE = "PASM", "過去形"
    PAST_PARTICIPLE = "PAPA", "過去分詞"
    PRESENT_PARTICIPLE = "PRPA", "現在分詞"
    THIRD_PERSON_SINGULAR = "THPS", "三人称単数"


class PhraseGroup(models.Model):
    name = models.CharField(max_length=20)


class Phrase(models.Model):
    english = models.CharField(max_length=20)
    japanese = models.CharField(max_length=20, null=True, blank=True)


class PhraseBase(Phrase):
    verb_form = models.CharField(
        max_length=4, choices=VerbForm.choices, default=VerbForm.BASE, editable=False
    )
    phrase_group = models.OneToOneField(
        PhraseGroup, on_delete=models.CASCADE, related_name="base"
    )

    def __str__(self):
        index = VerbForm.values.index(self.verb_form)
        return f"{self.english} ({VerbForm.names[index]})"


class PhrasePastSimple(Phrase):
    verb_form = models.CharField(
        max_length=4,
        choices=VerbForm.choices,
        default=VerbForm.PAST_SIMPLE,
        editable=False,
    )
    phrase_group = models.OneToOneField(
        PhraseGroup, on_delete=models.CASCADE, related_name="past_simple"
    )

    def __str__(self):
        index = VerbForm.values.index(self.verb_form)
        return f"{self.english} ({VerbForm.names[index]})"


class PhrasePastParticiple(Phrase):
    verb_form = models.CharField(
        max_length=4,
        choices=VerbForm.choices,
        default=VerbForm.PRESENT_PARTICIPLE,
        editable=False,
    )
    phrase_group = models.OneToOneField(
        PhraseGroup,
        on_delete=models.CASCADE,
        related_name="past_participle",
    )

    def __str__(self):
        index = VerbForm.values.index(self.verb_form)
        return f"{self.english} ({VerbForm.names[index]})"


class PhrasePresentParticiple(Phrase):
    verb_form = models.CharField(
        max_length=4,
        choices=VerbForm.choices,
        default=VerbForm.PRESENT_PARTICIPLE,
        editable=False,
    )
    phrase_group = models.OneToOneField(
        PhraseGroup,
        on_delete=models.CASCADE,
        related_name="present_participle",
    )

    def __str__(self):
        index = VerbForm.values.index(self.verb_form)
        return f"{self.english} ({VerbForm.names[index]})"


class PhraseThirdPersonSingular(Phrase):
    verb_form = models.CharField(
        max_length=4,
        choices=VerbForm.choices,
        default=VerbForm.THIRD_PERSON_SINGULAR,
        editable=False,
    )
    phrase_group = models.OneToOneField(
        PhraseGroup,
        on_delete=models.CASCADE,
        related_name="third_person_singular",
    )

    def __str__(self):
        index = VerbForm.values.index(self.verb_form)
        return f"{self.english} ({VerbForm.names[index]})"


class BeVerb(models.Model):
    personal_pronoun = models.CharField(max_length=3, choices=PersonalPronoun.choices)
    tense = models.CharField(max_length=7, choices=Tense.choices)
    text = models.CharField(max_length=5)


class PaVerb(models.Model):
    personal_pronoun = models.CharField(max_length=3, choices=PersonalPronoun.choices)
    tense = models.CharField(max_length=7, choices=Tense.choices)
    text = models.CharField(max_length=5)
