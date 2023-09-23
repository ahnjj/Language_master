from django import forms
from .models import Vocab
from .translators import google_translate
from .gpt import gpt_query

class VocabForm(forms.ModelForm):
    class Meta:
        model = Vocab
        fields = ['word_ko', 'word_fo', 'language', 'sentence', 'important']

    def clean(self):
        word_ko = self.cleaned_data.get('word_ko')
        word_fo = self.cleaned_data.get('word_fo')
        target = self.cleaned_data.get('language')
        if word_ko and not word_fo:   # 한국어 단어는 입력되었으나 영어 단어 입력이 안되어있을 경우 단어 번역해서 저장
            self.cleaned_data['word_fo'] = self._translate(word_ko,target)
        
        sentence = self.cleaned_data.get('sentence')
        if not sentence:   # 예문 안되어있을 경우 gpt추천
            self.cleaned_data['sentence'] = gpt_query(word_fo,target)
        

    @staticmethod
    def _translate(origin_text:str,target) -> str:
        # language
        lang_list = {
            "English" : "en",
            "en-US" : "en",
            "Japanese" : "ja",
            "ja-JP" : "ja",
            "Chinese" : "zh",
            "zh-CN" : "zh", 
            "Spanish" : "es",
            "es-ES" : "es",
            "French" : "fr",
            "fr-FR" : "fr",
            "German" : "de",
            "de-DE" : "de",
            "Russian" : "ru",
            "ru-RU" : "ru"
        }
        language = lang_list[target]
        translated = google_translate(origin_text, "auto", language)
        if not translated:
            raise forms.ValidationError("Cannot translate")
        return translated