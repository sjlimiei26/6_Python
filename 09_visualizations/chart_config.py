"""
    차트 관련 설정
"""
import platform

from matplotlib import font_manager

# ===================
#   한글 폰트
# ===================
# 운영체제(OS) 별로 기본 한글 폰트. (기본적으로 설치되어 있는 항목들)
_DEFAULT_FONT = {
    "Windows": ["Malgun Gothic"],
    "Darwin": ["AppleGothic"], # platform.system() 의 결과가 macOS 부르는 명칭
}

# 그 외의 폰트들. (리눅스, 도커 등등)
_FALLBACK = ["NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "IPAGothic"]

def find_korean_font():
    """
        설치된 폰트 중 한글을 표시할 수 있는 항목을 찾아 반환
    """

    # font_manager.fontManager.ttflist : matplotlib 에서 시스템을 훑어 만들어 둔 설치된 폰트 목록





def setup():
    pass