from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article, Category
from .serializers import ArticleSerializer
from user.permissions import RegistedMoreThanAWeekUser, IsAdminOrRegistedMoreThanAWeekUser
from django.db.models.query_utils import Q

# 사용자 게시글 기능
class UserArticle(APIView):
    permission_classes = [IsAdminOrRegistedMoreThanAWeekUser]

    # 게시글 조회 기능
    # 로그인한 사용자만 가능
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            msg = '로그인을 해주세요.'
            return Response({'message': msg})
        
        # articles = Article.objects.filter(author=user)

        # 현재 시간 기준 : 노출 시작 일자와 종료 일자 사이에 있는 게시글 만 보여주기
        show_date_now = timezone.now()
        qyery = Q(author=user) & Q(show_start_date__lte=show_date_now) & Q(show_end_date__gte=show_date_now)
        articles = Article.objects.filter(qyery).order_by("show_start_date")

        return Response(ArticleSerializer(articles, many=True).data)

    # 게시글 작성 기능
    # 관리자 or 가입 후 7일 지난 사용자만 가능
    def post(self, request):
        title = request.data['title']
        categorys = request.data['categorys'] 
        content = request.data['content']

        if len(title) <= 5:
            msg = 'title이 5자 이하이면 게시글을 작성할 수 없습니다.'
            return Response({'message': msg})

        if len(content) <=20:
            msg = 'content가 20자 이하이면 게시글을 작성할 수 없습니다.'
            return Response({'message': msg})
        
        if not categorys or len(categorys) == 0:
            msg = 'category를 지정해야합니다.'
            return Response({'message': msg})
        
        categorys = [Category.objects.get(category_name=category) for category in categorys]

        user = request.user

        article = Article.objects.create(author=user, title=title, content=content)
        article.category.set(categorys)
        article.save()

        return Response({'message': '게시글 저장 완료!'})