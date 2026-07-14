"""
Image Math Visualizer
- 이미지 없을 때: 왼쪽 버튼으로 NumPy/행렬 개념을 화면 중앙에 크게 설명
- 이미지 있을 때: 실제 이미지 변환 기능 (반전/확대축소/회전/색상)
"""

import math

import numpy as np
import streamlit as st

from utils.font_setup import setup_korean_font
setup_korean_font()

from utils.image_io import load_image_as_array, resize_if_too_large
from core.matrices import get_reflection_matrix, get_scaling_matrix, get_rotation_matrix
from core.transforms import apply_reflection, apply_scaling, apply_rotation
from core.color_ops import adjust_brightness, adjust_contrast, adjust_rgb_channels, convert_to_grayscale
from viz.matrix_display import show_matrix
from viz.coordinate_plot import plot_rotation_vector
from viz.histogram_plot import plot_rgb_histogram
from viz.concept_plots import plot_transform_grid, plot_color_swatches, plot_pixel_grid


CONCEPT_LABELS = {
    "numpy_basics": "🔢 NumPy와 행렬 기초",
    "matrix_add_sub": "➕➖ 행렬 덧셈/뺄셈",
    "matrix_mult": "✖️ 행렬 곱셈과 전치행렬",
    "image_rgb": "🖼️ 이미지의 행렬 표현 (RGB)",
    "brightness_color": "💡 밝기와 색상 조절",
}


def show_concept_numpy_basics():
    st.header(CONCEPT_LABELS["numpy_basics"])
    st.write(
        "NumPy는 파이썬에서 행렬과 배열을 쉽고 빠르게 계산하기 위해 사용하는 라이브러리입니다. "
        "일반적인 리스트는 한 줄(1차원)의 데이터만 저장하지만, NumPy 배열은 여러 행과 열로 이루어진 "
        "2차원 이상의 데이터를 저장할 수 있습니다."
    )
    st.write("예를 들어 1부터 9까지의 숫자를 3×3 형태로 저장하면 아래와 같은 행렬이 만들어집니다.")

    matrix = np.arange(1, 10).reshape(3, 3)
    show_matrix(matrix, title="3x3 행렬 (NumPy 배열)")

    st.write("행렬의 특정 위치 값은 행 번호와 열 번호로 접근합니다. (0번부터 시작)")
    col1, col2 = st.columns(2)
    with col1:
        row = st.slider("행 번호", 0, 2, 0, key="concept_np_row")
    with col2:
        col = st.slider("열 번호", 0, 2, 0, key="concept_np_col")

    st.latex(rf"\text{{matrix}}[{row}][{col}] = {matrix[row, col]}")


def show_concept_matrix_add_sub():
    st.header(CONCEPT_LABELS["matrix_add_sub"])
    st.write(
        "행렬의 덧셈은 같은 위치에 있는 숫자끼리 더하는 것이고, 뺄셈도 같은 방식으로 계산합니다. "
        "단, 이 연산은 두 행렬의 크기(행과 열의 개수)가 완전히 같을 때만 가능합니다."
    )

    st.subheader("직접 값을 바꿔보세요 (2x2 행렬)")
    col1, col2 = st.columns(2)
    with col1:
        st.write("행렬 A")
        a11 = st.number_input("A[0][0]", value=1, key="a11")
        a12 = st.number_input("A[0][1]", value=2, key="a12")
        a21 = st.number_input("A[1][0]", value=3, key="a21")
        a22 = st.number_input("A[1][1]", value=4, key="a22")
        matrix_a = np.array([[a11, a12], [a21, a22]])
        show_matrix(matrix_a, title="A")
    with col2:
        st.write("행렬 B")
        b11 = st.number_input("B[0][0]", value=5, key="b11")
        b12 = st.number_input("B[0][1]", value=6, key="b12")
        b21 = st.number_input("B[1][0]", value=7, key="b21")
        b22 = st.number_input("B[1][1]", value=8, key="b22")
        matrix_b = np.array([[b11, b12], [b21, b22]])
        show_matrix(matrix_b, title="B")

    operation = st.radio("연산 선택", ["덧셈 (A + B)", "뺄셈 (A - B)"], horizontal=True, key="concept_addsub_op")
    result = matrix_a + matrix_b if operation.startswith("덧셈") else matrix_a - matrix_b
    show_matrix(result, title="결과")

    st.info(
        "⚠️ 만약 A가 2×2이고 B가 3×3처럼 크기가 다르면, 덧셈과 뺄셈은 계산할 수 없습니다. "
        "행렬 연산에서는 모양(shape)이 항상 중요합니다."
    )


