##########################################
#
# 数据库工具函数封装
# author: TuYaxuan
# time: 2019/3/14
# 说明: 依赖app.models
#
###########################################


from app.models import TextMaterial

def text_query(key):
    text_material = TextMaterial.query.filter(TextMaterial.keyword == key).first()
    res = '' if text_material is None else text_material.content
    return "<br/>".join('<p>'+line+'</p>' for line in res.split('\n'))
