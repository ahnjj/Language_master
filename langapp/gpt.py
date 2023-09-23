from email import message
import os
import sys
import openai

from io import BytesIO
from tempfile import NamedTemporaryFile
from gtts import gTTS
import pygame

from dotenv import load_dotenv
from langapp.models import GptMessage


load_dotenv()  # 상위경로 경우 "..env"..?

openai.api_key = os.getenv("OPENAI_API_KEY")



def gpt_query(vocab, language, skip_save: bool = False) -> str:
    user_prompt = f'Give me one example sentence using {language} word {vocab} in advanced level and korean translation.\
                    Without english translation and pronounciation.'
    
    # 대화 내용 누적 필요 없지
    # global messages   # 코드 간결성 위해 전역변수 씀. 안티패턴임

    # if user_prompt:
    #     messages.append(
    #         {
    #             "role" : "user",
    #             "content" : user_prompt,
    #         }

    #     )
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[
                { "role": "system", "content": "Answer in a consistent style." },
                {  "role": "user", "content": user_prompt }
        ],
        temperature = 1, # 온도인자: 1 에 가까울 수록 그때 그때 다른 답을 준다. - openai제공
    )
    assistant_message = response["choices"][0]["message"]["content"]

    # 대화 내용 누적 필요 없지
    # if skip_save is False:
    #     messages.append(
    #         {
    #             "role": "assistant",
    #             "content": assistant_message,
    #         }
    #     )

    return assistant_message
