from rest_framework import serializers

from content.models.model_category import Category
from content.models.model_content import Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'content', 'description', 'slug', 'pub_date_time', 'categories_content',
                  ]


class CategorySerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True, source='categories_content')

    class Meta:
        model = Category
        fields = ['id', 'name', 'contents']
