"""
회전 개념을 설명하기 위한 단위원 + 벡터 시각화
"""

import math

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


def plot_rotation_vector(matrix: np.ndarray, angle: float):
    """
    단위원 위에서 각도 angle(도)만큼 회전한 벡터를 보여준다.
    이미지 좌표계(y축이 아래로 향함)를 기준으로 계산된 행렬이므로,
    화면에서도 실제 이미지처럼 보이도록 y축을 반전시켜서 그린다.
    """
    theta = math.radians(angle)

    before = np.array([1.0, 0.0])
    after = matrix @ before

    fig, ax = plt.subplots(figsize=(4.5, 4.5))

    circle_angles = np.linspace(0, 2 * math.pi, 200)
    ax.plot(np.cos(circle_angles), np.sin(circle_angles), color="lightgray", linewidth=1.5)

    arc_angles = np.linspace(0, theta, 100)
    ax.plot(0.3 * np.cos(arc_angles), 0.3 * np.sin(arc_angles), color="orange", linewidth=2)

    ax.annotate(
        "", xy=(before[0], before[1]), xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", color="steelblue", linewidth=2),
    )
    ax.text(before[0] + 0.05, before[1] + 0.05, "회전 전 (1,0)", color="steelblue", fontsize=9)

    ax.annotate(
        "", xy=(after[0], after[1]), xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", color="crimson", linewidth=2),
    )
    ax.text(after[0] + 0.05, after[1] + 0.05, f"회전 후 ({after[0]:.2f}, {after[1]:.2f})", color="crimson", fontsize=9)

    ax.plot([after[0], after[0]], [0, after[1]], linestyle="--", color="gray", linewidth=1)
    ax.plot([0, after[0]], [after[1], after[1]], linestyle="--", color="gray", linewidth=1)

    ax.axhline(0, color="gray", linewidth=0.5)
    ax.axvline(0, color="gray", linewidth=0.5)
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True, linestyle="--", alpha=0.3)

    ax.invert_yaxis()  # 이미지 좌표계 반영 → 화면상 반시계방향으로 보이게 함

    return fig