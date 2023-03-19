import random

from django.http import HttpResponse
from django.template import loader

from .models import (
    BeVerb,
    PaVerb,
    PersonalPronoun,
    Phrase,
    PhraseGroup,
    SentenceType,
    Subject,
    Template,
    Tense,
    VerbForm,
)


def index(request):
    html = loader.get_template("gym/index.html")
    context = get_sentence()
    return HttpResponse(html.render(context, request))


def register_phrases(request):
    html = loader.get_template("gym/register_phrases.html")
    context = {"verb_form": VerbForm}
    if len(request.GET) > 0:
        phrases = [
            Phrase(
                verb_form=VerbForm.BASE,
                english=request.GET.get("base_en"),
                japanese=request.GET.get("base_ja"),
            ),
            Phrase(
                verb_form=VerbForm.PRESENT_PARTICIPLE,
                english=request.GET.get("prpa_en"),
                japanese=request.GET.get("prpa_ja"),
            ),
            Phrase(
                verb_form=VerbForm.PAST_SIMPLE,
                english=request.GET.get("pasm_en"),
                japanese=request.GET.get("pasm_ja"),
            ),
            Phrase(
                verb_form=VerbForm.PAST_PARTICIPLE,
                english=request.GET.get("papa_en"),
                japanese=request.GET.get("papa_ja"),
            ),
            Phrase(
                verb_form=VerbForm.THIRD_PERSON_SINGULAR,
                english=request.GET.get("thps_en"),
                japanese=request.GET.get("thps_ja"),
            ),
        ]
        registered_phrases = Phrase.objects.bulk_create(phrases)

        # https://django.readthedocs.io/en/stable/topics/db/examples/one_to_one.html
        # Note that you must save an object before it can be assigned to a one-to-one relationship
        [phrase.save() for phrase in registered_phrases]

        PhraseGroup.objects.create(
            base=registered_phrases[0],
            present_participle=registered_phrases[1],
            past_simple=registered_phrases[2],
            past_participle=registered_phrases[3],
            third_person_singular=registered_phrases[4],
        )
    return HttpResponse(html.render(context, request))


def get_sentence():
    subject = Subject.objects.order_by("?").first()
    personal_pronoun_txt = subject.personal_pronoun
    tense = get_random_attr(Tense)
    sentence_type = get_random_attr(SentenceType)
    template = Template.objects.get(
        tense=tense["value"], sentence_type=sentence_type["value"]
    )
    beverb = BeVerb.objects.get(
        tense=tense["value"], personal_pronoun=personal_pronoun_txt
    )
    paverb = PaVerb.objects.get(
        tense=tense["value"], personal_pronoun=personal_pronoun_txt
    )

    phrase_group = PhraseGroup.objects.order_by("?").first()
    sentence = create_sentence(
        template.text,
        subject.text,
        phrase_group,
        beverb.text,
        paverb.text,
        personal_pronoun_txt,
    )
    response = {
        "subject": subject.text.capitalize(),
        "personal_pronoun": personal_pronoun_txt,
        "tense": tense["label"],
        "sentence_type": sentence_type["label"],
        "template": template.text,
        "sentence": sentence,
        "be-verb": beverb.text,
        "pa-verb": paverb.text,
        "phrase": phrase_group.base.english,
    }
    return response


def create_sentence(
    template_txt: str,
    subject_txt: str,
    phrase_group: PhraseGroup,
    beverb_txt: str,
    paverb_txt: str,
    personal_pronoun_txt: str,
):
    sentence = template_txt.replace("<subject>", subject_txt)
    sentence = sentence.replace("<phrase-base>", phrase_group.base.english)
    sentence = sentence.replace("<phrase-prpa>", phrase_group.present_participle.english)
    sentence = sentence.replace("<phrase-pasm>", phrase_group.past_simple.english)
    sentence = sentence.replace("<beverb>", beverb_txt)
    sentence = sentence.replace("<paverb>", paverb_txt)
    if personal_pronoun_txt == PersonalPronoun.THIRD_PERSON_SINGULAR:
        sentence = sentence.replace("<phrase>", phrase_group.third_person_singular.english)
    else:
        sentence = sentence.replace("<phrase>", phrase_group.base.english)

    return sentence.capitalize()


def get_random_attr(enum):
    index = random.randrange(0, len(enum))
    attr = {
        "name": enum.names[index],
        "value": enum.values[index],
        "label": enum.labels[index],
    }
    return attr
