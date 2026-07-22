import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Telekom Pazar & Churn Simülasyonu", layout="wide")

st.title("📱 Telekomünikasyon Pazar & Churn Simülasyonu")
st.caption("Fiyat zamları, cayma bedelleri ve altyapı kapasitesinin pazar paylarına etkisini simüle edin.")

# --- 1. YAN PANEL (GİRDİLER / PARAMETRELER) ---
st.sidebar.header("⚙️ Simülasyon Parametreleri")

# Pazar Büyüklüğü
toplam_musteri = st.sidebar.number_input("Toplam Simüle Edilecek Müşteri Sayısı", value=10000, step=1000)

st.sidebar.subheader("Operatör A (Zam Yapan)")
zam_A = st.sidebar.slider("A Operatörü Zam Oranı (%)", 0, 100, 40)
mevcut_pazar_A = st.sidebar.slider("A Başlangıç Pazar Payı (%)", 10, 80, 50)

st.sidebar.subheader("Pazar Koşulları")
cayma_cezasi_etkisi = st.sidebar.select_slider(
    "Cayma Bedeli Caydırıcılığı", 
    options=["Düşük (Kolay Geçiş)", "Orta", "Yüksek (Zor Geçiş)"],
    value="Orta"
)

# Cayma etkisi katsayısı
cayma_katsayisi = {"Düşük (Kolay Geçiş)": 0.8, "Orta": 0.5, "Yüksek (Zor Geçiş)": 0.2}[cayma_cezasi_etkisi]

# --- 2. SİMÜLASYON MOTORU ---
if st.button("🚀 Simülasyonu Çalıştır"):
    
    # Başlangıç Müşteri Dağılımı
    n_A = int(toplam_musteri * (mevcut_pazar_A / 100))
    n_diğer = toplam_musteri - n_A
    n_B = n_diğer // 2
    n_C = n_diğer - n_B

    # Müşteri Ayrılma (Churn) Olasılığı Hesabı
    base_churn_prob = (zam_A / 100) * (1 - cayma_katsayisi * 0.5)
    base_churn_prob = np.clip(base_churn_prob, 0, 0.95)

    # Binomial Dağılım ile kaç kişinin ayrılacağını simüle etme
    ayrilan_musteri = np.random.binomial(n_A, base_churn_prob)
    kalan_A = n_A - ayrilan_musteri

    # Ayrılanların B ve C'ye dağılması (%50 - %50 varsayım)
    giden_B = ayrilan_musteri // 2
    giden_C = ayrilan_musteri - giden_B

    yeni_B = n_B + giden_B
    yeni_C = n_C + giden_C

    # --- 3. SONUÇLARI GÖRSELLEŞTİRME ---
    st.markdown("---")
    
    # Özet Metrikler
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("A'dan Ayrılan Müşteri", f"{ayrilan_musteri:,}", delta=f"-{(ayrilan_musteri/n_A)*100:.1f}%", delta_color="inverse")
    col2.metric("A Yeni Müşteri Sayısı", f"{kalan_A:,}")
    col3.metric("B Yeni Müşteri Sayısı", f"{yeni_B:,}", delta=f"+{giden_B:,}")
    col4.metric("C Yeni Müşteri Sayısı", f"{yeni_C:,}", delta=f"+{giden_C:,}")

    # Grafik Verisi Hazırlama
    df_pazar = pd.DataFrame({
        "Operatör": ["A Operatörü", "B Operatörü", "C Operatör"],
        "Önceki Müşteri": [n_A, n_B, n_C],
        "Sonraki Müşteri": [kalan_A, yeni_B, yeni_C]
    })

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 Pazar Payı Değişimi")
        fig_bar = px.bar(df_pazar, x="Operatör", y=["Önceki Müşteri", "Sonraki Müşteri"], barmode="group")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("🍕 Yeni Pazar Payı Dağılımı")
        fig_pie = px.pie(df_pazar, names="Operatör", values="Sonraki Müşteri", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Endüstri Mühendisliği / Darboğaz Yorumu
    st.subheader("⚠️ Sistem ve Şebeke Darboğaz Yorumu")
    kullanim_orani_B = (yeni_B / (toplam_musteri * 0.4)) * 100
    
    if kullanim_orani_B > 100:
        st.error(f"🚨 **B Operatöründe Şebeke Aşırı Yüklendi!** Müşteri akını nedeniyle altyapı kapasitesi %{kullanim_orani_B:.1f} seviyesine ulaştı. Çekim kalitesinde düşüş bekleniyor.")
    else:
        st.success(f"✅ B ve C Operatörleri gelen müşteri yükünü başarıyla kaldırabiliyor. B Operatörü Kapasite Kullanımı: %{kullanim_orani_B:.1f}")
