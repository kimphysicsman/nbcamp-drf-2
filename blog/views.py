from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import Article, Category, Comment
from .serializers import ArticleSerializer, CommentSerializer
from user.permissions import RegistedMoreThanAWeekUser, IsAdminOrRegistedMoreThanAWeekUser
from django.db.models.query_utils import Q

# 사용자 게시글 기능
class UserArticle(APIView):
    permission_classes = [IsAdminOrRegistedMoreThanAWeekUser]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            msg = '로그인을 해주세요.'
            return Response({'message': msg})
        
        show_date_now = timezone.now()
        print(show_date_now)
        # qyery = Q(author=user) & Q(show_start_date__gte=show_date_now) & Q(show_end_date__lte=show_date_now)
        qyery = Q(author=user) & Q(show_start_date__lte=show_date_now) & Q(show_end_date__gte=show_date_now)
        articles = Article.objects.filter(qyery).order_by("show_start_date")

        return Response(ArticleSerializer(articles, many=True).data)

        # articles = Article.objects.all()
        # for article in articles:
        #     comments = article.comment_set.all()
        #     for comment in comments:
        #         print('--------------------')
        #         print(comment.author.username)
        #         print(comment.comment)
        
        # return Response({})

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


# test API
class TestAPI(APIView):
    # 코멘트 보여주기 기능
    def get(self, request):
        comments = Comment.objects.all() # 0개, 1개, 2개 이상
        return Response(CommentSerializer(comments, many=True).data)