from rest_framework import permissions

# 단어장, 암기완료 단어목록, 단어시험, 새로운 단어 추가 모두 로그인 되어있어야지만 접근 가능
class CustomReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):        # 새로운 단어 추가
        return request.user.is_authenticated
    
    # def has_unique_permission(self, request, view, obj):  # 나머지 : 내 아이디해당 부분만
    #     return 