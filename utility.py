try:
    from key import rsk, rsks
except:
    raise RuntimeError("未放入密钥文件")

ua = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
