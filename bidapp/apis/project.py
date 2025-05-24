from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Project, BidSection
from ..serializers import ProjectSerializer, BidSectionSerializer
from ..pagination import StandardResultsSetPagination


@api_view(['GET'])
@permission_classes([AllowAny])
def projects_list(request):
    """获取项目列表"""
    # 获取搜索查询参数
    search_query = request.query_params.get('search', '')
    
    # 构建查询
    queryset = Project.objects.all().order_by('-time_show')
    
    # 如果有搜索查询，则过滤结果
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(district_show__icontains=search_query)
        )
    
    # 使用分页器
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(queryset, request)
    
    if page is not None:
        serializer = ProjectSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    # 如果没有分页或分页错误，则返回所有结果
    serializer = ProjectSerializer(queryset[:10], many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_detail(request, project_id):
    """获取项目详情"""
    project = get_object_or_404(Project, project_id=project_id)
    html_content = project.notice_content
    bid_sections = BidSection.objects.filter(project_id=project.project_id)
    bid_sections_data = BidSectionSerializer(bid_sections, many=True).data
    return Response({
        "bid_sections": bid_sections_data,
        "html_content": html_content
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def today_update_count(request):
    """获取今日更新数量"""
    from django.utils import timezone
    from ..models import Bid, BidRank,BidSection
    today = timezone.now().date()

    project_count = BidSection.objects.filter(bid_open_time__date=today).count()
    bid_count = Bid.objects.filter(bid_open_time__date=today).count()
    bid_result_count = BidRank.objects.filter(open_time__date=today).count()
    
    return Response({
        'project_count': project_count,
        'bid_count': bid_count,
        'bid_result_count': bid_result_count
    })
