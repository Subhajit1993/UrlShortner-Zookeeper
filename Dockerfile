FROM bitnami/zookeeper:3.5.7

ENV ALLOW_ANONYMOUS_LOGIN=yes

EXPOSE 2181 2888 3888 8080