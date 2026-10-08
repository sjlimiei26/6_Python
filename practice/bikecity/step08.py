"""
    STEP 8. DB 적재
"""
import pandas as pd
import oracledb
from step07 import df6

# Oracle DB 접속 정보 설정 (실제 환경에 맞게 수정)
DB_USER = "write your username"
DB_PASSWORD = "write your password"
DB_DSN = "localhost:1521/xe"

def get_connection():
    try:
        return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    except Exception as e:
        return None

def load_to_db(df: pd.DataFrame, iteration: int):
    # 필요한 15개 컬럼만 순서대로 추출
    cols = [
        "rental_id", "bike_id", "user_id", "rent_time", "return_time", 
        "distance_km", "fee", "payment_method", "station_id", "district", 
        "bike_type", "gear_count", "daily_fee", "manufacture_year", "duration_min"
    ]
    df = df[cols].copy()
    
    # NaN이나 NaT는 None으로 치환해줍니다.    
    df = df.astype(object).where(df.notna(), None)
    
    # executemany에 맞게 튜플 리스트로 변환
    records = [tuple(x) for x in df.itertuples(index=False)]
    
    # Oracle UPSERT (MERGE INTO) 구문 작성
    # :1, :2 등은 executemany에 전달될 튜플의 위치 인덱스
    merge_query = """
    MERGE INTO rental_log r
    USING (
        SELECT :1 as rental_id, :2 as bike_id, :3 as user_id, :4 as rent_time, 
               :5 as return_time, :6 as distance_km, :7 as fee, :8 as payment_method, 
               :9 as station_id, :10 as district, :11 as bike_type, :12 as gear_count, 
               :13 as daily_fee, :14 as manufacture_year, :15 as duration_min 
        FROM dual
    ) s
    ON (r.rental_id = s.rental_id)
    WHEN MATCHED THEN
        UPDATE SET 
            r.bike_id = s.bike_id, r.user_id = s.user_id, r.rent_time = s.rent_time,
            r.return_time = s.return_time, r.distance_km = s.distance_km, r.fee = s.fee,
            r.payment_method = s.payment_method, r.station_id = s.station_id, 
            r.district = s.district, r.bike_type = s.bike_type, r.gear_count = s.gear_count,
            r.daily_fee = s.daily_fee, r.manufacture_year = s.manufacture_year, r.duration_min = s.duration_min
    WHEN NOT MATCHED THEN
        INSERT (rental_id, bike_id, user_id, rent_time, return_time, distance_km, fee, 
                payment_method, station_id, district, bike_type, gear_count, daily_fee, 
                manufacture_year, duration_min)
        VALUES (s.rental_id, s.bike_id, s.user_id, s.rent_time, s.return_time, s.distance_km, 
                s.fee, s.payment_method, s.station_id, s.district, s.bike_type, s.gear_count, 
                s.daily_fee, s.manufacture_year, s.duration_min)
    """
    
    conn = get_connection()
    if conn is None:
        print("  [알림] 오라클 접속 정보가 설정되지 않아, 접속 및 쿼리 실행을 스킵합니다.")
        print("  [알림] 실행 예정 쿼리: MERGE INTO rental_log ... (UPSERT)")
        return
        
    try:
        cursor = conn.cursor()
        
        # executemany로 대량 적재 실행
        cursor.executemany(merge_query, records)
        conn.commit()
        
        # Oracle에서 수행된 결과를 확인 (예시)
        cursor.execute("SELECT COUNT(*) FROM rental_log")
        total_rows = cursor.fetchone()[0]
        
        print(f"  [성공] 데이터 적재 완료. 현재 테이블 행 수: {total_rows:,}건")
        
    except Exception as e:
        print(f"적재 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("\t DB 적재 검증 (1회차)")
    load_to_db(df6, 1)
    
    print("-" * 60)
    print("\t DB 적재 검증 (2회차)")
    load_to_db(df6, 2)
    print("=" * 60)
