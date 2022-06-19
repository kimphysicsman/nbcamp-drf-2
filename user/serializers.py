from rest_framework import serializers
from .models import User, UserProfile, Hobby

class HobbySerializer(serializers.ModelSerializer):
   same_hobby_people = serializers.SerializerMethodField()
   # obj : hobby 객체
   def get_same_hobby_people(self, obj):
      people = obj.userprofile_set.all()
      name_list = [ person.user.username for person in people ]
      return name_list

   class Meta:
      model = Hobby
      fields = ['hobby', 'same_hobby_people']

class UserProfileSerializer(serializers.ModelSerializer):
   hobby = HobbySerializer(many=True)
   class Meta:
        model = UserProfile
        fields = ['age', 'hobby']

class UserSerializer(serializers.ModelSerializer):
   userprofile = UserProfileSerializer()
   class Meta:
        # serializer에 사용될 model, field지정
        model = User
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = ["username", "fullname", "email", "userprofile"]