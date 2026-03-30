FROM python:3.12-slim

# Install tk, xvfb, VNC server, noVNC, and system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3-tk \
       xvfb \
       x11vnc \
       novnc \
       websockify \
       libpng-dev \
       libjpeg-dev \
       build-essential \
       supervisor \
       curl \
       python3-setuptools \
       x11-xserver-utils \
       xfonts-base \
       adwaita-icon-theme \
       x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Set up VNC
RUN mkdir -p /root/.vnc
RUN x11vnc -storepasswd password /root/.vnc/passwd
RUN chmod 600 /root/.vnc/passwd

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY aceest_ui.py .

# Point the UI to backend service inside compose network by default
ENV API_BASE_URL=http://flask-app:5000

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose noVNC port
EXPOSE 6080

# Run supervisor to manage VNC and app
CMD ["/usr/bin/supervisord"]
