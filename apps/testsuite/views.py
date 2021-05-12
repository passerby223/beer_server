from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from config.models import Config
from utils.drf_utils.custom_json_response import JsonResponse
from .serializers import TestSuiteSerializer, RunTestSuiteSerializer
from .models import TestSuite
from utils.drf_utils.custom_model_view_set import CustomModelViewSet
from .tasks import run_testsuite


# Create your views here.
@extend_schema(tags=['套件管理'])
class TestSuitesViewSet(CustomModelViewSet):
    serializer_class = TestSuiteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return TestSuite.objects.all().order_by('-id')
        else:
            users_list = []
            for group_obj in self.request.user.groups.all():
                for user_obj in group_obj.user_set.all():
                    users_list.append(user_obj.username)
            # 当前登录用户所在的所有的用户组中所关联的所有用户集合(去重处理)
            users_set = list(set(users_list))
            queryset = TestSuite.objects.filter(
                Q(creator__in=users_set) & Q(modifier__in=users_set)).distinct().order_by(
                '-id')
            return queryset

    @action(methods=['post'], detail=True, serializer_class=RunTestSuiteSerializer)
    def run(self, request, pk=None):
        """
        启动运行测试套件任务
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get('config_id', False):
            # 选择某个配置来运行测试套件
            async_result = run_testsuite.delay(testsuite_id=get_object_or_404(TestSuite, pk=pk).id,
                                               config_id=get_object_or_404(Config, pk=request.data.get('config_id')).id,
                                               creator=request.user.username)
            return JsonResponse(data={"task_id": async_result.task_id}, code=20000,
                                msg=f'启动运行测试套件任务成功,任务id为{async_result.task_id},请稍后查看任务运行结果',
                                status=status.HTTP_200_OK)
        else:
            # 不选择配置直接执行测试套件
            async_result = run_testsuite.delay(testsuite_id=get_object_or_404(TestSuite, pk=pk).id,
                                               creator=request.user.username)
            return JsonResponse(data={"task_id": async_result.task_id}, code=20000,
                                msg=f'启动运行测试套件任务成功,任务id为{async_result.task_id},请稍后查看任务运行结果',
                                status=status.HTTP_200_OK)
