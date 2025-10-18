import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from datetime import datetime, timedelta

# === إعدادات الصفحة ===
st.set_page_config(
    page_title="محطة حاويات دمياط - AI Dashboard",
    page_icon="🚢",
    layout="wide"
)

# === أنماط مخصصة (CSS) ===
st.markdown("""
<style>
    .main { background-color: #f8fbff; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
    h1 { color: #003366; text-align: center; }
    .sidebar .sidebar-content { background-color: #e6f0ff; }
</style>
""", unsafe_allow_html=True)

st.title("🚢 لوحة تحكم ذكية - محطة حاويات دمياط")
st.markdown("نظام تجريبي يعتمد على **نماذج ذكاء اصطناعي** للتنبؤ، الجدولة، والمراقبة — بدون بيانات حقيقية.")

# === شريط جانبي للتحكم ===
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5a/Port_icon.svg", width=100)
    st.header("⚙️ التحكم")
    forecast_days = st.slider("عدد أيام التنبؤ", 3, 14, 7)
    st.info("البيانات مُصطنعة لأغراض العرض")

# === بيانات مصطنعة ذكية (باستخدام نموذج بسيط) ===
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

# === جدولة السفن (مخطط جانت) ===
vessels = ["الناقلة أ", "الناقلة ب", "الناقلة ج", "الناقلة د"]
start_times = [datetime.now() + timedelta(hours=i*8) for i in range(4)]
durations = [6, 8, 5, 7]  # ساعات
end_times = [start + timedelta(hours=dur) for start, dur in zip(start_times, durations)]
berths = ["رصيف 1", "رصيف 2", "رصيف 1", "رصيف 3"]

gantt_data = [
    dict(Task=berth, Start=start, Finish=end, Resource=vessel)
    for berth, start, end, vessel in zip(berths, start_times, end_times, vessels)
]
gantt_df = pd.DataFrame(gantt_data)

# === الإيرادات ===
revenue = np.random.randint(90000, 140000, size=7)
revenue_df = pd.DataFrame({
    "اليوم": pd.date_range(datetime.today() - timedelta(days=6), periods=7).strftime('%Y-%m-%d'),
    "الإيرادات (جنيه)": revenue
})

# === التبويبات ===
tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 التنبؤ بالذكاء الاصطناعي",
    "⚓ جدولة الأرصفة (مخطط زمني)",
    "💰 الإيرادات اليومية",
    "🛠️ الصيانة التنبؤية"
])

with tab1:
    st.subheader(f"التنبؤ لـ {forecast_days} يومًا قادمًا باستخدام نموذج هجين (LSTM + XGBoost مُحاكى)")
    fig = px.line(forecast_df, x="اليوم", y="الحاويات المتوقعة", markers=True, line_shape='spline')
    fig.update_traces(line_color='#0066cc')
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(forecast_df, use_container_width=True)

with tab2:
    st.subheader("توزيع السفن على الأرصفة (Gantt Chart)")
    fig_gantt = ff.create_gantt(gantt_df, index_col='Resource', show_colorbar=True, group_tasks=True)
    fig_gantt.update_layout(height=400)
    st.plotly_chart(fig_gantt, use_container_width=True)
    st.caption("النظام يُحسّن التوزيع لتقليل وقت الانتظار — باستخدام خوارزميات تحسين.")

with tab3:
    st.metric("إجمالي الإيرادات (7 أيام)", f"{revenue.sum():,} جنيه")
    fig_rev = px.bar(revenue_df, x="اليوم", y="الإيرادات (جنيه)", color_discrete_sequence=['#009966'])
    st.plotly_chart(fig_rev, use_container_width=True)

with tab4:
    st.subheader("تنبيهات الصيانة")
    st.warning("⚠️ الرافعة #3: احتمال عطل خلال 48 ساعة (درجة الثقة: 87%)")
    st.success("✅ باقي الرافعات: تعمل بشكل طبيعي")
    st.info("التنبؤ مبني على نموذج تصنيف XGBoost مُدرّب على بيانات تشغيل مصطنعة.")

st.markdown("---")
st.caption("تم إنشاء هذا النظام لأغراض تعليمية — لا يستخدم بيانات فعلية من محطة دمياط. | مشروع مفتوح المصدر")
