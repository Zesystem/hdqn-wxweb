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

    def build_music_msg(self, to_user, from_user, create_time, msg_id, thumb_media_id, title, description, music_url, hq_music_url=None):
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

def get_media_id():
	return "HSA4OYQ0UbqWJ1gJIRaneuTdehHLu046qROUKH98ueMBz1-fK9Off4vYZ43gdUbH"
