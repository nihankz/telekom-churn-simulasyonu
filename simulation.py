import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Telekom Analytics | Karar Destek & Pazar Simülatörü",
    page_icon="📶",
    layout="wide"
)

# --- ÖZEL CSS TASARIM DOKUNUŞLARI ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .metric-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2e3440;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- ÜST BAŞLIK BANDI ---
st.title("📶 Telekom Analytics Portal")
st.caption("Pazar Dinamikleri, Churn Analizi ve Bireysel Tarife Optimalizasyon Modeli")
st.markdown("---")

# --- SEKMELER ---
tab1, tab2 = st.tabs(["👤 Bireysel Tarife & Amortisman Analizi", "📊 Kurumsal Pazar & Churn Simülasyonu"])

# ==========================================
# SEKME 1: BİREYSEL HESAPLAYICI & TASARRUF
# ==========================================
with tab1:
    st.subheader("💡 Tarife Yenileme & Cayma Bedeli Hesaplayıcı")
    st.write("Mevcut teklifinizi piyasa koşullarıyla karşılaştırarak en rasyonel kararı verin.")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        mevcut_op = st.selectbox("Mevcut Operatörünüz", ["Turkcell", "Vodafone", "Türk Telekom"])
        mevcut_fiyat = st.number_input("Şu An Ödediğiniz Fatura (TL)", value=250, step=10)
    
    with col_b:
        teklif_fiyat = st.number_input("Operatörün Yenileme Teklifi (TL)", value=480, step=10)
        cayma_bedeli = st.number_input("Erken Ayrılma / Cayma Bedeli (TL)", value=400, step=50)

    with col_c:
        diger_op_fiyat = st.number_input("Rakip Operatör Ortalama Teklifi (TL)", value=310, step=10)
        taahhut_suresi = st.slider("Hedef Taahhüt Süresi (Ay)", 6, 24, 12)

    st.markdown("### 📈 Analiz & Karar Matrisi")
    
    aylik_tasarruf = teklif_fiyat - diger_op_fiyat
    toplam_tasarruf_donem = (aylik_tasarruf * taahhut_suresi) - cayma_bedeli
    
    m1, m2, m3 = st.columns(3)
    
    m1.metric(
        label="Aylık Potansiyel Fark", 
        value=f"{aylik_tasarruf:.0f} TL", 
        delta=f"{'Tasarruf' if aylik_tasarruf > 0 else 'Zarar'}",
        delta_color="normal" if aylik_tasarruf > 0 else "inverse"
    )
    
    amorti_ayi = (cayma_bedeli / aylik_tasarruf) if aylik_tasarruf > 0 else 0
    m2.metric(
        label="Cayma Bedeli Amortisman Süresi", 
        value=f"{amorti_ayi:.1f} Ay" if amorti_ayi > 0 else "N/A",
        help="Ödeyeceğiniz cayma bedelinin kaç ayda kendini amorti edeceğini gösterir."
    )
    
    m3.metric(
        label=f"{taahhut_suresi} Aylık Net Kazanç / Kayıp", 
        value=f"{toplam_tasarruf_donem:.0f} TL",
        delta_color="normal" if toplam_tasarruf_donem > 0 else "inverse"
    )

    if toplam_tasarruf_donem > 0:
        st.success(f"🎯 **Öneri:** Rakip operatöre geçmeniz, cayma bedelini ödemenize rağmen {taahhut_suresi} ayda net **{toplam_tasarruf_donem:.0f} TL** tasarruf sağlar.")
    else:
        st.info("ℹ️ **Öneri:** Cayma bedeli yüksek olduğu için mevcut teklifi kabul etmek veya taahhüt sonunu beklemek daha avantajlıdır.")

# ==========================================
# SEKME 2: SEKTÖREL PAZAR SİMÜLASYONU
# ==========================================
with tab2:
    st.subheader("🏢 BTK Verileri İle Sektörel Churn & Şebeke Yükü Simülasyonu")
    
    st.sidebar.header("⚙️ Simülasyon Senaryoları")
    toplam_abone = st.sidebar.number_input("Simüle Edilecek Müşteri Evreni", value=100000, step=10000)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Operatör Zam Stratejileri (%)")
    zam_tk = st.sidebar.slider("Turkcell Zam Oranı (%)", 0, 100, 40)
    zam_vf = st.sidebar.slider("Vodafone Zam Oranı (%)", 0, 100, 25)
    zam_tt = st.sidebar.slider("Türk Telekom Zam Oranı (%)", 0, 100, 20)

    # Başlangıç Müşteri Dağılımı (BTK Oranları)
    n_tk = int(toplam_abone * 0.41)
    n_vf = int(toplam_abone * 0.31)
    n_tt = toplam_abone - (n_tk + n_vf)

    # Churn Olasılıkları
    churn_tk = np.clip((zam_tk / 100) * 0.55, 0, 0.85)
    churn_vf = np.clip((zam_vf / 100) * 0.55, 0, 0.85)
    churn_tt = np.clip((zam_tt / 100) * 0.55, 0, 0.85)

    giden_tk = np.random.binomial(n_tk, churn_tk)
    giden_vf = np.random.binomial(n_vf, churn_vf)
    giden_tt = np.random.binomial(n_tt, churn_tt)

    son_tk = (n_tk - giden_tk) + (giden_vf // 2) + (giden_tt // 2)
    son_vf = (n_vf - giden_vf) + (giden_tk // 2) + (giden_tt // 2)
    son_tt = (n_tt - giden_tt) + (giden_tk // 2) + (giden_vf // 2)

    df_sektor = pd.DataFrame({
        "Operatör": ["Turkcell", "Vodafone", "Türk Telekom"],
        "Başlangıç": [n_tk, n_vf, n_tt],
        "Simülasyon Sonrası": [son_tk, son_vf, son_tt]
    })

    # Görselleştirme (Grafikler)
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("##### 📊 Operatör Bazlı Müşteri Akışı")
        fig_bar = go.Figure(data=[
            go.Bar(name='Başlangıç', x=df_sektor['Operatör'], y=df_sektor['Başlangıç'], marker_color='#4C566A'),
            go.Bar(name='Simülasyon Sonrası', x=df_sektor['Operatör'], y=df_sektor['Simülasyon Sonrası'], marker_color='#88C0D0')
        ])
        fig_bar.update_layout(barmode='group', template='plotly_dark', margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown("##### 🍕 Pazar Payı Dağılımı")
        fig_pie = px.pie(
            df_sektor, 
            names="Operatör", 
            values="Simülasyon Sonrası", 
            hole=0.4,
            color_discrete_sequence=['#FFC000', '#E60000', '#001E50'] # Turkcell, VF, TT Kurumsal Renkleri
        )
        fig_pie.update_layout(template='plotly_dark', margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    # İndirme Butonu
    st.markdown("---")
    csv_data = df_sektor.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Simülasyon Verilerini CSV Olarak İndir",
        data=csv_data,
        file_name='telekom_pazar_simulasyonu.csv',
        mime='text/csv',
    )
