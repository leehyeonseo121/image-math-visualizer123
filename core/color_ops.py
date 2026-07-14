"""
이미지 색상 조절 연산 (밝기, 대비, RGB 채널, 흑백 변환)
"""

import numpy as np


def adjust_brightness(image, value: int):
    """
    모든 픽셀에 value를 더해서 밝기를 조절합니다.
    """
    img = image.astype(np.float32)
    result = img + value
    return np.clip(result, 0, 255).astype(np.uint8)


def adjust_contrast(image, factor: float):
    """
    128을 기준으로 픽셀 값을 밀거나 당겨서 대비를 조절합니다.
    """
    img = image.astype(np.float32)
    result = (img - 128) * factor + 128
    return np.clip(result, 0, 255).astype(np.uint8)


def adjust_rgb_channels(image, r_scale: float, g_scale: float, b_scale: float):
    """
    R, G, B 채널 각각에 독립적으로 배율을 곱합니다.
    """
    img = image.astype(np.float32)
    result = img.copy()
    result[..., 0] = img[..., 0] * r_scale
    result[..., 1] = img[..., 1] * g_scale
    result[..., 2] = img[..., 2] * b_scale
    return np.clip(result, 0, 255).astype(np.uint8)


def convert_to_grayscale(image):
    """
    RGB 이미지를 흑백(그레이스케일)으로 변환합니다.
    표준 휘도(luminance) 공식을 사용합니다: 0.299R + 0.587G + 0.114B
    """
    img = image.astype(np.float32)
    gray = img[..., 0] * 0.299 + img[..., 1] * 0.587 + img[..., 2] * 0.114
    gray = np.clip(gray, 0, 255).astype(np.uint8)
    return np.stack([gray, gray, gray], axis=-1)