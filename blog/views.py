from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer

# 사용자 게시글 기능
class UserArticle(APIView):
    # # 사용자의 게시글의 제목 리스트 보여주기
    # def get(self, request):
    #     user = request.user
    #     if not user.is_authenticated:
    #         msg = '로그인을 해주세요.'
    #         return Response({'message': msg})

    #     articles = Article.objects.filter(author=user)

    #     titles = [ article.title for article in articles ]

    #     return Response({'titles': titles})

    # 사용자의 게시글 정보 보여주기
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            msg = '로그인을 해주세요.'
            return Response({'message': msg})
        
        articles = Article.objects.filter(author=user)

        return Response(ArticleSerializer(articles, many=True).data)