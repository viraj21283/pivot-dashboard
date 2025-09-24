import streamlit as st
import pandas as pd

def classic_pivots(high, low, close):
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    s1 = (2 * pivot) - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    r3 = high + 2*(pivot - low)
    s3 = low - 2*(high - pivot)
    return pivot, r1, s1, r2, s2, r3, s3

def fibonacci_pivots(high, low, close):
    pivot = (high + low + close) / 3
    diff = high - low
    r1 = pivot + 0.382 * diff
    r2 = pivot + 0.618 * diff
    r3 = pivot + 1.000 * diff
    s1 = pivot - 0.382 * diff
    s2 = pivot - 0.618 * diff
    s3 = pivot - 1.000 * diff
    return r1, s1, r2, s2, r3, s3

def camarilla_pivots(high, low, close):
    diff = high - low
    r1 = close + (diff) * 1.1/12
    r2 = close + (diff) * 1.1/6
    r3 = close + (diff) * 1.1/4
    r4 = close + (diff) * 1.1/2
    s1 = close - (diff) * 1.1/12
    s2 = close - (diff) * 1.1/6
    s3 = close - (diff) * 1.1/4
    s4 = close - (diff) * 1.1/2
    return r1, r2, r3, r4, s1, s2, s3, s4

def woodie_pivots(open_, high, low, close):
    pivot = (high + low + 2*open_) / 4
    r1 = (2 * pivot) - low
    s1 = (2 * pivot) - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    return pivot, r1, s1, r2, s2

def demark_pivots(open_, high, low, close):
    if close < open_:
        x = high + (2 * low) + close
    elif close > open_:
        x = (2 * high) + low + close
    else:
        x = high + low + (2 * close)
    pivot = x / 4
    r1 = x / 2 - low
    s1 = x / 2 - high
    return pivot, r1, s1

def calculate_all(row):
    symbol = row.get("Symbol", "")
    high = row.get("High", None)
    low = row.get("Low", None)
    close = row.get("Close", None)
    open_ = row.get("Open", close)
    prev_close = row.get("Previous Close", close)
    try:
        high = float(high)
        low = float(low)
        close = float(close)
        open_ = float(open_) if open_ is not None else close
        prev_close = float(prev_close) if prev_close is not None else close

        cpivot, cr1, cs1, cr2, cs2, cr3, cs3 = classic_pivots(high, low, close)
        fr1, fs1, fr2, fs2, fr3, fs3 = fibonacci_pivots(high, low, close)
        cam_r1, cam_r2, cam_r3, cam_r4, cam_s1, cam_s2, cam_s3, cam_s4 = camarilla_pivots(high, low, close)
        wpivot, wr1, ws1, wr2, ws2 = woodie_pivots(open_, high, low, close)
        dpivot, dr1, ds1 = demark_pivots(open_, high, low, close)

        return {
            "Symbol": symbol,
            "Classic_Pivot": cpivot,
            "Classic_R1": cr1, "Classic_S1": cs1, "Classic_R2": cr2, "Classic_S2": cs2, "Classic_R3": cr3, "Classic_S3": cs3,
            "Fibonacci_R1": fr1, "Fibonacci_S1": fs1, "Fibonacci_R2": fr2, "Fibonacci_S2": fs2, "Fibonacci_R3": fr3, "Fibonacci_S3": fs3,
            "Camarilla_R1": cam_r1, "Camarilla_R2": cam_r2, "Camarilla_R3": cam_r3, "Camarilla_R4": cam_r4,
            "Camarilla_S1": cam_s1, "Camarilla_S2": cam_s2, "Camarilla_S3": cam_s3, "Camarilla_S4": cam_s4,
            "Woodie_Pivot": wpivot, "Woodie_R1": wr1, "Woodie_S1": ws1, "Woodie_R2": wr2, "Woodie_S2": ws2,
            "DeMark_Pivot": dpivot, "DeMark_R1": dr1, "DeMark_S1": ds1
        }
    except Exception as e:
        return {"Symbol": symbol, "Error": str(e)}

st.title("Stock Pivots Calculator Dashboard")

uploaded_file = st.file_uploader("Upload OHLC CSV or Excel File", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.write("Sample Input Data:", df.head())

    output_rows = [calculate_all(row) for row in df.to_dict(orient='records')]
    output_df = pd.DataFrame(output_rows)
    st.write("Calculated Pivots:", output_df)

    st.download_button(
        label="Download Results Excel",
        data=output_df.to_excel(index=False, engine='xlsxwriter'),
        file_name="pivot_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.download_button(
        label="Download Results CSV",
        data=output_df.to_csv(index=False),
        file_name="pivot_output.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV or Excel file with stock OHLC data.")

st.markdown("""
- Supported columns: Symbol, Open, High, Low, Close, Previous Close.
- Handles any combination: OHLC, HLC, or with Previous Close.
- All pivots: Classic, Fibonacci, Camarilla, Woodie, DeMark.
""")

st.write("---")
st.markdown(
    """
    <div style='color:orange; font-weight:bold; font-size:15px;'>
    ⚠️ Disclaimer: This tool is for informational and educational use only. No warranty is given for calculation accuracy, completeness, or suitability for financial decisions. Use at your own risk.
    </div>
    <br>
    <div style='color:#d6249f; font-size:18px; font-weight:bold;'>
    ❤️ Made with Love by Viraj Shah.
    </div>
    """,
    unsafe_allow_html=True
)
