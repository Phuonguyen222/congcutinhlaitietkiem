import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Tính lãi tiền gửi tiết kiệm")
st.caption("Tính lãi theo phương pháp lãi đơn hoặc lãi kép")


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# GIAO DIỆN NHẬP LIỆU
# =========================
st.subheader("Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

with col2:
    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )

    loai_lai = st.selectbox(
        "Phương pháp tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 Tính lãi", type="primary", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được âm.")
        st.stop()

    # Quy đổi
    lai_suat_nam = lai_suat / 100
    so_nam = ky_han / 12

    # ---------------------------------
    # LÃI ĐƠN
    # ---------------------------------
    if loai_lai == "Lãi đơn":
        tong_tien_lai = tien_gui * lai_suat_nam * so_nam
        tong_goc_lai = tien_gui + tong_tien_lai

        # Lãi phát sinh mỗi tháng
        lai_thang = tien_gui * lai_suat_nam / 12

        # Lãi phát sinh mỗi quý
        lai_quy = tien_gui * lai_suat_nam / 4

        if hinh_thuc == "Lãnh lãi theo tháng":
            lai_dinh_ky = lai_thang
            ten_ky = "tháng"

        elif hinh_thuc == "Lãnh lãi theo quý":
            lai_dinh_ky = lai_quy
            ten_ky = "quý"

        else:
            lai_dinh_ky = tong_tien_lai
            ten_ky = "cuối kỳ"

    # ---------------------------------
    # LÃI KÉP
    # ---------------------------------
    else:
        if hinh_thuc == "Lãnh lãi theo tháng":
            so_ky = ky_han
            lai_suat_ky = lai_suat_nam / 12

            tong_goc_lai = tien_gui * (
                (1 + lai_suat_ky) ** so_ky
            )

            tong_tien_lai = tong_goc_lai - tien_gui

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_ky
            ten_ky = "tháng"

        elif hinh_thuc == "Lãnh lãi theo quý":
            so_ky = ky_han / 3
            lai_suat_ky = lai_suat_nam / 4

            tong_goc_lai = tien_gui * (
                (1 + lai_suat_ky) ** so_ky
            )

            tong_tien_lai = tong_goc_lai - tien_gui

            # Lãi của quý đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_ky
            ten_ky = "quý"

        else:
            # Lãi kép cuối kỳ: ghép lãi theo năm,
            # với số năm có thể là số thập phân.
            tong_goc_lai = tien_gui * (
                (1 + lai_suat_nam) ** so_nam
            )

            tong_tien_lai = tong_goc_lai - tien_gui
            lai_dinh_ky = tong_tien_lai
            ten_ky = "cuối kỳ"

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()
    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Lãi định kỳ",
            format_money(lai_dinh_ky)
        )
        st.caption(f"Lãi {ten_ky}")

    with col2:
        st.metric(
            "Tổng tiền lãi",
            format_money(tong_tien_lai)
        )

    with col3:
        st.metric(
            "Tổng gốc + lãi",
            format_money(tong_goc_lai)
        )

    # =========================
    # CHI TIẾT
    # =========================
    st.divider()

    st.subheader("📋 Chi tiết khoản tiền gửi")

    thong_tin = {
        "Số tiền gửi": format_money(tien_gui),
        "Kỳ hạn": f"{ky_han} tháng",
        "Lãi suất": f"{lai_suat:.2f}%/năm",
        "Phương pháp tính": loai_lai,
        "Hình thức nhận lãi": hinh_thuc,
        "Lãi định kỳ": format_money(lai_dinh_ky),
        "Tổng tiền lãi": format_money(tong_tien_lai),
        "Tổng gốc + lãi": format_money(tong_goc_lai),
    }

    for key, value in thong_tin.items():
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.write(f"**{key}**")
        with col_b:
            st.write(value)


# =========================
# GHI CHÚ
# =========================
with st.expander("ℹ️ Ghi chú về cách tính"):
    st.markdown(
        """
        **Lãi đơn:**

        Tiền lãi = Tiền gốc × Lãi suất năm × Số năm

        **Lãi kép:**

        Tiền cuối kỳ = Tiền gốc × (1 + Lãi suất kỳ) ^ Số kỳ

        - Lãnh lãi theo tháng: lãi suất được quy đổi theo 12 tháng/năm.
        - Lãnh lãi theo quý: lãi suất được quy đổi theo 4 quý/năm.
        - Lãnh lãi cuối kỳ: tính toàn bộ tiền lãi đến ngày đáo hạn.
        
        *Kết quả là mô phỏng theo công thức toán học, chưa xét thuế,
        phí hoặc quy định riêng của từng ngân hàng.*
        """
    )
