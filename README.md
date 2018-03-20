
Example .gitlab-ci.yml

```.gitlab-ci.yml
image: DOCKER-IMAGE

# anything else

before_script:
  - gitbook install
  - /usr/bin/env python /data/scripts/gitbook-summary

# anything else

```

Example DOCKFILE

```DOCKERFILE

FROM centos:7

RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
RUN yum clean all
RUN rm -rf /var/cache/yum
RUN yum makecache

RUN yum install -y epel-release
RUN yum install -y ack
RUN curl --silent --location https://rpm.nodesource.com/setup_8.x | bash -
RUN yum install -y nodejs

RUN npm install -g gitbook-cli
RUN npm install -g doctoc
RUN gitbook fetch latest

ADD gitbook-summary.py /data/scripts/gitbook-summary

```