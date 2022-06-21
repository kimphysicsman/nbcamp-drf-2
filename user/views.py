from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.contrib.auth import login, authenticate, logout
from .serializers import UserSerializer
from .models import User
from .permissions import RegistedMoreThanAWeekUser

# 유저 뷰 기능
class UserView(APIView):
    permission_classes = [RegistedMoreThanAWeekUser]

    # 현재 로그인한 유저 정보 보여주기
    def get(self, request):
        user = request.user
        
        if not user.is_authenticated:
            msg = '로그인을 해주세요'
            return Response({'message': msg})

        return Response(UserSerializer(user, context={'user': user}).data)

# 로그인 로그아웃 기능
class UserApiView(APIView):
    # 로그인
    def post(self, request):
        user = authenticate(request, **request.data)
        
        if not user:
            msg = '아이디 또는 패스워드를 확인해주세요.'
            return Response({'message': msg})

        login(request, user)
        msg = '로그인 성공!'
        return Response({'message': msg}, status=status.HTTP_200_OK)

    # 로그아웃
    def delete(self, request):
        logout(request)
        msg = '로그아웃 성공!'
        return Response({'message': msg})

