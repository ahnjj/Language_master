from django.shortcuts import render, redirect

from langapp.forms import VocabForm
from users import permissions
from .models import Vocab
from .permissions import CustomReadOnly     # 권한 추가

# 단어 전체 조회 뷰
def vocab_list(request):
    vocabs = Vocab.objects.filter(complete=False)
    permission_classes = [CustomReadOnly]     # 권한 추가 부분
    return render(request, 'langapp/vocab_list.html',{'vocabs' : vocabs})


# 각 단어 상세 조회 뷰
def vocab_detail(request, pk):
    vocab = Vocab.objects.get(id=pk)
    permission_classes = [CustomReadOnly]     # 권한 추가 부분
    return render(request, 'langapp/vocab_detail.html', {'vocab':vocab})


# 단어 등록 뷰
def vocab_post(request):
    if request.method == "POST":
        form = VocabForm(request.POST)
        permission_classes = [CustomReadOnly]     # 권한 추가 부분
        if form.is_valid():
            vocab = form.save(commit=False)
            vocab.save()
            return redirect('vocab_list')
    else:
        form = VocabForm()
    
    return render(request, 'langapp/vocab_post.html', {'form':form})

# 수정 뷰
def vocab_edit(request, pk):
    vocab = Vocab.objects.get(id=pk)
    permission_classes = [CustomReadOnly]     # 권한 추가 부분
    if request.method == "POST":
        form = VocabForm(request.POST, instance=vocab)
        if form.is_valid():
            vocab = form.save(commit=False)
            vocab.save()
            return redirect('vocab_list')
    else:
        form = VocabForm(instance = vocab)
    return render(request, 'langapp/vocab_post.html', {'form':form})


# 암기 완료 단어 목록
def complete_list(request):
    completes = Vocab.objects.filter(complete=True)
    permission_classes = [CustomReadOnly]     # 권한 추가 부분
    return render(request, 'langapp/complete_list.html', {'completes':completes})


# 단어 암기 여부 체크
# 암기 
def completed(request, pk):
    vocab = Vocab.objects.get(id=pk)
    vocab.complete = True
    vocab.save()
    return redirect('vocab_list')   # 완료목록으로 이동


# 미암기
def uncompleted(request, pk):
    vocab = Vocab.objects.get(id=pk)
    vocab.complete = False
    vocab.save()
    return redirect('complete_list')   # 전체 단어 목록(미암기)으로 이동


# 삭제 뷰
def vocab_destroy(request, pk):
    vocab = Vocab.objects.get(id=pk)
    vocab.delete()
    return redirect("vocab_list")





# # 단어 시험 뷰
# def vocab_test(request):


# # 단어 시험 틀린거 목록 뷰
# def test_failed(request):