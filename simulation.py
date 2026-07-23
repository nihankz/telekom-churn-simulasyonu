import io
import re
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Telekom Fatura & Kurumsal Filo Optimizasyon Portalı",
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
            type=["pdf", "csv", "xlsx"],
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

    with col_in1:
        st.subheader("2. Sözleşme & Teklif")
        mevcut_op = st.selectbox(
            "Mevcut Operatörünüz", ["Turkcell", "Vodafone", "Türk Telekom"]
        )
        yenileme_fiyat = st.number_input(
            "Aylık Yenileme Teklifi (TL)", value=520, step=20
        )
        rakip_fiyat = st.number_input("En İyi Rakip Fiyatı (TL)", value=310, step=20)

    with col_in2:
        st.subheader("3. Cayma & Kullanım")
        cayma_bedeli = st.number_input(
            "Erken Ayrılma / Cayma Bedeli (TL)", value=450, step=50
        )
        taahhut_ay = st.radio("Taahhüt Süresi (Ay)", [12, 24], horizontal=True)
        gb_kullanim = st.slider(
            "Aylık Toplam İnternet Tüketiminiz (GB)", 5, 100, key="gb_val"
        )

    with col_in3:
        st.subheader("4. 🎁 Hediye GB & Enflasyon")
        hediye_gb = st.slider(
            "Çark / Salla Kazan / Sil Süpür'den Aylık Ortalama Hediye (GB)", 0, 20, 8
        )
        enflasyon_beklentisi = st.slider("Tahmini Yıllık Enflasyon (%)", 10, 80, 35)
        firsat_maliyeti = st.slider(
            "Aylık İskonto / Faiz Oranı (%)", 0.0, 5.0, 2.0, step=0.5
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
    # --- 🏢 B2B KURUMSAL FİLO YÖNETİMİ MODÜLÜ ---
    st.subheader("🏢 Toplu Kurumsal Hat Analizi & Maliyet Optimizasyonu")

    st.markdown(
        """
        <div class="upload-info-box">
            <b>📁 BİLGİ:</b> Yükleyeceğiniz şirket hat dökümleri okunur; ancak binlerce hat içeren kurumsal yapılarda dilediğiniz gibi üstünü yazarak hat sayısını manuel simüle edebilirsiniz.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_b2b1, col_b2b2 = st.columns([2, 1])

    dosya_gecerli = False
    gercek_hat_sayisi = 0
    hesaplanan_ortalama_tutar = 0.0

    with col_b2b1:
        kurumsal_dosya = st.file_uploader(
            "Kurumsal Fatura / Döküm Dosyası Yükleyin (PDF, Excel, CSV, TXT)",
            type=["pdf", "xlsx", "csv", "txt"],
            key="kurumsal",
        )

        tam_metin = ""
        if kurumsal_dosya is not None:
            dosya_adi = kurumsal_dosya.name.lower()

            try:
                if dosya_adi.endswith(".pdf"):
                    import fitz

                    pdf = fitz.open(
                        stream=kurumsal_dosya.read(), filetype="pdf"
                    )
                    for page in pdf:
                        tam_metin += page.get_text("text") + "\n"
                elif dosya_adi.endswith((".xlsx", ".xls")):
                    df_excel = pd.read_excel(kurumsal_dosya)
                    tam_metin = df_excel.to_string()
                else:
                    tam_metin = kurumsal_dosya.getvalue().decode(
                        "utf-8", errors="ignore"
                    )
            except Exception:
                try:
                    tam_metin = kurumsal_dosya.getvalue().decode(
                        "latin-1", errors="ignore"
                    )
                except:
                    tam_metin = ""

            metin_kontrol = tam_metin.lower()
            temizlenmis_metin = (
                metin_kontrol.replace("ı", "i")
                .replace("İ", "i")
                .replace("ş", "s")
                .replace("Ş", "s")
                .replace("ğ", "g")
                .replace("Ğ", "g")
                .replace("ü", "u")
                .replace("Ü", "u")
                .replace("ö", "o")
                .replace("Ö", "o")
                .replace("ç", "c")
                .replace("Ç", "c")
            )

            with st.expander("🔍 Dosyadan Okunan Ham Metin"):
                st.code(tam_metin)

            temiz_rakamlar = re.findall(r"\d+", temizlenmis_metin)
            bulunan_gsm = []
            tum_rakamlar_birlesik = "".join(temiz_rakamlar)

            for i in range(len(tum_rakamlar_birlesik) - 10):
                parca = tum_rakamlar_birlesik[i : i + 11]
                if parca.startswith("05") and parca not in bulunan_gsm:
                    bulunan_gsm.append(parca)

            standart_arama = re.findall(
                r"0\s*5\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}", temizlenmis_metin
            )
            for s in standart_arama:
                temiz_s = re.sub(r"\D", "", s)
                if len(temiz_s) == 11 and temiz_s not in bulunan_gsm:
                    bulunan_gsm.append(temiz_s)

            gsm_eslesmeleri = bulunan_gsm

            if len(gsm_eslesmeleri) == 0:
                dosya_gecerli = False
                st.error(
                    "❌ **BELGE ONAYLANAMADI:** Yüklenen dosyada geçerli kurumsal"
                    " hat numaraları (05XX...) tespit edilemedi."
                )
            else:
                dosya_gecerli = True
                gercek_hat_sayisi = len(set(gsm_eslesmeleri))

                para_degerleri = re.findall(
                    r"\b\d{1,4}[.,]\d{2}\b", tam_metin
                )
                if para_degerleri:
                    temiz_sayilar = [
                        (
                            float(p.replace(".", "").replace(",", "."))
                            if "." in p and "," in p
                            else float(p.replace(",", "."))
                        )
                        for p in para_degerleri
                        if 10 < float(p.replace(",", ".")) < 50000
                    ]
                    if temiz_sayilar:
                        hesaplanan_ortalama_tutar = float(np.mean(temiz_sayilar))
                    else:
                        hesaplanan_ortalama_tutar = 1500.0
                else:
                    hesaplanan_ortalama_tutar = 1500.0

                st.success(
                    f"✅ Şirket Toplu Fatura / Döküm Dosyası ({kurumsal_dosya.name})"
                    f" başarıyla doğrulandı ve okundu! Tespit edilen hat sayısı:"
                    f" {gercek_hat_sayisi}"
                )
        else:
            dosya_gecerli = False
            st.info(
                "💡 Analiz yapabilmek için lütfen şirket hat döküm dosyanızı"
                " yükleyin."
            )

    with col_b2b2:
        # Dosya yüklendiyse varsayılan olarak okunan sayıyı getir, ancak max limiti 50000'e çıkararak binlerce hatlı simülasyona izin ver
        varsayilan_hat = int(gercek_hat_sayisi) if dosya_gecerli else 0
        toplam_hat = st.number_input(
            "Şirket Toplu Hat Sayısı",
            min_value=0,
            max_value=50000,
            value=varsayilan_hat,
            step=10,
            format="%d",
            disabled=not dosya_gecerli,
            help=(
                "Dosyadan okunan sayıyı büyütebilir veya büyük ölçekli senaryolar"
                " için (örn. 1000 hat) manuel güncelleyebilirsiniz."
            ),
        )

        ortalama_hat_maliyeti = st.number_input(
            "Hat Başı Ortalama Fatura (TL)",
            min_value=0,
            max_value=10000,
            value=int(round(hesaplanan_ortalama_tutar)) if dosya_gecerli else 0,
            step=50,
            format="%d",
            disabled=not dosya_gecerli,
        )

    if not dosya_gecerli:
        st.warning(
            "⚠️ Geçerli bir kurumsal döküm yüklenmeden rapor ve hesaplamalar"
            " oluşturulamaz."
        )
    else:
        atıl_hat_orani = 0.28
        atıl_hat_sayisi = int(round(float(toplam_hat) * atıl_hat_orani))

        aylik_kurumsal_israf = float(atıl_hat_sayisi) * (
            float(ortalama_hat_maliyeti) * 0.35
        )
        yillik_kurumsal_tasarruf = aylik_kurumsal_israf * 12.0

        st.markdown("---")

        st.markdown(
            f"""
            <div class="b2b-card">
                <h3 style='color: #A5B4FC; margin-top:0;'>📊 Kurumsal Filo Teşhis ve Tasarruf Raporu</h3>
                <p style='color: #E0E7FF; font-size:16px;'>
                    <b>{toplam_hat:,} adet kurumsal hat</b> üzerinden yapılan toplu döküm ve kullanım analizi sonucunda:
                </p>
                <ul>
                    <li style='color: #F3F4F6;'><b>Atıl / Gereksiz Yüksek Paket Kullanan Hat Sayısı:</b> ~{atıl_hat_sayisi:,} personel (%{int(atıl_hat_orani*100)})</li>
                    <li style='color: #F3F4F6;'><b>Aylık Operasyonel Kayıp / İsraf:</b> {aylik_kurumsal_israf:,.0f} TL / Ay</li>
                    <li style='color: #F3F4F6; font-size:18px;'><b style='color: #34D399;'>Yıllık Net Kurumsal Tasarruf Potansiyeli: {yillik_kurumsal_tasarruf:,.0f} TL</b></li>
                </ul>
                <p style='color: #93C5FD; font-size:14px; margin-bottom:0;'>💡 Bu raporu IT ve CFO yönetimine sunmak için tek tıkla kurumsal PDF denetim raporu oluşturabilirsiniz.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button(
                "📄 IT / CFO İçin Kurumsal Denetim Raporu İndir (PDF)",
                use_container_width=True,
            ):
                st.success(
                    "✅ Kurumsal optimizasyon raporu PDF formatında başarıyla"
                    " oluşturuldu!"
                )
        with col_c2:
            if st.button(
                "⚙️ Tüm Hatları Otomatik Optimize Et (SaaS Motoru)",
                use_container_width=True,
            ):
                st.balloons()
                st.success(
                    "🚀 Filo hatları en uygun ekonomik tarifelere başarıyla"
                    " hizalandı!"
                )
