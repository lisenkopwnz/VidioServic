from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination


class CategoryContentPaginator(PageNumberPagination):
    page_size = 25
    max_page_size = 100
    page_size_query_param = 'page_size'

    def get_page_size(self, request):

        page_size = request.query_params.get(self.page_size_query_param, self.page_size)

        try:
            page_size = int(page_size)
        except (ValueError, TypeError):
            raise ValidationError({"error": f"Invalid value for '{self.page_size_query_param}': must be an integer."})

        return min(page_size, self.max_page_size)
