import pandas as pd
import pymysql
import pandas.io.sql as psql

from hashlib import sha1

from statmart_config import *

def githash(data):
    s = sha1()
    s.update(("blob %u\0" % len(data)).encode("utf-8"))
    s.update(data)
    return s.hexdigest()

def get_db_connection():
    return pymysql.connect(host=statmart_db_host, 
            port=statmart_db_port, 
            user=statmart_db_user, 
            passwd=statmart_db_passwd,
            db=statmart_db_schema)