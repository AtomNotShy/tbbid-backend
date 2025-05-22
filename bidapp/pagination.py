from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    标准分页器，包含当前页码、每页数量、总数量、总页数、结果列表
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    last_page_strings = ('last',)

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
    
    def paginate_queryset(self, queryset, request, view=None):
        """
        重写分页方法，增加错误处理
        """
        try:
            # 尝试获取page_size参数
            page_size_str = request.query_params.get(self.page_size_query_param)
            if page_size_str:
                try:
                    self.page_size = int(page_size_str)
                    # 确保页面大小在允许范围内
                    if self.page_size > self.max_page_size:
                        self.page_size = self.max_page_size
                    elif self.page_size < 1:
                        self.page_size = 10
                except (ValueError, TypeError):
                    # 如果参数无效，使用默认页面大小
                    self.page_size = 10
            
            return super().paginate_queryset(queryset, request, view)
        except Exception as e:
            # 如果发生任何错误，记录错误并返回None
            print(f"Pagination error: {str(e)}")
            return None 