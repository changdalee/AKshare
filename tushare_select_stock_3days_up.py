# import akshare as ak
import tushare as ts
import pandas as pd

# import numpy as np
import sqlite3
from sqlite3 import OperationalError
from datetime import datetime
import io
import sys


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press F9 to toggle the breakpoint.


def df_to_sqlite(df, table_name, db_name, if_exists, index=False):
    """
    将pandas DataFrame存储到SQLite3数据库

    参数:
        df: 要存储的DataFrame
        table_name: 要创建的表名
        db_name: SQLite数据库文件名，默认为'data.db'
        if_exists: 表存在时的处理方式，可选'replace'、'append'、'fail'
        index: 是否将DataFrame的索引作为一列存储
    """
    try:
        # 连接到SQLite数据库（如果不存在则创建）
        conn = sqlite3.connect(db_name)
        """
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        print("数据库打开成功")
        c.execute("DELETE from {table_name};")
        conn.commit()
        conn.close()
        """
        # 将DataFrame写入SQLite表
        df.to_sql(name=table_name, con=conn, if_exists=if_exists, index=index)

        # 提交事务并关闭连接
        conn.commit()
        conn.close()

        print(f"成功将DataFrame存储到SQLite表 '{table_name}'，共 {len(df)} 行数据")
        return True

    except OperationalError as e:
        print(f"数据库操作错误: {str(e)}")
        return False
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False


def df_read_sqlite(df, table_name, db_name, today):
    """
    将pandas DataFrame存储到SQLite3数据库

    参数:
        df: 要存储的DataFrame
        table_name: 要创建的表名
        db_name: SQLite数据库文件名，默认为'data.db'
        if_exists: 表存在时的处理方式，可选'replace'、'append'、'fail'
        index: 是否将DataFrame的索引作为一列存储
    """
    try:
        # 连接到SQLite数据库（如果不存在则创建）
        conn = sqlite3.connect(db_name)
        """
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        print("数据库打开成功")
        c.execute("DELETE from {table_name};")
        conn.commit()
        conn.close()
        """
        # 将DataFrame写入SQLite表
        df = pd.read_sql_query(
            "SELECT * FROM " + table_name + " WHERE " + "days <= " + today,
            con=conn,
        )

        # 提交事务并关闭连接
        conn.commit()
        conn.close()

        print(f"成功将SQLite表 '{table_name}'，共 {len(df)} 行数据读取到DataFrame df")
        return True

    except OperationalError as e:
        print(f"数据库操作错误: {str(e)}")
        return False
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf8"
    )  # 强制标准输出UTF-8编码
    # 对pandas配置，列名与数据对其显示
    pd.set_option("display.unicode.ambiguous_as_wide", True)
    pd.set_option("display.unicode.east_asian_width", True)
    # 显示所有列
    pd.set_option("display.max_columns", None)
    # 显示所有行
    # pd.set_option('display.max_rows', None)

    token = "055680ead4592f1287876ef50197e46a76516c86268a33b8c0c565b0"
    ts.set_token(token)
    # print(ts.__version__)

    print_hi("PyCharm")

    df_stock_days = pd.DataFrame(columns=["days"])
    today = datetime.now().strftime("%Y%m%d")
    df_read_sqlite(
        df=df_stock_days, table_name="stock_days", db_name="akshare.db", today=today
    )

    print(df_stock_days)

    '''
    daybefore1 = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    daybefore2 = (datetime.now() - timedelta(days=2)).strftime("%Y%m%d")
    daybefore3 = (datetime.now() - timedelta(days=3)).strftime("%Y%m%d")
    daybefore4 = (datetime.now() - timedelta(days=4)).strftime("%Y%m%d")
    daybefore5 = (datetime.now() - timedelta(days=5)).strftime("%Y%m%d")

    pro = ts.pro_api()
    df_today = pro.daily(trade_date=daybefore1).fillna(0)
    df_yesterday = pro.daily(trade_date=daybefore2).fillna(0)
    df = pd.merge(df_today, df_yesterday, on="ts_code", how="left")
    # print(df)
    # print("\n" + "_" * 99 + "\n")
    """
    df['high_x']=np.where(df['vol_x']>2*df['vol_y'], '100', '0')
    #df = df[df['open_x'] > 0]
    df=df.drop(df[df['high_x'] == '0'].index)
    """
    df["vol_ratio"] = df["vol_x"] / df["vol_y"]
    # df['vol_ratio']=df['vol_ratio'].round(2)
    df = df.drop(df[df["vol_ratio"] < 1.1].index)
    df = df.drop(df[df["vol_ratio"] > 1.5].index)
    df = df[df["ts_code"].apply(lambda x: not str(x) > "687999.AA")]
    df["code"] = df["ts_code"].apply(lambda x: x[:6])

    conn = sqlite3.connect(
        "akshare.db"
    )  # 连接数据库:ml-citation{ref="3,6" data="citationList"}
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM stock_basic"
    )  # 执行查询:ml-citation{ref="10" data="citationList"}
    rows = cursor.fetchall()  # 获取所有结果:ml-citation{ref="6" data="citationList"}
    conn.close()  # 关闭连接:ml-citation{ref="8" data="citationList"}
    df_name = pd.DataFrame(rows, columns=["code", "name"])
    # print(df_name)
    df = pd.merge(df, df_name, on="code", how="left")
    df = df[
        df["name"].apply(
            lambda x: "ST" not in str(x)
            and "*ST" not in str(x)
            and "PT" not in str(x)
            and "退" not in str(x)
        )
    ]

    df = df[df["code"].apply(lambda x: not str(x) > "687999")]
    df = df[["code", "name", "trade_date_x", "vol_x", "close_x", "vol_ratio"]]
    df = df.rename(
        columns={
            "code": "code",
            "name": "name",
            "trade_date_x": "trade_date",
            "vol_x": "vol",
            "close_x": "close",
            "vol_ratio": "vol_ratio",
        }
    )
    print("\n" + "_" * 80 + "\n")
    print(df)
    # 存储到SQLite数据库
    df_to_sqlite(
        df=df,
        table_name="tushare_select_stock_zh_a_01",
        db_name="akshare.db",
        if_exists="replace",
    )
'''
