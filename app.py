import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="محطة حاويات دمياط - ذكاء اصطناعي", layout="wide")
st.title("🤖 لوحة تحكم ذكية - محطة حاويات دمياط")
st.markdown("تطبيق تجريبي مجاني لتنبؤات التداول، جدولة السفن، ومراقبة الأداء — بدون بيانات حقيقية.")

# =============== بيانات مصطنعة ===============
# تنبؤ الحاويات (7 أيام قادمة)
dates = pd.date_range(datetime.today(), periods=7, freq='D')
forecast = np.random.randint(3500, 5500, size=7)
forecast_df = pd.DataFrame({"اليوم": dates.strftime('%Y-%m-%d'), "الحاويات المتوقعة": forecast})

# جدولة السفن (5 سفن قادمة)
vessels = ["السفينة أ", "السفينة ب", "السفينة ج", "السفينة د", "السفينة هـ"]
etas = [(datetime.today() + timedelta(hours=i*6)).strftime('%Y-%m-%d %H:%M') for i in range(5)]
berths = ["رصيف 1", "رصيف 2", "رصيف 1", "رصيف 3", "رصيف 2"]
schedule_df = pd.DataFrame({"السفينة": vessels, "وقت الوصول": etas, "الرصيف المخصص": berths})

# إيرادات البوابات (7 أيام)
revenue_dates = pd.date_range(datetime.today() - timedelta(days=6), periods=7, freq='D')
revenue = np.random.randint(80000, 150000, size=7)
revenue_df = pd.DataFrame({"اليوم": revenue_dates.strftime('%Y-%m-%d'), "الإيرادات (جنيه)": revenue})

# =============== التبويبات ===============
tab1, tab2, tab3, tab4 = st.tabs(["📊 التنبؤ بالحاويات", "🚢 جدولة الأرصفة", "💰 مراقبة الإيرادات", "⚙️ الصيانة التنبؤية"])

with tab1:
    st.subheader("التنبؤ بعدد الحاويات للأيام القادمة")
    fig1 = px.line(forecast_df, x="اليوم", y="الحاويات المتوقعة", markers=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.dataframe(forecast_df, use_container_width=True)

with tab2:
    st.subheader("جدولة السفن على الأرصفة")
    st.dataframe(schedule_df, use_container_width=True)
    st.info("النظام يخصص الأرصفة تلقائيًا لتقليل وقت الانتظار.")

with tab3:
    st.subheader("إيرادات البوابات اليومية")
    fig3 = px.bar(revenue_df, x="اليوم", y="الإيرادات (جنيه)")
    st.plotly_chart(fig3, use_container_width=True)
    st.metric("إجمالي الإيرادات (7 أيام)", f"{revenue.sum():,} جنيه")

with tab4:
    st.subheader("الصيانة التنبؤية للرافعات")
    st.warning("⚠️ الرافعة #3: احتمال عطل خلال 48 ساعة (بناءً على بيانات التشغيل).")
    st.success("✅ الرافعات #1, #2, #4, #5: تعمل بشكل طبيعي.")
    st.info("النظام يستخدم نماذج ذكاء اصطناعي لتوقع الأعطال قبل حدوثها.")

st.markdown("---")
st.caption("تم إنشاء هذا التطبيق لأغراض تعليمية وتجريبية — لا يستخدم بيانات حقيقية. | مشروع مفتوح المصدر")
