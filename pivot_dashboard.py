import streamlit as st
import pandas as pd

def to_float(val, fallback=0.0):
    try:
        if pd.isna(val) or val is None or val == "":
            return fallback
        return float(val)
    except:
        return fallback

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
    return pivot, r1, s1, r2, s2, r3, s3

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

st.title("Stock Pivots Calculator Dashboard")

uploaded_file = st.file_uploader("Upload OHLC CSV or Excel File", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Map your column names to internal names
    df = df.rename(columns={
        "SYMBOL": "Symbol",
        "PREV_CL_PR": "Previous Close",
        "OPEN_PRICE": "Open",
        "HIGH_PRICE": "High",
        "LOW_PRICE": "Low",
        "CLOSE_PRICE": "Close"
    })
    st.write("Sample Input Data:", df.head())

    classic_rows = []
    fibonacci_rows = []
    camarilla_rows = []
    woodie_rows = []
    demark_rows = []

    for row in df.to_dict(orient='records'):
        symbol = row.get("Symbol", "")
        high = to_float(row.get("High"))
        low = to_float(row.get("Low"))
        close = to_float(row.get("Close"))
        open_ = to_float(row.get("Open"), close)
        prev_close = to_float(row.get("Previous Close"), close)

        try:
            cpivot, cr1, cs1, cr2, cs2, cr3, cs3 = classic_pivots(high, low, close)
            fr_pivot, fr1, fs1, fr2, fs2, fr3, fs3 = (cpivot,) + fibonacci_pivots(high, low, close)
            cam_r1, cam_r2, cam_r3, cam_r4, cam_s1, cam_s2, cam_s3, cam_s4 = camarilla_pivots(high, low, close)
            wpivot, wr1, ws1, wr2, ws2 = woodie_pivots(open_, high, low, close)
            dpivot, dr1, ds1 = demark_pivots(open_, high, low, close)

            classic_rows.append({
                "Symbol": symbol,
                "Pivot": cpivot,
                "R1": cr1, "S1": cs1, "R2": cr2, "S2": cs2, "R3": cr3, "S3": cs3,
            })
            fibonacci_rows.append({
                "Symbol": symbol,
                "Pivot": fr_pivot,
                "R1": fr1, "S1": fs1, "R2": fr2, "S2": fs2, "R3": fr3, "S3": fs3,
            })
            camarilla_rows.append({
                "Symbol": symbol,
                "R1": cam_r1, "R2": cam_r2, "R3": cam_r3, "R4": cam_r4,
                "S1": cam_s1, "S2": cam_s2, "S3": cam_s3, "S4": cam_s4,
            })
            woodie_rows.append({
                "Symbol": symbol,
                "Pivot": wpivot,
                "R1": wr1, "S1": ws1, "R2": wr2, "S2": ws2,
            })
            demark_rows.append({
                "Symbol": symbol,
                "Pivot": dpivot,
                "R1": dr1, "S1": ds1,
            })
        except Exception as e:
            # Error rows
            err_row = {"Symbol": symbol, "Error": str(e)}
            classic_rows.append(err_row)
            fibonacci_rows.append(err_row)
            camarilla_rows.append(err_row)
            woodie_rows.append(err_row)
            demark_rows.append(err_row)

    st.subheader("Classic Pivot Points")
    st.write(pd.DataFrame(classic_rows))

    st.subheader("Fibonacci Pivot Points")
    st.write(pd.DataFrame(fibonacci_rows))

    st.subheader("Camarilla Pivot Points")
    st.write(pd.DataFrame(camarilla_rows))

    st.subheader("Woodie Pivot Points")
    st.write(pd.DataFrame(woodie_rows))

    st.subheader("DeMark Pivot Points")
    st.write(pd.DataFrame(demark_rows))

    # Download CSV for all together as separate sheets merged (optional)
    combined_df = pd.concat([
        pd.DataFrame(classic_rows),
        pd.DataFrame(fibonacci_rows),
        pd.DataFrame(camarilla_rows),
        pd.DataFrame(woodie_rows),
        pd.DataFrame(demark_rows)
    ], axis=1)
    st.download_button(
        label="Download All Pivots CSV",
        data=combined_df.to_csv(index=False),
        file_name="pivot_output.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV or Excel file with stock OHLC data.")

st.markdown("""
- Supported columns on upload: SYMBOL, PREV_CL_PR, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE
- Mapped internally to: Symbol, Previous Close, Open, High, Low, Close
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
