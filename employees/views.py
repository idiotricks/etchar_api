from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from employees.models import Employee
from employees.serializers import EmployeeSerializer
from utils.models import generate_user, generate_string_code


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('-created_at')
    serializer_class = EmployeeSerializer
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'employee_code',
    ]
    filterset_fields = [
        'is_publish',
        'user',
        'marital_status',
    ]

    def perform_create(self, serializer):
        serializer.save(
            user=generate_user(),
            employee_code=generate_string_code(Employee)
        )

    @action(methods=['POST'], detail=True)
    def publish(self, request, pk=None):
        employee = self.get_object()
        if employee.salary <= 0:
            raise ValidationError(
                detail={
                    'salary': ['Invalid salary']
                }
            )

        if employee.marital_status == 'single' and employee.children > 0:
            raise ValidationError(
                detail={
                    'children': ['marital status and number of children is invalid']
                }
            )

        employee.is_publish = True
        employee.save()

        return Response(self.serializer_class(employee).data)

    @action(methods=['POST'], detail=True)
    def draft(self, request, pk=None):
        employee = self.get_object()
        employee.is_publish = False
        employee.save()

        return Response(self.serializer_class(employee).data)

    @action(methods=['POST'], detail=True)
    def sanity(self, request, pk=None):
        employee = self.get_object()
        employee.is_publish = True

        if not employee.last_name:
            employee.is_publish = False

        if employee.salary <= 0:
            employee.is_publish = False

        if employee.marital_status == 'single' and employee.children > 0:
            employee.children = 0

        if employee.marital_status == 'married' and employee.children > 2:
            employee.children = 1

        if not employee.first_name:
            employee.is_publish = False

        if len(employee.first_name) < 4:
            employee.is_publish = False

        if not employee.email:
            employee.is_publish = False

        if not employee.user:
            employee.is_publish = False

        employee.save()
        return Response(self.serializer_class(employee).data)