# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:23
# @Author  : anonymous
# @File    : serializers.py
# @Software: PyCharm
# @Description:
from utils.drf_utils.base_model_serializer import BaseModelSerializer
from .models import TestSuite


class TestSuiteSerializer(BaseModelSerializer):
    class Meta:
        model = TestSuite
        fields = '__all__'
        read_only_fields = ('creator', 'modifier')