def show_concept_matrix_mult():
    st.header(CONCEPT_LABELS["matrix_mult"])
    st.write(
        "일반 숫자의 곱셈과 달리, 행렬 곱셈에서는 **앞 행렬의 열 개수**와 **뒤 행렬의 행 개수**가 "
        "같아야 계산할 수 있습니다. 또한 순서를 바꾸면 결과가 달라질 수 있어서, "
        "일반 곱셈처럼 교환법칙이 성립하지 않습니다 (A×B ≠ B×A)."
    )

    st.subheader("직접 값을 바꿔보세요 (2x2 행렬)")
    col1, col2 = st.columns(2)
    with col1:
        st.write("행렬 A")
        a11 = st.number_input("A[0][0]", value=1, key="ma11")
        a12 = st.number_input("A[0][1]", value=2, key="ma12")
        a21 = st.number_input("A[1][0]", value=3, key="ma21")
        a22 = st.number_input("A[1][1]", value=4, key="ma22")
        matrix_a = np.array([[a11, a12], [a21, a22]])
        show_matrix(matrix_a, title="A")
    with col2:
        st.write("행렬 B")
        b11 = st.number_input("B[0][0]", value=5, key="mb11")
        b12 = st.number_input("B[0][1]", value=6, key="mb12")
        b21 = st.number_input("B[1][0]", value=7, key="mb21")
        b22 = st.number_input("B[1][1]", value=8, key="mb22")
        matrix_b = np.array([[b11, b12], [b21, b22]])
        show_matrix(matrix_b, title="B")

    col3, col4 = st.columns(2)
    with col3:
        show_matrix(matrix_a @ matrix_b, title="A × B")
    with col4:
        show_matrix(matrix_b @ matrix_a, title="B × A (다른 결과!)")

    st.divider()
    st.subheader("전치행렬 (Transpose)")
    st.write(
        "3×2 행렬과 3×2 행렬처럼, 앞 행렬의 열 개수와 뒤 행렬의 행 개수가 다르면 곱셈이 불가능합니다. "
        "이때 한 행렬의 행과 열을 서로 바꾸는 **전치행렬**을 이용하면 곱셈이 가능해집니다."
    )
    sample = np.array([[1, 2], [3, 4], [5, 6]])
    col5, col6 = st.columns(2)
    with col5:
        show_matrix(sample, title="원래 행렬 (3x2)")
    with col6:
        show_matrix(sample.T, title="전치행렬 (2x3)")


