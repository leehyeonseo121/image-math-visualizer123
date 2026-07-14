"""
matrices.py에서 만든 행렬을 실제 이미지에 적용하는 함수 모음
"""

import cv2
import numpy as np


def apply_reflection(image_array: np.ndarray, axis: str) -> np.ndarray:
    """
    이미지를 좌우 또는 상하로 반전시킨다.
    """
    if axis == "horizontal":
        return np.flip(image_array, axis=1)
    elif axis == "vertical":
        return np.flip(image_array, axis=0)
    else:
        raise ValueError("axis는 'horizontal' 또는 'vertical'이어야 합니다.")


def apply_scaling(image_array: np.ndarray, scale_x: float, scale_y: float) -> np.ndarray:
    """
    이미지를 가로/세로 배율만큼 확대 또는 축소한다.
    """
    height, width = image_array.shape[:2]
    new_width = max(1, int(width * scale_x))
    new_height = max(1, int(height * scale_y))
    return cv2.resize(image_array, (new_width, new_height))


def apply_rotation(image_array: np.ndarray, angle_degrees: float) -> np.ndarray:
    """
    이미지를 중심을 기준으로 회전시킨다. (원본과 같은 크기 유지)
    """
    height, width = image_array.shape[:2]
    center = (width / 2, height / 2)

    rotation_matrix_cv = cv2.getRotationMatrix2D(center, angle_degrees, 1.0)
    rotated = cv2.warpAffine(image_array, rotation_matrix_cv, (width, height))
    return rotated