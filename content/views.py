from rest_framework import generics, status
from rest_framework.response import Response

from content.models.model_category import Category
from content.serializers import CategorySerializer


class ContentApiView(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        category_name = self.request.query_params.get('names', None)

        if category_name:
            category_name_list = category_name.split(',')
            return (Category.objects.prefetch_related('categories_content')
                                    .filter(name__in=category_name_list))

        return Category.objects.prefetch_related('categories_content').all()

    def get(self, request, *args, **kwargs):
        categories = self.get_queryset()

        if not categories.exists() and request.query_params.get('names'):
            return Response({"error": "No categories found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(categories, many=True)

        return Response(serializer.data)



