from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from news.models import News, Comment
from news.serializers import (
    NewsSerializer,
    CommentSerializer, CommentReadSerializer
)

from students.permissions import IsStudent, IsTeacher


class NewsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(
            author__clazz=self.request.user.student.clazz
        )

    def retrieve(self, request, pk=None):
        news = get_object_or_404(self.get_queryset(), id=pk)
        serializer = self.serializer_class(news)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def create(self, request):
        context = {'request': request}

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

        if news.author != request.user.student:
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

        if news.author != request.user.student:
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
    permission_classes = (IsAuthenticated, IsStudent)
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        return CommentReadSerializer if self.request.method in ('GET',) else CommentSerializer

    def create(self, request, news_pk=None):
        news = get_object_or_404(News, id=news_pk)
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

    def update(self, request, news_pk=None, pk=None):
        news = get_object_or_404(News, id=news_pk)
        comment = get_object_or_404(news.comment_set, id=pk)

        if comment.posted_by != request.user.student:
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

    def destroy(self, request, news_pk=None, pk=None):
        news = get_object_or_404(News, id=news_pk)
        comment = get_object_or_404(news.comment_set, id=pk)

        if comment.posted_by != request.user.student:
            return Response(
                {'message': 'You can delete only your own comments.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        comment.delete()

        return Response(
            {'message': 'Comment successfully deleted.'},
            status=status.HTTP_200_OK
        )
