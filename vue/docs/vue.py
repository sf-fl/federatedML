from flask import Flask, render_template
from flask_cors import CORS
import os
import socket

app = Flask(__name__,
            template_folder="./",
            static_folder="./static")
CORS(app)


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__ =='__main__':
    import sys
    os.chdir((sys.path[0]))
    ip = get_host_ip()  # todo 存ip
    port = 5000   # todo 读配置
    path_list = os.listdir('./static/js')
    fl = ''
    for filename in path_list:
        if 'app.' in filename and 'map' not in filename:
            fl = filename
    with open("./static/js/"+fl, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # 写的方式打开文件
    with open("./static/js/"+fl, "w", encoding="utf-8") as f_w:
        for line in lines:
            if "/flp" in line:
              # 替换
                line = line.replace("/flp", 'http://'+ip+':'+str(port))
            f_w.write(line)
    app.run(host='0.0.0.0',port='8082')
