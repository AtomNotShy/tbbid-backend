from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from ..models import CompanyInfo, EmployeeInfo, Bid, BidRank, WinnerBidInfo, PersonPerformance
from ..serializers import CompanyInfoSerializer, EmployeeInfoSerializer, BidSerializer, BidRankSerializer, WinnerBidInfoSerializer, PersonPerformanceSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_search(request):
    """公司搜索API"""
    query = request.GET.get('query', '').strip()
    if not query:
        return Response([])

    companies = CompanyInfo.objects.filter(
        models.Q(name__icontains=query) |
        models.Q(corp_code__icontains=query) |
        models.Q(corp__icontains=query)
    )[:20]

    company_data = []
    for company in companies:
        data = CompanyInfoSerializer(company).data
        employees = EmployeeInfo.objects.filter(corp_code=company.corp_code)
        data['employees'] = EmployeeInfoSerializer(employees, many=True).data
        company_data.append(data)
    
    return Response(company_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_bids(request):
    """获取公司投标记录"""
    corp_code = request.GET.get('corp_code', '').strip()
    page = int(request.GET.get('page', 1))
    PAGE_SIZE = 20
    
    if not corp_code:
        return Response({'results': [], 'count': 0})
    
    # 先查公司名称
    try:
        company = CompanyInfo.objects.get(corp_code=corp_code)
        company_name = company.name
    except CompanyInfo.DoesNotExist:
        return Response({'results': [], 'count': 0})
    
    # 用公司名称查投标记录
    bids = Bid.objects.filter(bidder_name__icontains=company_name)
    total = bids.count()
    bids = bids.order_by('-bid_open_time')[(page-1)*PAGE_SIZE:page*PAGE_SIZE]
    serializer = BidSerializer(bids, many=True)
    
    return Response({'results': serializer.data, 'count': total})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_wins(request):
    """获取公司中标记录"""
    corp_code = request.GET.get('corp_code', '').strip()
    page = int(request.GET.get('page', 1))
    PAGE_SIZE = 20

    if not corp_code:
        return Response({'results': [], 'count': 0})

    # 查公司名称
    try:
        company = CompanyInfo.objects.get(corp_code=corp_code)
        company_name = company.name
    except CompanyInfo.DoesNotExist:
        return Response({'results': [], 'count': 0})

    # 用公司名称查bid_rank表，rank=1为中标
    wins = BidRank.objects.filter(bidder_name__icontains=company_name, rank=1)
    total = wins.count()
    wins = wins.order_by('-open_time')[(page-1)*PAGE_SIZE:page*PAGE_SIZE]
    serializer = BidRankSerializer(wins, many=True)

    return Response({'results': serializer.data, 'count': total})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_achievements(request):
    """获取公司全国业绩（winner_bid_info表）"""
    corp_code = request.GET.get('corp_code', '').strip()
    if not corp_code:
        return Response({'results': [], 'count': 0})

    # 查公司名称
    try:
        company = CompanyInfo.objects.get(corp_code=corp_code)
        company_name = company.name
    except CompanyInfo.DoesNotExist:
        return Response({'results': [], 'count': 0})

    page = int(request.GET.get('page', 1))
    PAGE_SIZE = 20
    # winner_bid_info表查公司中标业绩
    achievements = WinnerBidInfo.objects.filter(bidder_name__icontains=company_name)
    total = achievements.count()
    achievements = achievements.order_by('-create_time')[(page-1)*PAGE_SIZE:page*PAGE_SIZE]
    serializer = WinnerBidInfoSerializer(achievements, many=True)

    return Response({'results': serializer.data, 'count': total})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def achievement_detail(request, pk):
    """全国业绩详情（winner_bid_info表）"""
    try:
        achievement = WinnerBidInfo.objects.get(pk=pk)
    except WinnerBidInfo.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)
    serializer = WinnerBidInfoSerializer(achievement)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_manager_performances(request):
    """获取公司项目经理业绩（person_performance表）"""
    corp_code = request.GET.get('corp_code', '').strip()
    if not corp_code:
        return Response({'results': [], 'count': 0})

    page = int(request.GET.get('page', 1))
    PAGE_SIZE = 20
    
    # 查询该公司的项目经理业绩记录
    performances = PersonPerformance.objects.filter(corp_code=corp_code)
    total = performances.count()
    performances = performances.order_by('-updated_at')[(page-1)*PAGE_SIZE:page*PAGE_SIZE]
    serializer = PersonPerformanceSerializer(performances, many=True)

    return Response({'results': serializer.data, 'count': total})

