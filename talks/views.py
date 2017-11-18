from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from students.permissions import IsUserAuthor
from .serializers import TalksSerializer
from .models import Talk


class TalksViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsUserAuthor),
        'destroy': (IsAdminUser,),
    }
    serializer_class = TalksSerializer
    queryset = Talk.objects.all()
    word_filters = ('topic', 'author__username')

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def create(self, request, *args, **kwargs):
        context = {'request': request}

        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        talk = generics.get_object_or_404(Talk, id=kwargs['pk'])
        self.check_object_permissions(request, talk)

        serializer = self.get_serializer(talk, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VoteTalk(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        talk = generics.get_object_or_404(Talk, id=kwargs['pk'])

        if kwargs['action'] == 'upvote':
            talk.votes.up(request.user.id)
        elif kwargs['action'] == 'downvote':
            talk.votes.delete(request.user.id)

        talk.save()

        return Response({'votes': talk.votes.count()}, status=status.HTTP_200_OK)
