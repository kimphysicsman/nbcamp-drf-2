from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        author_name = obj.author.username
        return author_name

    class Meta:
        model = Product
        fields = ["title", "author", "content", "created_at", "show_start_at",
                  "show_end_at"]

    def validate(self, data):
        if 'babo' in data.get('title'):
            raise serializers.ValidationError(
                    detail={"error": "부적절한 단어를 사용할 수 없습니다."},
                )

        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        files = self.context.get('request').FILES
        thumbnail = files.get('thumbnail')

        product = Product(author=author, thumbnail=thumbnail, **validated_data)
        product.save()

        return product

    # instance : 수정할 object
    # validated_data : 수정할 내용
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance