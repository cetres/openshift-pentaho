FROM alpine:3.6

MAINTAINER Gustavo Oliveira <cetres@gmail.com>

RUN apk update && \
    apk add openjdk8-jre ca-certificates openssl bash webkitgtk && \
    update-ca-certificates

ENV JAVA_HOME=/usr/lib/jvm/default-jvm/jre
ENV PDI_VERSION=7.1 \
    PDI_BUILD=7.1.0.0-12 \
    JRE_HOME=${JAVA_HOME} \
    PENTAHO_JAVA_HOME=${JAVA_HOME} \
    DEST_DIR=/opt/pentaho \
    PENTAHO_HOME=/opt/pentaho/data-integration \
    PATH=${PATH}:${JAVA_HOME}/bin

#RUN adduser -h ${DEST_DIR} -s /bin/false -D -u 555 ${PENTAHO_USERNAME}

RUN mkdir -p ${DEST_DIR} && \
    wget -qO /tmp/pdi-ce.zip https://downloads.sourceforge.net/project/pentaho/Data%20Integration/${PDI_VERSION}/pdi-ce-${PDI_BUILD}.zip && \
    unzip -q /tmp/pdi-ce.zip -d ${DEST_DIR} && \
    rm -f /tmp/pdi-ce.zip

ADD docker-entrypoint.sh /opt/pentaho/data-integration/docker-entrypoint.sh

VOLUME ["/opt/pentaho/repository"]

WORKDIR /opt/pentaho/data-integration
EXPOSE 8080
#ENTRYPOINT []
CMD ["/bin/bash", "/opt/pentaho/data-integration/docker-entrypoint.sh", "master"]
