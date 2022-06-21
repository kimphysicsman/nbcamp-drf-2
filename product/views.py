from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import Product
from .serializers import ProductSerializer
from django.utils import timezone
from django.db.models.query_utils import Q


# 제품 관련 기능
class ProductView(APIView):
    # 제품 조회 기능
    def get(self, request):
        user = request.user             # 현재 로그인한 유저
        show_now_at = timezone.now()    # 현재 시간
        # show_now_at = "2022-06-24 00:00:00"   # 임의 시간

        # 작성자가 현재 로그인한 유저 이거나
        # 현재시간이 노출 시작시간과 종료시간 사이인 제품만 조회
        query = Q(author=user) | (Q(show_start_at__lte=show_now_at) & Q(show_end_at__gte=show_now_at))
        products = Product.objects.filter(query)
        
        # 모든 제품 조회
        # products = Product.objects.all()
        return Response(ProductSerializer(products, many=True).data)

    # 제품 생성 기능
    def post(self, request):
        product_serializer = ProductSerializer(data=request.data, context={'request': request})
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({'message': '저장 완료!'}, status=status.HTTP_200_OK)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 제품 수정 기능
    def put(self, request):
        product_id = request.data.pop('product_id')[0]
        product = Product.objects.get(id=product_id)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response({"message": "수정 완료!!"}, status=status.HTTP_200_OK)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)