"""
    DB 연동
"""
from _db import connect, USER, HOST, PORT, NAME

# connection 객체 반환 -> _db.py의 connect 함수
conn = connect()

# cursor() => Cursor 객체 반환
#   excute(sql) 함수를 통해 쿼리문을 실행한 결과를 반환받을 수 있음
with conn.cursor() as cur:
    cur.execute("SELECT (SELECT banner FROM v$version WHERE ROWNUM <= 1) AS v, "
                "sys_context('USERENV', 'DB_NAME') AS db FROM dual")

    # 한 행짜리 결과 : fetchone / 여러 행 결과 : fetchall
    row = cur.fetchone()

print(f"접속 : {USER}@{HOST}:{PORT}/{NAME}")
print(f"조회 결과 : v: {row[0]} / db: {row[1]}")