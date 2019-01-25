from flask import Flask
from app.wxapi import wxinter

app = Flask(__name__)

@app.route('/wx', methods=['GET', 'POST'])
def wx():
    """微信token接口验证"""
    return wxinter.wx_check()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
