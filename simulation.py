import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Sayfa Ayarları
st.set_page_config(
    page_title="Telekom Financial Analytics Portal", 
    page_icon="📊", 
    layout="wide"
)

st.title("📊 Telekomünikasyon Finansal Karar & Optimasyon Portalı")
st.caption("Enflasyon ayarlanmış Net Bugünkü Değer (NPV), Birim GB Maliyet Eğrisi ve Sözleşme Risk Skoru Analizi")
st.markdown("---")

# --- GİRDİ PANELİ ---
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    st.subheader("1. Sözleşme & Teklif")
    mevcut_op = st.selectbox("Mevcut Operatör", ["Turkcell", "Vodafone", "Türk Telekom"])
    yenileme_fiyat = st.number_input("Aylık Yenileme Teklifi (TL)", value=500, step=25)
    rakip_fiyat = st.number_input("En İyi Rakip Fiyatı (TL)", value=340, step=25)

with col_in2:
    st.subheader("2. Cayma & Taahhüt")
    cayma_bedeli = st.number_input("Mevcut Cayma Bedeli (TL)", value=600, step=50)
    taahhut_ay = st.selectbox("Taahhüt Süresi (Ay)", [12, 24], index=0)
    gb_kullanim = st.slider("Aylık Ortalama İnternet (GB)", 5, 100, 25)

with col_in3:
    st.subheader("3. Makroekonomik Parametreler")
    enflasyon_beklentisi = st.slider("Yıllık Tahmini Enflasyon (%)", 0, 100, 35)
    firsat_maliyeti = st.slider("Aylık İskonto / Faiz Oranı (%)", 0.0, 5.0, 2.0, step=0.5)

# --- FİNANSAL ALGORİTMA (NPV & ENFLASYON AYARLAMASI) ---
# Aylık iskonto oranı
r = firsat_maliyeti / 100

# Nakit Akışları Hesabı
npv_mevcut = sum([yenileme_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)])
npv_rakip = cayma_bedeli + sum([rakip_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)])

net_npv_kazanc = npv_mevcut - npv_rakip
gb_basa_maliyet_mevcut = yenileme_fiyat / gb_kullanim
gb_basa_maliyet_rakip = rakip_fiyat / gb_kullanim

# Risk Skoru Hesabı (0 - 100)
risk_skoru = min(100, int((cayma_bedeli / (yenileme_fiyat * 2)) * 30 + (taahhut_ay / 12) * 40 + (enflasyon_beklentisi / 100) * 30))

st.markdown("---")

# --- SONUÇ PANELİ ---
st.subheader("📈 Analitik Değerlendirme & Finansal Rapor")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    label="Bugünkü Net Değer (NPV) Kazancı", 
    value=f"{abs(net_npv_kazanc):,.0f} TL", 
    delta="Rakip Avantajlı" if net_npv_kazanc > 0 else "Mevcut Avantajlı",
    delta_color="normal" if net_npv_kazanc > 0 else "inverse"
)

m2.metric(
    label="Mevcut GB Başı Maliyet", 
    value=f"{gb_basa_maliyet_mevcut:.2f} TL/GB"
)

m3.metric(
    label="Rakip GB Başı Maliyet", 
    value=f"{gb_basa_maliyet_rakip:.2f} TL/GB",
    delta=f"-{(1 - gb_basa_maliyet_rakip/gb_basa_maliyet_mevcut)*100:.1f}%"
)

m4.metric(
    label="Sözleşme Risk Skoru", 
    value=f"{risk_skoru} / 100",
    help="Yüksek skor, yüksek enflasyon ve uzun taahhüt döneminde esnekliğinizi kaybettiğinizi gösterir."
)

# --- GRAFİK KISMI ---
st.markdown("### 📉 Zaman İçi Nakit Akışı & Maliyet Birikimi")

aylar = list(range(1, taahhut_ay + 1))
kumulatif_mevcut = [sum([yenileme_fiyat / ((1 + r) ** i) for i in range(1, t + 1)]) for t in aylar]
kumulatif_rakip = [cayma_bedeli + sum([rakip_fiyat / ((1 + r) ** i) for i in range(1, t + 1)]) for t in aylar]

fig = go.Figure()
fig.add_trace(go.Scatter(x=aylar, y=kumulatif_mevcut, mode='lines+markers', name='Mevcut Operatör (Kumulatif NPV)', line=dict(color='#FF4B4B', width=3)))
fig.add_trace(go.Scatter(x=aylar, y=kumulatif_rakip, mode='lines+markers', name='Rakip Operatör (Cayma Dahil NPV)', line=dict(color='#00CC96', width=3)))

fig.update_layout(
    title="Ay Bazında Finansal Yük & Başabaş (Break-Even) Analizi",
    xaxis_title="Ay",
    yaxis_title="Toplam Bugünkü Değer (TL)",
    template="plotly_dark",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Karar Özeti
if net_npv_kazanc > 0:
    st.success(f"🎯 **Finansal Model Tavesiyesi:** Enflasyon ve iskonto oranı hesaba katıldığında, cayma bedelini peşin ödeyip rakip operatöre geçmek dönemsel olarak net **{net_npv_kazanc:,.0f} TL bugünkü değer kazancı** sağlamaktadır.")
else:
    st.warning(f"⚠️ **Finansal Model Tavsiyesi:** Peşin cayma bedeli yükü nedeniyle mevcut teklifi kabul etmek finansal açıdan daha rasyoneldir.")
    
