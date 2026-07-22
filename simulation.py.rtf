{\rtf1\ansi\ansicpg1254\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import numpy as np\
import pandas as pd\
import plotly.graph_objects as go\
\
# --- SAYFA AYARLARI ---\
st.set_page_config(\
    page_title="Telekom Fatura & Kurumsal Filo Optimizasyon Portal\uc0\u305 ", \
    page_icon="\uc0\u55356 \u57314 ", \
    layout="wide"\
)\
\
# --- SESSION STATE ---\
if 'gb_val' not in st.session_state:\
    st.session_state.gb_val = 25\
if 'fatura_okundu' not in st.session_state:\
    st.session_state.fatura_okundu = False\
\
def set_template(gb):\
    st.session_state.gb_val = gb\
\
def simule_ocr_ornek():\
    st.session_state.fatura_okundu = True\
    st.session_state.gb_val = 20\
    st.toast("\uc0\u55357 \u56516  Fatura ve gizli harcama kalemleri ba\u351 ar\u305 yla tarand\u305 !", icon="\u55357 \u56589 ")\
\
# --- \'d6ZEL CSS TASARIMI ---\
st.markdown("""\
    <style>\
    .main \{ background-color: #0e1117; \}\
    .hero-header \{\
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);\
        padding: 24px;\
        border-radius: 12px;\
        border: 1px solid #374151;\
        margin-bottom: 20px;\
    \}\
    .dark-pattern-card \{\
        background-color: #2a1215;\
        border: 1px solid #ef4444;\
        padding: 16px;\
        border-radius: 8px;\
        margin-top: 10px;\
    \}\
    .gift-card \{\
        background-color: #064e3b;\
        border: 1px solid #10b981;\
        padding: 14px;\
        border-radius: 8px;\
        margin-top: 10px;\
    \}\
    .b2b-card \{\
        background-color: #1e1b4b;\
        border: 1px solid #6366f1;\
        padding: 16px;\
        border-radius: 8px;\
        margin-top: 10px;\
    \}\
    </style>\
""", unsafe_allow_html=True)\
\
# --- BA\uc0\u350 LIK BANNER ---\
st.markdown("""\
    <div class="hero-header">\
        <h1 style='color: #F3F4F6; margin:0;'>\uc0\u55356 \u57314  Kurumsal Filo & Bireysel Fatura Optimizasyon Portal\u305 </h1>\
        <p style='color: #9CA3AF; margin-top: 5px; margin-bottom:0;'>AI Destekli Fatura Taramas\uc0\u305 , Gizli Yan Hizmet Dedekt\'f6r\'fc ve B2B Harcama Optimizasyon Motoru</p>\
    </div>\
""", unsafe_allow_html=True)\
\
# --- ANA MOD\'dcL SE\'c7\uc0\u304 M\u304  ---\
modul_secimi = st.radio(\
    "\'c7al\uc0\u305 \u351 ma Modunu Se\'e7in:", \
    ["\uc0\u55357 \u56420  Bireysel Hat Optimizasyonu", "\u55356 \u57314  Kurumsal Filo Y\'f6netimi (B2B SaaS)"], \
    horizontal=True\
)\
\
st.markdown("---")\
\
if modul_secimi == "\uc0\u55357 \u56420  Bireysel Hat Optimizasyonu":\
    st.subheader("\uc0\u55357 \u56516  1. Ak\u305 ll\u305  Fatura Taramas\u305  & Gizli Kalem Yakalay\u305 c\u305 ")\
\
    col_ocr1, col_ocr2 = st.columns([2, 1])\
\
    with col_ocr1:\
        uploaded_file = st.file_uploader("E-Fatura PDF veya G\'f6rselini Y\'fckleyin", type=['pdf', 'png', 'jpg', 'jpeg'])\
        if uploaded_file is not None:\
            st.session_state.fatura_okundu = True\
            st.success("\uc0\u9989  Fatura ba\u351 ar\u305 yla y\'fcklendi ve ayr\u305 \u351 t\u305 r\u305 ld\u305 .")\
\
    with col_ocr2:\
        st.write("Faturan\uc0\u305 z yok mu? Gizli yan hizmet ve hediye GB sim\'fclasyonunu test edin:")\
        st.button("\uc0\u55357 \u56589  \'d6rnek Faturada Analiz Yap", on_click=simule_ocr_ornek, use_container_width=True)\
\
    if st.session_state.fatura_okundu:\
        st.info("""\
        \uc0\u55357 \u56589  **Fatura \'d6zet Bilgisi:**\
        * **Mevcut Paket:** 35 GB Paket (Ana Bedel: 442 TL)\
        * **Son 3 Ay Ortalama Kullan\uc0\u305 m:** **20 GB**\
        """)\
        \
        st.markdown("""\
        <div class="dark-pattern-card">\
            <h4 style='color: #F87171; margin-top:0;'>\uc0\u9888 \u65039  2 Adet Onays\u305 z / \u350 effaf Olmayan Yan Hizmet Kalemi Tespit Edildi!</h4>\
            <ul>\
                <li style='color: #F3F4F6;'><b>Dijital Servis / M\'fczik Aboneli\uc0\u287 i:</b> 49 TL / Ay</li>\
                <li style='color: #F3F4F6;'><b>A\uc0\u351 \u305 m Koruma G\'fcvence Paketi:</b> 29 TL / Ay</li>\
            </ul>\
            <p style='color: #10B981; font-weight: bold; margin-bottom:0;'>\uc0\u55357 \u56481  Bu 2 ek kalemi iptal ettirerek H\u304 \'c7 PAKET DE\u286 \u304 \u350 T\u304 RMEDEN y\u305 lda net 936 TL tasarruf edebilirsiniz!</p>\
        </div>\
        """, unsafe_allow_html=True)\
\
    st.markdown("---")\
\
    st.markdown("##### \uc0\u9889  Manuel Profil Se\'e7imi")\
    col_b1, col_b2, col_b3, _ = st.columns([1, 1, 1, 2])\
    with col_b1:\
        st.button("\uc0\u55356 \u57235  \'d6\u287 renci (15 GB)", on_click=set_template, args=(15,), use_container_width=True)\
    with col_b2:\
        st.button("\uc0\u55357 \u56420  Standart (25 GB)", on_click=set_template, args=(25,), use_container_width=True)\
    with col_b3:\
        st.button("\uc0\u55357 \u56960  Yo\u287 un Kullan\u305 m (50 GB)", on_click=set_template, args=(50,), use_container_width=True)\
\
    st.markdown("---")\
\
    col_in1, col_in2, col_in3 = st.columns(3)\
\
    with col_in1:\
        st.subheader("2. S\'f6zle\uc0\u351 me & Teklif")\
        mevcut_op = st.selectbox("Mevcut Operat\'f6r\'fcn\'fcz", ["Turkcell", "Vodafone", "T\'fcrk Telekom"])\
        yenileme_fiyat = st.number_input("Ayl\uc0\u305 k Yenileme Teklifi (TL)", value=520, step=20)\
        rakip_fiyat = st.number_input("En \uc0\u304 yi Rakip Fiyat\u305  (TL)", value=310, step=20)\
\
    with col_in2:\
        st.subheader("3. Cayma & Kullan\uc0\u305 m")\
        cayma_bedeli = st.number_input("Erken Ayr\uc0\u305 lma / Cayma Bedeli (TL)", value=450, step=50)\
        taahhut_ay = st.radio("Taahh\'fct S\'fcresi (Ay)", [12, 24], horizontal=True)\
        gb_kullanim = st.slider("Ayl\uc0\u305 k Toplam \u304 nternet T\'fcketiminiz (GB)", 5, 100, key="gb_val")\
\
    with col_in3:\
        st.subheader("4. \uc0\u55356 \u57217  Hediye GB & Enflasyon")\
        hediye_gb = st.slider("\'c7ark / Salla Kazan / Sil S\'fcp\'fcr'den Ayl\uc0\u305 k Ortalama Hediye (GB)", 0, 20, 8)\
        enflasyon_beklentisi = st.slider("Tahmini Y\uc0\u305 ll\u305 k Enflasyon (%)", 10, 80, 35)\
        firsat_maliyeti = st.slider("Ayl\uc0\u305 k \u304 skonto / Faiz Oran\u305  (%)", 0.0, 5.0, 2.0, step=0.5)\
\
    net_satin_alinmasi_gereken_gb = max(0, gb_kullanim - hediye_gb)\
\
    r = firsat_maliyeti / 100\
\
    npv_mevcut = sum([yenileme_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)])\
    npv_rakip = cayma_bedeli + sum([rakip_fiyat / ((1 + r) ** t) for t in range(1, taahhut_ay + 1)])\
    net_npv_kazanc = npv_mevcut - npv_rakip\
