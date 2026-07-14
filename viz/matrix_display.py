"""
행렬을 화면에 표시하는 함수 (임의 크기 행렬 지원)
"""

import numpy as np
import streamlit as st


def show_matrix(matrix, title: str = ""):
    matrix = np.array(matrix)

    if title:
        st.write(f"**{title}**")

    rows = []
    for row in matrix:
        row_str = " & ".join(_format_value(v) for v in row)
        rows.append(row_str)

    latex_body = r" \\ ".join(rows)
    st.latex(r"\begin{bmatrix}" + latex_body + r"\end{bmatrix}")


def _format_value(value) -> str:
    try:
        if float(value).is_integer():
            return f"{int(value)}"
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)