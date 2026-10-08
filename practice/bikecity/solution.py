"""
    전체 파이프라인 실행
"""
import os
import subprocess

def run_step(step_name):
    print(f"\n[{step_name} 실행 중...]")
    subprocess.run(["python", step_name], check=True)

if __name__ == "__main__":
    steps = [
        "step01.py",
        "step02.py",
        "step03.py",
        "step04.py",
        "step05.py",
        "step06.py",
        "step07.py",
        "step08.py"
    ]
    
    for step in steps:
        if os.path.exists(step):
            run_step(step)
    
    print("\n[전체 파이프라인 실행 완료]")
