import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Fatura & Taahhüt Analytics Portal", 
    page_icon="📲", 
    layout="wide"
)

# --- BİLGİ / ŞABLON BUTONLARI İÇİN MANTIKSAL HAZIRLIK ---
if 'gb_val' not in st.session_state:
    st.session_state.gb_val = 25

def set_template(gb):
    st.session_state.gb_val = gb

# --- ÖZEL CSS TASARIMI ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .hero-header {
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #374151;
        margin-bottom: 25px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- BAŞLIK / HERO BANNER ---
st.markdown("""
    <div class="hero-header">
        <h1 style='color: #F3F4F6; margin:0;'>📲 Fatura & Taahhüt Akıllı Karar Portalı</h1>
        <p style='color: #9CA3AF; margin-top: 5px; margin-bottom:0;'>Enflasyon Korumalı NPV Analizi, Operatör Karşılaştırma ve Taahhüt Risk Yönetimi</p>
    </div>
""", unsafe_allow_html=True)

# --- HIZLI PROFİL ŞABLONLARI ---
st.markdown("##### ⚡ Hızlı Profil Seçimi")
col_b1, col_b2, col_b3, _ = st.columns([1, 1, 1, 2])
with col_b1:
    st.button("🎓 Öğrenci (15 GB)", on_click=set_template, args=(15,), use_container_width=True)
with col_b2:
    st.button("👤 Standart (25 GB)", on_click=set_template, args=(25,), use_container_width=True)
with col_b3:
    st.button("🚀 Yoğun Kullanım (50 GB)", on_click=set_template, args=(50,), use_container_width=True)

st.markdown("---")

# --- GİRDİ PANELİ ---
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    st.subheader("1. Sözleşme & Teklif")
    mevcut_op = st.selectbox("Mevcut Operatörünüz", ["Turkcell", "Vodafone", "Türk Telekom"])
    yenileme_fiyat = st.number_input("Aylık Yenileme Teklifi (TL)", value=480, step=20)
    rakip_fiyat = st.number_input("En İyi Rakip Fiyatı (TL)", value=320, step=20)

with col_in2:
    st.subheader("2. Cayma & Kullanım")
    cayma_bedeli = st.number_input("Erken Ayrılma / Cayma Bedeli (TL)", value=500, step=50)
    taahhut_ay = st.radio("Taahhüt Süresi (Ay)", [12, 24], horizontal=True)
    gb_kullanim = st.slider("Aylık İnternet İhtiyacı (GB)", 5, 100, key="gb_val")

with col_in3:
    st.subheader("3. Makro Parametreler")
    enflasyon_beklentisi = st.slider("Tahmini Yıllık Enflasyon (%)", 10, 80, 35)
    firsat_maliyeti = st.slider("Aylık İskonto / Faiz Oranı (%)", 0.0, 5.0, 2.0, step=0.5)

# --- FİNANSAL ALGORİTMA (NPV & ENFLASYON) ---
r = firsat_maliyeti / 100

npv_mevcut = sum([yenileme_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)])
npv_rakip = cayma_bedeli + sum([rakip_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)])
net_npv_kazanc = npv_mevcut - npv_rakip

gb_maliyet_mevcut = yenileme_fiyat / gb_kullanim
gb_maliyet_rakip = rakip_fiyat / gb_kullanim

# Konfeti Efekti (Büyük tasarruf varsa)
if net_npv_kazanc > 1000:
    st.balloons()

st.markdown("---")

# --- ANALİZ VE GRAFİK EKRANI ---
st.subheader("📊 Analitik Karar & Karşılaştırma Raporu")

c_left, c_right = st.columns([1, 1])

with c_left:
    st.markdown("##### 🎯 Fiyat Verimliliği (Piyasa Göstergesi)")
    
    # Gauge Termometre Grafiği
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = yenileme_fiyat,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Teklif Fiyatı vs Rakip Ort."},
        delta = {'reference': rakip_fiyat, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, rakip_fiyat * 2]},
            'bar': {'color': "#3B82F6"},
            'steps' : [
                {'range': [0, rakip_fiyat], 'color': "rgba(16, 185, 129, 0.2)"},
                {'range': [rakip_fiyat, rakip_fiyat * 1.5], 'color': "rgba(245, 158, 11, 0.2)"},
                {'range': [rakip_fiyat * 1.5, rakip_fiyat * 2], 'color': "rgba(239, 68, 68, 0.2)"}
            ],
        }
    ))
    fig_gauge.update_layout(template="plotly_dark", height=280, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with c_right:
    st.markdown("##### 📈 Birim Maliyet Kıyaslaması")
    
    m1, m2 = st.columns(2)
    m1.metric("Mevcut GB Başı Maliyet", f"{gb_maliyet_mevcut:.2f} TL/GB")
    m2.metric("Rakip GB Başı Maliyet", f"{gb_maliyet_rakip:.2f} TL/GB", delta=f"-{(1 - gb_maliyet_rakip/gb_maliyet_mevcut)*100:.1f}%")
    
    st.markdown("---")
    
    if net_npv_kazanc > 0:
        st.success(f"🔥 **FIRSAT:** Enflasyon ayarlı Net Bugünkü Değer (NPV) hesabına göre, cayma bedelini ödeyip rakibe geçmek **{taahhut_ay} ayda net {net_npv_kazanc:,.0f} TL** cebinizde bırakıyor!")
    else:
        st.info("🛡️ **KORUMA:** Cayma bedeli yüksek olduğu için mevcut teklifte kalmak şu an daha rasyonel.")

# Akış Grafiği
st.markdown("##### 📉 Ay Bazında Kumulatif Finansal Yük")
aylar = list(range(1, taahhut_ay + 1))
kumulatif_mevcut = [sum([yenileme_fiyat / ((1 + r) ** i) for i in range(1, t + 1)]) for t in aylar]
kumulatif_rakip = [cayma_bedeli + sum([rakip_fiyat / ((1 + r) ** i) for i in range(1, t + 1)]) for t in aylar]

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=aylar, y=kumulatif_mevcut, mode='lines+markers', name='Mevcut Operatör', line=dict(color='#EF4444', width=3)))
fig_line.add_trace(go.Scatter(x=aylar, y=kumulatif_rakip, mode='lines+markers', name='Rakip Operatör (Cayma Dahil)', line=dict(color='#10B981', width=3)))
fig_line.update_layout(template="plotly_dark", height=320, margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Ay", yaxis_title="Toplam Maliyet (TL)")

st.plotly_chart(fig_line, use_container_width=True)
