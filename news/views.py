from rest_framework import generics, viewsets, status
# from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from students.permissions import IsStudent, IsTeacher, IsUserAuthor

from .models import News, Comment
from .serializers import NewsSerializer, CommentSerializer, CommentReadSerializer
from .permissions import IsCommentAuthor
from .filters import TeachersListFilterBackend, ClassNumberFilterBackend


class NewsDefaultViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = NewsSerializer

    def get_clazz_info(self):
        raise NotImplementedError()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        clazz_info = self.get_clazz_info()

        return dict(list(context.items()) + list(clazz_info.items()))

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    filters = (TeachersListFilterBackend,)


class NewsTeachersClassNumberList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    filter_backends = (TeachersListFilterBackend, ClassNumberFilterBackend,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['class_number'] = self.kwargs['class_number']

        return context

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsTeachersViewSet(NewsDefaultViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated, IsTeacher),
        'retrieve': (IsAuthenticated, IsTeacher),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher, IsUserAuthor),
        'destroy': (IsAuthenticated, IsTeacher, IsUserAuthor)
    }

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_clazz_info(self):
        return self.kwargs


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
        context['news'] = generics.get_object_or_404(News, id=self.get_news_pk(self.kwargs))

        return context

    def get_news_pk(self, kwargs):
        return kwargs.get('studentsNews_pk', kwargs.get('teachersNews_pk', None))

    def get_queryset(self):
        return Comment.objects.filter(news__pk=self.get_news_pk(self.kwargs))

    # def update(self, request, *args, **kwargs):
    #     news = generics.get_object_or_404(News, id=self.get_news_pk(kwargs))
    #     comment = generics.get_object_or_404(news.comment_set, id=kwargs['pk'])
    #     self.check_object_permissions(request, comment)

    #     serializer = self.get_serializer(comment, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     headers = self.get_success_headers(serializer.data)

    #     return Response(serializer.validated_data, status=status.HTTP_200_OK, headers=headers)

    # def destroy(self, request, *args, **kwargs):
    #     news = generics.get_object_or_404(News, id=self.get_news_pk(kwargs))
    #     comment = generics.get_object_or_404(news.comment_set, id=kwargs['pk'])
    #     self.check_object_permissions(request, comment)

    #     comment.delete()

    #     return Response(
    #         {'message': 'Comment successfully deleted.'},
    #         status=status.HTTP_200_OK
    #     )
