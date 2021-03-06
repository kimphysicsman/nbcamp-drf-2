from rest_framework import serializers
from .models import User, UserProfile, Hobby

class HobbySerializer(serializers.ModelSerializer):
   same_hobby_people = serializers.SerializerMethodField()
   # obj : hobby 객체
   def get_same_hobby_people(self, obj):
      user = self.context.get('user')
      userprofiles = obj.userprofile_set.exclude(user=user)
      # userprofiles = obj.userprofile_set.all()
      name_list = [ userprofile.user.username for userprofile in userprofiles ]
      return name_list

   class Meta:
      model = Hobby
      fields = ['hobby', 'same_hobby_people']

   # class Meta:
   #    model = Hobby
   #    fields = "__all__"

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
        fields = ["username", "password", "fullname", "email", "userprofile"]

        extra_kwargs = {
            'password': {'write_only': True}
        }

   def create(self, validated_data):
      userprofile = validated_data.pop('userprofile')
      password = validated_data.pop('password')
      user = User.objects.create(**validated_data)
      user.set_password(password)
      user.save()
      
      hobbys = userprofile.pop('hobby')
      hobbys = [Hobby.objects.get(hobby=hobby['hobby']) for hobby in hobbys]
      userprofile = UserProfile.objects.create(user=user, **userprofile)
      userprofile.hobby.set(hobbys)
      userprofile.save()

      return user   