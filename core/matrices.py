"""
변환에 사용되는 행렬을 만드는 함수 모음
"""

import math

import numpy as np


def get_reflection_matrix(axis: str) -> np.ndarray:
    """
    좌우반전 또는 상하반전에 사용되는 2x2 행렬을 반환한다.

    axis="horizontal" -> 좌우반전
    axis="vertical"   -> 상하반전
    """
    if axis == "horizontal":
        return np.array([[-1, 0],
                          [0, 1]])
    elif axis == "vertical":
        return np.array([[1, 0],
                          [0, -1]])
    else:
        raise ValueError("axis는 'horizontal' 또는 'vertical'이어야 합니다.")


def get_scaling_matrix(scale_x: float, scale_y: float) -> np.ndarray:
    """
    확대/축소에 사용되는 2x2 행렬을 반환한다.
    """
    return np.array([[scale_x, 0],
                      [0, scale_y]])


def get_rotation_matrix(angle_degrees: float) -> np.ndarray:
    """
    주어진 각도(도 단위)만큼 이미지를 회전시키는 2x2 행렬을 반환한다.

    주의: 이미지 좌표계는 y축이 "아래로" 향하기 때문에, 이 행렬은
    core/transforms.py의 apply_rotation()이 OpenCV로 이미지에 실제
    적용하는 값과 정확히 일치하도록 맞춰져 있다. (일반 수학 그래프의
    표준 회전행렬과는 부호가 다르다 — 이건 정상이다.)

        [ cosθ   sinθ ]
        [-sinθ   cosθ ]
    """
    theta = math.radians(angle_degrees)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    return np.array([[cos_t, sin_t],
                      [-sin_t, cos_t]])