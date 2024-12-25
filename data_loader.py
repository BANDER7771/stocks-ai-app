import yfinance as yf
import pandas as pd

def download_stock_data(ticker, start_date, end_date):
    """
    تحميل بيانات الأسهم التاريخية باستخدام yfinance
    """
    try:
        # تحميل البيانات
        data = yf.download(ticker, start=start_date, end=end_date)
        
        # التحقق من البيانات
        if data.empty:
            print(f"لا توجد بيانات للسهم {ticker} في الفترة المحددة.")
            return None
        
        # إعادة البيانات بعد تنظيف الأعمدة
        data.reset_index(inplace=True)
        print(f"تم تحميل بيانات السهم {ticker} بنجاح.")
        return data
    except Exception as e:
        print(f"حدث خطأ أثناء تحميل بيانات السهم {ticker}: {e}")
        return None

# اختبار الكود
if __name__ == "__main__":
    ticker = "AAPL"  # رمز السهم (يمكن تغييره)
    start_date = "2020-01-01"
    end_date = "2023-12-31"
    
    stock_data = download_stock_data(ticker, start_date, end_date)
    if stock_data is not None:
        print(stock_data.head())  # طباعة أول 5 صفوف من البيانات
