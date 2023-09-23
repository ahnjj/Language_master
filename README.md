# Language Master

### function

```bash
자동 단어 번역
기본 단어장 CRUD기능
중요도, 완료 기능
예문 추천 - openai

# 시험 기능
# TTS: 문장, 단어 읽어주기 
```

### requirements

```python
# coding: utf-8

# 오디오 재생을 위함
pygame==2.5.0

# 장고 웹프레임워크
django==4.2.1

# 파이썬에서 보다 손쉬운 환경변수 처리
python-dotenv==1.0.0

# 장고 내에서 보다 손쉬운 환경변수 처리 (python-dotenv에 더해, 장고 친화적인 기능 지원)
django-environ==0.10.0

# openai api 사용을 위한 라이브러리
openai==0.27.7

# 장고 내에서 보다 손쉬운 bootstrap5 사용을 위한 라이브러리
django-bootstrap5==23.1

# HTTP 요청 및 HTML 파서 라이브러리
requests
beautifulsoup4

# 구글번역 크롤링을 통한 음성 생성 라이브러리
gTTS==2.3.2
```

### model

1. model 설계

```python
- language : 영어, 일본어, 중국어, 스페인어, 프랑스어, 독일어, 러시아어 
- 입력받을 단어
- 외울 단어 : 한국어 번역한 것
- 예문 : 추후에 openai api 연결해서 처리할것
- 완료 여부
- 중요 여부
- 시험 탈락 여부
```

1. 마이그레이션
2. 관리자 페이지 모델 등록

### 단어 전체 조회

1. 템플릿

![Untitled](image/Untitled.png)

1. 뷰

```python
# 단어 전체 조회 뷰
def vocab_list(request):
    vocabs = Vocab.objects.filter(complete=False)
    return render(request, 'langapp/vocab_list.html',{'vocabs' : vocabs})
```

1. Url

```python
# langapp/urls.py
urlpatterns = [
    path('', views.vocab_list, name = 'vocab_list'),
]

# Langmaster/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path('langapp/', include('langapp.urls')),
]
```

### 상세 단어 조회

1. 템플릿

![Untitled](image/Untitled%201.png)

1. view

```python
# 각 단어 상세 조회 뷰
def vocab_detail(request, pk):
    vocab = Vocab.objects.get(id=pk)
    return render(request, 'langapp/vocab_detail.html', {'vocab':vocab})
```

1. url

```python
path('<int:pk>/', views.vocab_detail, name = 'vocab_detail'),
```

### 단어 생성 - form

1. form

```python
from django import forms
from .models import Vocab

class VocabForm(forms.ModelForm):
    class Meta:
        model = Vocab
        fields = ('word_ko', 'language', 'sentence', 'important')
```

1. template

![Untitled](image/Untitled%202.png)

1. views

```python
# 단어 등록 뷰
def vocab_post(request):
    if request.method == "POST":
        form = VocabForm(request.POST)
        if form.is_valid():
            vocab = form.save(commit=False)
            vocab.save()
            return redirect('vocab_list')
    else:
        form = VocabForm()
    
    return render(request, 'langapp/vocab_post.html', {'form':form})
```

1. urls

```python
path('post/', views.vocab_post, name='vocab_post'),
```

### 수정

Templates, form 수정 필요 없음

1. views
2. url

```python
path('<int:pk>/edit/',views.vocab_edit, name = 'vocab_edit'),
```

### 완료

1. 템플릿

![Untitled](image/Untitled%203.png)

1. view

```python
# 암기 완료 단어 목록
def complete_list(request):
    completes = Vocab.objects.filter(complete=True)
    return render(request, 'langapp/vocab_list.html', {'completes':completes})

# 단어 암기 여부 체크
# 암기 
def completed(request, pk):
    vocab = Vocab.objects.get(id=pk)
    vocab.complete = True
    vocab.save()
    return redirect('complete_list')   # 완료목록으로 이동

# 미암기
def uncompleted(request, pk):
    vocab = Vocab.objects.get(id=pk)
    vocab.complete = False
    vocab.save()
    return redirect('vocab_list')   # 전체 단어 목록(미암기)으로 이동
```

1. url
- complete → uncomplete로 바꾸는 경우 Url을 어떻게 설계할 것인가?

```python
path('complete/', views.complete_list, name='complete_list'),
path('complete/<int:pk>/', views.completed, name='completed'),  # 완료 체크
path('uncompleted/<int:pk>/', views.uncompleted, name='uncompleted'),  # 마완료 체크
```

### 삭제

- 템플릿 필요 없음
1. view

```python
# 삭제 뷰
def vocab_destroy(request, pk):
    vocab = Vocab.objects.get(id=pk)
    vocab.delete()
    return redirect("vocab_list")
```

1. url

```python
path('delete/<int:pk>/', views.vocab_destroy, name='vocab_destroy'),  # 삭제
```

### 번역 기능

![Untitled](image/Untitled%204.png)

- 구글 번역기 (모바일창) 크롤링
- 영어, 일본어, 중국어, 스페인어, 프랑스어, 러시아어, 독일어
1. **번역 기능**
- 한국어 단어 입력시 자동 해당 언어로 번역해서 단어 저장
1. **form 수정(단어 자동 번역)**

```python
def clean(self):
        word_ko = self.cleaned_data.get('word_ko')
        word_en = self.cleaned_data.get('word_fo')
        target = self.cleaned_data.get('language')
        if word_ko and not word_en:   # 한국어 단어는 입력되었으나 영어 단어 입력이 안되어있을 경우 단어 번역해서 저장
          self.cleaned_data['word_fo'] = self._translate(word_ko,target)

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
```

### chatgpt에게 예문 추천 받기 (수정중)

- **GPT Prompt**

```python
Give me some example sentence using {언어} word {단어} in {레벨} level and korean translation.
Without english translation and pronounciation.
```

![Untitled](image/Untitled%205.png)

### 시도1. 예문 추천 여부 안받고 예문 미입력시 자동으로 추천해주는 상황

- ~~openai 무료 토큰을 모두 사용해서 재 시도 해봐야함~~
1. gpt 쿼리 받는 함수

```python
# 유저가 날리는 메세지
user_prompt = f'Give me one example sentence using {language} word {vocab} in advanced level and korean translation.\
                    Without english translation and pronounciation.'
```

```python
# gpt 응답 받기
response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[
                { "role": "system", "content": "Answer in a consistent style." },
                {  "role": "user", "content": **user_prompt** }
        ],
        temperature = 1, # 온도인자: 1 에 가까울 수록 그때 그때 다른 답을 준다. - openai제공
    )
assistant_message = response["choices"][0]["message"]["content"]
```

### 시험 기능(구현중)

## Issue

1. `ModuleNotFoundError: No module named 'requests’`
- translators 기능을 구현중에 크롤링 할때 페이지 요청을 받아야해서 임포트했는데 오류가 떴다.
- 해결 : `pip install requests`

1. 중국어 : 영어로 번역됨

1. chatgpt api key오류

![Untitled](image/Untitled%206.png)

해결 : 새로운 Key 발급했더니

```python
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
```

![Untitled](image/Untitled%207.png)

- 할당량을 다 썼다고 한다…. 유료 업그레이드 해야한다….

해결 : 

1. 문장 추천 칸에 placeholder를 추가하고 싶음

1. 디자인 정돈