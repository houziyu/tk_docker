import pymysql
import traceback
from lib import  config
def test_mysql(sql):
    mysql_config = config.api_test_mysql
    print(mysql_config)
    conn = pymysql.connect(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],
                           database=mysql_config['database'],port=mysql_config['prot'], charset=mysql_config['charset'])
    db = conn.cursor()
    try:
        # 执行sql语句
        db.execute(sql)
        # 获取所有记录列表
        result = db.fetchall()
        return  result
    except Exception:
        result = 'traceback.format_exc():\n%s' % traceback.format_exc()
        error = {'error':result}
        return error