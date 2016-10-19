from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Class, Subject, Exam


def _exams_view(request, exams):
    paginator = Paginator(exams, 10)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'exams/list.html', {'exams': exams})


def all_exams_list(request):
    exams = Exam.objects.all().order_by('-date')

    return _exams_view(request, exams)


def all_class_exams_list(request, class_number):
    exams = Exam.objects.filter(clazz__number=class_number)

    return _exams_view(request, exams)


def class_exam_list(request, class_number, class_title):
    clazz = Class.objects.filter(number=class_number, title=class_title)
    exams = Exam.objects.filter(clazz=clazz).order_by('-date')

    return _exams_view(request, exams)
