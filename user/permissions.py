from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status
from datetime import timedelta
from django.utils import timezone

class RegistedMoreThanAWeekUser(BasePermission):
    """
    가입일 기준 3일 이상 지난 사용자만 접근 가능
    """
    message = '가입 후 3일 이상 지난 사용자만 사용하실 수 있습니다.'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.join_date < (timezone.now() - timedelta(days=3)))

class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)


class IsAdminOrRegistedMoreThanAWeekUser(BasePermission):
    """
    관리자 또는 가입일 기준 7일 이상 지난 사용자만 접근 가능
    """
    message = '관리자 또는 가입 후 7일 이상 지난 사용자만 게시글을 작성하실 수 있습니다.'

    SAFE_METHODS = ('GET', )

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if user.is_authenticated and user.is_admin:
            return True
            
        if user.is_authenticated and request.user.join_date < (timezone.now() - timedelta(days=7)):
            return True

        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        
        return False