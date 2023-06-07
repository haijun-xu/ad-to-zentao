import requests
import json
from ldap3 import Server, Connection, SUBTREE

def get_ad_users():
    # 设置 AD 服务器信息
    server_address = 'ldap:/*/:389'
    username = '*'
    password = '*'

    # 连接到 AD 服务器
    server = Server(server_address)
    conn = Connection(server, user=username, password=password, auto_bind=True)

    # 设置查询参数
    base_dn = ''  # 设置查询的基础 DN
    search_filter = '(objectClass=organizationalPerson)'  # 设置搜索过滤条件
    attributes = ['cn', 'sAMAccountName', 'mail']  # 设置要检索的属性列表

    # 执行查询
    conn.search(base_dn, search_filter, attributes=attributes, search_scope=SUBTREE)

    # 获取查询结果
    result_entries = conn.entries

    # 打印用户信息
    # for entry in result_entries:
        # print(f"Username: {entry.sAMAccountName.value}")
        # print(f"Full Name: {entry.cn.value}")
        # print(f"Email: {entry.mail.value}")
        # print("==============================")
        # 设置要创建的用户信息
        # print(entry.sAMAccountName.value + "," + entry.cn.value)

    # 关闭连接
    conn.unbind()
    return  result_entries

def get_token():
    url = 'http://*/api.php/v1/tokens'
    data = '{"account": "admin", "password": "Zentaosjrk!1"}'
    re = requests.post(url, data=data)
    token = json.loads(re.content.decode("utf-8"))['token']
    return  token


def create_user(token,data):
    adduser_url = 'http://*/api.php/v1/users'
    headers = {
        "Token": token
    }
    try:
        re1 = requests.post(adduser_url, headers=headers, data=data)
        if re1.status_code == 201:
            print(data["realname"]," create success")
    except Exception as e:
        print("create error,maybe interface error")


def get_zentao_useraccount(token):
    data = {
        "page": 1,
        "limit": 10000
    }
    headers = {
        "Token": token
    }
    url = 'http://*/api.php/v1/users'
    re = requests.get(url, headers=headers, params=data)
    user_total = json.loads(re.content.decode("utf-8"))['total']
    user_list = json.loads(re.content.decode("utf-8"))['users']
    if user_total == len(user_list):
        account = [i['account'] for i in user_list]
    else:
        account = "zentao用户列表没有拉取完整"
    return  account


if __name__ == '__main__':
    token = get_token()
    s=get_zentao_useraccount(token)
    ad_userlist = get_ad_users()
    ss=0
    for i in ad_userlist:
        if i.sAMAccountName.value in s:
            # print(i.sAMAccountName.value," 已存在")
            pass
        else:
            data={"account": i.sAMAccountName.value, "password": "123qwe!@#", "realname": i.cn.value}
            # data={
            #     "account": i.sAMAccountName.value,
            #     "password": "123qwe!@#",
            #     "realname": i.cn.value,
            #     "mail": i.mail.value
            # }
            create_user(token,data)

