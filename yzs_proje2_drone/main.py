import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# --- MODÜLLERDEN ÇAĞIRMA (Import) ---
from data.coordinates import coordinates
from core.matrix_utils import get_distance_matrix
from core.ant_algorithm import AntColonyOptimizer

# Sayfa Ayarları
st.set_page_config(page_title="Isparta Drone Rota", layout="wide")

# Oturum Durumu
if 'hesaplama_yapildi' not in st.session_state:
    st.session_state['hesaplama_yapildi'] = False
if 'rota_sonucu' not in st.session_state:
    st.session_state['rota_sonucu'] = None

st.title("🚁 Isparta Drone Rota Optimizasyonu")

# --- Yan Menü ---
st.sidebar.header("Algoritma Parametreleri")

all_locations = list(coordinates.keys())
secilen_yerler = st.sidebar.multiselect(
    "Noktaları Seçiniz (Hepsi Varsayılan):",
    options=all_locations,
    default=all_locations
)

st.sidebar.markdown("---")
n_ants = st.sidebar.slider("Karınca Sayısı (Ants)", 10, 100, 30)
n_iterations = st.sidebar.slider("İterasyon Sayısı", 10, 200, 50)
decay = st.sidebar.slider("Buharlaşma Oranı (Decay)", 0.1, 0.99, 0.95)
alpha = st.sidebar.slider("Feromon Önemi (Alpha)", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Mesafe Önemi (Beta)", 0.1, 5.0, 2.0)

st.sidebar.markdown("---")
btn_start = st.sidebar.button("🚀 Optimizasyonu Başlat")
btn_reset = st.sidebar.button("🔄 Haritayı Temizle")

if btn_start:
    st.session_state['hesaplama_yapildi'] = True
    st.session_state['run_needed'] = True 

if btn_reset:
    st.session_state['hesaplama_yapildi'] = False
    st.session_state['rota_sonucu'] = None

# Merkez Bulma
if len(secilen_yerler) > 0:
    selected_coords = {k: coordinates[k] for k in secilen_yerler}
    avg_lat = sum([v[0] for v in selected_coords.values()]) / len(selected_coords)
    avg_lon = sum([v[1] for v in selected_coords.values()]) / len(selected_coords)
else:
    selected_coords = {}
    avg_lat, avg_lon = 37.76, 30.55

# --- EKRAN AKIŞI ---
if st.session_state['hesaplama_yapildi'] and len(secilen_yerler) >= 3:
    if st.session_state.get('run_needed') or st.session_state['rota_sonucu'] is None:
        with st.spinner("Rota optimize ediliyor..."):
            distance_matrix, city_names = get_distance_matrix(selected_coords)
            
            aco = AntColonyOptimizer(
                distances=distance_matrix, 
                n_ants=n_ants, 
                n_best=int(n_ants/2), 
                n_iterations=n_iterations, 
                decay=decay, 
                alpha=alpha, 
                beta=beta
            )
            
            best_path, history = aco.run()
            
            path_indices = best_path[0]
            total_distance = best_path[1]
            rota_isimleri = [city_names[i] for i, j in path_indices]
            rota_isimleri.append(rota_isimleri[0]) 

            st.session_state['rota_sonucu'] = {
                'total_distance': total_distance,
                'rota_isimleri': rota_isimleri,
                'history': history,
                'selected_coords': selected_coords
            }
            st.session_state['run_needed'] = False

    sonuc = st.session_state['rota_sonucu']
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=11)
    for name, (lat, lon) in sonuc['selected_coords'].items():
        folium.Marker([lat, lon], popup=name, icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
    
    route_coords = [sonuc['selected_coords'][name] for name in sonuc['rota_isimleri']]
    folium.PolyLine(route_coords, color="blue", weight=4, opacity=0.8).add_to(m)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🗺️ Rota Haritası")
        st_folium(m, width=800, height=500)
    with col2:
        st.success(f"✅ Mesafe: {sonuc['total_distance']:.2f} km")
        fig, ax = plt.subplots(figsize=(5,3))
        ax.plot(sonuc['history'])
        ax.set_title("Optimizasyon")
        ax.grid(True)
        st.pyplot(fig)
        st.dataframe(pd.DataFrame(sonuc['rota_isimleri'], columns=["Sıra"]))

else:
    if len(secilen_yerler) < 3:
        st.warning("⚠️ En az 3 nokta seçiniz.")
    else:
        st.info(f"ℹ️ {len(secilen_yerler)} nokta seçili.")
    
    m_init = folium.Map(location=[avg_lat, avg_lon], zoom_start=11)
    for name, (lat, lon) in selected_coords.items():
        folium.CircleMarker([lat, lon], radius=5, color="blue", fill=True, popup=name).add_to(m_init)
    st_folium(m_init, width=1000, height=500)