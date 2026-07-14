"""
이미지 입출력 관련 공통 함수 모음
"""

import numpy as np
from PIL import Image


def load_image_as_array(uploaded_file) -> np.ndarray:
    """
    Streamlit의 st.file_uploader가 반환한 파일 객체를
    numpy 배열(H, W, 3) 형태로 변환한다.
    """
    image = Image.open(uploaded_file).convert("RGB")
    return np.array(image)


def resize_if_too_large(image_array: np.ndarray, max_size: int = 600) -> np.ndarray:
    """
    이미지가 너무 크면 처리 속도를 위해 축소한다.
    """
    height, width = image_array.shape[:2]
    longer_side = max(height, width)

    if longer_side <= max_size:
        return image_array

    scale = max_size / longer_side
    new_width = int(width * scale)
    new_height = int(height * scale)

    image = Image.fromarray(image_array)
    resized = image.resize((new_width, new_height))
    return np.array(resized)