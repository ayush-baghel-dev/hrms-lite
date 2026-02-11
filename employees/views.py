from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer

@api_view(['GET', 'POST'])
def employee_list(request):
    """
    List all employees or create a new employee
    """
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if 'employee_id' in str(e):
                    return Response(
                        {'employee_id': ['An employee with this Employee ID already exists']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif 'email' in str(e):
                    return Response(
                        {'email': ['An employee with this email already exists']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {'error': 'Database error occurred'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def employee_detail(request, pk):
    """
    Retrieve or delete an employee
    """
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(
            {'error': 'Employee not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def attendance_list(request):
    """
    List all attendance records or create a new attendance record
    
    """

    if request.method == 'GET':
        employee_id = request.query_params.get('employee_id')
        date = request.query_params.get('date')

        attendances = Attendance.objects.all()

        # Filter by employee
        if employee_id:
            if not Employee.objects.filter(pk=employee_id).exists():
                return Response(
                    {'error': 'Employee not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            attendances = attendances.filter(employee_id=employee_id)

        # Filter by date
        if date:
            attendances = attendances.filter(date=date)

        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    # if request.method == 'GET':
    #     employee_id = request.query_params.get('employee_id')
    #     date = request.query_params.get('date')
    #     attendances = Attendance.objects.all()

    #     if employee_id:
    #         attendances = attendances.filter(employee_id=employee_id)

    #     if date:
    #         attendances = attendances.filter(date=date)

        
    #     if employee_id:
    #         try:
    #             employee = Employee.objects.get(pk=employee_id)
    #             attendances = Attendance.objects.filter(employee=employee)
    #         except Employee.DoesNotExist:
    #             return Response(
    #                 {'error': 'Employee not found'},
    #                 status=status.HTTP_404_NOT_FOUND
    #             )
    #     else:
    #         attendances = Attendance.objects.all()
        
    #     serializer = AttendanceSerializer(attendances, many=True)
    #     return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'error': 'Attendance already exists for this employee on this date.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def attendance_detail(request, pk):
    """
    Delete an attendance record
    """
    try:
        attendance = Attendance.objects.get(pk=pk)
    except Attendance.DoesNotExist:
        return Response(
            {'error': 'Attendance record not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'DELETE':
        attendance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)