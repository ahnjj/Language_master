from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="langapp/index.html"), name='index'), # 단어 전체목록
    path('list/', views.vocab_list, name = 'vocab_list'),  # 단어 전체 목록
    path('list/<int:pk>/', views.vocab_detail, name = 'vocab_detail'),  # 개별 단어 상세 조회
    path('post/', views.vocab_post, name='vocab_post'),  # 단어 등록
    path('list/<int:pk>/edit/',views.vocab_edit, name = 'vocab_edit'),  # 수정
    path('complete/', views.complete_list, name='complete_list'),  # 완료 목록
    path('complete/<int:pk>/', views.completed, name='completed'),  # 완료 체크
    path('uncomplete/<int:pk>/', views.uncompleted, name='uncompleted'),  # 미완료 체크
    path('delete/<int:pk>/', views.vocab_destroy, name='vocab_destroy'),  # 삭제
    # path()   # 단어 시험
    ]