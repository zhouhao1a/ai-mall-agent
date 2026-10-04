"""
自检脚本：验证 JWT 能正常签发、正常解析，篡改后解析失败。
"""

from app.core.security import create_access_token, decode_access_token

token = create_access_token(1)
print("token      :", token)
print("解出来     :", decode_access_token(token))
print("乱改签名后 :", decode_access_token(token[:-5] + "aaaaa"))
print("随便传个串 :", decode_access_token("hello"))
