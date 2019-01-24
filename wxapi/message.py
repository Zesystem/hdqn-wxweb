msg_text_type_module = '''
<xml>
    <ToUserName>< ![CDATA[%s] ]>
    </ToUserName>
    <FromUserName>< ![CDATA[%s] ]>
    </FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType>< ![CDATA[text] ]>
    </MsgType>
    <Content>< ![CDATA[%s] ]>
    </Content>
    <MsgId>%s</MsgId>
</xml>
'''

msg_image_type_module = '''
<xml>
    <ToUserName>< ![CDATA[%s] ]>
    </ToUserName>
    <FromUserName>< ![CDATA[%s] ]>
    </FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType>< ![CDATA[image] ]>
    </MsgType>
    <PicUrl>< ![CDATA[%s] ]>
    </PicUrl>
    <MediaId>< ![CDATA[%s] ]>
    </MediaId>
    <MsgId>%d</MsgId>
</xml>
'''

msg_voice_type_module = '''
<xml>
    <ToUserName>< ![CDATA[%s] ]>
    </ToUserName>
    <FromUserName>< ![CDATA[%s] ]>
    </FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType>< ![CDATA[voice] ]>
    </MsgType>
    <MediaId>< ![CDATA[%s] ]>
    </MediaId>
    <Format>< ![CDATA[%s] ]>
    </Format>
    <MsgId>%d</MsgId>
</xml>
'''

msg_video_type_module = '''
<xml>
    <ToUserName>< ![CDATA[%s] ]>
    </ToUserName>
    <FromUserName>< ![CDATA[%s] ]>
    </FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType>< ![CDATA[video] ]>
    </MsgType>
    <MediaId>< ![CDATA[%s] ]>
    </MediaId>
    <ThumbMediaId>< ![CDATA[%s] ]>
    </ThumbMediaId>
    <MsgId>%d</MsgId>
</xml>
'''

msg_location_type_module = '''
<xml>
    <ToUserName>< ![CDATA[%s] ]>
    </ToUserName>
    <FromUserName>< ![CDATA[%s] ]>
    </FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType>< ![CDATA[location] ]>
    </MsgType>
    <Location_X>%.6f</Location_X>
    <Location_Y>%.6f</Location_Y>
    <Scale>%d</Scale>
    <Label>< ![CDATA[%s] ]>
    </Label>
    <MsgId>%d</MsgId>
</xml>
'''

msg_link_type_module = '''
<xml>
    <ToUserName>< ![CDATA[%s] ]>
    </ToUserName>
    <FromUserName>< ![CDATA[%s] ]>
    </FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType>< ![CDATA[link] ]>
    </MsgType>
    <Title>< ![CDATA[%s] ]>
    </Title>
    <Description>< ![CDATA[%s] ]>
    </Description>
    <Url>< ![CDATA[%s] ]>
    </Url>
    <MsgId>%d</MsgId>
</xml>
'''

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

    def build_text_msg(self, from_user, to_user, create_time, msg_id, content):
        msg = '<xml>'
        msg += self.msg_base % (from_user, to_user, create_time, 'text', msg_id)
        msg += '<Content><![CDATA[%s]]></Content>\n' % content
        msg += '</xml>'
        return msg

    def build_image_msg(self, from_user, to_user, create_time, msg_id, pic_url, media_id):
        msg = '<xml>'
        msg += self.msg_base % (from_user, to_user, create_time, 'image', msg_id)
        msg += '<PicUrl><![CDATA[%s]]></PicUrl>\n' % pic_url
        msg += '<MediaId><![CDATA[%s]]></MediaId>\n' % media_id
        msg += '</xml>'
        return msg

    def build_voice_msg(self, from_user, to_user, create_time, msg_id, media_id):
        msg = '<xml>'
        msg += self.msg_base % (from_user, to_user, create_time, 'voice', msg_id)
        msg += '<PicUrl><![CDATA[%s]]></PicUrl>\n' % pic_url
        msg += '<MediaId><![CDATA[%s]]></MediaId>\n' % media_id
        msg += '</xml>'
        return msg

    def build_video_msg(self, from_user, to_user, create_time, msg_id, media_id, thumb_media_id):
        msg = '<xml>'
        msg += self.msg_base % (from_user, to_user, create_time, 'video', msg_id)
        msg += '<MediaId><![CDATA[%s]]></MediaId>\n' % media_id
        msg += '<ThumbMediaId><![CDATA[%s]]></ThumbMediaId>\n' % thumb_media_id
        msg += '</xml>'
        return msg

    def build_location_msg(self, from_user, to_user, create_time, msg_id, x, y, scale, label):
        msg = '<xml>\n'
        msg += self.msg_base % (from_user, to_user, create_time, 'location', msg_id)
        msg += '<Location_X><![CDATA[%.6f]]></Location_X>\n' % x
        msg += '<Location_Y><![CDATA[%.6f]]></Location_Y>\n' % y
        msg += '<Scale>%d</Scale>\n' % scale
        msg += '<Label><![CDATA[%s]]></Label>\n' % label
        msg += '</xml>'
        return msg

    def build_link_msg(self, from_user, to_user, create_time, msg_id, title, description, url):
        msg = '<xml>'
        msg += self.msg_base
        msg %= (from_user, to_user, create_time, 'link', msg_id)
        msg += '<Title><![CDATA[%s]]></Title>\n' % title
        msg += '<Description><![CDATA[%s]]></Description>\n' % description
        msg += '<Url><![CDATA[%s]]></Url>\n' % url
        msg += '</xml>'
        return msg

def get_media_id():
	return "HSA4OYQ0UbqWJ1gJIRaneuTdehHLu046qROUKH98ueMBz1-fK9Off4vYZ43gdUbH"