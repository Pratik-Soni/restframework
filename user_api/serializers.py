'''
Created on 28-Jul-2016

@author: pratiksoni
'''


from django.contrib.auth.models import User, Group
from rest_framework import serializers
from user_api.models import UserDetails, LANGUAGE_CHOICES

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
        
        
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

"""
class UserDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    last = serializers.CharField(required=False, allow_blank=True, max_length=100)
    address = serializers.CharField(required=False, allow_blank=True, max_length=500)
    number = serializers.IntegerField()
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='Hindi' )

    def create(self,validate_date):
        return UserDetails.objects.create(**validate_date)
    
    def update(self, instance, validate_data):
        instance.name = validate_data.get('name', instance.name)
        instance.last = validate_data.get('last', instance.last)
        instance.address = validate_data.get('address', instance.address)
        instance.number = validate_data.get('number', instance.number)
        instance.language = validate_data.get('language', instance.language)
        instance.save()
        return instance        
"""

class UserDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = UserDetails
        fields = ('id', 'name', 'last', 'address', 'number', 'language', 'owner',)
        


class UsersSerializer(serializers.ModelSerializer):
    userdetail = serializers.PrimaryKeyRelatedField(many=True, queryset=UserDetails.objects.all())
    #print user
    class Meta:
        model = User
        fileds = ('id', 'username', 'userdetail')
        

