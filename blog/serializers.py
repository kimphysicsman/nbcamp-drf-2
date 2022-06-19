from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Article, Comment, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_name"]


# class CommentSerializer(serializers.ModelSerializer):
#    comments = serializers.SerializerMethodField()
#    # obj : hobby 객체
#    def get_comments(self, obj):
#       people = obj.userprofile_set.all()
#       name_list = [ person.user.username for person in people ]
#       return name_list

#    class Meta:
#       model = Hobby
#       fields = ['hobby', 'same_hobby_people']

class ArticleSerializer(serializers.ModelSerializer):
    # comment = CommentSerializer(many=True)
    category = CategorySerializer(many=True)
    author = serializers.SerializerMethodField()
    def get_author(self, obj):
        author_name = obj.author.username
        return author_name

    class Meta:
        model = Article
        fields = ["title", "author", "category", "content"]