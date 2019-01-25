from flask import request, make_response, render_template
import time
import hashlib
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
from .message import MessageBuilder, get_media_id

mb = MessageBuilder()
def wx_check():
    """微信token接口验证"""
    if request.method == 'GET':
        data = request.args
        if len(data) == 0:
            return render_template('wxinter.html')
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
        xml_rec = ET.fromstring(rec)          
        to_user = xml_rec.find('ToUserName').text
        from_user = xml_rec.find('FromUserName').text
        msg_id = xml_rec.find('MsgId').text
        msg_type = xml_rec.find('MsgType').text

        if msg_type == 'text':
            xml_msg = mb.build_news_msg(from_user, to_user, int(time.time()), int(msg_id), 'test', 'this is a test!','http://files.jb51.net/file_images/article/201602/201621691400759.jpg?20161169148', 'http://files.jb51.net/file_images/article/201602/201621691400759.jpg?20161169148')
            # xml_msg = mb.build_text_msg(from_user, to_user, int(time.time()), int(msg_id), "get text message")
        elif msg_type == 'image':
            xml_msg = mb.build_text_msg(from_user, to_user, int(time.time()), int(msg_id), "get image message")
        elif msg_type == 'voice':
            xml_msg = mb.build_text_msg(from_user, to_user, int(time.time()), int(msg_id), "get voice message")
        elif msg_type == 'video':
            xml_msg = mb.build_text_msg(from_user, to_user, int(time.time()), int(msg_id), "get video message")
        elif msg_type == 'location':
            xml_msg = mb.build_text_msg(from_user, to_user, int(time.time()), int(msg_id), "get location message")
        elif msg_type == 'link':
            xml_msg = mb.build_text_msg(from_user, to_user, int(time.time()), int(msg_id), "get link message")
        else:
            return '欢迎使用河大青年!'
        response = make_response(xml_msg)
        response.content_type = 'application/xml'
        return response

        # print(rec)
        # xml_msg = mb.build_text_msg(from_user, to_user, int(time.time()), int(msg_id), content)
        # xml_msg = mb.build_image_msg(from_user, to_user, int(time.time()), int(msg_id), 'koSj3Ps5plMVrASaOA8d88X2sgIcJJKdyFzuN9k384NPVuOpcsCdg7ZthSVRTxWe')
        # weixin adjust!!!
        # xml_msg = mb.build_news_msg(from_user, to_user, int(time.time()), int(msg_id), 2, ['test', 'dev'], ['test', 'dev'], ['http://files.jb51.net/file_images/article/201602/201621691400759.jpg?20161169148', 'http://files.jb51.net/file_images/article/201602/201621691400759.jpg?20161169148'], ['http://files.jb51.net/file_images/article/201602/201621691432892.jpg?201611691440', 'http://files.jb51.net/file_images/article/201602/201621691400759.jpg?20161169148'])
        # xml_msg = mb.build_news_msg(from_user, to_user, int(time.time()), int(msg_id), 'test', 'this is a test!','http://files.jb51.net/file_images/article/201602/201621691400759.jpg?20161169148', 'http://files.jb51.net/file_images/article/201602/201621691400759.jpg?20161169148')
        # xml_msg = mb.build_video_msg(from_user, to_user, int(time.time()), int(msg_id), 'bCFWwpuBixR72foHVsrkeL955JVrPI-Hb4Jp6KdHPqlCLG_0vbPj67uPgga1E2jm', '哈哈', '嘿嘿的')
        # xml_msg = mb.build_voice_msg(from_user, to_user, int(time.time()), int(msg_id), '8Hx1XOzTtwx_dECEps8tXr0ZSwPZUvkiyLCAhVe8Ch_maBe_SyzpI4UE0MyKSB7_')
        # xml_msg = mb.build_music_msg(from_user, to_user, int(time.time()), int(msg_id), '_aV304Lds_eMIhQegJV3M8h4LeGxH2rx9SF3LNFGQ0cIgWb-PSJ8C2oW42d3sp1Y', 'xzq', 'tf', 'http://www.ytmp3.cn/down/56232.mp3', 'http://www.ytmp3.cn/down/56232.mp3')
        # print(xml_msg)


