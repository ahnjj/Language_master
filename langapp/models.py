from wsgiref.simple_server import demo_app
from django.db import models
from typing import TypedDict, Literal, List


# GPT 응답 받기
class GptMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class Vocab(models.Model):
    class Language(models.TextChoices):
        ENGLISH = "en-US", "English"
        JAPANESE = "ja-JP" , "Japanese"
        CHINESE = "zh-CN", "Chinese"
        SPANISH = "es-ES" , "Spanish"
        FRENCH = "fr-FR", "French"
        GERMAN = "de-DE", "German"
        RUSSIAN = "ru-RU", "Russian"


    word_ko = models.CharField(max_length=100, verbose_name = "Meaning")  # 한국어 단어
    word_fo = models.CharField(max_length=100, blank=True, verbose_name="Vocab")  # 외국어 단어(번역한것)
    language = models.CharField(max_length=10, choices=Language.choices, default=Language.ENGLISH, verbose_name="Language")
    sentence = models.TextField(blank=True, verbose_name="Sentence") # 예문
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    failed = models.BooleanField(default=False) # 단어시험 통과 못한것



    def __str__(self):
        return self.word_ko