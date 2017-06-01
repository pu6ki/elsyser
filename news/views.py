from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from students.models import Class
from students.permissions import IsStudent, IsTeacher, IsUserAuthor
from .models import News, Comment
from .serializers import NewsSerializer, CommentSerializer, CommentReadSerializer
from .permissions import IsCommentAuthor


class NewsStudentsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated, IsStudent),
        'retrieve': (IsAuthenticated, IsStudent),
        'create': (IsAuthenticated, IsStudent),
        'update': (IsAuthenticated, IsStudent, IsUserAuthor),
        'destroy': (IsAuthenticated, IsStudent, IsUserAuthor)
    }
    serializer_class = NewsSerializer

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['clazz'] = self.request.user.student.clazz

        return context

    def get_queryset(self):
        return News.objects.filter(clazz=self.request.user.student.clazz)

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
        news = get_object_or_404(News, id=kwargs['pk'])
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

    def get(self, request, *args, **kwargs):
        news = News.objects.filter(
            author=request.user,
            clazz__number=kwargs['class_number']
        )
        serializer = self.serializer_class(news, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        classes = Class.objects.filter(number=kwargs['class_number'])

        posted_news = 0
        for clazz in classes:
            context = {'clazz': clazz, 'request': request}

            serializer = self.serializer_class(context=context, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            posted_news += 1

        return Response(
            {'message': '{} news were posted.'.format(posted_news)},
            status=status.HTTP_201_CREATED
        )


class NewsTeachersViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated, IsTeacher),
        'retrieve': (IsAuthenticated, IsTeacher),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher, IsUserAuthor),
        'destroy': (IsAuthenticated, IsTeacher, IsUserAuthor)
    }
    serializer_class = NewsSerializer

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['clazz'] = Class.objects.get(
            number=self.kwargs['class_number'],
            letter=self.kwargs['class_letter']
        )

        return context

    def get_queryset(self):
        return News.objects.filter(author=self.request.user)

    def list(self, request, *args, **kwargs):
        news = self.get_queryset().filter(
            clazz__number=kwargs['class_number'],
            clazz__letter=kwargs['class_letter']
        )

        serializer = self.serializer_class(news, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
        news = get_object_or_404(self.get_queryset(), id=kwargs['pk'])
        self.check_object_permissions(request, news)

        news.delete()

        return Response(
            {'message': 'Post successfully deleted.'},
            status=status.HTTP_200_OK
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
