from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView

from .models import Exam


def exams_list(request):
    exams = Exam.objects.all().order_by('-date')
    paginator = Paginator(exams, 10)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'exams/list.html', {'exams': exams})


class ExamDetailView(DetailView):
    model = Exam
    template_name = 'exams/detail.html'
