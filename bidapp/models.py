from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    MEMBERSHIP_CHOICES = [
        ('free', '免费会员'),
        ('silver', '银牌会员'),
        ('gold', '金牌会员'),
        ('vip', 'VIP会员'),
    ]
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name='电话')
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name='公司')
    membership_level = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='free', verbose_name='会员等级')
    membership_start = models.DateTimeField(blank=True, null=True, verbose_name='会员开始时间')
    membership_end = models.DateTimeField(blank=True, null=True, verbose_name='会员结束时间')

    @property
    def is_membership_active(self):
        now = timezone.now()
        return (
            self.membership_level != 'free'
            and self.membership_start is not None
            and self.membership_end is not None
            and self.membership_start <= now <= self.membership_end
        )

class Bid(models.Model):
    project_id = models.CharField()
    section_id = models.CharField()
    section_name = models.CharField()
    bidder_name = models.CharField()
    bid_amount = models.FloatField(blank=True, null=True)
    bid_open_time = models.DateTimeField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bid'
        unique_together = (('project_id', 'section_id', 'bidder_name'),)


class BidRank(models.Model):
    project_id = models.CharField()
    section_name = models.CharField()
    section_id = models.CharField()
    bidder_name = models.CharField()
    rank = models.IntegerField()
    manager_name = models.CharField(blank=True, null=True)
    win_amt = models.FloatField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    open_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bid_rank'
        unique_together = (('project_id', 'section_id', 'bidder_name'),)


class BidSection(models.Model):
    project_id = models.ForeignKey('Project', models.DO_NOTHING, to_field='project_id', db_column='project_id')
    section_name = models.CharField()
    section_id = models.CharField()
    bid_size = models.IntegerField(blank=True, null=True)
    bid_open_time = models.DateTimeField(blank=True, null=True)
    info_source = models.CharField(blank=True, null=True)
    lot_ctl_amt = models.FloatField(blank=True, null=True)
    session_size = models.IntegerField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    winning_bidder = models.CharField(blank=True, null=True)
    winning_amount = models.FloatField(blank=True, null=True)
    winning_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bid_section'
        unique_together = (('project_id', 'section_id'),)

class Project(models.Model):
    project_id = models.CharField(unique=True)
    title = models.CharField(blank=True, null=True)
    time_show = models.DateTimeField(blank=True, null=True)
    platform_name = models.CharField(blank=True, null=True)
    classify_show = models.CharField(blank=True, null=True)
    url = models.CharField(blank=True, null=True)
    notice_content = models.TextField(blank=True, null=True)
    district_show = models.CharField(blank=True, null=True)
    session_size = models.IntegerField(blank=True, null=True)
    company_req = models.CharField(blank=True, null=True)
    person_req = models.CharField(blank=True, null=True)
    construction_funds = models.CharField(blank=True, null=True)
    project_duration = models.CharField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    stage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class CompanyInfo(models.Model):
    name = models.CharField()
    corp_code = models.CharField(unique=True)
    corp = models.CharField(blank=True, null=True)
    corp_asset = models.CharField(blank=True, null=True)
    reg_address = models.CharField(blank=True, null=True)
    valid_date = models.CharField(blank=True, null=True)
    qualifications = ArrayField(
        models.CharField(max_length=255, blank=True),
        blank=True,
        null=True
    )
    bid_count = models.IntegerField(blank=True, null=True)
    win_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_info'


class EmployeeInfo(models.Model):
    name = models.CharField()
    corp_code = models.ForeignKey(CompanyInfo, models.CASCADE, db_column='corp_code', to_field='corp_code')
    role = models.CharField(blank=True, null=True)
    cert_code = models.CharField(unique=True, blank=True, null=True)
    major = ArrayField(
        models.CharField(max_length=255, blank=True),
        blank=True,
        null=True
    )
    valid_date = models.CharField(blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    id_number = models.CharField(max_length = 18, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_info'


class PersonPerformance(models.Model):
    """个人业绩信息"""
    name = models.CharField(max_length=255, verbose_name='姓名')
    corp_code = models.ForeignKey(CompanyInfo, models.CASCADE, db_column='corp_code', to_field='corp_code')
    corp_name = models.CharField(max_length=255, verbose_name='企业名称')
    project_name = models.CharField(max_length=255, verbose_name='项目名称')
    data_level = models.CharField(max_length=50, verbose_name='数据级别')
    role = models.CharField(max_length=100, verbose_name='角色')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'person_performance'
        verbose_name = '个人业绩'
        verbose_name_plural = '个人业绩'

    def __repr__(self):
        return f"PersonPerformance(name='{self.name}', corp_code='{self.corp_code}')"

    def __str__(self):
        return f"{self.name} - {self.corp_name}"
    

class ExcelProcessing(models.Model):
    """用于存储处理过的Excel文件信息"""
    original_filename = models.CharField(max_length=255, verbose_name='原始文件名')
    processed_file = models.FileField(upload_to='processed_files/', verbose_name='处理后的文件')
    processing_params = models.JSONField(blank=True, null=True, verbose_name='处理参数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = 'Excel处理记录'
        verbose_name_plural = 'Excel处理记录'
    
    def __str__(self):
        return f"{self.original_filename} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class WinnerBidInfo(models.Model):
    project_name = models.CharField(max_length=255, verbose_name="项目名称")
    company = models.ForeignKey(
        CompanyInfo,
        on_delete=models.CASCADE,
        to_field='corp_code',
        db_column='corp_code',
        verbose_name="公司"
    )
    bidder_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="中标单位名称")
    area_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="地区代码")
    win_amt = models.FloatField(null=True, blank=True, verbose_name="中标金额")
    create_time = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")
    tender_org_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="招标单位")
    tos = models.CharField(max_length=50, null=True, blank=True, verbose_name="类别")
    url = models.URLField(max_length=500, null=True, blank=True, verbose_name="详情页URL")
    notice_content = models.TextField(null=True, blank=True, verbose_name="公告内容")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'winner_bid_info'
        verbose_name = '中标信息'
        verbose_name_plural = '中标信息'
        unique_together = ['company', 'project_name']

    def __str__(self):
        return f"{self.project_name} - {self.bidder_name}"
