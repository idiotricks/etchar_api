from django.contrib.auth.models import User
from rest_framework import serializers

from employees.models import Employee
from users.serializers import UserSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        if obj.user:
            # To late, i need to get (refresh) up to date user
            user = User.objects.get(username=obj.user)
            return UserSerializer(user).data
        return None

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = [
            'employee_code',
            'user',
            'is_publish',
        ]

