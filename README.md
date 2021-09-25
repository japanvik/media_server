# media_server
A very simple python media (video) server using flask. Use the docker image and mount your video directories to servethem

## Requirements
- FFMpeg
- python 3.9

## Installation
- apt install ffmpeg (or equivalent for your distribution)
- pip install -f requirements.txt

## Usage
1. mount your media files in /media (TODO: make this changeable via command line parameters)
2. run the api.py and point your browser to localhost:9000 for a test html rendering

## Docker
Using docker to run the system is the best option.
1. Build the image by running 
```bash
docker build .
```
2. mount a directory with mp4 videos to /media
```bash
docker run -v {FULL_PATH_TO_YOUR_VIDEO_FILES}:/media -p 9000:9000 {DOCKER_IMAGE_NAME}
```
and hit the browser on port 9000