\
    gb_maliyet_mevcut = yenileme_fiyat / gb_kullanim\
    gb_maliyet_rakip = rakip_fiyat / net_satin_alinmasi_gereken_gb if net_satin_alinmasi_gereken_gb > 0 else 0\
\
    if net_npv_kazanc > 1000:\
        st.balloons()\
\
    st.markdown("---")\
\
    st.subheader("\uc0\u55357 \u56522  Analitik Karar & Kar\u351 \u305 la\u351 t\u305 rma Raporu")\
\
    if hediye_gb > 0:\
        st.markdown(f"""\
        <div class="gift-card">\
            <h4 style='color: #6EE7B7; margin-top:0;'>\uc0\u55356 \u57217  Hediye GB Optimizasyon Te\u351 hisi</h4>\
            <p style='color: #ECFDF5; font-size:15px; margin-bottom:0;'>\
                Ayl\uc0\u305 k <b>\{gb_kullanim\} GB</b> ihtiyac\u305 n\u305 z\u305 n <b>\{hediye_gb\} GB</b> kadarl\u305 k k\u305 sm\u305 n\u305  \'c7ark / Salla Kazan / Sil S\'fcp\'fcr ile \'fccretsiz kar\u351 \u305 l\u305 yorsunuz. \
                Operat\'f6rden sat\uc0\u305 n alman\u305 z gereken <b>ger\'e7ek paket b\'fcy\'fckl\'fc\u287 \'fc sadece \{net_satin_alinmasi_gereken_gb\} GB!</b> \
                Bu sayede bir alt pakete ge\'e7erek faturan\uc0\u305 z\u305  d\'fc\u351 \'fcrebilirsiniz.\
            </p>\
        </div>\
        """, unsafe_allow_html=True)\
