FROM debian

RUN mkdir /metabase

RUN apt update
RUN apt upgrade
RUN apt install -y wget
RUN apt install -y default-jdk-headless
RUN wget -O /metabase.jar http://downloads.metabase.com/v0.32.8/metabase.jar

RUN groupadd metabasegroup && \
    useradd -U -m -G metabasegroup metabase && \
    chown -R metabase:metabase /metabase

VOLUME /metabase

EXPOSE 3000
WORKDIR /metabase/
#CMD ["java", "-jar", "/metabase.jar"]
ENTRYPOINT ["java", "-jar", "/metabase.jar"]

USER metabase

