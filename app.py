import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# إعدادات الصفحة
st.set_page_config(page_title="فلتر أسهم تاسي بالذكاء الاصطناعي", layout="wide")
st.title("📊 فلتر السوق السعودي (TASI) الذكي")
st.write("برنامج ويب مجاني لتحليل وتصفية الأسهم السعودية بناءً على المؤشرات الفنية.")

# قائمة ببعض أبرز شركات السوق السعودي كمثال (يمكن التعديل عليها أو ربطها بملف كامل)
TICKERS = {
    "الراجحي": "1120",
    "أرامكو": "2222",
    "الأهلي": "1180",
    "سابك": "2010",
    "STC": "7010",
    "معادن": "1211.SR",
    "كهرباء السعودية": "5110",
    "مصرف الإنماء": "1150"
}

# واجهة الفلاتر في القائمة الجانبية
st.sidebar.header("🎛️ خيارات الفلترة الفنية")
min_price = st.sidebar.slider("الحد الأدنى للسعر (ريال)", 0, 200, 10)
max_price = st.sidebar.slider("الحد الأقصى للسعر (ريال)", 10, 500, 150)
rsi_filter = st.sidebar.selectbox("حالة مؤشر RSI (مؤشر القوة النسبية)", ["الكل", "تشبع شراء (RSI > 70)", "تشبع بيع - فرصة (RSI < 30)"])

@st.cache_data(ttl=3600)  # تخزين البيانات مؤقتاً لمدة ساعة لسرعة الأداء
def get_stock_data():
    data_list = []
    for name, ticker in TICKERS.items():
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="3mo")
            if not df.empty:
                # حساب المؤشرات الفنية
                df['RSI'] = ta.rsi(df['Close'], length=14)
                latest = df.iloc[-1]
                
                data_list.append({
                    "الشركة": name,
                    "الرمز": ticker.replace(".SR", ""),
                    "السعر الحالي (ريال)": round(latest['Close'], 2),
                    "حجم التداول": int(latest['Volume']),
                    "مؤشر RSI": round(latest['RSI'], 2) if not pd.isna(latest['RSI']) else 50
                })
        except Exception as e:
            continue
    return pd.DataFrame(data_list)

# تحميل البيانات
with st.spinner("جاري سحب بيانات تاسي الحالية..."):
    df_stocks = get_stock_data()

# تطبيق الفلاتر
if not df_stocks.empty:
    # فلتر السعر
    filtered_df = df_stocks[(df_stocks["السعر الحالي (ريال)"] >= min_price) & (df_stocks["السعر الحالي (ريال)"] <= max_price)]
    
    # فلتر RSI
    if rsi_filter == "تشبع شراء (RSI > 70)":
        filtered_df = filtered_df[filtered_df["مؤشر RSI"] > 70]
    elif rsi_filter == "تشبع بيع - فرصة (RSI < 30)":
        filtered_df = filtered_df[filtered_df["مؤشر RSI"] < 30]
        
    # عرض النتائج
    st.subheader(f"🔍 الأسهم المطابقة للفلاتر ({len(filtered_df)} شركة)")
    st.dataframe(filtered_df, use_container_width=True)
    
    # رؤية الذكاء الاصطناعي المبسطة
    st.info("💡 **نصيحة الذكاء الاصطناعي:** الأسهم التي يتراوح مؤشر RSI لها تحت 30 قد تكون في مناطق ارتداد (فرصة شراء)، بينما فوق 70 قد تكون متضخمة.")
else:
    st.error("نعتذر، واجهنا مشكلة في جلب البيانات الحالية للسوق.")
