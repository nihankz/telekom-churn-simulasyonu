from io import BytesIO
import io
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate
import streamlit as st

st.set_page_config(page_title="SubOpt", page_icon="📱", layout="wide")

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

st.title("📱 SubOpt")
st.caption("Bireysel ve Kurumsal Telekom Optimizasyon Platformu")

sayfa = st.sidebar.radio("Modül", ["👤 Bireysel", "🏢 Kurumsal"])

# ==========================================================
# BİREYSEL
# ==========================================================

if sayfa == "👤 Bireysel":

    st.header("👤 Bireysel Hat Analizi")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        operator = st.selectbox("Operatör", ["Turkcell", "Vodafone", "Türk Telekom"])

    with c2:
        aylik = st.number_input("Aylık Fatura", 50, 5000, 520)

    with c3:
        rakip = st.number_input("Rakip Teklifi", 50, 5000, 360)

    with c4:
        cayma = st.number_input("Cayma Bedeli", 0, 10000, 500)

    st.divider()

    sol, sag = st.columns(2)

    with sol:
        gb = st.slider("Aylık Kullanım (GB)", 1, 100, 25)
        hediye = st.slider("Hediye GB", 0, 20, 5)

    with sag:
        ay = st.selectbox("Taahhüt", [12, 24])
        iskonto = st.slider("İskonto (%)", 0.0, 10.0, 2.0, 0.5)

    gercek = max(1, gb - hediye)
    r = iskonto / 100

    npv_mevcut = sum(aylik / ((1 + r) ** i) for i in range(1, ay + 1))
    npv_rakip = cayma + sum(rakip / ((1 + r) ** i) for i in range(1, ay + 1))
    kazanc = npv_mevcut - npv_rakip
    tasarruf = max(0, (aylik - rakip) * 12 - cayma)

    st.divider()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Mevcut", f"{aylik:.0f} TL")
    k2.metric("Rakip", f"{rakip:.0f} TL")
    k3.metric("NPV", f"{kazanc:,.0f} TL")
    k4.metric("Yıllık Tasarruf", f"{tasarruf:,.0f} TL")

    if tasarruf > 0:
        st.success(
            f"💰 Operatör değiştirmeniz halinde yaklaşık {tasarruf:,.0f} TL tasarruf edebilirsiniz."
        )
    else:
        st.warning("Mevcut paket ekonomik görünüyor.")

    st.divider()
    st.subheader("📊 Operatör Karşılaştırması")

    karsilastirma = pd.DataFrame({
        "Operatör": ["Turkcell", "Vodafone", "Türk Telekom"],
        "Aylık Ücret (TL)": [
            aylik,
            max(50, aylik * 0.85),
            max(50, aylik * 0.90),
        ],
    })

    karsilastirma["Yıllık Maliyet (TL)"] = (
        karsilastirma["Aylık Ücret (TL)"] * 12
    ).round(0)

    st.dataframe(karsilastirma, use_container_width=True)

    en_iyi = karsilastirma.loc[karsilastirma["Yıllık Maliyet (TL)"].idxmin()]

    st.success(
        f"🏆 En avantajlı seçenek: **{en_iyi['Operatör']}** ({en_iyi['Yıllık Maliyet (TL)']:,.0f} TL / yıl)"
    )

    st.divider()
    st.subheader("🎯 SubOpt Paket Önerisi")
    paketler = pd.DataFrame({
        "Operatör": ["Turkcell", "Vodafone", "Türk Telekom"],
        "Paket": ["Platinum 30 GB", "Red 25 GB", "Prime 30 GB"],
        "GB": [30, 25, 30],
        "Dakika": [3000, 2000, 3000],
        "Aylık Ücret": [439, 379, 395],
    })

    uygun = paketler[(paketler["GB"] >= gb)].copy()
    if uygun.empty:
        uygun = paketler.copy()
    uygun = uygun.sort_values("Aylık Ücret")

    st.dataframe(uygun, use_container_width=True, hide_index=True)

    en_iyi = uygun.iloc[0]
    tasarruf_yil = max(0, (aylik - en_iyi["Aylık Ücret"]) * 12)
    st.success(
        f"""
## 🏆 SubOpt Önerisi

**{en_iyi['Operatör']}**

**{en_iyi['Paket']}**

📦 {en_iyi['GB']} GB

📞 {en_iyi['Dakika']} DK

💰 {en_iyi['Aylık Ücret']} TL / Ay

💸 Tahmini yıllık tasarruf:
**{tasarruf_yil:,.0f} TL**
"""
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Mevcut", "Rakip"], y=[aylik, rakip]))
    fig.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# KURUMSAL
# ==========================================================

else:

    st.header("🏢 Kurumsal Filo Analizi")

    dosya = st.file_uploader("Excel veya CSV yükleyin", type=["xlsx", "xls", "csv"])

    if dosya is not None:

        if dosya.name.endswith(("xlsx", "xls")):
            df = pd.read_excel(dosya)
        else:
            df = pd.read_csv(dosya)

        df = df.dropna(how="all")

        required_columns = {
            "Hat No",
            "Kullanıcı",
            "Departman",
            "Operatör",
        }
        missing = required_columns - set(df.columns)
        if missing:
            st.error(
                f"""
❌ Desteklenmeyen Dosya

Bu uygulama yalnızca kurumsal telekom hat dökümlerini analiz eder.

Eksik sütunlar:{", ".join(sorted(missing))}
"""
            )
            st.stop()

        operators = ["Turkcell", "Vodafone", "Türk Telekom"]

        if "Operatör" in df.columns:
            bulunan = df["Operatör"].astype(str).isin(operators).sum()

            if bulunan == 0:
                st.error(
                    """
❌ Bu dosya telekom hat dökümü olarak doğrulanamadı.
"""
                )
                st.stop()

        st.success(f"✅ {len(df)} kayıt başarıyla okundu.")

        st.divider()
        st.dataframe(df, use_container_width=True)
        st.divider()

        toplam_hat = len(df)
        sayisal = df.select_dtypes(include=np.number)

        toplam_tutar = 0
        ortalama = 0
        kolon = None

        if not sayisal.empty:
            if "Toplam (TL)" in df.columns:
                kolon = "Toplam (TL)"
            elif "Toplam" in df.columns:
                kolon = "Toplam"
            else:
                kolon = st.selectbox("Maliyet Sütunu", sayisal.columns)

            df[kolon] = pd.to_numeric(df[kolon], errors="coerce")

            toplam_tutar = df[kolon].sum()
            ortalama = df[kolon].mean()

        if not sayisal.empty and kolon:
            df["Risk Skoru"] = np.where(
                df[kolon] > ortalama * 1.5,
                "🔴 Yüksek",
                np.where(df[kolon] > ortalama, "🟡 Orta", "🟢 Düşük"),
            )

            def ai_detayli_aciklama(row, ort):
                maliyet = row[kolon]
                if maliyet > ort * 1.5:
                    return (
                        "🔴 Paket gözden geçirilsin.<br><b>Neden?</b><br>• Şirket "
                        f"ortalamasının çok üzerinde maliyet.<br>• Tahmini yıllık "
                        f"kayıp: {(maliyet - ort)*12:,.0f} TL"
                    )
                elif maliyet > ort:
                    return (
                        "🟡 Operatörden yeni teklif alın.<br><b>Neden?</b><br>• Fatura "
                        "ortalamanın üzerinde."
                    )
                else:
                    return (
                        "🟢 Mevcut paket uygun.<br><b>Neden?</b><br>• Maliyet optimum "
                        "seviyede."
                    )

            df["AI Önerisi"] = df.apply(
                lambda row: ai_detayli_aciklama(row, ortalama), axis=1
            )

            limit = ortalama * 1.5
            riskli = df[df[kolon] > limit]
            potansiyel = riskli[kolon].sum() * 0.20
            # Tahmini Fazla Ödeme Hesabı

df["Beklenen Maliyet"] = ortalama

df["Aylık Fazla Ödeme"] = (
    df[kolon] - df["Beklenen Maliyet"]
).clip(lower=0)

df["Yıllık Fazla Ödeme"] = (
    df["Aylık Fazla Ödeme"] * 12
)

toplam_fazla_odeme = df["Yıllık Fazla Ödeme"].sum()

            st.error(
                f"""
# 🚨 Tasarruf Alarmı

SubOpt analizine göre şirketinizde

**{len(riskli)} adet yüksek maliyetli hat** bulundu.

Bu hatlar optimize edilirse

## 💰 Yaklaşık {potansiyel*12:,.0f} TL

yıllık tasarruf sağlanabilir.
"""
            )

        yuksek_risk_orani = (
            len(df[df[kolon] > ortalama * 1.5]) / toplam_hat
            if toplam_hat > 0
            else 0
        )
        saglik_skoru = max(
            0, min(100, int(100 - (yuksek_risk_orani * 100 * 1.2)))
        )

        if saglik_skoru >= 80:
            skor_renk = "🟢 İyi"
        elif saglik_skoru >= 50:
            skor_renk = "🟡 Orta"
        else:
            skor_renk = "🔴 Kritik"

        st.markdown(
            f"""
            <div class="kpi">
                <h3>📊 Telekom Finansal Sağlık Skoru</h3>
                <h1 style="font-size: 48px; margin: 0;">{saglik_skoru} / 100</h1>
                <p style="font-size: 18px; font-weight: bold;">{skor_renk}</p>
                <hr style="border-color: #374151;">
                <p style="font-size: 14px; color: #9ca3af; margin-bottom: 0;">
                    Paket Verimliliği: %{max(0, 100 - int(yuksek_risk_orani*100))} | 
                    Maliyet Verimliliği: %{min(100, int(ortalama*100/toplam_tutar*toplam_hat)) if toplam_tutar > 0 else 0} | 
                    Taahhüt Riski: Düşük
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Toplam Hat", f"{toplam_hat}")
        k2.metric("Toplam Maliyet", f"{toplam_tutar:,.0f} TL")
        k3.metric("Ortalama", f"{ortalama:,.0f} TL")
k4.metric(
    "Tahmini Fazla Ödeme",
    f"{toplam_fazla_odeme:,.0f} TL/yıl"
)
        st.divider()

        col_left, col_right = st.columns(2)

        with col_left:
            if "Operatör" in df.columns:
                operator_df = df["Operatör"].value_counts().reset_index()
                operator_df.columns = ["Operatör", "Hat"]

                fig_operator = px.pie(
                    operator_df,
                    values="Hat",
                    names="Operatör",
                    hole=0.55,
                    title="📡 Operatör Dağılımı",
                )
                st.plotly_chart(fig_operator, use_container_width=True)

        with col_right:
            if "Departman" in df.columns and kolon:
                departman = df.groupby("Departman")[kolon].sum().reset_index()

                fig_departman = px.bar(
                    departman,
                    x="Departman",
                    y=kolon,
                    text_auto=".2f",
                    title="🏢 Departman Bazlı Maliyet",
                )
                st.plotly_chart(fig_departman, use_container_width=True)

        st.divider()
        kategorik = list(df.select_dtypes(include="object").columns)

        if kategorik:
            secim = st.selectbox("Dağılım Grafiği", kategorik)
            grafik = df[secim].astype(str).value_counts().reset_index()
            grafik.columns = [secim, "Adet"]

            fig = px.bar(
                grafik, x=secim, y="Adet", text="Adet", title=f"{secim} Dağılımı"
            )
            st.plotly_chart(fig, use_container_width=True)

        if not sayisal.empty and kolon:
            fig2 = px.histogram(df, x=kolon, nbins=20, title=f"{kolon} Dağılımı")
            st.plotly_chart(fig2, use_container_width=True)

            st.divider()
            st.subheader("🤖 AI Executive Summary")

            en_pahali_departman = (
                df.groupby("Departman")[kolon].sum().sort_values(ascending=False)
            )
            en_pahali_hat = df.sort_values(kolon, ascending=False).iloc[0]

            st.info(
                f"""
### 📊 Yönetici Özeti

📱 Aktif Hat Sayısı: **{toplam_hat}**

💰 Toplam Aylık Telekom Gideri:
**{toplam_tutar:,.2f} TL**

📈 Hat Başına Ortalama:
**{ortalama:,.2f} TL**

🏢 En yüksek maliyetli departman:
**{en_pahali_departman.index[0]}**
(**{en_pahali_departman.iloc[0]:,.2f} TL**)

🔥 En pahalı hat:
**{en_pahali_hat['Hat No']}**
(**{en_pahali_hat[kolon]:,.2f} TL**)

💡 SubOpt önerisi:
En yüksek maliyetli departman ve en pahalı ilk 10 hat öncelikli olarak incelenmelidir.
"""
            )

            st.subheader("🚨 Ortalama Üzeri Maliyetli Hatlar")

            if len(riskli):
                st.warning(
                    f"{len(riskli)} adet hat şirket ortalamasının %50 üzerinde maliyet oluşturuyor."
                )

                st.dataframe(
                    riskli[
                        [
                            "Hat No",
                            "Kullanıcı",
                            "Departman",
                            "Operatör",
                            kolon,
                        ]
                    ],
                    use_container_width=True,
                )

                st.subheader("💸 SubOpt Tasarruf Potansiyeli")
                st.metric("Tahmini Yıllık Tasarruf", f"{potansiyel*12:,.0f} TL")
                st.progress(min(potansiyel / 10000, 1.0))

            else:
                st.success("Riskli maliyet oluşturan hat bulunamadı.")

            st.subheader("💰 En Pahalı 10 Kayıt (AI Önerileri ile)")

            st.dataframe(
                df.sort_values(kolon, ascending=False)[
                    [
                        "Hat No",
                        "Kullanıcı",
                        "Departman",
                        "Operatör",
                        kolon,
                        "Risk Skoru",
                        "AI Önerisi",
                    ]
                ].head(10),
                use_container_width=True,
            )

            # Gelişmiş AI Copilot Modülü
            st.divider()
            st.subheader("🤖 SubOpt Gelişmiş AI Copilot")
            st.caption(
                "Veri setiniz hakkında doğal dille detaylı analiz alın (Örn: 'En yüksek maliyetli departman hangisi?', 'Riskli hat oranı nedir?', 'Operatör dağılımı nasıl?')"
            )

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"], unsafe_allow_html=True)

            copilot_data = {
                "toplam_hat": toplam_hat,
                "toplam_maliyet": toplam_tutar,
                "ortalama": ortalama,
                "saglik_skoru": saglik_skoru,
                "riskli_hat": len(riskli),
                "tasarruf": potansiyel * 12,
                "en_pahali_hat": en_pahali_hat["Hat No"],
                "en_pahali_kullanici": en_pahali_hat.get("Kullanıcı", "Bilinmiyor"),
                "en_pahali_departman": en_pahali_departman.index[0],
                "operatorler": df["Operatör"].value_counts().to_dict(),
            }

            def copilot_answer(question, data):
                q = question.lower()
                if "kaç hat" in q or "hat say" in q:
                    return f"📱 Şirketinizde toplam **{data['toplam_hat']} adet hat** bulunmaktadır."
                elif "toplam maliyet" in q or "fatura" in q or "gider" in q:
                    return f"💰 Toplam aylık telekom maliyeti **{data['toplam_maliyet']:,.2f} TL**."
                elif "ortalama" in q:
                    return f"📊 Hat başına ortalama maliyet **{data['ortalama']:,.2f} TL**."
                elif "en pahalı departman" in q or "departman" in q:
                    return f"🏢 En yüksek maliyetli departman **{data['en_pahali_departman']}**."
                elif "en pahalı kullanıcı" in q or "kullanıcı" in q:
                    return f"👤 En yüksek maliyetli kullanıcı **{data['en_pahali_kullanici']}**."
                elif "risk" in q or "kritik" in q:
                    return f"🚨 Şirketinizde **{data['riskli_hat']} adet** yüksek riskli hat bulunmaktadır."
                elif "tasarruf" in q or "kazanç" in q:
                    return f"💸 Tahmini yıllık tasarruf potansiyeli **{data['tasarruf']:,.0f} TL**."
                elif "skor" in q or "sağlık" in q:
                    return f"📈 Finansal sağlık skorunuz **{data['saglik_skoru']}/100**."
                elif "operatör" in q:
                    return f"📡 Operatör dağılımı: {data['operatorler']}"
                else:
                    return (
                        "Bu konuda elimdeki analiz verileriyle yardımcı olabilirim. "
                        "Örneğin: kaç hat var, en pahalı departman, riskli hatlar, tasarruf potansiyeli."
                    )

            user_prompt = st.chat_input("Veri setine soru sorun...")
            if user_prompt:
                st.session_state.messages.append({"role": "user", "content": user_prompt})
                with st.chat_message("user"):
                    st.markdown(user_prompt)

                response_text = copilot_answer(user_prompt, copilot_data)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                with st.chat_message("assistant"):
                    st.markdown(response_text, unsafe_allow_html=True)

            # PDF Raporu Dışa Aktar
            st.divider()
            st.subheader("📄 Yönetici Raporu Dışa Aktar")

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()

            try:
                font_yolu = None
                if os.name == "nt":
                    if os.path.exists("C:/Windows/Fonts/arial.ttf"):
                        font_yolu = "C:/Windows/Fonts/arial.ttf"
                else:
                    paths = [
                        "/Library/Fonts/Arial.ttf",
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    ]
                    for p_th in paths:
                        if os.path.exists(p_th):
                            font_yolu = p_th
                            break

                if font_yolu:
                    pdfmetrics.registerFont(TTFont("SeciciFont", font_yolu))
                    styles["Heading1"].fontName = "SeciciFont"
                    styles["Heading2"].fontName = "SeciciFont"
                    styles["BodyText"].fontName = "SeciciFont"
            except Exception:
                pass

            story = []
            story.append(Paragraph("<b>SUBOPT TELEKOM OPTİMİZASYON RAPORU</b>", styles["Heading1"]))
            story.append(Paragraph(f"Aktif Hat Sayısı: {toplam_hat}", styles["BodyText"]))
            story.append(Paragraph(f"Toplam Aylık Maliyet: {toplam_tutar:,.2f} TL", styles["BodyText"]))
            story.append(Paragraph(f"Hat Başına Ortalama: {ortalama:,.2f} TL", styles["BodyText"]))
            story.append(Paragraph(f"Finansal Sağlık Skoru: {saglik_skoru}/100", styles["BodyText"]))
            story.append(Paragraph(f"Riskli Hat Sayısı: {len(riskli)}", styles["BodyText"]))
            story.append(Paragraph(f"Tahmini Yıllık Tasarruf: {potansiyel*12:,.0f} TL", styles["BodyText"]))
            story.append(Paragraph("<br/><b>Yönetici Önerileri</b>", styles["Heading2"]))
            story.append(Paragraph("• Riskli hatlar için yeni operatör teklifleri alın.", styles["BodyText"]))
            story.append(Paragraph("• En pahalı departman detaylı incelenmelidir.", styles["BodyText"]))
            story.append(Paragraph("• Ortalama üzerindeki hatlar optimize edilmelidir.", styles["BodyText"]))
            doc.build(story)
            pdf = buffer.getvalue()

            st.download_button(
                label="📄 PDF Yönetici Raporunu İndir",
                data=pdf,
                file_name="SubOpt_Rapor.pdf",
                mime="application/pdf",
            )

    else:
        st.info("📄 Analiz için Excel dosyası yükleyin.")
