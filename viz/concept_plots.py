"""
이미지 없이도 개념을 설명하기 위한 시각화 함수 모음
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_transform_grid(matrix: np.ndarray, title: str = ""):
    square = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
        [0, 0],
    ]).T

    transformed = matrix @ square

    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ax.plot(square[0], square[1], color="steelblue", linewidth=2, marker="o", label="변환 전")
    ax.plot(transformed[0], transformed[1], color="crimson", linewidth=2, marker="o", label="변환 후")

    ax.axhline(0, color="gray", linewidth=0.5)
    ax.axvline(0, color="gray", linewidth=0.5)
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend()
    if title:
        ax.set_title(title, fontsize=10)

    all_x = np.concatenate([square[0], transformed[0]])
    all_y = np.concatenate([square[1], transformed[1]])
    margin = 1.0
    ax.set_xlim(float(min(all_x)) - margin, float(max(all_x)) + margin)
    ax.set_ylim(float(min(all_y)) - margin, float(max(all_y)) + margin)

    return fig


def plot_color_swatches(colors, labels):
    """
    RGB 색상 값들을 정사각형 색상 견본으로 나란히 보여준다.
    colors: [(r, g, b), ...] 각 값은 0~1 사이
    """
    n = len(colors)
    fig, axes = plt.subplots(1, n, figsize=(1.8 * n, 2.0))
    if n == 1:
        axes = [axes]

    for ax, color, label in zip(axes, colors, labels):
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=color, edgecolor="gray"))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(label, fontsize=9)

    fig.tight_layout()
    return fig


def plot_pixel_grid(matrix: np.ndarray, grid_size: int = 4, title: str = ""):
    """
    작은 정사각형 격자(픽셀 대신)에 변환행렬을 적용해서
    확대/축소 시 픽셀 영역이 어떻게 늘어나거나 줄어드는지 보여준다.
    """
    fig, ax = plt.subplots(figsize=(4.5, 4.5))

    for i in range(grid_size):
        for j in range(grid_size):
            square = np.array([
                [j, j + 1, j + 1, j, j],
                [i, i, i + 1, i + 1, i],
            ])
            transformed = matrix @ square
            ax.plot(square[0], square[1], color="steelblue", linewidth=0.8, alpha=0.5)
            ax.plot(transformed[0], transformed[1], color="crimson", linewidth=1.2)

    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.3)
    if title:
        ax.set_title(title, fontsize=10)

    return fig