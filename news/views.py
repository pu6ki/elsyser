from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework_word_filter import FullWordSearchFilter

from students.permissions import IsStudent, IsTeacher, IsUserAuthor

from .models import News
from .serializers import NewsSerializer, CommentSerializer, CommentReadSerializer
from .filters import TeachersListFilterBackend, ClassNumberFilterBackend


class NewsDefaultViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer

    def get_clazz_info(self):
        raise NotImplementedError()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        return dict(context, **self.get_clazz_info())

    def get_queryset(self):
        class_info = self.get_clazz_info()
        class_number = class_info['class_number']
        class_letter = class_info['class_letter']

        common_news = News.objects.filter(class_number=class_number, class_letter='')
        news = News.objects.filter(class_number=class_number, class_letter=class_letter)

        return common_news | news


class NewsStudentsViewSet(NewsDefaultViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated, IsStudent),
        'retrieve': (IsAuthenticated, IsStudent),
        'create': (IsAuthenticated, IsStudent),
        'update': (IsAuthenticated, IsStudent, IsUserAuthor),
        'destroy': (IsAuthenticated, IsStudent, IsUserAuthor)
    }
    filter_backends = (FullWordSearchFilter,)
    word_fields = ('title', 'author__username')

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_clazz_info(self):
        clazz = self.request.user.student.clazz

        return {
            'class_number': clazz.number,
            'class_letter': clazz.letter
        }


class NewsTeachersList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    filters = (TeachersListFilterBackend, FullWordSearchFilter)
    word_fields = ('title',)


class NewsTeachersClassNumberList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    filter_backends = (TeachersListFilterBackend, ClassNumberFilterBackend, FullWordSearchFilter)
    word_fields = ('title',)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['class_number'] = self.kwargs['class_number']

        return context


class NewsTeachersViewSet(NewsDefaultViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated, IsTeacher),
        'retrieve': (IsAuthenticated, IsTeacher),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher, IsUserAuthor),
        'destroy': (IsAuthenticated, IsTeacher, IsUserAuthor)
    }
    filter_backends = (FullWordSearchFilter,)
    word_fields = ('title',)

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_clazz_info(self):
        return self.kwargs


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsUserAuthor),
        'destroy': (IsAuthenticated, IsUserAuthor)
    }

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_serializer_class(self):
        return CommentReadSerializer if self.request.method in ('GET',) else CommentSerializer

    def get_news_pk(self):
        return self.kwargs.get('studentsNews_pk', self.kwargs.get('teachersNews_pk'))

    def get_related_news(self):
        return generics.get_object_or_404(News, id=self.get_news_pk())

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['news'] = self.get_related_news()

        return context

    def get_queryset(self):
        news = self.get_related_news()

        return news.comments.all()
