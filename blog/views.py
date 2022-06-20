from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article, Category
from .serializers import ArticleSerializer
from user.permissions import RegistedMoreThanAWeekUser

# 사용자 게시글 기능
class UserArticle(APIView):
    permission_classes = [RegistedMoreThanAWeekUser]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            msg = '로그인을 해주세요.'
            return Response({'message': msg})
        
        articles = Article.objects.filter(author=user)

        return Response(ArticleSerializer(articles, many=True).data)

    # 게시글 작성 기능
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