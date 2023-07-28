FROM centos:7.9.2009
MAINTAINER liubz "mrbingzhao@qq.com"

# 更新系统并升级
RUN yum -y update && \
    yum -y upgrade && \
    yum clean all

RUN yum install git gcc libpcap-devel gcc-c++ openssl-devel bzip2-devel libffi-devel wget make chrpath gzip -y # buildkit

#RUN yum install -y centos-release-scl rh-python38 which # 仓库注册 安装python3.8
# 创建软连接
#RUN ln -s /opt/rh/rh-python38/root/usr/bin/python3 /usr/local/bin/python3
#RUN ln -s /opt/rh/rh-python38/root/usr/bin/pip3 /usr/local/bin/pip3

RUN cd /opt && wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz && tar xzf Python-3.8.7.tgz && cd Python-3.8.7 && ./configure --enable-optimizations && make altinstall # buildkit
RUN rm -rf /opt/Python-3.8.7.tgz
RUN ln -s /usr/local/bin/pip3.8 /usr/local/bin/pip3 && ln -s /usr/local/bin/python3.8 /usr/local/bin/python3
#RUN yum -y install python36 python36-devel && \
RUN yum -y install git boost-devel boost-test boost zlib bzip2 xz cmake make gcc-c++ && \
    yum clean all
# install kenlm
#ADD kenlm.zip /opt/kenlm/
#WORKDIR /opt/kenlm/
#RUN pip3 install https://github.com/kpu/kenlm/archive/master.zip
#RUN pip3 install kenlm.zip
#RUN rm -rf /opt/kenlm/
RUN pip3 install kenlm
# clone repo
#RUN git clone --depth=1 https://github.com/shibing624/pycorrector.git
#WORKDIR /home/work/pycorrector
WORKDIR /root/Server/
ADD examples /root/Server/
# install requirements.txt
RUN pip3 install -U pip setuptools
RUN pip3 install jieba pypinyin numpy six transformers>=4.1.1 flask flasgger urllib3==1.26.16 torch -i https://pypi.tuna.tsinghua.edu.cn/simple
# install pycorrector by pip3
RUN pip3 install pycorrector -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip3 install torch -i https://pypi.tuna.tsinghua.edu.cn/simple
# support chinese with utf-8
RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
ENV LC_ALL zh_CN.UTF-8
RUN export LC_ALL=zh_CN.UTF-8
RUN export LANG=zh_CN.UTF-8
CMD /bin/bash