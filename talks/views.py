from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_word_filter import FullWordSearchFilter

from students.permissions import IsUserAuthor
from .serializers import MeetupSerializer, TalkSerializer
from .filters import MeetupsFilterBackend
from .models import Meetup


class MeetupsViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAdminUser,),
        'update': (IsAdminUser,),
        'destroy': (IsAdminUser,),
    }
    queryset = Meetup.objects.all()
    filter_backends = (MeetupsFilterBackend,)
    serializer_class = MeetupSerializer

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]


class TalksViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsUserAuthor),
        'upvote': (IsAuthenticated,),
        'downvote': (IsAuthenticated,),
        'destroy': (IsAdminUser,),
    }
    serializer_class = TalkSerializer
    filter_backends = (FullWordSearchFilter,)
    word_filters = ('topic', 'author__username')

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_related_meetup(self):
        return generics.get_object_or_404(Meetup, id=self.kwargs['meetups_pk'])

    def get_queryset(self):
        meetup = self.get_related_meetup()
        return meetup.talks.all()

    def get_object(self):
        return generics.get_object_or_404(self.get_queryset(), id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        context = {
            'request': request,
            'meetup': self.get_related_meetup()
        }

        serializer = self.get_serializer_class()(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        talk = self.get_object()
        self.check_object_permissions(request, talk)

        serializer = self.get_serializer(talk, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def vote(self, request, up=True):
        talk = self.get_object()

        print('up = {}'.format(up))
        print(request.user.id)

        talk.votes.up(request.user.id) if up else talk.votes.delete(request.user.id)
        talk.save()
        print('votes: {}'.format(talk.votes.count()))

        return Response({'votes_count': talk.votes.count()}, status=status.HTTP_200_OK)

    @detail_route(methods=['put'])
    def upvote(self, request, *args, **kwargs):
        return self.vote(request)

    @detail_route(methods=['put'])
    def downvote(self, request, *args, **kwargs):
        print('in downvote view')
        return self.vote(request, up=False)
