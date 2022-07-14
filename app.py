'''
Author: yll yangll-h@glodon.com
Date: 2020-08-18 19:32:17
LastEditors: yll yangll-h@glodon.com
LastEditTime: 2022-07-14 21:39:43
FilePath: /composetest/app.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import time
import redis
from flask import Flask
from flask import request


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)



@app.route('/')
def heme():
    count = get_hit_count()
    name = 'yll'
    return 'Hello World! I {} have been seen {} times.\n'.format(name, count)



@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run()
    

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


