from flask import Flask, request, make_response
import hashlib
import time
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
from wxapi.message import MessageBuilder

app = Flask(__name__)
mb = MessageBuilder()

@app.route('/wx', methods=['GET', 'POST'])
def wx():
    """微信token接口验证"""
    if request.method == 'GET':
        data = request.args
        if len(data) == 0:
            return 'hello, this is handle view'
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        token = 'dev4hdqn'

        grp = [token, timestamp, nonce]
        grp.sort()
        hashcode = hashlib.sha1(''.join(grp).encode('utf-8')).hexdigest()

        print("handle/GET func: hashcode, signature:", hashcode, signature)
        if hashcode == signature:
            return make_response(echostr)
    else:
        rec = request.stream.read()
        print(rec.decode())
        return ""
        xml_rec = ET.fromstring(rec)          
        to_user = xml_rec.find('ToUserName').text
        from_user = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        msg_id = xml_rec.find('MsgId').text
        content = message_process(content)
        xml_response = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><MsgId>%d</MsgId></xml>"
        xml_msg = mb.build_text_msg(from_user, to_user, str(int(time.time())), int(msg_id), content)
        response = make_response(xml_msg)
        response.content_type = 'application/xml'
        return response
    return 'welcome to hdqn!'

def message_process(content):
    return "hello, this is hdqn-dev-test!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
