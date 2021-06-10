#!/bin/bash
# 获取CPU核数
cpu_core_nums=$(cat /proc/cpuinfo | grep "cores" | uniq | awk '{print $4}')

while ! nc -z mysql 3306 ; do
    echo "正在等待MySQL服务启动..."
    sleep 3
done

echo "MySQL服务已启动完毕。"

while ! nc -z rabbitmq 5672 ; do
    echo "正在等待rabbitmq服务启动..."
    sleep 3
done

echo "rabbitmq服务已启动完毕。"
nohup celery -A beer_server worker -l INFO >> celery.log 2>&1 &
echo "启动Celery异步任务队列服务完毕。即将开始部署Django项目。"

python3 manage.py collectstatic --noinput \
    && echo "收集静态文件完毕。" \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && echo "项目数据迁移完毕。" \
    && python3 manage.py init_admin \
    && python3 manage.py update_global_function_content \
    && echo "初始化系统管理员数据和全局函数文件完毕。" \
    && gunicorn --workers=$((cpu_core_nums * 2 + 1)) --bind=0.0.0.0 beer_server.wsgi