\
    st.write("")\
\
    c_left, c_right = st.columns([1, 1])\
\
    with c_left:\
        st.markdown("##### \uc0\u55356 \u57263  Fiyat Verimlili\u287 i (Piyasa G\'f6stergesi)")\
        \
        fig_gauge = go.Figure(go.Indicator(\
            mode = "gauge+number+delta",\
            value = yenileme_fiyat,\
            domain = \{'x': [0, 1], 'y': [0, 1]\},\
            title = \{'text': "Teklif Fiyat\uc0\u305  vs Rakip Ort."\},\
            delta = \{'reference': rakip_fiyat, 'increasing': \{'color': "red"\}, 'decreasing': \{'color': "green"\}\},\
            gauge = \{\
                'axis': \{'range': [None, rakip_fiyat * 2]\},\
                'bar': \{'color': "#3B82F6"\},\
                'steps' : [\
                    \{'range': [0, rakip_fiyat], 'color': "rgba(16, 185, 129, 0.2)"\},\
                    \{'range': [rakip_fiyat, rakip_fiyat * 1.5], 'color': "rgba(245, 158, 11, 0.2)"\},\
                    \{'range': [rakip_fiyat * 1.5, rakip_fiyat * 2], 'color': "rgba(239, 68, 68, 0.2)"\}\
                ],\
            \}\
        ))\
        fig_gauge.update_layout(template="plotly_dark", height=280, margin=dict(l=20, r=20, t=30, b=20))\
        st.plotly_chart(fig_gauge, use_container_width=True)\
\
    with c_right:\
        st.markdown("##### \uc0\u55357 \u56520  Birim GB Maliyet K\u305 yaslamas\u305 ")\
        \
        m1, m2 = st.columns(2)\
        m1.metric("Mevcut GB Ba\uc0\u351 \u305  Maliyet", f"\{gb_maliyet_mevcut:.2f\} TL/GB")\
        m2.metric("Optimizasyonlu GB Ba\uc0\u351 \u305  Maliyet", f"\{gb_maliyet_rakip:.2f\} TL/GB", delta=f"-\{(1 - gb_maliyet_rakip/gb_maliyet_mevcut)*100:.1f\}%" if gb_maliyet_mevcut > 0 else None)\
        \
        st.markdown("---")\
        \
        if net_npv_kazanc > 0:\
            st.success(f"\uc0\u55357 \u56613  **A\u350 IRI TASARRUF FIRSATI:** Cayma bedelini \'f6deyip hediye GB'lar\u305 n\u305 zla optimize edilmi\u351  rakip pakete ge\'e7mek, **\{taahhut_ay\} ayda net \{net_npv_kazanc:,.0f\} TL** cebinizde b\u305 rak\u305 yor!")\
        else:\
            st.info("\uc0\u55357 \u57057 \u65039  **KORUMA:** Cayma bedeli y\'fcksek oldu\u287 u i\'e7in mevcut teklifte kalmak \u351 u an daha rasyonel.")\
\
    st.markdown("##### \uc0\u55357 \u56521  Ay Baz\u305 nda Kumulatif Finansal Y\'fck")\
    aylar = list(range(1, taahhut_ay + 1))\
    kumulatif_mevcut = [sum([yenileme_fiyat / ((1 + r) ** i) for i in range(1, t + 1)]) for t in aylar]\
    kumulatif_rakip = [cayma_bedeli + sum([rakip_fiyat / ((1 + r) ** i) for i in range(1, t + 1)]) for t in aylar]\
