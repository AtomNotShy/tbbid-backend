from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Project, BidSection, BidRank


class PaginationTestCase(TestCase):
    """分页功能测试"""
    
    def setUp(self):
        """创建测试数据"""
        self.client = APIClient()
        
        # 创建15个测试项目
        for i in range(15):
            Project.objects.create(
                project_id=f"test_project_{i}",
                title=f"测试项目 {i}",
                district_show=f"测试区域 {i}",
                time_show="2023-05-01 12:00:00"
            )
        
        # 创建15个测试标段
        for i in range(15):
            BidSection.objects.create(
                section_id=f"test_section_{i}",
                section_name=f"测试标段 {i}",
                project_id_id=f"test_project_{i % 5}",
                bid_open_time="2023-05-01 12:00:00"
            )
        
        # 创建15个测试中标结果
        for i in range(15):
            BidRank.objects.create(
                bidder_name=f"测试公司 {i}",
                project_id=f"test_project_{i % 5}",
                section_id=f"test_section_{i % 5}",
                section_name=f"测试标段 {i % 5}",
                rank=i % 3 + 1,
                open_time="2023-05-01 12:00:00"
            )
    
    def test_projects_pagination(self):
        """测试项目列表分页"""
        url = reverse('projects_list')
        
        # 测试默认分页
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertTrue('count' in response.data)
        self.assertTrue('total_pages' in response.data)
        self.assertEqual(len(response.data['results']), 10)  # 默认每页10条
        
        # 测试自定义页面大小
        response = self.client.get(f"{url}?page_size=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # 每页5条
        
        # 测试页码
        response = self.client.get(f"{url}?page=2&page_size=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # 第2页，每页5条
        self.assertEqual(response.data['current'], 2)  # 当前页为第2页
    
    def test_bid_sections_pagination(self):
        """测试标段列表分页"""
        url = reverse('bid_sections_list')
        
        # 测试默认分页
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), 10)  # 默认每页10条
    
    def test_bid_results_pagination(self):
        """测试中标结果列表分页"""
        url = reverse('bid_result')
        
        # 测试默认分页
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), 10)  # 默认每页10条
    
    def test_search_functionality(self):
        """测试搜索功能"""
        # 测试项目搜索
        url = reverse('projects_list')
        response = self.client.get(f"{url}?search=项目 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertTrue('1' in item['title'])
        
        # 测试标段搜索
        url = reverse('bid_sections_list')
        response = self.client.get(f"{url}?search=标段 2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertTrue('2' in item['section_name'])
        
        # 测试中标结果搜索
        url = reverse('bid_result')
        response = self.client.get(f"{url}?search=公司 3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertTrue('3' in item['bidder_name']) 