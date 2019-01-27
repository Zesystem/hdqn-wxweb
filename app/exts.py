from app.utils.hbujwxt import HbuJwxt
hbujwxt = HbuJwxt()

from app.wxapi.message import MessageBuilder, MessageProcessor
mp = MessageProcessor(MessageBuilder())
