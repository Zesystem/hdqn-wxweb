##########################################
#
# 微信信息处理工具类封装
# author: TuYaxuan
# time: 2019/3/14
# 说明: 整个微信公众号内的消息回复处理
#
###########################################

from flask import g, make_response, session
from app import db, app_config
from app.exts import hbujwxt
from app.models import User, TextMaterial, PhoneList
from app.utils import status
from app.wxapi import wxevent
from app.utils.userprocess import UserProcessor 
from app.utils.weatherutil import getWeather
from app.utils.bookutil import book_query
from app.utils.expressutil import express_query
from app.utils.busutil import nearbystation_query, line_query, transfer_query
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
import time

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
        """
        文本消息回复
        content: 文本内容
        """
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'text', msg_id)
        msg += '<Content><![CDATA[%s]]></Content>\n' % content
        msg += '</xml>'
        return msg

    def build_image_msg(self, to_user, from_user, create_time, msg_id, media_id):
        """
        图片消息回复
        media_id: 多媒体图片文件id
        """
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'image', msg_id)
        msg += '<Image><MediaId><![CDATA[%s]]></MediaId></Image>\n' % media_id
        msg += '</xml>'
        return msg

    def build_voice_msg(self, to_user, from_user, create_time, msg_id, media_id):
        """
        语音消息回复
        media_id: 多媒体语音文件id
        """
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'voice', msg_id)
        msg += '<Voice><MediaId><![CDATA[%s]]></MediaId></Voice>\n' % media_id
        msg += '</xml>'
        return msg

    def build_video_msg(self, to_user, from_user, create_time, msg_id, media_id, title, description):
        """
        视频消息回复
        media_id： 多媒体视频文件id
        title: 标题
        description: 简介
        """
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
        """
        音乐消息回复
        thumb_media_id: 多媒体缩略图文件id
        title: 标题
        description: 简介
        music_url: 普通音质音乐链接
        hq_music_url: 高清音质音乐链接
        """
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
        """
        图文消息回复
        title: 标题
        description: 简介
        pic_url: 封面图片链接
        url: 图文链接
        """
        msg = '<xml>'
        msg += self.msg_base % (to_user, from_user, create_time, 'news', msg_id)
        msg += '<ArticleCount>%d</ArticleCount>\n' % 1
        msg += '<Articles>\n'
        msg += self._build_article(title, description, pic_url, url)
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
    """信息处理器"""
    __slots__ = ['mb', 'xml_rec', 'to_user', 'from_user', 'create_time', 'msg_id', 'msg_type']
    def __init__(self, mb):
        self.mb = mb

    def check_reply(self, receieve):
        """消息内容验证回复处理"""
        self.xml_rec = ET.fromstring(receieve)
        self.to_user = self.xml_rec.find('ToUserName').text
        g.openid = self.from_user = self.xml_rec.find('FromUserName').text
        self.create_time = int(time.time()) # int(self.xml_rec.find('CreateTime').text)
        self.msg_type = self.xml_rec.find('MsgType').text

        self.msg_id = self.xml_rec.find('MsgId')
        if self.msg_id is not None:
            self.msg_id = int(self.msg_id.text)
        else:
            self.msg_id = 0

        if self.msg_type == 'text':
            return self.text_reply()
        if self.msg_type == 'event':
            return self.event_reply()
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
            xml_msg = '欢迎使用河大青年!'

        if self.msg_type != 'text':
            xml_msg = '欢迎使用河大青年!'
        response = make_response(xml_msg)
        response.content_type = 'application/xml'
        return response
    
    def text_process(self, keyword):
        """文本关键字数据库查询"""
        text_material =  TextMaterial.query.filter(TextMaterial.keyword == keyword).first()
        if text_material is not None:
            return text_material.content
        return ''


    def text_reply(self):
        """处理文本内容回复"""
        content = self.xml_rec.find('Content').text
        reply = self.text_process(content)
        if reply == '':
            #__________________________________________________
            # 河小博
            #__________________________________________________

            ##############################
            # 绑定账号处理
            ##############################
            if content.startswith('绑定'):
                grp = content.split(' ')
                if len(grp) != 3 or grp[2].isspace():
                    reply = self.text_process('绑定格式')
                else:
                    g.userinfo = {'username':grp[1], 'password':grp[2]}
                    code = UserProcessor.bind_user()
                    if code == status.CODE_SUCCESS:
                        reply = self.text_process('绑定成功')
                    elif code == status.CODE_EXIST:
                        reply = self.text_process('已经绑定')
                    else:
                        reply = self.text_process('绑定失败')
            elif content.startswith('确认解绑'):
                code = UserProcessor.unbind_user()
                if code == status.CODE_SUCCESS:
                    reply = self.text_process('解绑成功')
                elif code == status.CODE_NOT_EXIST:
                    reply = self.text_process('绑定学号')
                else:
                    reply = self.text_process('系统错误')
            ##############################
            # 修改密码处理
            ##############################
            elif content.startswith('改密'):
                user = User.query.filter(User.openid == g.openid).first()
                if user is not None:
                    grp = content.split(' ')
                    if len(grp) != 2 or grp[1].isspace():
                        reply = self.text_process('改密格式')
                    else:
                        g.userinfo = {'username':user.studentID, 'password':grp[1]}
                        code = UserProcessor.update_user()
                        if code == status.CODE_SUCCESS:
                            reply = self.text_process('改密成功')
                        else:
                            reply = self.text_process('改密失败')
                else:
                    reply = self.text_process('绑定学号')
            ##############################
            # 查询学籍处理
            ##############################
            elif content.startswith('我的学籍'):
                user = UserProcessor.get_user()
                if user is not None:
                    g.userinfo = {'username':user.studentID, 'password':user.studentPWD}
                    reply = ''
                    res = hbujwxt.query_schoolrool(g.userinfo)
                    if res['code'] == status.CODE_SUCCESS:
                        data = res['data']
                        for k,v in data.items():
                            reply += '{} {}\n'.format(k, v)
                else:
                    reply = self.text_process('绑定学号')
            ##############################
            # 查询本学期成绩处理
            ##############################
            elif content.startswith('我的成绩'):
                user = UserProcessor.get_user()
                if user is not None:
                    g.userinfo = {'username':user.studentID, 'password':user.studentPWD}
                    reply = '学号: {}\n'.format(g.userinfo['username'])
                    res = hbujwxt.query_this_term_score(g.userinfo)
                    reply += '课程名********成绩********排名\n'
                    if res['code'] == status.CODE_SUCCESS:
                        data = res['data']   
                        for courseinfo in data:
                            reply += '-'*40 + '\n'
                            reply += '{}**{}**{}\n'.format(*courseinfo)
                else:
                    reply = self.text_process('绑定学号')
            ##############################
            # 查询所有成绩处理
            ##############################
            elif content.startswith('所有成绩'):
                user = UserProcessor.get_user()
                if user is not None:
                    g.userinfo = {'username':user.studentID, 'password':user.studentPWD}    
                    reply = '学号: {}\n'.format(g.userinfo['username'])      
                    res = hbujwxt.query_each_term_score(g.userinfo)
                    if res['code'] == status.CODE_SUCCESS:
                        data = res['data']
                        for term in data:
                            reply += '-'*40 + '\n'
                            reply += term['term_name'] + '\n'
                            for courseinfo in term['scores']:
                                reply += '{} {}\n'.format(*courseinfo)
                            reply += '-'*40 + '\n\n'
                else:
                    reply = self.text_process('绑定学号')
            ##############################
            # 查询课表处理
            ##############################
            elif content.startswith('课表查询'):
                user = UserProcessor.get_user()
                if user is not None:
                    reply = '<a href="{app_domain}public/curriculum?openid={openid}">好好学习，天天向上，HELLO~我是河小博~点击查看课表信息～～</a>'.format(
                        app_domain = app_config.APP_DOMAIN,
                        openid = g.openid
                    )
                else:
                    reply = self.text_process('绑定学号')
            ##############################
            # 网上评教
            ##############################
            elif content.startswith('网上评教'):
                user = UserProcessor.get_user()
                if user is not None:
                    reply = '<a href="{app_domain}public/evaluate?openid={openid}">好好学习，天天向上，HELLO~我是河小博~点击进入网上评教</a>'.format(
                        app_domain = app_config.APP_DOMAIN,
                        openid = g.openid
                    )
                else:
                    reply = self.text_process('绑定学号')
            ##############################
            # 图书信息
            ##############################
            elif content.startswith('图书'):
                grp = content.split(' ')
                if len(grp) != 2 or grp[1].isspace():
                    reply = self.text_process('图书信息')
                else:
                    reply = '<a href="{app_domain}public/book?openid={openid}&book_name={book_name}">好好学习，天天向上，HELLO~我是河小博~点击查看图书详情</a>'.format(
                        app_domain = app_config.APP_DOMAIN,
                        openid = g.openid,
                        book_name = grp[1]
                    )
            ##############################
            # 空闲自习室
            ##############################
            elif content.startswith('空闲自习室'):
                reply = '<a href="{app_domain}public/spareclassroom?openid={openid}">好好学习，天天向上，HELLO~我是河小博~点击进入查询空闲自习室</a>'.format(
                    app_domain = app_config.APP_DOMAIN,
                    openid = g.openid
                )
            #__________________________________________________
            # 河小知
            #__________________________________________________
             
            ##############################
            # 天气查询
            ##############################
            elif content.startswith('天气'):
                grp = content.split(' ')
                if len(grp) != 2 or grp[1].isspace():
                    reply = self.text_process('天气预报')
                else:
                    res = getWeather(grp[1])
                    if res['code'] == status.CODE_SUCCESS:
                        reply = '查询结果如下\n'
                        for item in res['data'].values():
                            reply +=  item + '\n'
                    elif res['code'] == status.CODE_NOT_EXIST:
                        reply = '查询的城市不存在哦～～～'
                    else:
                        reply = '服务器资源错误，联系管理员修复~~~'
            ##############################
            # 公交查询
            ##############################
            elif content.startswith('附近公交'):
                grp = content.split(' ')
                if len(grp) != 2 or grp[1].isspace():
                    reply = self.text_process('公交查询')
                else:
                    res = nearbystation_query(grp[1])
                    if res['code'] == status.CODE_SUCCESS:
                        reply = '附近的公交站点如下\n'
                        for num, item in enumerate(res['data']):
                            reply += '【{}】{}\n'.format(num, item)
                    else:
                        reply = '没有查询到该地点附近公交\n请检查地点是否输入有误～～～'
            elif content.startswith('公交'):
                grp = content.split(' ')
                grp_len = len(grp)
                if grp_len == 2 and not grp[1].isspace():
                    res = line_query(grp[1])
                    if res['code'] == status.CODE_SUCCESS:
                        reply = '路线查询结果如下\n'
                        for num, item in enumerate(res['data']):
                            reply += '({}){}\n'.format(num, item)
                    else:
                        reply = '没有你要查询的路线\n请检查路线是否输入有误～～～'
                elif grp_len == 3 and not grp[2].isspace():
                    res = transfer_query(*grp[1:])
                    if res['code'] == status.CODE_SUCCESS:
                        reply = '换乘路线查询结果如下\n'
                        for num, item in enumerate(res['data']):
                            reply += '【{}】{}\n'.format(num, item)
                    else:
                        reply = '没有你要查询的换乘信息\n请检查换乘起始地点是否输入有误～～～'
                else:
                    reply = self.text_process('公交查询')
            ##############################
            # 快递查询
            ##############################
            if content.startswith('快递'):
                grp = content.split(' ')
                if len(grp) != 2 or grp[1].isspace():
                    reply = self.text_process('快递查询')
                else:
                    res = express_query(grp[1])
                    if res['code'] == status.CODE_SUCCESS:
                        reply = '查到的快递信息如下\n'
                        for item in res['data']:
                            reply += '-'*40 + '\n'
                            reply +=  '{} : {}\n'.format(item['time'], item['context'])
                    elif res['code'] == status.CODE_NOT_EXIST:
                        reply = '查询快递单号可能不在哦～～～'
                    else:
                        reply = '服务器资源错误，请联系管理员修复～～～'
            ##############################
            # 电话查询
            ##############################
            elif content.startswith('办公机构'):
                reply = '<a href="{app_domain}public/phone?openid={openid}">点我即可查看所有办公机构哦～～～</a>'.format(
                        app_domain = app_config.APP_DOMAIN,
                        openid = g.openid
                    )
            elif content.startswith('电话'):
                grp = content.split(' ')
                if len(grp) != 2 or grp[1].isspace():
                    reply = self.text_process('办公电话')
                else:
                    phone = PhoneList.query.filter(PhoneList.address.like('%{}%'.format(grp[1]))).first()
                    if phone:
                        reply = '查询的电话如下\n'
                        reply += '{} {}'.format(phone.address, phone.phone)
                    else:
                        reply = '暂时没有你要查询的办公电话\n请检查你输入的办公机构名称'
            ##############################
            # 社团活动
            ##############################
            ######### __________ #########

            #__________________________________________________
            # 河掌柜
            #__________________________________________________

            ##############################
            # 意见反馈
            ##############################
            elif content.startswith('意见反馈'):
                reply = '<a href="{app_domain}public/feedback?openid={openid}">点击便可访问反馈页面</a>'.format(
                    app_domain = app_config.APP_DOMAIN,
                    openid = g.openid
                )

        if reply == "":
            reply = self.text_process('留言')
        return self.mb.build_text_msg(self.from_user, self.to_user, self.create_time, self.msg_id, reply)            

    def event_reply(self):
        """处理事件内容回复"""
        event = self.xml_rec.find('Event').text
        if event == 'subscribe':
            reply = self.text_process('关注')
            return self.mb.build_text_msg(self.from_user, self.to_user, self.create_time, self.msg_id, reply)
        elif event == 'unsubscribe':
            reply = 'success'
            user = User.query.filter(User.openid == g.openid).first()
            if user is not None:
                db.session.delete(user)
                db.session.commit()
        elif event == 'event1':
            reply = self.text_process('成绩查询')
        elif event == 'event2':
            reply = self.text_process('图书信息')
        elif event == 'event3':
            reply = '<a href="{app_domain}public/book?openid={openid}&book_name={book_name}">好好学习，天天向上，HELLO~我是河小博~点击查看图书详情</a>'.format(
                app_domain = app_config.APP_DOMAIN，
                openid = g.openid,
                book_name = grp[1])
        elif event == 'event4':
            reply = '<a href="{app_domain}public/evaluate?openid={openid}">好好学习，天天向上，HELLO~我是河小博~点击进入网上评教</a>'.format(
                app_domain = app_config.APP_DOMAIN,
                openid = g.openid
            )
        elif event == 'event5':
            reply = self.text_process('创业就业')
        elif event == 'event6':
            reply = self.text_process('后勤报修')
        elif event == 'event7':
            reply = self.text_process('河大全景')
        return reply

    def image_reply(self):
        """处理图片内容回复"""
        pass           

    def voice_reply(self):
        """处理语音内容回复"""
        pass

    def video_reply(self):
        """处理视频内容回复"""
        pass 

    def music_reply(self):
        """处理音乐内容回复"""
        pass

    def news_reply(self):
        """处理图文内容回复"""
        pass

