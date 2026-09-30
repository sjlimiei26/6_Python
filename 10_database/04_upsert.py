"""
    멱등성과 upsert
"""
import time
import pandas as pd

from _db import connect, get_engine, prices_path, ENCODING

N = 2_000
conn = connect()
engine = get_engine()

df = pd.read_csv(prices_path(), encoding=ENCODING, parse_dates=["date"])
cols = ["code","date","open","high","low","close","volume","change","changeRate"]

sample = df.head(N)[cols].copy()   # 2000개 데이터 복제

# rows 변수에 df -> list(tuple) 변환하여 저장
rows = [tuple(c) for c in sample.itertuples()]

def quote(c):
    return f'"{c}"' if c in ("date", "change", "changeRate") else c

COL_SQL = ", ".join(quote(c) for c in cols)
PH = ", ".join([f":{i+1}" for i in range(len(cols))])

def make_table(name, unique=False):
    """
        실습용 테이블을 생성하는 함수
        - name : 테이블명
        - unique : UNIQUE(code, date) 설정 여부
    """
    def drop_table(cur, name):
        try:
            cur.execute(f"DROP TABLE {name}")
        except Exception as e:
            if "ORA-00942" not in str(e):
                raise

    with conn.cursor() as cur:
        drop_table(cur, name)

        uk = ', CONSTRAINT uk_code_date UNIQUE (code, "date")' if unique else ''
        cur.execute(f"""
            CREATE TABLE {name} (
                id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                code    VARCHAR2(20)    NOT NULL,
                "date"  DATE            NOT NULL,
                open    NUMBER(20), high    NUMBER(20), low     NUMBER(20),close   NUMBER(20),
                volume  NUMBER(20), "change" NUMBER(20), "changeRate"  NUMBER(6, 2)
                {uk}           
            )
        """)

def count(name):
    """ 전달받은 테이블의 행 개수를 조회하여 반환 """
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {name}")
        return cur.fetchone()[0]

"""
    * UPSERT (Update or Insert)
      => 데이터가 없으면 추가, 있으면 수정(갱신)
    - MERGE INTO 구문

    데이터의 중복을 방지하기 위해, 추가하기 전에 SELECT로 값이 있는 지 확인할 수는 있으나
    조회(SELECT, 1번) 후 추가 또는 갱신(INSERT/UPDATE, 2번) ..SQL 2배로 사용해야함..

    추가/갱신을 동시에 진행하기 위해 UPSERT 를 적용함(사용)!
"""

PLAIN = f"INSERT INTO {{t}} ({COL_SQL}) VALUES ({PH})"
# {t} 는 이후에 .format(t="테이블명") 를 적용할 예정임!

MERGE_USING_SQL = ", ".join(f":{i+1} AS {quote(c)}" for i, c in enumerate(cols))
UPSERT = f"""
    MERGE INTO {{t}} dst
    USING (SELECT {MERGE_USING_SQL} FROM dual) src
    ON (dst.code = src.code AND dst."date" = src."date")
    WHEN MATCHED THEN
        UPDATE SET dst.open = src.open, dst.high = src.high, dst.low = src.low,
                   dst.close = src.close, dst.volume = src.volume, 
                   dst."change" = src."change", dst."changeRate" = src."changeRate"
    WHEN NOT MATCHED THEN
        INSERT ({COL_SQL})
        VALUES (src.code, src."date", src.open, src.high, src.low, src.close, src.volume, src."change", src."chageRate")
"""