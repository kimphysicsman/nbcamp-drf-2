from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
from .models import Product, Review

class ProductSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        author_name = obj.author.username
        return author_name

    class Meta:
        model = Product
        fields = ["title", "author", "content", "created_at",
                  "show_end_at", 'update_at', 'price', 'is_active']

    def validate(self, data):
        if 'babo' in data.get('title'):
            raise serializers.ValidationError(
                    detail={"error": "부적절한 단어를 사용할 수 없습니다."},
                )
        
        now = timezone.now()
        
        if  data.get('show_end_at') and now > data.get('show_end_at'):
            raise serializers.ValidationError(
                    detail={"error": "노출 종료 일자는 현재보다 과거일 수 없습니다."},
                )

        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        files = self.context.get('request').FILES
        thumbnail = files.get('thumbnail')
        
        product = Product(author=author, thumbnail=thumbnail, 
                          **validated_data)
        product.save()
        
        created_at = product.created_at
        end_msg = f'    {created_at.strftime("%Y/%m/%d %H:%M:%S")} 에 등록된 상품입니다.    '

        product.content = product.content + '\n' + end_msg
        product.save()

        return product

    # instance : 수정할 object
    # validated_data : 수정할 내용
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        updated_at = instance.update_at
        start_msg = f'    {updated_at.strftime("%Y/%m/%d  %H:%M:%S")} 에 수정되었습니다.    ' 
        instance.content = start_msg + '\n' + instance.content
        instance.is_active = True
        instance.save()

        return instance


class ReivewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        author_name = obj.author.username
        return author_name

    class Meta:
        model = Review
        fields = ["author", "content", "rating", "created_at",]

class ProductDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()     # 상품 작성자
    avg_rating = serializers.SerializerMethodField() # 평균 review 평점
    review = serializers.SerializerMethodField()     # 가장 최근 review

    def get_author(self, obj):
        author_name = obj.author.username
        return author_name

    def get_review(self, obj):
        reviews = Review.objects.filter(product=obj).order_by("-created_at")
        if 0 < len(reviews):
            return ReivewSerializer(reviews[0]).data
        else:
            return None

    # 평균 review 평점 구하기
    def get_avg_rating(self, obj):
        reviews = Review.objects.filter(product=obj)
        if 0 < len(reviews):
            total_rating = 0
            for review in reviews:
                total_rating += review.rating
            avg_rating = total_rating / len(reviews)
            return avg_rating
        else:
            return None

    class Meta:
        model = Product
        fields = ["title", "author", "content", "created_at",
                  "show_end_at", 'update_at', 'price', 'is_active',
                  "avg_rating", 'review']