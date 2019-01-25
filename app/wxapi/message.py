# msg_text_type_module = '''
# <xml>
#     <ToUserName>< ![CDATA[%s] ]>
#     </ToUserName>
#     <FromUserName>< ![CDATA[%s] ]>
#     </FromUserName>
#     <CreateTime>%d</CreateTime>
#     <MsgType>< ![CDATA[text] ]>
#     </MsgType>
#     <Content>< ![CDATA[%s] ]>
#     </Content>
#     <MsgId>%s</MsgId>
# </xml>
# '''

# msg_image_type_module = '''
# <xml>
#     <ToUserName>< ![CDATA[%s] ]>
#     </ToUserName>
#     <FromUserName>< ![CDATA[%s] ]>
#     </FromUserName>
#     <CreateTime>%d</CreateTime>
#     <MsgType>< ![CDATA[image] ]>
#     </MsgType>
#     <PicUrl>< ![CDATA[%s] ]>
#     </PicUrl>
#     <MediaId>< ![CDATA[%s] ]>
#     </MediaId>
#     <MsgId>%d</MsgId>
# </xml>
# '''

# msg_voice_type_module = '''
# <xml>
#     <ToUserName>< ![CDATA[%s] ]>
#     </ToUserName>
#     <FromUserName>< ![CDATA[%s] ]>
#     </FromUserName>
#     <CreateTime>%d</CreateTime>
#     <MsgType>< ![CDATA[voice] ]>
#     </MsgType>
#     <MediaId>< ![CDATA[%s] ]>
#     </MediaId>
#     <Format>< ![CDATA[%s] ]>
#     </Format>
#     <MsgId>%d</MsgId>
# </xml>
# '''

# msg_video_type_module = '''
# <xml>
#     <ToUserName>< ![CDATA[%s] ]>
#     </ToUserName>
#     <FromUserName>< ![CDATA[%s] ]>
#     </FromUserName>
#     <CreateTime>%d</CreateTime>
#     <MsgType>< ![CDATA[video] ]>
#     </MsgType>
#     <MediaId>< ![CDATA[%s] ]>
#     </MediaId>
#     <ThumbMediaId>< ![CDATA[%s] ]>
#     </ThumbMediaId>
#     <MsgId>%d</MsgId>
# </xml>
# '''

# msg_location_type_module = '''
# <xml>
#     <ToUserName>< ![CDATA[%s] ]>
#     </ToUserName>
#     <FromUserName>< ![CDATA[%s] ]>
#     </FromUserName>
#     <CreateTime>%d</CreateTime>
#     <MsgType>< ![CDATA[location] ]>
#     </MsgType>
#     <Location_X>%.6f</Location_X>
#     <Location_Y>%.6f</Location_Y>
#     <Scale>%d</Scale>
#     <Label>< ![CDATA[%s] ]>
#     </Label>
#     <MsgId>%d</MsgId>
# </xml>
# '''

# msg_link_type_module = '''
# <xml>
#     <ToUserName>< ![CDATA[%s] ]>
#     </ToUserName>
#     <FromUserName>< ![CDATA[%s] ]>
#     </FromUserName>
#     <CreateTime>%d</CreateTime>
#     <MsgType>< ![CDATA[link] ]>
#     </MsgType>
#     <Title>< ![CDATA[%s] ]>
#     </Title>
#     <Description>< ![CDATA[%s] ]>
#     </Description>
#     <Url>< ![CDATA[%s] ]>
#     </Url>
#     <MsgId>%d</MsgId>
# </xml>
# '''

