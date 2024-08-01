from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import AuthorOrReadOnly, ReadOnly


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        id = self.kwargs.get('pk')
        if id:
            return Post.objects.filter(id=id)
        return Post.objects.all()

    def get_permissions(self):
        if self.action == 'retrieve':
            return [ReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def get_permissions(self):
        if self.action == 'retrieve':
            return [ReadOnly()]
        return super().get_permissions()

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return Post.objects.get(pk=post_id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, post=self.get_post())


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        following = serializer.validated_data.get('following')
        queryset = Follow.objects.filter(
            user=self.request.user, following=following)
        if following == self.request.user:
            raise ValidationError(
                'Невозможно оформить подписку на самого себя!')
        if queryset.exists():
            raise ValidationError(
                'Вы уже подписаны на данного пользователя!')
        serializer.save(user=self.request.user)
