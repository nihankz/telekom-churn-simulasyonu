import streamlit as st
import pandas as pd

# Sayfa Ayarları (Mobil Uyumlu)
st.set_page_config(page_title="Fatura & Taahhüt Asistanı", page_icon="📲", layout="centered")

st.title("📲 Fatura & Taahhüt Akıllı Asistanı")
st.write("Taahhüdünüz bitiyor mu? Yenilemeden önce 1 dakikada cebinizden çıkacak parayı hesaplayın.")

st.markdown("---")

# 1. Kullanıcı Girdileri
mevcut_op = st.selectbox("Şu an kullandığınız operatör:", ["Turkcell", "Vodafone", "Türk Telekom"])

col1, col2 = st.columns(2)
with col1:
    yeni_teklif = st.number_input("Operatörün yeni dönem teklifi (TL/Ay):", value=450, step=10)
    cayma_bedeli = st.number_input("Şu an ayrılırsanız cayma bedeli (TL):", value=0, step=50)

with col2:
    ihtiyac_gb = st.select_slider("Aylık Ortalama İnternet İhtiyacınız:", options=["10 GB", "15 GB", "20 GB", "30 GB", "Sınırsız"], value="20 GB")
    taahhut_ay = st.radio("Düşündüğünüz Taahhüt Süresi:", [12, 24], horizontal=True)

# Piyasa Ortalama Fiyat Mantığı (Varsayımsal Paket Fiyatları)
piyasa_fiyatlari = {
    "10 GB": {"Turkcell": 280, "Vodafone": 220, "Türk Telekom": 210},
    "15 GB": {"Turkcell": 340, "Vodafone": 270, "Türk Telekom": 250},
    "20 GB": {"Turkcell": 420, "Vodafone": 320, "Türk Telekom": 300},
    "30 GB": {"Turkcell": 520, "Vodafone": 410, "Türk Telekom": 390},
    "Sınırsız": {"Turkcell": 750, "Vodafone": 600, "Türk Telekom": 580}
}

# Rakip operatörlerin o paket için ortalama en iyi fiyatı
rakip_fiyatlar = [v for k, v in piyasa_fiyatlari[ihtiyac_gb].items() if k != mevcut_op]
en_iyi_rakip_fiyat = min(rakip_fiyatlar)

# Hesaplamalar
aylik_fark = yeni_teklif - en_iyi_rakip_fiyat
toplam_yillik_mevcut = yeni_teklif * taahhut_ay
toplam_yillik_rakip = (en_iyi_rakip_fiyat * taahhut_ay) + cayma_bedeli
net_tasarruf = toplam_yillik_mevcut - toplam_yillik_rakip

st.markdown("---")
st.subheader("🎉 Karar & Tasarruf Analiziniz")

if net_tasarruf > 0:
    st.success(f"### 💡 Operatör Değiştirmek Mantıklı!")
    st.markdown(f"""
    * Rakip operatörlerde **{ihtiyac_gb}** paketleri ortalama **{en_iyi_rakip_fiyat} TL/Ay** seviyesinde.
    * Cayma bedelini (**{cayma_bedeli} TL**) ödeseniz bile, **{taahhut_ay} ayda net {net_tasarruf:,.0f} TL** cebinizde kalıyor!
    * Aylık ortalama tasarrufunuz: **{aylik_fark:.0f} TL/Ay**.
    """)
else:
    st.info(f"### 🛑 Mevcut Operatörünüzde Kalın!")
    st.markdown(f"""
    * Size sunulan **{yeni_teklif} TL** teklif, piyasadaki benzer **{ihtiyac_gb}** paketlerine göre oldukça avantajlı.
    * Başka operatöre geçmek şu aşamada maliyetinizi artırır veya değmez.
    """)

st.caption("Fiyatlar genel piyasa ortalamalarına göre bilgilendirme amaçlı hesaplanmıştır.")
  
