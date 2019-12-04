
from scripts.MyRequest import HandleRequest
from scripts.Mysql_mobileCX import Hadle_Mysql
from scripts.MyYuml import do_yuml
from readpath.handle_path import User_File_Path


def creat_user(reg_name, pwd="12366666", type=1):
    # 创建请求对象
    do_request = HandleRequest()
    # 创建数据库对象
    do_sql = Hadle_Mysql()
    # 添加请求头
    do_request.add_hesders(do_yuml.read_yuml('request', 'version'))
    # 获取url
    url = do_yuml.read_yuml('request', 'url') + '/member/register'
    # 获取数据库userid
    sql = do_yuml.read_yuml('mysql', 'userid')
    while True:
        phone = do_sql.notexist_phone()
        par = {"mobile_phone": phone, "pwd": pwd, "type": type, "reg_name": reg_name}
        # 调用注册接口发送请求
        do_request.send(url, data=par)

        # 获取用户id
        result = do_sql.run(sql=sql, args=(phone, ))
        if result:
            user_id = result["id"] # 如果查询的sql数据正确，用户id取值结果中的id
            break

        # 用字典来构造用户信息
    userinfo ={ reg_name:
        {'id': user_id,'reg_name':reg_name,'mobile_phone':phone,'pwd':pwd}}

    #关闭连接
    do_request.close()
    do_sql.close()
    return userinfo

def getuserinfo():
    """
    创建3个账号
    :return:
    """
    users={}
    users.update(creat_user('admin',type=0))#管理员就是平台审核人
    users.update(creat_user('borrow'))#借款人
    users.update(creat_user('investor'))#投资人
    do_yuml.write_yuml(users,User_File_Path)#将注册的三个账号写入yaml的配置文件中



if __name__ == '__main__':
    # getuserinfo()
    pass

