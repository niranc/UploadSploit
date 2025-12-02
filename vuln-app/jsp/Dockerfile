FROM tomcat:9-jdk11

WORKDIR /usr/local/tomcat

RUN rm -rf webapps/*

COPY . webapps/vuln-jsp

EXPOSE 8080

CMD ["catalina.sh", "run"]


