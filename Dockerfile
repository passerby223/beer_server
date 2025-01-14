FROM python:3.8
WORKDIR /root/beer_server
ENV LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY . .
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" > /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list \
    && apt update \
    && apt install -y netcat \
    && pip3 install -i https://pypi.doubanio.com/simple -U pip \
    && pip3 install -i https://pypi.doubanio.com/simple -r requirements.txt \
    && chmod +x ./deploy_server.sh
ENTRYPOINT /bin/bash deploy_server.sh