import random

from django.db.models import Count, Max
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import (
    BeVerb,
    Log,
    PaVerb,
    PersonalPronoun,
    PhraseBase,
    PhraseGroup,
    PhrasePastParticiple,
    PhrasePastSimple,
    PhrasePresentParticiple,
    PhraseThirdPersonSingular,
    SentenceType,
    Subject,
    Template,
    Tense,
    VerbForm,
)


def index(request):
    html = loader.get_template("gym/index.html")
    context = {}
    return HttpResponse(html.render(context, request))


def train(request):
    html = loader.get_template("gym/train.html")
    context = get_sentence()
    return HttpResponse(html.render(context, request))


def list_phrases(request):
    html = loader.get_template("gym/list_phrases.html")
    phrases = PhraseGroup.objects.all()
    context = {"phrases": phrases}
    return HttpResponse(html.render(context, request))


def list_logs(request):
    html = loader.get_template("gym/list_logs.html")
    logs = Log.objects.values("date").annotate(count=Count("*")).order_by("date").reverse()
    max = logs.aggregate(max=Max("count"))["max"]
    context = {"logs": logs, "max": max}
    return HttpResponse(html.render(context, request))


def register_phrases(request):
    # baseと同じ文字列をPhrageGroupの名前とする
    phrase_group = PhraseGroup(name=request.POST["base_en"])
    phrase_group.save()

    base = PhraseBase(
        phrase_group=phrase_group,
        english=request.POST["base_en"],
        japanese=request.POST["base_ja"],
    )
    base.save()

    present_participle = PhrasePresentParticiple(
        phrase_group=phrase_group,
        english=request.POST["prpa_en"],
        japanese=request.POST["prpa_ja"],
    )
    present_participle.save()

    past_simple = PhrasePastSimple(
        phrase_group=phrase_group,
        english=request.POST["pasm_en"],
        japanese=request.POST["pasm_ja"],
    )
    past_simple.save()

    past_participle = PhrasePastParticiple(
        phrase_group=phrase_group,
        english=request.POST["papa_en"],
        japanese=request.POST["papa_ja"],
    )
    past_participle.save()

    third_person_singular = PhraseThirdPersonSingular(
        phrase_group=phrase_group,
        english=request.POST["thps_en"],
        japanese=request.POST["thps_ja"],
    )
    third_person_singular.save()


@ensure_csrf_cookie
def api_register_phrases(request):
    if request.method == "GET":
        return JsonResponse({})
    if request.method == "POST":
        request.POST = request.GET
        register_phrases(request)

    return HttpResponse(status=200)


def html_register_phrases(request):
    html = loader.get_template("gym/register_phrases.html")
    context = {"verb_form": VerbForm}
    if request.method == "POST":
        register_phrases(request)

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
        "base_ja": phrase_group.base.japanese,
        "id": phrase_group.id,
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


@ensure_csrf_cookie
def api_logging(request):
    if request.method == "GET":
        return JsonResponse({})
    if request.method == "POST":
        request.POST = request.GET

        id = request.POST["phrase_group_id"]
        result = request.POST["result"]

        pg = PhraseGroup.objects.get(id=id)
        log = Log(phrase_group=pg, result=result)
        pg.clean()
        log.save()

    return HttpResponse(status=201)
