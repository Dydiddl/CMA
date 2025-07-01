# CMA 데스크톱 애플리케이션 Dockerfile
FROM python:3.12-slim

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    # GUI 관련 패키지
    libxcb-cursor0 \
    libxcb-xinerama0 \
    libxcb-randr0 \
    libxcb-keysyms1 \
    libxcb-image0 \
    libxcb-icccm4 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-render0 \
    libxcb-render-util0 \
    libxcb-util1 \
    # 폰트 관련 패키지
    fonts-noto-cjk \
    fonts-dejavu \
    # 기타 필요한 패키지
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 한글 폰트 설치 (D2Coding)
RUN mkdir -p /usr/share/fonts/truetype/d2coding && \
    wget -O /tmp/D2Coding.zip "https://github.com/naver/d2codingfont/archive/refs/heads/master.zip" && \
    unzip /tmp/D2Coding.zip -d /tmp/ && \
    cp /tmp/d2codingfont-master/D2Coding*.ttf /usr/share/fonts/truetype/d2coding/ && \
    fc-cache -fv && \
    rm -rf /tmp/D2Coding.zip /tmp/d2codingfont-master

# 환경 변수 설정
ENV QT_QPA_PLATFORM=xcb
ENV LANG=ko_KR.UTF-8
ENV LC_ALL=ko_KR.UTF-8

# 포트 노출 (필요시)
EXPOSE 8000

# 실행 명령
CMD ["python", "main.py"] 