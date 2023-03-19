import random

from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import (
    BeVerb,
    PaVerb,
    PersonalPronoun,
    PhraseGroup,
    SentenceType,
    Subject,
    Template,
    Tense,
)


def index(request):
    html = loader.get_template("gym/index.html")
    context = {}
    return HttpResponse(html.render(context, request))


def get_sentence(request):
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
    return JsonResponse(response)


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
