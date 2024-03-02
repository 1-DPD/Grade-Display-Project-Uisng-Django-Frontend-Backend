from django.shortcuts import render
from .forms import StudentForm
from .models import Student
from google.auth.credentials import Credentials
from google.oauth2 import service_account
import gspread

def home(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            save_to_google_spreadsheet(student)
    else:
        form = StudentForm()

    students = Student.objects.all()
    for student in students:
        student.sum_marks = student.math_marks + student.physics_marks + student.chemistry_marks
        student.avg_marks = student.sum_marks / 3
        student.grade = get_grade(student.avg_marks)

    context = {'form': form, 'students': students}
    return render(request, 'grades/home.html', context)

def save_to_google_spreadsheet(student):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(r"C:\path\to\your\credentials\file.json")
    client = gspread.authorize(creds)

    sheet = client.open('Your Google Spreadsheet Name').sheet1
    row = [student.name, student.roll_number, student.math_marks, student.physics_marks, student.chemistry_marks]
    sheet.append_row(row)

def get_grade(avg_marks):
    if avg_marks >= 90:
        return 'A'
    elif avg_marks >= 80:
        return 'B'
    elif avg_marks >= 70:
        return 'C'
    elif avg_marks >= 60:
        return 'D'
    else:
        return 'F'
