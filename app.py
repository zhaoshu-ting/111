import streamlit as st

st.set_page_config(page_title="经营测算工具", layout="wide")

# 侧边菜单
with st.sidebar:
    st.header("经营测算")
    menu_option = st.radio("", ["达人佣金计算", "投产平衡点"], index=1)

if menu_option == "投产平衡点":
    # 头部区域
    st.markdown("""
    <div style="border:1px solid #e6e8eb; border-radius:8px; padding:20px; background:#f8fafe;">
        <h1 style="margin:0; font-size:28px;">投产平衡点</h1>
        <p style="color:#666; margin:4px 0 0 0;">计算广告后台至少需要达到多少支付投产比，才能覆盖退款与全部经营成本。</p>
    </div>
    """, unsafe_allow_html=True)
    col_reset, _ = st.columns([1,5])
    with col_reset:
        if st.button("重置"):
            st.session_state.clear()
            st.rerun()

    st.info("投产比按`支付销售额 ÷ 推广费用`计算。退款单不产生比例费用，衣服成本视为可收回，但每单固定费用仍会损失。")

    # 左右两栏布局
    col_left, col_right = st.columns([1,1])
    with col_left:
        st.markdown("### 输入基础数据")
        selling_price = st.number_input("*售卖价(¥)", min_value=0.0, value=0.0, step=1.0)
        cloth_cost = st.number_input("*衣服成本(¥)", min_value=0.0, value=0.0, step=1.0)
        refund_rate = st.number_input("*退款率(%)", min_value=0.0, max_value=100.0, value=0.00, step=0.01)
        tax_rate = st.number_input("*税费点数(%)", min_value=0.0, max_value=100.0, value=8.00, step=0.01)
        misc_fee = st.number_input("*杂费(¥)", min_value=0.0, value=2.00, step=0.1)

        st.markdown("""
        <div style="background:#eef5ff; padding:12px; border-radius:6px;">
        <b>计算公式</b><br>
        可投推广费 = (1 − 退款率) × (售卖价 × (88.5% − 税费点数) − 衣服成本) − (7.20 + 杂费)<br>
        投产平衡点 = 售卖价 ÷ 可投推广费
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("### 测算结果")
        if selling_price > 0 and cloth_cost >=0:
            r = refund_rate / 100
            t = tax_rate / 100
            investable_ad = (1 - r) * (selling_price * (0.885 - t) - cloth_cost) - (7.20 + misc_fee)
            if investable_ad <= 0:
                st.error("❌ 可投推广费 ≤0，此定价下无论投产多高都无法盈利！")
            else:
                break_even_roas = selling_price / investable_ad
                st.success(f"✅ 投产平衡点：{break_even_roas:.2f}")
                st.write(f"单件可投推广费：¥{investable_ad:.2f}")
                st.write(f"说明：广告投产比必须大于 {break_even_roas:.2f} 才可以实现不亏损")
        else:
            st.markdown("<div style='text-align:center; padding:40px; color:#777;'>填写完整数据后自动计算</div>", unsafe_allow_html=True)

elif menu_option == "达人佣金计算":
    st.header("达人佣金计算")
    st.write("计算最高佣金金额与比例")
    sell_p = st.number_input("售卖价", min_value=0.0)
    cost_p = st.number_input("商品成本", min_value=0.0)
    tax_pct = st.number_input("税费%", value=8.0)
    if sell_p>0:
        max_commission = sell_p * 0.885 - sell_p*(tax_pct/100) - cost_p -7.2 -2
        max_rate = max_commission / sell_p *100
        st.write(f"最高可承担佣金：{max_commission:.2f}元，佣金上限比例：{max_rate:.2f}%")
