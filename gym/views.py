import json
import random
from collections import deque

from django.core.paginator import Paginator
from django.db.models import Count, F, Max, Subquery
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie

from . import settings
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

QUESTION_BUFFER = deque()


def index(request):
    html = loader.get_template("gym/index.html")
    context = {}
    return HttpResponse(html.render(context, request))


def template_training(request):
    html = loader.get_template("gym/training/template_training.html")
    context = {}
    return HttpResponse(html.render(context, request))


def phrase_training(request):
    html = loader.get_template("gym/training/phrase_training.html")
    context = {}
    return HttpResponse(html.render(context, request))


def list_phrases(request):
    html = loader.get_template("gym/list_phrases.html")
    phrases = PhraseGroup.objects.all().order_by("id").reverse()
    pagenator = Paginator(phrases, settings.LIST_PHRASE_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = pagenator.get_page(page_number)
    context = {"page_obj": page_obj}
    return HttpResponse(html.render(context, request))


def list_logs(request):
    html = loader.get_template("gym/list_logs.html")
    logs = Log.objects.values("date").annotate(count=Count("*")).order_by("date").reverse()
    max = logs.aggregate(max=Max("count"))["max"]
    context = {"logs": logs, "max": max}
    return HttpResponse(html.render(context, request))


def toggle_phrases(data):
    phrase_group = PhraseGroup.objects.get(id=data["id"])
    phrase_group.active = not phrase_group.active
    phrase_group.save()
    return phrase_group.active


def register_phrases(data):
    # baseと同じ文字列をPhrageGroupの名前とする
    phrase_group = PhraseGroup(name=data["base_en"])
    phrase_group.save()

    base = PhraseBase(
        phrase_group=phrase_group,
        english=data["base_en"],
        japanese=data["base_ja"],
    )
    base.save()

    present_participle = PhrasePresentParticiple(
        phrase_group=phrase_group,
        english=data["prpa_en"],
        japanese=data["prpa_ja"],
    )
    present_participle.save()

    past_simple = PhrasePastSimple(
        phrase_group=phrase_group,
        english=data["pasm_en"],
        japanese=data["pasm_ja"],
    )
    past_simple.save()

    past_participle = PhrasePastParticiple(
        phrase_group=phrase_group,
        english=data["papa_en"],
        japanese=data["papa_ja"],
    )
    past_participle.save()

    third_person_singular = PhraseThirdPersonSingular(
        phrase_group=phrase_group,
        english=data["thps_en"],
        japanese=data["thps_ja"],
    )
    third_person_singular.save()


@ensure_csrf_cookie
def api_register_phrases(request):
    if request.method == "GET":
        return JsonResponse({})

    if request.method == "POST":
        data = json.loads(request.body)
        register_phrases(data)

    return HttpResponse(status=200)


@ensure_csrf_cookie
def api_toggle_phrases(request):
    if request.method == "GET":
        return JsonResponse({})

    if request.method == "POST":
        data = json.loads(request.body)
        toggle_phrases(data)

    return HttpResponse(status=201)


def html_register_phrases(request):
    html = loader.get_template("gym/register_phrases.html")
    context = {"verb_form": VerbForm}
    if request.method == "POST":
        register_phrases(request.POST)

    return HttpResponse(html.render(context, request))


def buffer_questions():
    # [優先度1] ログの個数が少ないもの
    subquery = (
        PhraseGroup.objects.filter(active=True)
        .values("id")
        .annotate(count=Count("logs"))
        .order_by("count")[: settings.QUESTION_BUFFER_LENGTH]
    ).annotate(pg_id=F("id"))

    # ログの個数がすべてのフレーズで最大数に達していたら...
    if subquery[0]["count"] == settings.MAX_LOG_COUNT:
        # [優先度2]正解のログの個数が少ないもの
        subquery = (
            Log.objects.filter(result="succeed", phrase_group__active=True)
            .values("phrase_group")
            .annotate(count=Count("*"))
            .order_by("count")[: settings.QUESTION_BUFFER_LENGTH]
        ).annotate(pg_id=F("phrase_group__id"))

    phrase_groups = PhraseGroup.objects.filter(id__in=Subquery(subquery.values("pg_id")))

    for pg in phrase_groups:
        QUESTION_BUFFER.append(pg)


def get_phrase_group():
    if len(QUESTION_BUFFER) > 0:
        return QUESTION_BUFFER.popleft()

    else:
        buffer_questions()
        return QUESTION_BUFFER.popleft()

    # DEBUG
    # print(subquery)
    # print(phrase_group)


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
    phrase_group = get_phrase_group()

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
        data = json.loads(request.body)

        pg = PhraseGroup.objects.get(id=data["phrase_group_id"])
        log = Log(phrase_group=pg, result=data["result"])

        pg.clean()
        log.save()

        return HttpResponse(status=201)


def api_sentence(request):
    context = get_sentence()
    return JsonResponse(context)
