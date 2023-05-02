import requests
import json
import redis
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

access_token_redis_key = "bb_wework_access_token"

url = "https://api-cn.louisvuitton.cn/api/zhs-cn/catalog/availability/nvprod3600089v"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
}
response = requests.get(url, headers=headers)

res = response.content.decode();
# print(res)
# print(type(res))
jsonres = json.loads(res)
print(jsonres)
# print(type(jsonres))

print(jsonres['skuAvailability'][0]['inStock'])
print(jsonres['skuAvailability'][0]['skuId'])

inStock = jsonres['skuAvailability'][0]['inStock'];
skuId = jsonres['skuAvailability'][0]['skuId'];

corpId = "ww7cfe17b78df8141e"
corpSecret = "eIDu4Uz3gxV79ADJQ6O94oDFWZXMKaEdJLRlL2U5tek"

# # redis部分逻辑start
# r = redis.Redis(host='sh-crs-bi6by7rh.sql.tencentcdb.com', port=23996, password='ueN6T2MvS$MVs%63n3')

# # 从 Redis 服务器读取数据
# access_token_redis = r.get(access_token_redis_key)
# print(3333333333)
# print(access_token_redis)
# print(3333333333)

# if access_token_redis is None:
#     access_token_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+corpId+"&corpsecret="+corpSecret
#     access_token_res_response = requests.get(access_token_url, headers=headers)
#     access_token_res = access_token_res_response.content.decode();
#     json_access_token_res = json.loads(access_token_res)
#     # access_token = json_access_token_res['access_token'];
#     print("===============access token=================")
#     print(json_access_token_res)
#     print("===============access token=================")
#     access_token_final = json_access_token_res['access_token']
#     r.setex(access_token_redis_key,5400,access_token_final)
# else:
#     access_token_final = access_token_redis
# # redis部分逻辑end
# access_token_final = access_token_final.decode('utf-8')

# msg_push_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+access_token_final;

if inStock:
    msg_bb = "到货啦！"
else:
    msg_bb = "还没到货！"

# post_data = {
#     "touser" : "SunYiTao|MiaoMiao",
#     "msgtype" : "text",
#     "agentid" : 1000006,
#     "text" : {
#        "content" : "skuId:"+skuId+"inStock:"+msg
#    },
# }

# response = requests.post(msg_push_url, data=post_data)

# # 打印响应内容
# print(response.text)


# 邮件内容设置
msg = MIMEMultipart()
msg.attach(MIMEText("skuId:"+skuId+"inStock:"+msg_bb, 'plain', 'utf-8'))


# 发件人和收件人设置
sender = '390239178@qq.com'
receiver = '310342623@qq.com'
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = '包包推送'

# 发送邮件
try:
    smtp = smtplib.SMTP('smtp.qq.com', 587)
    smtp.starttls()
    smtp.login(sender, 'yhqutvhwwjiwbgeh')  # 替换成你的邮箱账号和密码
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('邮件发送成功')
except Exception as e:
    print('邮件发送失败：', e)



