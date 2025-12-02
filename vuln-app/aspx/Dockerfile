FROM mono:latest

RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list && \
    apt-get update && apt-get install -y mono-xsp4 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

EXPOSE 8081

CMD ["xsp4", "--port=8081", "--nonstop", "--root=/app"]


