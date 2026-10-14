
import streamlit as st

# Cấu hình giao diện
st.set_page_config(
    page_title="Tính chỉ số DTI",
    page_icon="🏦",
    layout="centered"
)

# Tiêu đề ứng dụng
st.title("🏦 CÔNG CỤ TÍNH CHỈ SỐ DTI")
st.write(
    "Hệ thống hỗ trợ đánh giá khả năng vay vốn "
    "dựa trên hệ số nợ trên thu nhập (DTI)."
)

st.divider()

# Nhập dữ liệu
st.subheader("1. Nhập thông tin khách hàng")

col1, col2 = st.columns(2)

with col1:
    STV = st.number_input(
        "Số tiền vay mới (VNĐ)",
        min_value=0,
        value=800_000_000,
        step=10_000_000
    )

    THV = st.number_input(
        "Thời hạn vay (năm)",
        min_value=1,
        value=5,
        step=1
    )

    LS = st.number_input(
        "Lãi suất vay (%/năm)",
        min_value=0.0,
        value=12.0,
        step=0.5
    )

    TN = st.number_input(
        "Thu nhập hàng tháng (VNĐ)",
        min_value=1,
        value=45_000_000,
        step=1_000_000
    )

with col2:
    NC = st.number_input(
        "Khoản nợ cũ phải trả/tháng (VNĐ)",
        min_value=0,
        value=10_000_000,
        step=1_000_000
    )

    CPSH = st.number_input(
        "Chi phí sinh hoạt/người/tháng (VNĐ)",
        min_value=0,
        value=4_000_000,
        step=500_000
    )

    SN = st.number_input(
        "Số người trong gia đình",
        min_value=1,
        value=3,
        step=1
    )

st.divider()

# Nút tính toán
if st.button("🧮 TÍNH CHỈ SỐ DTI", use_container_width=True):

    # Tính gốc trả hàng tháng
    tien_goc = STV / (THV * 12)

    # Tính lãi hàng tháng theo dư nợ ban đầu
    tien_lai = STV * (LS / 100 / 12)

    # Tổng tiền trả nợ hàng tháng
    tong_no = tien_goc + tien_lai + NC

    # Tổng chi phí sinh hoạt gia đình
    tong_CPSH = CPSH * SN

    # Thu nhập sau chi phí sinh hoạt
    thu_nhap_con_lai = TN - tong_CPSH

    # Kiểm tra điều kiện tính DTI
    if thu_nhap_con_lai <= 0:
        st.error(
            "Không thể tính DTI: Thu nhập sau chi phí "
            "sinh hoạt phải lớn hơn 0."
        )

    else:
        # Công thức DTI theo code ban đầu
        DTI = tong_no / thu_nhap_con_lai

        # Hiển thị kết quả
        st.subheader("2. Kết quả tính toán")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Chỉ số DTI",
                value=f"{DTI * 100:.2f}%"
            )

        with col2:
            st.metric(
                label="Thu nhập còn lại sau sinh hoạt",
                value=f"{thu_nhap_con_lai:,.0f} VNĐ"
            )

        st.write(
            f"**Tổng tiền trả nợ hàng tháng:** "
            f"{tong_no:,.0f} VNĐ"
        )

        st.write(
            f"**Tổng chi phí sinh hoạt:** "
            f"{tong_CPSH:,.0f} VNĐ"
        )

        st.divider()

        # Kết luận theo điều kiện người dùng yêu cầu
        st.subheader("3. Kết luận")

        if DTI < 0.70:
            st.error(
                "❌ KHÔNG ĐƯỢC VAY - Chỉ số DTI dưới 70%."
            )
        else:
            st.success(
                "✅ ĐƯỢC VAY - Chỉ số DTI từ 70% trở lên."
            )

        # Hiển thị công thức
        with st.expander("Xem chi tiết cách tính"):
            st.write(
                f"Tiền gốc/tháng = {STV:,.0f} / "
                f"({THV} × 12) = {tien_goc:,.0f} VNĐ"
            )

            st.write(
                f"Tiền lãi/tháng = {STV:,.0f} × "
                f"({LS}% / 12) = {tien_lai:,.0f} VNĐ"
            )

            st.write(
                f"Tổng nợ/tháng = {tong_no:,.0f} VNĐ"
            )

            st.write(
                f"DTI = {tong_no:,.0f} / "
                f"{thu_nhap_con_lai:,.0f} "
                f"= {DTI * 100:.2f}%"
            )
