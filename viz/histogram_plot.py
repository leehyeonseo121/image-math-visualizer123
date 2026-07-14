"""
RGB 히스토그램을 그려주는 시각화 함수
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_rgb_histogram(image_array: np.ndarray):
    """
    이미지의 R, G, B 채널별 픽셀 값 분포를 히스토그램으로 그린다.
    """
    fig, ax = plt.subplots(figsize=(5, 3))

    colors = ["red", "green", "blue"]
    labels = ["R", "G", "B"]

    for i, (color, label) in enumerate(zip(colors, labels)):
        channel_values = image_array[:, :, i].flatten()
        ax.hist(channel_values, bins=50, color=color, alpha=0.5, label=label)

    ax.set_xlim(0, 255)
    ax.set_xlabel("Pixel value")
    ax.set_ylabel("Count")
    ax.set_title("RGB Histogram")
    ax.legend()

    return fig