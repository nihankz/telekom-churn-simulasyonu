import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Telekom Karar Destek & Pazar Simülatörü", layout="wide")

st.title("📱 Telekomünikasyon Karar Destek & Pazar Simülatörü")
st.caption("Gerçek pazar verileri ve operatör dinamikleriyle kişisel tarife analizi ve pazar simülasyonu.")

# --- SEKMELER ---
tab1, tab2 = st.tabs(["👤 Bireysel Kullanıcı Hesaplayıcı", "📊 Sektörel Pazar Simülasyonu"])

# ==========================================
# SEKME 1: BİREYSEL KULLANICI HESAPLAYICI
# ==========================================
with tab1:
    st.header("Mevcut Tarifenizi & Zam Teklifini Değerlendirin")
    st.write("Mevcut operatörünüzün sunduğu yenileme teklifini girerek diğer operatörlere geçmenin mantıklı olup olmadığını hesaplayın.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        mevcut_op = st.selectbox("Mevcut Operatörünüz", ["Turkcell", "Vodafone", "Türk Telekom"])
        mevcut_fiyat = st.number_input("Şu An Ödediğiniz Aylık Fatura (TL)", value=250, step=10)
        teklif_fiyat = st.number_input("Operatörün Yenileme İçin İstediği Fatura (TL)", value=450, step=10)
        cayma_bedeli = st.number_input("Şu An Ayrılırsanız Ödeyeceğiniz Cayma Bedeli (TL)", value=300, step=50)

    with col_b:
        st.subheader("Diğer Operatörlerin Ortalama Teklifleri")
        # Gerçekçi varsayılan piyasa ortalamaları
        diger_op_fiyat = st.number_input("Rakip Operatörlerin Benzer Paket Fiyatı (TL)", value=320, step=10)
        
    if st.button("🧮 Benim İçin Hesapla"):
        fark_aylik = teklif_fiyat - diger_op_fiyat
        st.markdown("---")
        
        if fark_aylik > 0:
            amorti_ayi = np.ceil(cayma_bedeli / fark_aylik) if fark_aylik > 0 else 0
            st.warning(f"⚠️ Rakip operatöre geçmek aylık **{fark_aylik:.0f} TL** tasarruf sağlar.")
            if cayma_bedeli > 0:
                st.info(f"💡 **Cayma Bedeli Analizi:** Ödeyeceğiniz {cayma_bedeli} TL cayma bedelini, yeni operatördeki tasarrufunuzla **{int(amorti_ayi)}. ayda** amorti edebilirsiniz (12 aylık taahhütte kârlısınız).")
            else:
                st.success("✅ Taahhüdünüz bittiği için cayma bedeli ödemeden doğrudan rakip operatöre geçmeniz avantajlı görünmektedir.")
        else:
            st.success("✅ Mevcut operatörünüzün teklifi piyasa ortalamasına göre oldukça avantajlı duruyor, kalmanız tavsiye edilir.")

# ==========================================
# SEKME 2: SEKTÖREL PAZAR SİMÜLASYONU
# ==========================================
with tab2:
    st.header("BTK Verilerine Dayalı Pazar & Churn Simülasyonu")
    
    st.sidebar.header("⚙️ Pazar Senaryoları")
    toplam_abone = st.sidebar.number_input("Toplam Simüle Edilecek Müşteri", value=100000, step=10000)
    
    st.sidebar.subheader("Zam Oranları (%)")
    zam_turkcell = st.sidebar.slider("Turkcell Zam Oranı (%)", 0, 100, 35)
    zam_vodafone = st.sidebar.slider("Vodafone Zam Oranı (%)", 0, 100, 25)
    zam_tt = st.sidebar.slider("Türk Telekom Zam Oranı (%)", 0, 100, 20)

    # Gerçek BTK Yaklaşık Pazar Payları (%41 Turkcell, %31 Vodafone, %28 TT)
    n_turkcell = int(toplam_abone * 0.41)
    n_vodafone = int(toplam_abone * 0.31)
    n_tt = toplam_abone - (n_turkcell + n_vodafone)

    if st.sidebar.button("🚀 Pazar Simülasyonunu Çalıştır"):
        # Churn Oranları Hesabı
        churn_tk = np.clip((zam_turkcell / 100) * 0.6, 0, 0.8)
        churn_vf = np.clip((zam_vodafone / 100) * 0.6, 0, 0.8)
        churn_tt = np.clip((zam_tt / 100) * 0.6, 0, 0.8)

        giden_tk = np.random.binomial(n_turkcell, churn_tk)
        giden_vf = np.random.binomial(n_vodafone, churn_vf)
        giden_tt = np.random.binomial(n_tt, churn_tt)

        # Yeni Pazar Dağılımı (Ayrılanlar diğer ikisine eşit dağılır)
        son_tk = (n_turkcell - giden_tk) + (giden_vf // 2) + (giden_tt // 2)
        son_vf = (n_vodafone - giden_vf) + (giden_tk // 2) + (giden_tt // 2)
        son_tt = (n_tt - giden_tt) + (giden_tk // 2) + (giden_vf // 2)

        df_sektor = pd.DataFrame({
            "Operatör": ["Turkcell", "Vodafone", "Türk Telekom"],
            "Mevcut Abone": [n_turkcell, n_vodafone, n_tt],
            "Simülasyon Sonrası Abone": [son_tk, son_vf, son_tt]
        })

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Abone Sayısı Değişimi")
            fig_bar = px.bar(df_sektor, x="Operatör", y=["Mevcut Abone", "Simülasyon Sonrası Abone"], barmode="group")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("🍕 Yeni Pazar Payı Dağılımı")
            fig_pie = px.pie(df_sektor, names="Operatör", values="Simülasyon Sonrası Abone", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
