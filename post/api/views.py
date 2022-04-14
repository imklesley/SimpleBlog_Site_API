from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from account.models import Account
from ..models import BlogPost
from .serializers import BlogPostSerializer


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def api_detail_post_view(request, slug):
    """
    This endpoint will return data of a post using the slug
    """
    try:
        post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response({'detail': "Post do not exists"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        post = BlogPostSerializer(post, many=False)
        return Response(post.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_post_view(request, slug):
    """
    This endpoint will update a object using the slug for located
    """

    try:
        post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if post.author != user:
        return Response("You don't have permission to edit this post.", status=status.HTTP_400_BAD_REQUEST)

    data = {}

    if request.method == 'PUT':
        serializer = BlogPostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['detail'] = 'Post Updated Successfully'
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'detail': f'Error trying update the post with slug: {slug}',
                'errors': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_post_view(request, slug):
    """The endpoint will delete the post using the post slug"""
    try:
        post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(data={'detail': "The post you trying to delete does not exists"},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if post.author != user:
        return Response("You don't have permission to delete this post.", status=status.HTTP_400_BAD_REQUEST)

    data = {}

    if request.method == 'DELETE':
        delete_operation = post.delete()

        if delete_operation:
            data['detail'] = 'Delete successfully'
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['detail'] = 'Delete Failed'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def api_create_post_view(request):
    """The endpoint will create a post"""
    data = {}

    author_account = request.user

    post = BlogPost.objects.create(author=author_account)

    serializer = BlogPostSerializer(post, data=request.data)

    if serializer.is_valid():
        serializer.save()
        data['detail'] = 'Post Created Successfully'
        data['data'] = serializer.data
        return Response(data, status.HTTP_201_CREATED)
    else:
        data['detail'] = 'Error tryng to create a new post'
        data['errors'] = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)
