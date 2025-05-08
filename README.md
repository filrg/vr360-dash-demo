# 360° Video Streaming with DASH and VR Support

This project demonstrates how to stream 360° video content using [dash.js](https://github.com/Dash-Industry-Forum/dash.js) for MPEG-DASH playback and [A-Frame 1.7.0](https://github.com/aframevr/aframe) for WebVR integration.

## Features

* Adaptive bitrate streaming with MPEG-DASH
* VR headset compatibility via WebXR (A-Frame)
* HTTPS support using a self-signed certificate

## Requirements

> **Note:** A secure (HTTPS) connection is required for VR functionality in most modern browsers.

### Server Dependencies

Install `nghttp2` server:

```bash
sudo apt install http2-server
```

## Quick Start

### 1. Generate DASH Assets

Navigate to the video asset directory and run the following command to encode the video and generate the MPD file:

```bash
cd root/assets/

ffmpeg -re -i Application.MP4 \
-map 0:v -map 0:a \
-c:v libx264 -c:a aac \
-b:v:0 8000k -s:v:0 3840x1920 -profile:v:0 main \
-b:v:1 5000k -s:v:1 2560x1280 -profile:v:1 main \
-b:v:2 2500k -s:v:2 1920x960  -profile:v:2 baseline \
-b:v:3 1000k -s:v:3 1280x640  -profile:v:3 baseline \
-bf 1 -keyint_min 120 -g 120 -sc_threshold 0 -b_strategy 0 \
-ar 48000 \
-use_template 1 -use_timeline 1 \
-adaptation_sets "id=0,streams=v id=1,streams=a" \
-f dash manifest.mpd
```

### 2. Generate a Self-Signed Certificate

Navigate to the project root and create the certificate:

```bash
cd ../../
openssl req -new -x509 -newkey rsa:2048 -keyout private.key -out certificate.crt -days 365 -nodes
```

### 3. Start the HTTP/2 Server

Run the server with HTTPS enabled:

```bash
cd root
nghttpd -a 0.0.0.0 8080 ../private.key ../certificate.crt -v
```

### 4. Access the Demo

On the client side, open a web browser and navigate to:

```
https://localhost:8080
```

> Ensure you accept the browser's security warning for the self-signed certificate.

