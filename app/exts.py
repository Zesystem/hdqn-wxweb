##########################################
#
# 扩展
# author: TuYaxuan
# time: 2019/3/14
# 说明: 防循环引用
#
###########################################


from app.utils.hbujwxt import HbuJwxt
hbujwxt = HbuJwxt()

from app.wxapi.message import MessageBuilder, MessageProcessor
mp = MessageProcessor(MessageBuilder())

from multiprocessing import Lock
lock = Lock()