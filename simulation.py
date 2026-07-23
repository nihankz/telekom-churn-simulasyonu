import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="SubOpt",
    page_icon="📱",
    layout="wide"
)

st.markdown("""
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
""",unsafe_allow_html=True)

st.title("📱 SubOpt")
st.caption("Bireysel ve Kurumsal Telekom Optimizasyon Platformu")

sayfa=st.sidebar.radio(
    "Modül",
    [
        "👤 Bireysel",
        "🏢 Kurumsal"
    ]
)

# ==========================================================
# BİREYSEL
# ==========================================================

if sayfa=="👤 Bireysel":

    st.header("👤 Bireysel Hat Analizi")

    c1,c2,c3,c4=st.columns(4)

    with c1:
        operator=st.selectbox(
            "Operatör",
            [
                "Turkcell",
                "Vodafone",
                "Türk Telekom"
            ]
        )

    with c2:
        aylik=st.number_input(
            "Aylık Fatura",
            50,
            5000,
            520
        )

    with c3:
        rakip=st.number_input(
            "Rakip Teklifi",
            50,
            5000,
            360
        )

    with c4:
        cayma=st.number_input(
            "Cayma Bedeli",
            0,
            10000,
            500
        )

    st.divider()

    sol,sag=st.columns(2)

    with sol:

        gb=st.slider(
            "Aylık Kullanım (GB)",
            1,
            100,
            25
        )

        hediye=st.slider(
            "Hediye GB",
            0,
            20,
            5
        )

    with sag:

        ay=st.selectbox(
            "Taahhüt",
            [12,24]
        )

        iskonto=st.slider(
            "İskonto (%)",
            0.0,
            10.0,
            2.0,
            0.5
        )

    gercek=max(1,gb-hediye)

    r=iskonto/100

    npv_mevcut=sum(
        aylik/((1+r)**i)
        for i in range(1,ay+1)
    )

    npv_rakip=cayma+sum(
        rakip/((1+r)**i)
        for i in range(1,ay+1)
    )

    kazanc=npv_mevcut-npv_rakip

    tasarruf=max(
        0,
        (aylik-rakip)*12-cayma
    )

    st.divider()

    k1,k2,k3,k4=st.columns(4)

    k1.metric(
        "Mevcut",
        f"{aylik:.0f} TL"
    )

    k2.metric(
        "Rakip",
        f"{rakip:.0f} TL"
    )

    k3.metric(
        "NPV",
        f"{kazanc:,.0f} TL"
    )

    k4.metric(
        "Yıllık Tasarruf",
        f"{tasarruf:,.0f} TL"
    )

    if tasarruf>0:

        st.success(
            f"💰 Operatör değiştirmeniz halinde yaklaşık {tasarruf:,.0f} TL tasarruf edebilirsiniz."
        )

    else:

        st.warning(
            "Mevcut paket ekonomik görünüyor."
        )

    fig=go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Mevcut","Rakip"],
            y=[aylik,rakip]
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # ==========================================================
# KURUMSAL
# ==========================================================

else:

    st.header("🏢 Kurumsal Filo Analizi")

    dosya = st.file_uploader(
        "Excel veya CSV yükleyin",
        type=["xlsx", "xls", "csv"]
    )

    if dosya is not None:

        if dosya.name.endswith(("xlsx", "xls")):
            df = pd.read_excel(dosya)
        else:
            df = pd.read_csv(dosya)

        df = df.dropna(how="all")

        st.success(f"✅ {len(df)} kayıt başarıyla okundu.")

        st.divider()

        st.dataframe(df, use_container_width=True)

        st.divider()

        toplam_hat = len(df)

        sayisal = df.select_dtypes(include=np.number)

        toplam_tutar = 0
        ortalama = 0

        if not sayisal.empty:

            # Toplam (TL) sütununu otomatik bul
    if "Toplam (TL)" in df.columns:
    kolon = "Toplam (TL)"
    elif "Toplam" in df.columns:
    kolon = "Toplam"
    else:
    kolon = st.selectbox(
        "Maliyet Sütunu",
        sayisal.columns
    )

# Sayıya çevir
df[kolon] = (
    df[kolon]
    .astype(str)
    .str.replace("TL", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)

df[kolon] = pd.to_numeric(
    df[kolon],
    errors="coerce"
)

toplam_tutar = df[kolon].sum()
ortalama = df[kolon].mean()

        k1, k2, k3 = st.columns(3)

        k1.metric(
            "Toplam Hat",
            f"{toplam_hat}"
        )

        k2.metric(
            "Toplam Maliyet",
            f"{toplam_tutar:,.0f} TL"
        )

        k3.metric(
            "Ortalama",
            f"{ortalama:,.0f} TL"
        )

        st.divider()

        kategorik = list(
            df.select_dtypes(include="object").columns
        )

        if kategorik:

            secim = st.selectbox(
                "Dağılım Grafiği",
                kategorik
            )

            grafik = (
                df[secim]
                .astype(str)
                .value_counts()
                .reset_index()
            )

            grafik.columns = [secim, "Adet"]

            fig = px.bar(
                grafik,
                x=secim,
                y="Adet",
                text="Adet",
                title=f"{secim} Dağılımı"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if not sayisal.empty:

            fig2 = px.histogram(
                df,
                x=kolon,
                nbins=20,
                title=f"{kolon} Dağılımı"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            st.subheader("💰 En Pahalı 10 Kayıt")

            st.dataframe(
                df.sort_values(
                    kolon,
                    ascending=False
                ).head(10),
                use_container_width=True
            )

            tasarruf = toplam_tutar * 0.15

            st.success(
                f"💸 Tahmini yıllık tasarruf: {tasarruf:,.0f} TL"
            )

    else:

        st.info("📄 Analiz için Excel dosyası yükleyin.")

