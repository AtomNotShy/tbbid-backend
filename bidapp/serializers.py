from rest_framework import serializers
from .models import Project, Bid, BidRank, BidSection, CompanyInfo, EmployeeInfo, User,WinnerBidInfo

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['notice_content']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'

class BidRankSerializer(serializers.ModelSerializer):
    names = serializers.SerializerMethodField()

    class Meta:
        model = BidRank
        fields = '__all__'  # 或手动列出 fields + 'bidder_name'

    def get_names(self, obj):
        return obj.bidder_name.split(';') if obj.bidder_name else []


# class BidRankSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BidRank
#         fields = '__all__'

class BidSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidSection
        fields = '__all__'

class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'

class EmployeeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeInfo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'company', 'membership_level', 'membership_start', 'membership_end', 'is_membership_active']


class WinnerBidInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinnerBidInfo
        fields = '__all__'