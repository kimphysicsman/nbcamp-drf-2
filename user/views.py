from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.contrib.auth import login, authenticate, logout


# 유저 
class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'message': 'this is get method!'})


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