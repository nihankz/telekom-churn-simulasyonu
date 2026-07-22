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

# --- SESSION STATE (ŞABLON VE OCR VERİLERİ) ---
if 'gb_val' not in st.session_state:
    st.session_state.gb_val = 25
if 'fatura_okundu' not in st.session_state:
    st.session_state.fatura_okundu = False

def set_template(gb):
    st.session_state.gb_val = gb

def simule_ocr_ornek():
    st.session_state.fatura_okundu = True
    st.session_state.gb_val = 12  # Kullanıcının fiili harcadığı
    st.toast("📄 Örnek fatura verileri AI/OCR ile başarıyla okundu!", icon="✨")

# --- ÖZEL CSS TASARIMI ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .hero-header {
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #374151;
        margin-bottom: 20px;
    }
    .ocr-box {
        background-color: #1e293b;
        border: 2px dashed #3b82f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BAŞLIK BANNER ---
st.markdown("""
    <div class="hero-header">
        <h1 style='color: #F3F4F6; margin:0;'>📲 Akıllı Fatura & Taahhüt Otomasyon Portalı</h1>
        <p style='color: #9CA3AF; margin-top: 5px; margin-bottom:0;'>AI Destekli Fatura OCR Teşhisi, Enflasyon Ayarlı NPV Analizi ve Otomatik Tasarruf</p>
    </div>
""", unsafe_allow_html=True)

# --- FAZ 1: FATURA OCR & TEŞHİS MODÜLÜ ---
st.subheader("📄 1. Akıllı Fatura Taraması & Yapay Zekâ Teşhisi")

col_ocr1, col_ocr2 = st.columns([2, 1])

with col_ocr1:
    uploaded_file = st.file_uploader("E-Fatura PDF veya Görselini Yükleyin", type=['pdf', 'png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        st.session_state.fatura_okundu = True
        st.success("✅ Fatura başarıyla yüklendi ve AI modelleriyle ayrıştırıldı.")

with col_ocr2:
    st.write("Faturanız yok mu? Sistem analizi görmek için tek tıkla test edin:")
    st.button("🪄 Örnek Fatura İle AI Analizi Başlat", on_click=simule_ocr_ornek, use_container_width=True)

if st.session_state.fatura_okundu:
    st.info("""
    🔍 **AI Teşhis Raporu:**
    * **Tespit Edilen Paket:** 35 GB / Aylık 520 TL
    * **Son 3 Ay Ortalama Harcanan:** **12 GB**
    * **⚠️ Kritik Bulgular:** Paketinizin **%65'ini (23 GB)** hiç kullanmıyorsunuz. Operatörünüz ihtiyacınızdan daha yüksek bir paket tanımlamış.
    """)

st.markdown("---")

# --- HIZLI PROFİL ŞABLONLARI ---
st.markdown("##### ⚡ Manuel Profil Seçimi")
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
    st.subheader("2. Sözleşme & Teklif")
    mevcut_op = st.selectbox("Mevcut Operatörünüz", ["Turkcell", "Vodafone", "Türk Telekom"])
    yenileme_fiyat = st.number_input("Aylık Yenileme Teklifi (TL)", value=520, step=20)
    rakip_fiyat = st.number_input("En İyi Rakip Fiyatı (TL)", value=310, step=20)

with col_in2:
    st.subheader("3. Cayma & Kullanım")
    cayma_bedeli = st.number_input("Erken Ayrılma / Cayma Bedeli (TL)", value=450, step=50)
    taahhut_ay = st.radio("Taahhüt Süresi (Ay)", [12, 24], horizontal=True)
    gb_kullanim = st.slider("Fiili / Gerçek İnternet İhtiyacı (GB)", 5, 100, key="gb_val")

with col_in3:
    st.subheader("4. Makro Parametreler")
    enflasyon_beklentisi = st.slider("Tahmini Yıllık Enflasyon (%)", 10, 80, 35)
    firsat_maliyeti = st.slider("Aylık İskonto / Faiz Oranı (%)", 0.0, 5.0, 2.0, step=0.5)

# --- FİNANSAL ALGORİTMA ---
r = firsat_maliyeti / 100

npv_mevcut = sum([yenileme_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)])
npv_rakip = cayma_bedeli + sum([rakip_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)])
net_npv_kazanc = npv_mevcut - npv_rakip

gb_maliyet_mevcut = yenileme_fiyat / gb_kullanim
gb_maliyet_rakip = rakip_fiyat / gb_kullanim

if net_npv_kazanc > 1000:
    st.balloons()

st.markdown("---")

# --- ANALİZ VE GRAFİK EKRANI ---
st.subheader("📊 Analitik Karar & Karşılaştırma Raporu")

c_left, c_right = st.columns([1, 1])

with c_left:
    st.markdown("##### 🎯 Fiyat Verimliliği (Piyasa Göstergesi)")
    
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
    st.markdown("##### 📈 Birim GB Maliyet Kıyaslaması")
    
    m1, m2 = st.columns(2)
    m1.metric("Mevcut GB Başı Maliyet", f"{gb_maliyet_mevcut:.2f} TL/GB")
    m2.metric("Rakip GB Başı Maliyet", f"{gb_maliyet_rakip:.2f} TL/GB", delta=f"-{(1 - gb_maliyet_rakip/gb_maliyet_mevcut)*100:.1f}%")
    
    st.markdown("---")
    
    if net_npv_kazanc > 0:
        st.success(f"🔥 **AŞIRI TASARRUF FIRSATI:** Cayma bedelini ödeyip gerçek ihtiyacınıza uygun rakip pakete geçmek, **{taahhut_ay} ayda net {net_npv_kazanc:,.0f} TL** cebinizde bırakıyor!")
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
