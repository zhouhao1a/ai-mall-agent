#0 成功 / 1xxx 通用 / 2xxx 用户 / 3xxx 商品 / 4xxx 订单
def success(data=None,message="success",code=0):
    return {"code": code, "message": message, "data": data}

def fail(data=None,message="fail",code=1):
    return {"code":code,"message":message,"data":data}