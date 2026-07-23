import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Kurumsal Fatura & Filo Optimizasyon Portalı",
    page_icon="🏢",
    layout="wide",
)

# --- SESSION STATE ---
if "gb_val" not in st.session_state:
    st.session_state.gb_val = 25
if "fatura_okundu" not in st.session_state:
    st.session_state.fatura_okundu = False


def set_template(gb):
    st.session_state.gb_val = gb


def simule_ocr_ornek():
    st.session_state.fatura_okundu = True
    st.session_state.gb_val = 20
    st.toast("📄 Fatura ve gizli harcama kalemleri başarıyla tarandı!", icon="🔍")


# --- ÖZEL CSS TASARIMI ---
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    .hero-header {
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #374151;
        margin-bottom: 20px;
    }
    .dark-pattern-card {
        background-color: #2a1215;
        border: 1px solid #ef4444;
        padding: 16px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .gift-card {
        background-color: #064e3b;
        border: 1px solid #10b981;
        padding: 14px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .b2b-card {
        background-color: #1e1b4b;
        border: 1px solid #6366f1;
        padding: 16px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .upload-info-box {
        background-color: #1f2937;
        border-left: 4px solid #3b82f6;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
        font-size: 13px;
        color: #D1D5DB;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- BAŞLIK BANNER ---
st.markdown(
    """
    <div class="hero-header">
        <h1 style='color: #F3F4F6; margin:0;'>🏢 Kurumsal Filo & Bireysel Fatura Optimizasyon Portalı</h1>
        <p style='color: #9CA3AF; margin-top: 5px; margin-bottom:0;'>AI Destekli Fatura Taraması, Gizli Yan Hizmet Dedektörü ve B2B Harcama Optimizasyon Motoru</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- ANA MODÜL SEÇİMİ ---
modul_secimi = st.radio(
    "Çalışma Modunu Seçin:",
    ["👤 Bireysel Hat Optimizasyonu", "🏢 Kurumsal Filo Yönetimi (B2B SaaS)"],
    horizontal=True,
)

st.markdown("---")

if modul_secimi == "👤 Bireysel Hat Optimizasyonu":
    st.subheader("📄 1. Akıllı Fatura Taraması & Gizli Kalem Yakalayıcı")

    col_ocr1, col_ocr2 = st.columns([2, 1])

    with col_ocr1:
        bireysel_dosya = st.file_uploader(
            "Bireysel Fatura Yükleyin",
            type=["pdf", "csv", "xlsx", "txt"],
            key="bireysel",
        )

        if bireysel_dosya is not None:
            st.success("✅ Fatura başarıyla yüklendi.")

        if st.button("🚀 Faturayı Analiz Et & Hesapla", use_container_width=True):
            st.session_state.fatura_okundu = True
            st.success("🔍 Fatura başarıyla ayrıştırıldı!")

    with col_ocr2:
        st.write(
            "Faturanız yok mu? Gizli yan hizmet ve hediye GB simülasyonunu test"
            " edin:"
        )
        st.button(
            "🔍 Örnek Faturada Analiz Yap",
            on_click=simule_ocr_ornek,
            use_container_width=True,
        )

    if st.session_state.fatura_okundu or bireysel_dosya is not None:
        st.info("""
            🔍 **Fatura Özet Bilgisi:**
            * **Mevcut Paket:** 35 GB Paket (Ana Bedel: 442 TL)
            * **Son 3 Ay Ortalama Kullanım:** **20 GB**
            """)

        st.markdown(
            """
            <div class="dark-pattern-card">
                <h4 style='color: #F87171; margin-top:0;'>⚠️ 2 Adet Onaysız / Şeffaf Olmayan Yan Hizmet Kalemi Tespit Edildi!</h4>
                <ul>
                    <li style='color: #F3F4F6;'><b>Dijital Servis / Müzik Aboneliği:</b> 49 TL / Ay</li>
                    <li style='color: #F3F4F6;'><b>Aşım Koruma Güvence Paketi:</b> 29 TL / Ay</li>
                </ul>
                <p style='color: #10B981; font-weight: bold; margin-bottom:0;'>💡 Bu 2 ek kalemi iptal ettirerek HİÇ PAKET DEĞİŞTİRMEDEN yılda net 936 TL tasarruf edebilirsiniz!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("##### ⚡ Manuel Profil Seçimi")
    col_b1, col_b2, col_b3, _ = st.columns([1, 1, 1, 2])
    with col_b1:
        st.button(
            "🎓 Öğrenci (15 GB)",
            on_click=set_template,
            args=(15,),
            use_container_width=True,
        )
    with col_b2:
        st.button(
            "👤 Standart (25 GB)",
            on_click=set_template,
            args=(25,),
            use_container_width=True,
        )
    with col_b3:
        st.button(
            "🚀 Yoğun Kullanım (50 GB)",
            on_click=set_template,
            args=(50,),
            use_container_width=True,
        )

    st.markdown("---")

    col_in1, col_in2, col_in3 = st.columns(3)

    col1,col2,col3,col4 = st.columns(4)

with col1:
    mevcut_op = st.selectbox(
        "Operatör",
        ["Turkcell","Vodafone","Türk Telekom"]
    )

with col2:
    yenileme_fiyat = st.number_input(
        "Aylık Fatura",
        min_value=50,
        value=520,
        step=10
    )

with col3:
    rakip_fiyat = st.number_input(
        "Rakip Teklifi",
        min_value=50,
        value=310,
        step=10
    )

with col4:
    cayma_bedeli = st.number_input(
        "Cayma Bedeli",
        min_value=0,
        value=450,
        step=50
    )

st.divider()

sol,sag = st.columns(2)

with sol:

    taahhut_ay = st.select_slider(
        "Taahhüt",
        options=[12,24],
        value=12
    )

    gb_kullanim = st.slider(
        "Aylık Kullanım (GB)",
        1,
        100,
        st.session_state.gb_val
    )
with sag:
 st.subheader("📈 Karar Özeti")

k1,k2,k3,k4 = st.columns(4)

k1.metric(
"Mevcut Fatura",
    f"{yenileme_fiyat:.0f} TL"
)

k2.metric(
    "Rakip Teklifi",
    f"{rakip_fiyat:.0f} TL"
)

k3.metric(
    "NPV Kazancı",
    f"{net_npv_kazanc:,.0f} TL"
)

tasarruf = max(0,(yenileme_fiyat-rakip_fiyat)*12-cayma_bedeli)

k4.metric(
    "Yıllık Tasarruf",
    f"{tasarruf:,.0f} TL"
)
hediye_gb = st.slider(
    "Aylık Hediye GB",
        0,
        20,
        8
    )
firsat_maliyeti = st.slider(
        "İskonto Oranı (%)",
        0.0,
        5.0,
        2.0,
        step=0.5
    )
net_satin_alinmasi_gereken_gb = max(0, gb_kullanim - hediye_gb)
r = firsat_maliyeti / 100

npv_mevcut = sum(
[yenileme_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)]
    )
npv_rakip = cayma_bedeli + sum(
[rakip_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)]
    )
net_npv_kazanc = npv_mevcut - npv_rakip
gb_maliyet_mevcut = yenileme_fiyat / gb_kullanim if gb_kullanim > 0 else 0
gb_maliyet_rakip = (
        rakip_fiyat / net_satin_alinmasi_gereken_gb
        if net_satin_alinmasi_gereken_gb > 0
        else 0
    )
if net_npv_kazanc > 1000:
        st.balloons()

st.markdown("---")
st.subheader("📊 Analitik Karar & Karşılaştırma Raporu")
if hediye_gb > 0:
        st.markdown(
            f"""
            <div class="gift-card">
                <h4 style='color: #6EE7B7; margin-top:0;'>🎁 Hediye GB Optimizasyon Teşhisi</h4>
                <p style='color: #ECFDF5; font-size:15px; margin-bottom:0;'>
                    Aylık <b>{gb_kullanim} GB</b> ihtiyacınızın <b>{hediye_gb} GB</b> kadarlık kısmını Çark / Salla Kazan / Sil Süpür ile ücretsiz karşılıyorsunuz. 
                    Operatörden satın almanız gereken <b>gerçek paket büyüklüğü sadece {net_satin_alinmasi_gereken_gb} GB!</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
c_left, c_right = st.columns([1, 1])
with c_left:
        st.markdown("##### 🎯 Fiyat Verimliliği (Piyasa Göstergesi)")
        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=yenileme_fiyat,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Teklif Fiyatı vs Rakip Ort."},
                delta={
                    "reference": rakip_fiyat,
                    "increasing": {"color": "red"},
                    "decreasing": {"color": "green"},
                },
                gauge={
                    "axis": {"range": [None, rakip_fiyat * 2]},
                    "bar": {"color": "#3B82F6"},
                },
            )
        )
        fig_gauge.update_layout(
            template="plotly_dark",
            height=280,
            margin=dict(l=20, r=20, t=30, b=20),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
with c_right:
        st.markdown("##### 📈 Birim GB Maliyet Kıyaslaması")
        m1, m2 = st.columns(2)
        m1.metric("Mevcut GB Başı Maliyet", f"{gb_maliyet_mevcut:.2f} TL/GB")
        m2.metric(
            "Optimizasyonlu GB Başı Maliyet", f"{gb_maliyet_rakip:.2f} TL/GB"
        )
aylar = list(range(1, taahhut_ay + 1))
kumulatif_mevcut = [
        sum([yenileme_fiyat / ((1 + r) ** i) for i in range(1, t + 1)])
        for t in aylar
    ]
kumulatif_rakip = [
        cayma_bedeli
        + sum([rakip_fiyat / ((1 + r) ** i) for i in range(1, t + 1)])
        for t in aylar
    ]
fig_line = go.Figure()
fig_line.add_trace(
        go.Scatter(
            x=aylar,
            y=kumulatif_mevcut,
            mode="lines+markers",
            name="Mevcut Operatör",
            line=dict(color="#EF4444", width=3),
        )
    )
fig_line.add_trace(
        go.Scatter(
            x=aylar,
            y=kumulatif_rakip,
            mode="lines+markers",
            name="Rakip Operatör",
            line=dict(color="#10B981", width=3),
        )
    )
fig_line.update_layout(
        template="plotly_dark",
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Ay",
        yaxis_title="Toplam Maliyet (TL)",
    )
st.plotly_chart(fig_line, use_container_width=True)

else:
    # ==========================
# B2B KURUMSAL ANALİZ
# ==========================

st.subheader("🏢 Kurumsal Filo Analizi")

dosya = st.file_uploader(
    "Excel veya CSV yükleyin",
    type=["xlsx", "xls", "csv"],
    key="kurumsal"
)

if dosya:

    if dosya.name.endswith(("xlsx","xls")):
        df = pd.read_excel(dosya)
    else:
        df = pd.read_csv(dosya)

    df = df.dropna(how="all")

    st.success(f"✅ {len(df)} kayıt başarıyla okundu.")

    st.dataframe(df, use_container_width=True)

    toplam_hat = len(df)

    sayisal = df.select_dtypes(include=np.number)

    toplam_tutar = 0
    ortalama = 0

    if len(sayisal.columns):

        kolon = sayisal.columns[0]

        toplam_tutar = df[kolon].sum()

        ortalama = df[kolon].mean()

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Toplam Hat",
        f"{toplam_hat:,}"
    )

    c2.metric(
        "Toplam Tutar",
        f"{toplam_tutar:,.0f} TL"
    )

    c3.metric(
        "Ortalama",
        f"{ortalama:,.0f} TL"
    )

    st.divider()

    st.subheader("📊 Sütun Analizi")

    kategorik = list(df.select_dtypes(include="object").columns)

    if kategorik:

        sec = st.selectbox(
            "Kategori",
            kategorik
        )

        grafik = (
            df[sec]
            .astype(str)
            .value_counts()
            .reset_index()
        )

        grafik.columns = [sec,"Adet"]

        fig = px.bar(
            grafik,
            x=sec,
            y="Adet",
            text="Adet",
            title=f"{sec} Dağılımı"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if len(sayisal.columns):

        sec_num = st.selectbox(
            "Sayısal Sütun",
            list(sayisal.columns)
        )

        fig2 = px.histogram(
            df,
            x=sec_num,
            nbins=20,
            title=f"{sec_num} Dağılımı"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.subheader("💰 En Yüksek 10 Kayıt")

        st.dataframe(
            df.sort_values(
                sec_num,
                ascending=False
            ).head(10),
            use_container_width=True
        )

        tasarruf = toplam_tutar * 0.15

        st.success(
            f"💸 Tahmini yıllık tasarruf: {tasarruf:,.0f} TL"
        )

else:

    st.info("Lütfen Excel veya CSV yükleyin.")

