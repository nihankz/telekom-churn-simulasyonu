Şu an kodunun en başında şu bölüm var:
st.markdown(
    """
<style>

.block-container{
    padding-top:2rem;
}

.kpi{
    background:#1f2937;
    padding:18px;
    border-radius:12px;
    border:1px solid #374151;
    text-align:center;
}

.green{
    background:#052e16;
    border:1px solid #16a34a;
    padding:16px;
    border-radius:10px;
}

.red{
    background:#450a0a;
    border:1px solid #dc2626;
    padding:16px;
    border-radius:10px;
}

.blue{
    background:#172554;
    border:1px solid #2563eb;
    padding:16px;
    border-radius:10px;
}

</style>
""",
    unsafe_allow_html=True,
)
Bunun tamamını sil.
Yerine bunu koy:
st.markdown(
    """
<style>

.block-container{
    padding-top:1.5rem;
    padding-left:3rem;
    padding-right:3rem;
}


/* Ana başlık */
h1{
    font-weight:700;
    letter-spacing:-1px;
}


/* Kartlar */
div[data-testid="metric-container"]{
    background:#111827;
    border:1px solid #374151;
    padding:18px;
    border-radius:16px;
    box-shadow:0 4px 12px rgba(0,0,0,0.15);
}


/* Metric başlığı */
div[data-testid="metric-container"] label{
    color:#9ca3af;
    font-size:14px;
}


/* Metric değer */
div[data-testid="metric-container"] [data-testid="stMetricValue"]{
    font-size:32px;
    font-weight:700;
}


/* Genel kutu */
.info-card{
    background:#111827;
    padding:22px;
    border-radius:18px;
    border:1px solid #374151;
}


/* Başarı kartı */
.success-card{
    background:#052e16;
    padding:22px;
    border-radius:18px;
    border:1px solid #16a34a;
}


/* Risk kartı */
.warning-card{
    background:#451a03;
    padding:22px;
    border-radius:18px;
    border:1px solid #f97316;
}


/* Tablo */
div[data-testid="stDataFrame"]{
    border-radius:15px;
}


/* Sidebar */
section[data-testid="stSidebar"]{
    background:#0f172a;
}

</style>
""",
    unsafe_allow_html=True,
)
