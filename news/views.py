from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from students.permissions import IsStudent, IsTeacher, IsUserAuthor
from .models import News, Comment
from .serializers import NewsSerializer, CommentSerializer, CommentReadSerializer
from .permissions import IsCommentAuthor


class NewsDefaultViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = NewsSerializer
    permission_classes_by_action = {}

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_queryset(self):
        raise NotImplementedError()

    def retrieve(self, request, *args, **kwargs):
        news = get_object_or_404(self.get_queryset(), id=kwargs['pk'])

        serializer = self.serializer_class(news)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        news = get_object_or_404(self.get_queryset(), id=kwargs['pk'])
        self.check_object_permissions(request, news)

        serializer = self.serializer_class(news, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        news = get_object_or_404(News, id=kwargs['pk'])
        self.check_object_permissions(request, news)

        news.delete()

        return Response(
            {'message': 'Post successfully deleted.'},
            status=status.HTTP_200_OK
        )


class NewsStudentsViewSet(NewsDefaultViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated, IsStudent),
        'retrieve': (IsAuthenticated, IsStudent),
        'create': (IsAuthenticated, IsStudent),
        'update': (IsAuthenticated, IsStudent, IsUserAuthor),
        'destroy': (IsAuthenticated, IsStudent, IsUserAuthor)
    }

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['class_number'] = self.request.user.student.clazz.number

        return context

    def get_queryset(self):
        clazz = self.request.user.student.clazz

        common_news = News.objects.filter(class_number=clazz.number, class_letter='')
        news = News.objects.filter(class_number=clazz.number, class_letter=clazz.letter)

        return common_news | news


class NewsTeachersList(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        news = News.objects.filter(author=request.user)

        serializer = self.serializer_class(news, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NewsTeachersClassNumberList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = NewsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['class_number'] = self.kwargs['class_number']

        return context

    def get(self, request, *args, **kwargs):
        news = News.objects.filter(
            author=request.user,
            class_number=kwargs['class_number']
        )
        serializer = self.serializer_class(news, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsTeachersViewSet(NewsDefaultViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated, IsTeacher),
        'retrieve': (IsAuthenticated, IsTeacher),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher, IsUserAuthor),
        'destroy': (IsAuthenticated, IsTeacher, IsUserAuthor)
    }

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['class_number'] = self.kwargs['class_number']
        context['class_letter'] = self.kwargs['class_letter']

        return context

    def get_queryset(self):
        return News.objects.filter(
            class_number=self.kwargs['class_number'],
            class_letter=self.kwargs['class_letter'],
            author=self.request.user
        )


class CommentsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsCommentAuthor),
        'destroy': (IsAuthenticated, IsCommentAuthor)
    }

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_serializer_class(self):
        return CommentReadSerializer if self.request.method in ('GET',) else CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['news'] = get_object_or_404(News, id=self.get_news_pk(self.kwargs))

        return context

    def get_news_pk(self, kwargs):
        return kwargs.get('studentsNews_pk', kwargs.get('teachersNews_pk', None))

    def list(self, request, *args, **kwargs):
        comments = Comment.objects.filter(news__pk=self.get_news_pk(kwargs))

        serializer = self.get_serializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs['pk'])

        serializer = self.get_serializer(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        news = get_object_or_404(News, id=self.get_news_pk(kwargs))
        comment = get_object_or_404(news.comment_set, id=kwargs['pk'])
        self.check_object_permissions(request, comment)

        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        news = get_object_or_404(News, id=self.get_news_pk(kwargs))
        comment = get_object_or_404(news.comment_set, id=kwargs['pk'])
        self.check_object_permissions(request, comment)

        comment.delete()

        return Response(
            {'message': 'Comment successfully deleted.'},
            status=status.HTTP_200_OK
        )