from app.utils.hbujwxt import HbuJwxt
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class MessageBuilder(object):
    __msg_base = '''
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<MsgId>%d</MsgId>
'''

    @property
    def msg_base(self):
        return self.__msg_base

    def build_text_msg(self, to_user, from_user, create_time, msg_id, content):
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'text', msg_id)
        msg += '<Content><![CDATA[%s]]></Content>\n' % content
        msg += '</xml>'
        return msg

    def build_image_msg(self, to_user, from_user, create_time, msg_id, media_id):
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'image', msg_id)
        msg += '<Image><MediaId><![CDATA[%s]]></MediaId></Image>\n' % media_id
        msg += '</xml>'
        return msg

    def build_voice_msg(self, to_user, from_user, create_time, msg_id, media_id):
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'voice', msg_id)
        msg += '<Voice><MediaId><![CDATA[%s]]></MediaId></Voice>\n' % media_id
        msg += '</xml>'
        return msg

    def build_video_msg(self, to_user, from_user, create_time, msg_id, media_id, title, description):
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'video', msg_id)
        msg += '<Video>\n'
        msg += '<MediaId><![CDATA[%s]]></MediaId>\n' % media_id
        msg += '<Title><![CDATA[%s]]></Title>\n' % title
        msg += '<Description><![CDATA[%s]]></Description>\n' % description
        msg += '</Video>\n'
        msg += '</xml>'
        return msg

    def build_music_msg(self, to_user, from_user, create_time, msg_id, thumb_media_id, title, description, music_url, hq_music_url):
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'music', msg_id)
        msg += '<Music>\n'
        msg += '<Title><![CDATA[%s]]></Title>\n' % title if title else ""
        msg += '<Description><![CDATA[%s]]></Description>\n' % description
        msg += '<MusicUrl><![CDATA[%s]]></MusicUrl>\n' % music_url
        msg += '<HQMusicUrl><![CDATA[%s]]></HQMusicUrl>\n' % hq_music_url
        msg += '<ThumbMediaId><![CDATA[%s]]></ThumbMediaId>\n' % thumb_media_id
        msg += '</Music>\n'
        msg += '</xml>'
        return msg

    def build_news_msg(self, to_user, from_user, create_time, msg_id, title, description, pic_url, url):
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'news', msg_id)
        msg += '<ArticleCount>%d</ArticleCount>\n' % 1
        msg += '<Articles>\n'
        msg += self._build_article(title, description, pic_url, url)
        # weixin adjust!!!
        # for title, description, pic_url, url in zip(titles, descriptions, pic_urls, urls):
        #     msg += self._build_article(title, description, pic_url, url)
        msg += '</Articles>\n' 
        msg += '</xml>'
        return msg

    def _build_article(self, title, description, pic_url, url):
        article = '<item>\n'
        article += '<Title><![CDATA[%s]]></Title>\n' % title
        article += '<Description><![CDATA[%s]]></Description>\n' % description
        article += '<PicUrl><![CDATA[%s]]></PicUrl>\n' % pic_url
        article += '<Url><![CDATA[%s]]></Url>\n' % url
        article += '</item>\n'
        return article

class MessageProcessor(object):
    __slots__ = ['mb', 'hbujwxt', 'xml_rec', 'to_user', 'from_user', 'msg_id', 'create_time', 'msg_type']
    def __init__(self):
        self.mb = MessageBuilder()
        self.hbujwxt = HbuJwxt()

    def check_reply(self, receieve):
        self.xml_rec = ET.fromstring(receieve)
        self.to_user = self.xml_rec.find('ToUserName').text
        self.from_user = self.xml_rec.find('FromUserName').text
        self.create_time = int(self.xml_rec.find('CreateTime').text)
        self.msg_id = int(self.xml_rec.find('MsgId').text)
        self.msg_type = self.xml_rec.find('MsgType').text
        if self.msg_type == 'text':
            return self.text_reply()
        elif self.msg_type == 'image':
            pass
        elif self.msg_type == 'voice':
            pass
        elif self.msg_type == 'video':
            pass
        elif self.msg_type == 'location':
            pass
        elif self.msg_type == 'link':
            pass
        else:
            return '欢迎使用河大青年!'

        if self.msg_type != 'text':
            return '欢迎使用河大青年!'
        response = make_response(xml_msg)
        response.content_type = 'application/xml'
        return response

    def text_reply(self):
        userinfo = {'username':'20171004113', 'password':'199892.lw'}
        content = self.xml_rec.find('Content').text
        data = ""
        if content.startswith('我的学籍'):
            data = self.hbujwxt.query_schoolrool(userinfo)
        elif content.startswith('我的成绩'):
            data = self.hbujwxt.query_this_term_score(userinfo)       
        elif content.startswith('我的成绩'):
            data = self.hbujwxt.query_each_term_score(userinfo)
        else:
            data = "未知信息格式"        
        return self.mb.build_text_msg(self.to_user,
            self.from_user,
            self.create_time,
            self.msg_id, data)            

    def image_reply(self):
        pass           

    def voice_reply(self):
        pass

    def video_reply(self): 
        pass 

    def music_reply(self):
        pass

    def news_reply(self):
        pass