def show_concept_image_rgb():
    st.header(CONCEPT_LABELS["image_rgb"])
    st.write(
        "컴퓨터는 사진을 그림 그대로 저장하지 않고, 수많은 숫자로 저장합니다. "
        "흑백 이미지는 각 위치(픽셀)에 밝기 값 하나만 저장하고, 컬러 이미지는 "
        "빨강(R), 초록(G), 파랑(B) 세 가지 색의 값을 함께 저장합니다."
    )
    st.write("즉, 컬러 이미지의 픽셀 하나는 사실 [R, G, B] 세 개의 숫자로 표현됩니다.")

    fig = plot_color_swatches(
        colors=[(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (0, 0, 0)],
        labels=["[1,0,0]\n빨강", "[0,1,0]\n초록", "[0,0,1]\n파랑", "[1,1,1]\n흰색", "[0,0,0]\n검정"],
    )
    st.pyplot(fig)


def show_concept_brightness_color():
    st.header(CONCEPT_LABELS["brightness_color"])

    st.subheader("1. 곱셈을 이용한 밝기 조절")
    st.write(
        "이미지의 모든 픽셀 값에 1보다 작은 수를 곱하면 전체적으로 어두워지고, "
        "1보다 큰 수를 곱하면 밝아집니다."
    )
    mult_factor = st.slider("곱할 값", 0.0, 2.0, 1.0, 0.1, key="concept_mult_factor")
    base_color = 0.6
    result_color = min(1.0, base_color * mult_factor)
    fig1 = plot_color_swatches(
        colors=[(base_color, base_color, base_color), (result_color, result_color, result_color)],
        labels=["원본", f"× {mult_factor:.1f}"],
    )
    st.pyplot(fig1)

    st.divider()
    st.subheader("2. 스칼라 더하기/빼기를 이용한 밝기 조절")
    st.write(
        "모든 픽셀 값에 일정한 숫자를 더하면 이미지가 밝아지고, 일정한 숫자를 빼면 어두워집니다. "
        "곱셈과 비슷해 보이지만 변화하는 방식에는 차이가 있습니다 (곱셈은 비율로, 덧셈은 일정량으로 변합니다)."
    )
    add_value = st.slider("더할 값 (스칼라)", -0.5, 0.5, 0.0, 0.05, key="concept_add_value")
    result_add = min(1.0, max(0.0, base_color + add_value))
    fig2 = plot_color_swatches(
        colors=[(base_color, base_color, base_color), (result_add, result_add, result_add)],
        labels=["원본", f"{add_value:+.2f}"],
    )
    st.pyplot(fig2)

    st.divider()
    st.subheader("3. 특정 색상 채널만 변화시키기")
    st.write(
        "RGB 이미지에서 빨간색 채널의 값만 증가시키면 이미지가 붉게 보입니다. "
        "초록색이나 파란색 채널만 바꾸면 각각 다른 색감을 만들 수 있습니다."
    )
    r_val = st.slider("R (빨강)", 0.0, 1.0, 0.5, 0.05, key="concept_r")
    g_val = st.slider("G (초록)", 0.0, 1.0, 0.5, 0.05, key="concept_g")
    b_val = st.slider("B (파랑)", 0.0, 1.0, 0.5, 0.05, key="concept_b")
    fig3 = plot_color_swatches(colors=[(r_val, g_val, b_val)], labels=[f"[{r_val:.1f}, {g_val:.1f}, {b_val:.1f}]"])
    st.pyplot(fig3)


CONCEPT_FUNCTIONS = {
    "numpy_basics": show_concept_numpy_basics,
    "matrix_add_sub": show_concept_matrix_add_sub,
    "matrix_mult": show_concept_matrix_mult,
    "image_rgb": show_concept_image_rgb,
    "brightness_color": show_concept_brightness_color,
}


def main():
    st.set_page_config(
        page_title="Image Math Visualizer",
        page_icon="🧮",
        layout="wide",
    )

    if "concept_view" not in st.session_state:
        st.session_state["concept_view"] = None

    st.title("🧮 Image Math Visualizer")
    st.caption("이미지 변환을 통해 행렬(Matrix)과 벡터 연산을 시각적으로 배워보세요.")

    st.sidebar.header("1. 이미지 업로드")
    uploaded_file = st.sidebar.file_uploader(
        "이미지를 선택하세요 (jpg, png)",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is None:
        st.sidebar.divider()
        st.sidebar.header("2. 개념 살펴보기")
        st.sidebar.caption("이미지 없이도 NumPy와 행렬 개념을 먼저 확인할 수 있어요.")

        for key, label in CONCEPT_LABELS.items():
            if st.sidebar.button(label, use_container_width=True, key=f"btn_{key}"):
                st.session_state["concept_view"] = key

        if st.session_state["concept_view"] is None:
            st.info("왼쪽에서 개념 버튼을 눌러보세요. 이미지를 업로드하면 실제 변환 기능을 사용할 수 있어요.")
        else:
            CONCEPT_FUNCTIONS[st.session_state["concept_view"]]()
        return

    st.sidebar.divider()
    st.sidebar.header("2. 변환 선택")
    transform_option = st.sidebar.radio(
        "적용할 변환을 선택하세요",
        options=["없음", "좌우반전", "상하반전", "확대/축소", "회전", "색상(밝기/대비/RGB/흑백)"],
    )

    scale_x, scale_y = 1.0, 1.0
    angle = 0
    grayscale_on = False
    brightness_value = 0
    contrast_factor = 1.0
    r_scale, g_scale, b_scale = 1.0, 1.0, 1.0

    if transform_option == "확대/축소":
        st.sidebar.header("3. 배율 조절")
        scale_x = st.sidebar.slider("가로 배율", min_value=0.2, max_value=3.0, value=1.0, step=0.1)
        scale_y = st.sidebar.slider("세로 배율", min_value=0.2, max_value=3.0, value=1.0, step=0.1)
    elif transform_option == "회전":
        st.sidebar.header("3. 각도 조절")
        angle = st.sidebar.slider("회전 각도 (도)", min_value=0, max_value=360, value=0, step=1)
    elif transform_option == "색상(밝기/대비/RGB/흑백)":
        st.sidebar.header("3. 색상 조절")
        grayscale_on = st.sidebar.checkbox("흑백으로 변환", value=False)
        brightness_value = st.sidebar.slider("밝기", min_value=-100, max_value=100, value=0, step=5)
        contrast_factor = st.sidebar.slider("대비", min_value=0.2, max_value=3.0, value=1.0, step=0.1)
        st.sidebar.subheader("채널별 배율")
        r_scale = st.sidebar.slider("Red 배율", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
        g_scale = st.sidebar.slider("Green 배율", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
        b_scale = st.sidebar.slider("Blue 배율", min_value=0.0, max_value=2.0, value=1.0, step=0.1)

    original_image = load_image_as_array(uploaded_file)
    original_image = resize_if_too_large(original_image, max_size=600)

    transformed_image = original_image
    used_matrix = None

    if transform_option == "좌우반전":
        used_matrix = get_reflection_matrix("horizontal")
        transformed_image = apply_reflection(original_image, "horizontal")
    elif transform_option == "상하반전":
        used_matrix = get_reflection_matrix("vertical")
        transformed_image = apply_reflection(original_image, "vertical")
    elif transform_option == "확대/축소":
        used_matrix = get_scaling_matrix(scale_x, scale_y)
        transformed_image = apply_scaling(original_image, scale_x, scale_y)
    elif transform_option == "회전":
        used_matrix = get_rotation_matrix(angle)
        transformed_image = apply_rotation(original_image, angle)
    elif transform_option == "색상(밝기/대비/RGB/흑백)":
        step0 = convert_to_grayscale(original_image) if grayscale_on else original_image
        step1 = adjust_brightness(step0, brightness_value)
        step2 = adjust_contrast(step1, contrast_factor)
        transformed_image = adjust_rgb_channels(step2, r_scale, g_scale, b_scale)

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("원본 이미지")
        st.image(original_image, use_container_width=True)
        st.caption(f"이미지 크기: {original_image.shape[1]} x {original_image.shape[0]} (가로 x 세로)")

    with right_col:
        st.subheader("변환된 이미지")
        st.image(transformed_image, use_container_width=True)
        if transform_option == "없음":
            st.caption("사이드바에서 변환을 선택해보세요.")
        else:
            st.caption(f"적용된 변환: {transform_option}")

    st.divider()
    st.subheader("수학적 설명")

    if transform_option == "없음":
        st.write("변환을 선택하면 여기에 사용된 행렬 또는 연산이 표시됩니다.")

    elif transform_option == "회전":
        theta_rad = math.radians(angle)
        cos_val = math.cos(theta_rad)
        sin_val = math.sin(theta_rad)

        st.markdown("#### 1. cos·sin은 어디서 나온 값인가?")
        st.write(
            "반지름이 1인 원(단위원) 위에서, x축으로부터 반시계 방향으로 "
            "θ만큼 이동한 점의 좌표가 정확히 (cosθ, sinθ) 입니다."
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"**현재 회전 각도 θ = {angle}도**")
            st.latex(rf"\cos({angle}°) = {cos_val:.3f}")
            st.latex(rf"\sin({angle}°) = {sin_val:.3f}")

            st.markdown("#### 2. 회전 행렬")
            show_matrix(used_matrix, title="회전행렬 (이미지 좌표계 기준)")

        with col2:
            fig = plot_rotation_vector(used_matrix, angle)
            st.pyplot(fig)
            st.caption(
                "회색 원: 단위원 / 주황 호: 각도 θ / "
                "파랑 화살표: 회전 전 (1,0) / 빨강 화살표: 회전 후"
            )

    elif transform_option == "색상(밝기/대비/RGB/흑백)":
        st.write(
            f"흑백 변환: {'적용됨' if grayscale_on else '미적용'} / "
            f"밝기: {brightness_value:+d} / 대비 배율: {contrast_factor:.1f}배 / "
            f"R배율: {r_scale:.1f}, G배율: {g_scale:.1f}, B배율: {b_scale:.1f}"
        )
        fig = plot_rgb_histogram(transformed_image)
        st.pyplot(fig)

    elif transform_option == "확대/축소":
        show_matrix(used_matrix, title=f"{transform_option}에 사용된 행렬")
        st.write(f"가로 배율: {scale_x:.1f}배, 세로 배율: {scale_y:.1f}배가 적용되었습니다.")
        fig = plot_pixel_grid(used_matrix, grid_size=4, title="픽셀 격자의 확대/축소 예시")
        st.pyplot(fig)
        st.caption("파랑: 변환 전 픽셀 격자 / 빨강: 변환 후 픽셀 격자 — 격자 크기가 배율만큼 늘어나거나 줄어드는 것을 볼 수 있습니다.")

    else:
        show_matrix(used_matrix, title=f"{transform_option}에 사용된 행렬")
        st.write(
            "이미지 안의 모든 점 (x, y)에 위 행렬을 곱하면, "
            "새로운 위치 (x', y')로 이동합니다."
        )


if __name__ == "__main__":
    main()