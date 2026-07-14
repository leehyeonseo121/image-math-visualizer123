"""
matplotlib에서 한글(및 관련 기호)이 깨지지 않도록 폰트를 등록하는 유틸
"""

import os
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\malgun.ttf",
    r"C:\Windows\Fonts\malgunbd.ttf",
    r"C:\Windows\Fonts\gulim.ttc",
]


def setup_korean_font():
    for path in _FONT_CANDIDATES:
        if os.path.exists(path):
            fm.fontManager.addfont(path)
            font_name = fm.FontProperties(fname=path).get_name()
            plt.rcParams["font.family"] = font_name
            plt.rcParams["axes.unicode_minus"] = False
            return font_name

    plt.rcParams["axes.unicode_minus"] = False
    return None