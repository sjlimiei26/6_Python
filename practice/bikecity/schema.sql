-- 이미 테이블이 존재하는 경우 삭제 (필요 시 주석 해제)
-- BEGIN
--     EXECUTE IMMEDIATE 'DROP TABLE rental_log';
-- EXCEPTION
--     WHEN OTHERS THEN
--         IF SQLCODE != -942 THEN
--             RAISE;
--         END IF;
-- END;
-- /

CREATE TABLE rental_log (
    rental_id VARCHAR2(50) PRIMARY KEY,
    bike_id VARCHAR2(50),
    user_id VARCHAR2(50),
    rent_time TIMESTAMP,
    return_time TIMESTAMP,
    distance_km NUMBER(10, 2),
    fee NUMBER,
    payment_method VARCHAR2(50),
    station_id VARCHAR2(50),
    district VARCHAR2(50),
    bike_type VARCHAR2(50),
    gear_count NUMBER,
    daily_fee NUMBER,
    manufacture_year NUMBER,
    duration_min NUMBER(10, 2)
);
