import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from datetime import datetime, timedelta

# إعدادات الصفحة
st.set_page_config(
    page_title="محطة حاويات دمياط - AI Dashboard",
    page_icon="🚢",
    layout="wide"
)

# تنسيق احترافي (بدون أي ملفات خارجية)
st.markdown("""
<style>
    .main { background-color: #ffffff; }
    h1 { color: #003366; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stMetric { 
        background: #f8fbff; 
        border-radius: 10px; 
        padding: 15px; 
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        border-left: 4px solid #0066cc;
        text-align: center;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# الشعار والعنوان
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5a/Port_icon.svg", width=70)
with col2:
    st.title("لوحة تحكم ذكية - محطة حاويات دمياط")

st.markdown("<div style='text-align: center; color: #0066cc; margin-bottom: 20px;'>نظام تجريبي يعتمد على نماذج ذكاء اصطناعي للتنبؤ، الجدولة، والمراقبة</div>", unsafe_allow_html=True)

# شريط جانبي
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5a/Port_icon.svg", width=50)
    st.header("⚙️ التحكم")
    forecast_days = st.slider("عدد أيام التنبؤ", 3, 14, 7)
    st.info("البيانات مُصطنعة لأغراض العرض")

# توليد بيانات في الذاكرة (بدون حفظ ملفات)
np.random.seed(42)
dates = pd.date_range(datetime.today(), periods=forecast_days, freq='D')
base = 4000
trend = np.linspace(0, 200, forecast_days)
seasonal = 300 * np.sin(2 * np.pi * np.arange(forecast_days) / 7)
noise = np.random.normal(0, 150, forecast_days)
forecast = (base + trend + seasonal + noise).astype(int)
forecast = np.clip(forecast, 2500, 6000)

forecast_df = pd.DataFrame({
    "اليوم": dates.strftime('%Y-%m-%d'),
    "الحاويات المتوقعة": forecast
})

# جدولة السفن
vessels = ["الناقلة أ", "الناقلة ب", "الناقلة ج", "الناقلة د"]
start_times = [datetime.now() + timedelta(hours=i*8) for i in range(4)]
durations = [6, 8, 5, 7]
end_times = [start + timedelta(hours=dur) for start, dur in zip(start_times, durations)]
berths = ["رصيف 1", "رصيف 2", "رصيف 1", "رصيف 3"]

gantt_data = [
    dict(Task=berth, Start=start, Finish=end, Resource=vessel)
    for berth, start, end, vessel in zip(berths, start_times, end_times, vessels)
]

# الإيرادات
revenue = np.random.randint(90000, 140000, size=7)
revenue_df = pd.DataFrame({
    "اليوم": pd.date_range(datetime.today() - timedelta(days=6), periods=7).strftime('%Y-%m-%d'),
    "الإيرادات (جنيه)": revenue
})

# التبويبات
tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 التنبؤ بالذكاء الاصطناعي",
    "⚓ جدولة الأرصفة",
    "💰 الإيرادات",
    "🛠️ الصيانة"
])

with tab1:
    st.caption("تم التنبؤ باستخدام نموذج هجين مُدرّب (LSTM + XGBoost مُحاكى)")
    fig = px.line(forecast_df, x="اليوم", y="الحاويات المتوقعة", markers=True)
    fig.update_traces(line_color='#0066cc')
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(forecast_df, use_container_width=True)

with tab2:
    st.subheader("توزيع السفن على الأرصفة")
    fig_gantt = ff.create_gantt(gantt_data, index_col='Resource', show_colorbar=True, group_tasks=True)
    fig_gantt.update_layout(height=400)
    st.plotly_chart(fig_gantt, use_container_width=True)

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("إجمالي الإيرادات (7 أيام)", f"{revenue.sum():,} جنيه")
    with col_b:
        st.metric("متوسط اليوم", f"{int(revenue.mean()):,} جنيه")
    fig_rev = px.bar(revenue_df, x="اليوم", y="الإيرادات (جنيه)", color_discrete_sequence=['#009966'])
    st.plotly_chart(fig_rev, use_container_width=True)

with tab4:
    st.subheader("تنبيهات الصيانة التنبؤية")
    st.warning("⚠️ الرافعة #3: احتمال عطل خلال 48 ساعة (درجة الثقة: 87%)")
    st.success("✅ الرافعات #1, #2, #4: تعمل بشكل طبيعي")
    st.info("النظام يستخدم نموذج تصنيف ذكي لتوقع الأعطال قبل حدوثها.")

st.markdown("---")
st.caption("تم إنشاء هذا النظام لأغراض تعليمية — لا يستخدم بيانات فعلية من محطة دمياط. | مشروع مفتوح المصدر")
