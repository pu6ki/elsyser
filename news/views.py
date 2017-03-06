from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from news.models import News, Comment
from news.serializers import (
    NewsSerializer,
    CommentSerializer, CommentReadSerializer
)

from students.models import Class
from students.permissions import IsStudent, IsTeacher


class NewsStudentsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(clazz=self.request.user.student.clazz)

    def retrieve(self, request, pk=None):
        news = get_object_or_404(self.get_queryset(), id=pk)
        serializer = self.serializer_class(news)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        context = {'request': request, 'clazz': request.user.student.clazz}

        serializer = self.serializer_class(
            context=context, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, pk=None):
        news = get_object_or_404(News, id=pk)

        if news.author != request.user:
            return Response(
                {'message': 'You can edit only your own posts.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.serializer_class(
            news, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def destroy(self, request, pk=None):
        news = get_object_or_404(News, id=pk)

        if news.author != request.user:
            return Response(
                {'message': 'You can delete only your own posts.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

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

    def get_queryset(self, class_number=None):
        return News.objects.filter(
            author=self.request.user,
            clazz__number=class_number
        )

    def get(self, request, class_number=None):
        serializer = self.serializer_class(
            self.get_queryset(class_number), many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, class_number=None):
        classes = Class.objects.filter(number=class_number)

        posted_news = 0
        for clazz in classes:
            context = {'clazz': clazz, 'request': request}

            serializer = self.serializer_class(
                context=context, data=request.data
            )
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            posted_news += 1

        return Response(
            {'message': '{} news were posted.'.format(posted_news)},
            status=status.HTTP_201_CREATED
        )


class NewsTeachersViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(author=self.request.user)

    def list(self, request, class_number=None, class_letter=None):
        news = self.get_queryset().filter(
            clazz__number=class_number,
            clazz__letter=class_letter
        )
        serializer = self.serializer_class(news, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, class_number=None, class_letter=None, pk=None):
        news = get_object_or_404(self.get_queryset(), id=pk)
        serializer = self.serializer_class(news)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, class_number=None, class_letter=None):
        clazz = Class.objects.get(number=class_number, letter=class_letter)
        context = {'request': request, 'clazz': clazz}

        serializer = self.serializer_class(
            context=context, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, pk=None, *args, **kwargs):
        news = get_object_or_404(self.get_queryset(), id=pk)

        if news.author != request.user:
            return Response(
                {'message': 'You can edit only your own posts.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.serializer_class(
            news, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def destroy(self, request, pk=None, *args, **kwargs):
        news = get_object_or_404(self.get_queryset(), id=pk)

        if news.author != request.user:
            return Response(
                {'message': 'You can delete only your own posts.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        news.delete()

        return Response(
            {'message': 'Post successfully deleted.'},
            status=status.HTTP_200_OK
        )


class CommentsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return CommentReadSerializer if self.request.method in ('GET',) else CommentSerializer

    def get_news_pk(self, kwargs):
        return kwargs.get(
            'studentsNews_pk', kwargs.get('teachersNews_pk', None)
        )

    def list(self, *args, **kwargs):
        comments = Comment.objects.filter(news__pk=self.get_news_pk(kwargs))

        serializer = self.get_serializer_class()(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        news = get_object_or_404(News, id=self.get_news_pk(kwargs))
        context = {'request': request, 'news': news}

        serializer = self.get_serializer_class()(
            context=context, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        news = get_object_or_404(News, id=self.get_news_pk(kwargs))
        comment = get_object_or_404(news.comment_set, id=kwargs['pk'])

        if comment.posted_by != request.user:
            return Response(
                {'message': 'You can edit only your own comments.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer_class()(
            comment, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        news = get_object_or_404(News, id=self.get_news_pk(kwargs))
        comment = get_object_or_404(news.comment_set, id=kwargs['pk'])

        if comment.posted_by != request.user:
            return Response(
                {'message': 'You can delete only your own comments.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        comment.delete()

        return Response(
            {'message': 'Comment successfully deleted.'},
            status=status.HTTP_200_OK
        )
