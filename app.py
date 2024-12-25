import pandas_ta as ta
print("Pandas-ta imported successfully")
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from technical_analysis import add_technical_indicators
from data_loader import download_stock_data

# عنوان التطبيق
st.title("تحليل الأسهم باستخدام المؤشرات الفنية والتنبؤات المستقبلية")

# إدخال المستخدم
ticker = st.text_input("أدخل رمز السهم (مثل: AAPL):", value="AAPL")
start_date = st.date_input("تاريخ البداية:", value=pd.to_datetime("2020-01-01"))
end_date = st.date_input("تاريخ النهاية:", value=pd.to_datetime("2023-12-31"))
future_days = st.slider("عدد الأيام للتنبؤ:", min_value=1, max_value=30, value=5)

if st.button("تحميل البيانات والتنبؤ"):
    with st.spinner("جاري تحميل البيانات..."):
        # تحميل بيانات السهم
        stock_data = download_stock_data(ticker, start_date, end_date)
        
        if stock_data is not None:
            # إعادة تسمية الأعمدة
            stock_data.columns = ['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']

            # إضافة المؤشرات الفنية
            stock_data = add_technical_indicators(stock_data)

            if stock_data is not None:
                st.success("تم تحميل البيانات وإضافة المؤشرات الفنية بنجاح!")
                
                # عرض البيانات
                st.subheader("البيانات:")
                st.dataframe(stock_data.tail())
                
                # رسم المؤشرات
                st.subheader("الرسومات البيانية:")
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(stock_data['Date'], stock_data['Close'], label="Close Price")
                ax.plot(stock_data['Date'], stock_data['SMA_20'], label="SMA 20")
                ax.plot(stock_data['Date'], stock_data['EMA_20'], label="EMA 20")
                ax.fill_between(stock_data['Date'], stock_data['BB_upper'], stock_data['BB_lower'], color='gray', alpha=0.3, label="Bollinger Bands")
                ax.legend()
                ax.set_title("Close Price and Indicators")
                ax.set_xlabel("Date")
                ax.set_ylabel("Price")
                st.pyplot(fig)
                
                # التنبؤ بالأسعار المستقبلية
                st.subheader("التنبؤات المستقبلية:")
                stock_data['Prediction'] = stock_data['Close'].shift(-future_days)
                X = stock_data[['Close']].values[:-future_days]
                y = stock_data['Prediction'].values[:-future_days]
                
                # تقسيم البيانات إلى تدريب واختبار
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # تدريب النموذج
                model = LinearRegression()
                model.fit(X_train, y_train)
                
                # التنبؤ
                future_X = stock_data[['Close']].values[-future_days:]
                predictions = model.predict(future_X)
                
                # عرض التنبؤات
                future_dates = pd.date_range(stock_data['Date'].iloc[-1], periods=future_days+1)[1:]
                prediction_df = pd.DataFrame({"Date": future_dates, "Predicted Close": predictions})
                st.dataframe(prediction_df)
                
                # رسم التنبؤات
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(stock_data['Date'], stock_data['Close'], label="Actual Prices")
                ax.plot(prediction_df['Date'], prediction_df['Predicted Close'], label="Predicted Prices", linestyle="--")
                ax.legend()
                ax.set_title("Actual vs Predicted Prices")
                ax.set_xlabel("Date")
                ax.set_ylabel("Price")
                st.pyplot(fig)
            else:
                st.error("فشل في إضافة المؤشرات الفنية.")
        else:
            st.error(f"لا توجد بيانات للسهم {ticker} في الفترة المحددة.")
