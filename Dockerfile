# Build from repository root: docker build -f Dockerfile -t fake-news-agent .
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /build
COPY spring-agent/pom.xml spring-agent/pom.xml
COPY spring-agent/src spring-agent/src
RUN mvn -f spring-agent/pom.xml -DskipTests package
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /build/spring-agent/target/fake-news-agent-1.0.0.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
