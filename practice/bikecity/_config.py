""" 공통 모듈 """
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

ENCODING = "utf-8-sig"

def path(name):
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError("데이터셋이 준비되지 않았습니다.")
    
    return os.path.join(DATA_DIR, name)

def raw_bikes_path():
    return path("raw-bikes.csv")

def raw_rentals_path():
    return path("raw-rentals.csv")

def stations_path():
    return path("stations.csv")