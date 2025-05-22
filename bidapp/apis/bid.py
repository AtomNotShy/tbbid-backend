from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Bid, BidRank, BidSection
from ..serializers import BidSerializer, BidRankSerializer, BidSectionSerializer
from ..pagination import StandardResultsSetPagination


@api_view(['GET'])
@permission_classes([AllowAny])
def bid_sections_list(request):
    """获取标段列表"""
    # 获取搜索查询参数
    search_query = request.query_params.get('search', '')
    
    # 构建查询
    queryset = BidSection.objects.all().order_by('-bid_open_time')
    
    # 如果有搜索查询，则过滤结果
    if search_query:
        queryset = queryset.filter(
            Q(section_name__icontains=search_query)
        )
    
    # 使用分页器
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(queryset, request)
    
    if page is not None:
        serializer = BidSectionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    # 如果没有分页或分页错误，则返回所有结果
    serializer = BidSectionSerializer(queryset[:10], many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bid_detail(request, pk):
    """获取投标详情"""
    try:
        bid_section = BidSection.objects.get(pk=pk)
        section_id = bid_section.section_id
        project_id = bid_section.project_id_id
        lot_ctl_amt = bid_section.lot_ctl_amt
        bids = Bid.objects.filter(section_id=section_id, project_id=project_id)
    except Bid.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)
    
    serializer = BidSerializer(bids, many=True)
    # 为每个投标对象增加lot_ctl_amt字段
    data = serializer.data
    for item in data:
        item['lot_ctl_amt'] = lot_ctl_amt
    
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def bid_result(request):
    """获取投标结果列表"""
    # 获取搜索查询参数
    search_query = request.query_params.get('search', '')
    
    # 构建查询
    queryset = BidRank.objects.all().order_by('-open_time')
    
    # 如果有搜索查询，则过滤结果
    if search_query:
        queryset = queryset.filter(
            Q(section_name__icontains=search_query) |
            Q(bidder_name__icontains=search_query)
        )
    
    # 使用分页器
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(queryset, request)
    
    if page is not None:
        serializer = BidRankSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    # 如果没有分页或分页错误，则返回所有结果
    serializer = BidRankSerializer(queryset[:6], many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bid_result_detail(request, pk):
    """获取投标结果详情"""
    try:
        bid_rank = BidRank.objects.get(pk=pk)
        project_id = bid_rank.project_id
        section_id = bid_rank.section_id
        all_ranks = BidRank.objects.filter(
            project_id=project_id, 
            section_id=section_id
        ).order_by('rank')
    except BidRank.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)
    
    serializer = BidRankSerializer(all_ranks, many=True)
    return Response(serializer.data)
