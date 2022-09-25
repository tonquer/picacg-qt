cd src
pyinstaller --clean --onedir --name PicACG \
    --hidden-import waifu2x_vulkan --hidden-import PySide6 --hidden-import requests \
    --hidden-import urllib3 --hidden-import websocket-client --hidden-import pillow \
    --hidden-import config 
    --hidden-import component
    --hidden-import server
    --hidden-import task
    --hidden-import tools
    --hidden-import view
    --strip --windowed -i Icon.icns \
    start.py