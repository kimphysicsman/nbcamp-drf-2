from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Article, Comment, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_name"]


class CommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comment
      fields = ['author', 'comment']

class ArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    category = CategorySerializer(many=True)
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        author_name = obj.author.username
        return author_name

    def get_comments(self, obj):
        comments = Comment.objects.filter(article=obj)
        return [f'{comment.author} - {comment.comment}' for comment in comments ]

    class Meta:
        model = Article
        fields = ["title", "author", "category", "content", "comments"]