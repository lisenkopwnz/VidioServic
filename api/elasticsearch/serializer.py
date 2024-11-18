from rest_framework import serializers


class ContentDocumentSerializer(serializers.Serializer):
    """
    Сериализатор для документа ContentDocument.
    """
    title = serializers.CharField()
    description = serializers.CharField()
    preview_image = serializers.CharField()
    slug = serializers.CharField()
    pub_date_time = serializers.DateTimeField()
    is_private = serializers.BooleanField()
    categories_content = serializers.ListField(child=serializers.CharField())
    author_content = serializers.CharField(source='author_content.username')

    class Meta:
        fields = (
            'title',
            'description',
            'preview_image',
            'slug',
            'pub_date_time',
            'is_private',
            'categories_content',
            'author_content_username'
        )