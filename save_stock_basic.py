import akshare as ak
import pandas as pd
import sqlite3
from sqlite3 import OperationalError

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.

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
        '''
        c = conn.cursor()
        print("数据库打开成功")
        c.execute("DELETE from {table_name};")
        conn.commit()
        '''
        # 将DataFrame写入SQLite表
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists=if_exists,
            index=index
        )

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #对pandas配置，列名与数据对其显示
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    #pd.set_option('display.max_rows', None)

    print_hi('PyCharm')


    #个股信息查询-雪球
    #stock_individual_basic_info_xq_df = ak.stock_individual_basic_info_xq(symbol="SZ002126")
    stock_individual_basic_info_xq_df = ak.stock_individual_basic_info_xq(symbol="SH601127")
    print(stock_individual_basic_info_xq_df)

    #df = pd.DataFrame(stock_individual_basic_info_xq_df)
    #df = df.fillna(0)  # 填充所有NaN为0

    # 方法1: 直接通过列名列表选择（最常用）
    #selected_cols = ['股票代码', '股票简称', '最新价','量价齐升天数','所属行业']
    #df1 = df[selected_cols]
    #df = df1.rename(columns={'股票代码': 'code', '股票简称': 'name', '最新价': 'open','量价齐升天数':'ljqs_days','所属行业':'industry'})

    #df = df[df['name'].apply(lambda x: 'ST' not in str(x) and '*ST' not in str(x) and 'PT' not in str(x) and '退' not in str(x))]

    #print(df)
    print("\n" + "_" * 80 + "\n")
'''
    # 存储到SQLite数据库
    df_to_sqlite(
        df=df,
        table_name='stock_basic',
        db_name='akshare.db',
        if_exists='replace'
    )
'''