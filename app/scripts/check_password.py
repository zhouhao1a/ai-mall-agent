"""验证 security.py 里的两个函数是否正常工作。"""
from app.core.security import hash_password, verify_password

pwd = "123456"

h1 = hash_password(pwd)  # 第一次算哈希
h2 = hash_password(pwd)  # 同一个密码，再算一次
print("第一次:", h1)
print("第二次:", h2)
print("两次结果一样吗:", h1 == h2)
print()

print("正确密码验证:", verify_password("123456", h1))
print("错误密码验证:", verify_password("000000", h1))