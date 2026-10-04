"""
统一响应外壳：所有接口都返回 {code, message, data}。
code 分段：0 成功 / 1xxx 通用 / 2xxx 用户 / 3xxx 商品 / 4xxx 订单。
失败不要在接口里手拼，抛 BizError 交给全局处理器。
"""

#0 成功 / 1xxx 通用 / 2xxx 用户 / 3xxx 商品 / 4xxx 订单
def success(data=None,message="success",code=0):
    return {"code": code, "message": message, "data": data}

def fail(data=None,message="fail",code=1):
    return {"code":code,"message":message,"data":data}
