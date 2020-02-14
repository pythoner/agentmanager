FROM centos:7

RUN mkdir /etc/agentmanager
RUN mkdir /var/log/agentmanager
COPY ./  /opt


RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
RUN sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo && yum makecache

RUN yum install -y epel-release
RUN yum install -y python2-pip

WORKDIR /opt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN python setup.py install 

#RUN pwd && ls
COPY ./etc /etc/agentmanager

COPY ./bin/agentmanager-api  /usr/local/bin/

EXPOSE 8081
CMD ["/bin/bash", "./start.sh"]
#CMD ["agentmanager-api"]

