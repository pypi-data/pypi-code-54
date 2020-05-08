
from .server import BaseServer
from hehe import he
import datetime;

"""
 * Uwsgi服务接口类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  uwsgi --http :8001 --wsgi-file main.py  --master --processes 4 --threads 2
 server {
        listen 80;
        server_name www.hehey.cn;

        location ~* \.(eot|ttf|woff|svg|otf)$ {
            add_header Access-Control-Allow-Origin *;
        }

        location ~ .*\.(gif|jpg|jpeg|bmp|png|ico|txt|js|css|eot|ttf|woff|svg|otf|woff2|mp4)$ {
            root /home/hehe/work/python/hehey/apps/assets/home;
        }


        client_max_body_size 50m;

        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:8002;

        }

        #location / {
        #        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        #        proxy_set_header Host $http_host;
        #        proxy_pass http://127.0.0.1:8000;
        #
        #        fastcgi_param SCRIPT_FILENAME $fastcgi_script_name;
        #        fastcgi_param PATH_INFO $fastcgi_script_name;
        #}

        error_log /home/hehe/www/logs/home_error.log error;
}

 *</pre>
 *<B>日志：</B>
 *<pre>
 *  略
 *</pre>
 *<B>注意事项：</B>
 *<pre>
 *  略
 *</pre>
"""


def millis(t1, t2):
    micros = (t2 - t1).microseconds
    delta = micros/1000
    return delta

class UwsgiServer(BaseServer):


    def run(self):

        return getattr(self,'wsgiApp');

    def wsgiApp(self,environ, start_response):

        start_milli_time = datetime.datetime.now()
        # 创建对应的应用类对象
        app = he.config.appClass(he.config);
        # 创建请求对象
        app.initReqeust(environ)
        # 运行应用
        app.runApp();

        # 返回响应body
        response = app.getRespone()

        # 设置响应头部
        start_response(response.buildHttpStatus(), response.buildHttpHeaders())
        # end_milli_time = datetime.datetime.now()



        return response.getContent()