\
    fig_line = go.Figure()\
    fig_line.add_trace(go.Scatter(x=aylar, y=kumulatif_mevcut, mode='lines+markers', name='Mevcut Operat\'f6r', line=dict(color='#EF4444', width=3)))\
    fig_line.add_trace(go.Scatter(x=aylar, y=kumulatif_rakip, mode='lines+markers', name='Rakip Operat\'f6r (Cayma Dahil)', line=dict(color='#10B981', width=3)))\
    fig_line.update_layout(template="plotly_dark", height=320, margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Ay", yaxis_title="Toplam Maliyet (TL)")\
\
    st.plotly_chart(fig_line, use_container_width=True)\
\
else:\
    # --- \uc0\u55356 \u57314  B2B KURUMSAL F\u304 LO Y\'d6NET\u304 M\u304  MOD\'dcL\'dc ---\
    st.subheader("\uc0\u55356 \u57314  Toplu Kurumsal Hat Analizi & Maliyet Optimizasyonu")\
    \
    col_b2b1, col_b2b2 = st.columns([2, 1])\
    \
    with col_b2b1:\
        st.file_uploader("\uc0\u350 irket Toplu Fatura / D\'f6k\'fcm Dosyas\u305 n\u305  Y\'fckleyin (Excel / CSV / ZIP PDF)", type=['xlsx', 'csv', 'zip'])\
        st.info("\uc0\u55357 \u56481  Sistem, \u351 irketteki t\'fcm \'e7al\u305 \u351 an hatlar\u305 n\u305 n kullan\u305 m oranlar\u305 n\u305  tarayarak a\u351 \u305 r\u305  faturaland\u305 r\u305 lan veya at\u305 l kalan hatlar\u305  otomatik tespit eder.")\
    \
    with col_b2b2:\
        toplam_hat = st.number_input("\uc0\u350 irket Toplu Hat Say\u305 s\u305 ", value=150, step=10)\
        ortalama_hat_maliyeti = st.number_input("Hat Ba\uc0\u351 \u305  Ortalama Fatura (TL)", value=480, step=20)\
\
    at\uc0\u305 l_hat_orani = 0.28 \
    at\uc0\u305 l_hat_sayisi = int(toplam_hat * at\u305 l_hat_orani)\
    aylik_kurumsal_israf = at\uc0\u305 l_hat_sayisi * (ortalama_hat_maliyeti * 0.35)\
    yillik_kurumsal_tasarruf = aylik_kurumsal_israf * 12\
\
    st.markdown("---")\
    \
    st.markdown(f"""\
    <div class="b2b-card">\
        <h3 style='color: #A5B4FC; margin-top:0;'>\uc0\u55357 \u56522  Kurumsal Filo Te\u351 his ve Tasarruf Raporu</h3>\
        <p style='color: #E0E7FF; font-size:16px;'>\
            <b>\{toplam_hat\} adet kurumsal hat</b> \'fczerinde yap\uc0\u305 lan toplu OCR ve kullan\u305 m analizi sonucunda:\
        </p>\
        <ul>\
            <li style='color: #F3F4F6;'><b>At\uc0\u305 l / Gereksiz Y\'fcksek Paket Kullanan Hat Say\u305 s\u305 :</b> ~\{at\u305 l_hat_sayisi\} personel (%\{int(at\u305 l_hat_orani*100)\})</li>\
            <li style='color: #F3F4F6;'><b>Ayl\uc0\u305 k Operasyonel Kay\u305 p / \u304 sraf:</b> \{aylik_kurumsal_israf:,.0f\} TL / Ay</li>\
            <li style='color: #F3F4F6; font-size:18px;'><b style='color: #34D399;'>Y\uc0\u305 ll\u305 k Net Kurumsal Tasarruf Potansiyeli: \{yillik_kurumsal_tasarruf:,.0f\} TL</b></li>\
        </ul>\
        <p style='color: #93C5FD; font-size:14px; margin-bottom:0;'>\uc0\u55357 \u56481  Bu raporu IT ve CFO y\'f6netimine sunmak i\'e7in tek t\u305 kla kurumsal PDF denetim raporu olu\u351 turabilirsiniz.</p>\
    </div>\
    """, unsafe_allow_html=True)\
    \
    st.write("")\
    \
    col_c1, col_c2 = st.columns(2)\
    with col_c1:\
        if st.button("\uc0\u55357 \u56516  IT / CFO \u304 \'e7in Kurumsal Denetim Raporu \u304 ndir (PDF)", use_container_width=True):\
            st.success("\uc0\u9989  Kurumsal optimizasyon raporu PDF format\u305 nda ba\u351 ar\u305 yla olu\u351 turuldu!")\
    with col_c2:\
        if st.button("\uc0\u9881 \u65039  T\'fcm Hatlar\u305  Otomatik Optimize Et (SaaS Motoru)", use_container_width=True):\
            st.balloons()\
            st.success("\uc0\u55357 \u56960  Filo hatlar\u305  en uygun ekonomik tarifelere ba\u351 ar\u305 yla hizaland\u305 !")}