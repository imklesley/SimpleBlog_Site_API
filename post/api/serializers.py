from rest_framework import serializers

from post.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image', 'slug','date_updated', 'date_published']
