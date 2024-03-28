FROM eclipse-temurin:17-jdk-jammy
WORKDIR /app
COPY target/OSINT-Collector-0.0.1-SNAPSHOT.jar /app/OSINT-Collector-0.0.1-SNAPSHOT.jar
EXPOSE 8080
LABEL authors="ciromarrazzo"

CMD ["java", "-jar", "OSINT-Collector-0.0.1-SNAPSHOT.jar"]