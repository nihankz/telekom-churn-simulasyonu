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

