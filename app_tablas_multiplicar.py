import random
import re
from pathlib import Path
import streamlit as st

BASES = [Path(__file__).resolve().parent, Path.cwd()]


@st.cache_data
def buscar_audios():
    """Busca todos los mp3 del repositorio y los asocia a su tabla por el nombre."""
    encontrados = {}
    for base in BASES:
        for f in sorted(base.rglob("*.mp3")):
            m = re.search(r"(\d+)", f.stem)
            if m and 1 <= int(m.group(1)) <= 10:
                encontrados.setdefault(int(m.group(1)), f)
    return encontrados

st.set_page_config(page_title="Las tablas mágicas", page_icon="🦄", layout="centered")

st.markdown(
    """
<style>
.stApp{background:linear-gradient(180deg,#fff0f8,#efe9ff);}
h1,h2,h3{color:#a23b9a;}
.big{font-size:2.6rem;text-align:center;font-weight:700;color:#7b3fa0;margin:10px 0;}
.fila{font-size:1.5rem;text-align:center;padding:6px;margin:4px 0;border-radius:12px;background:#ffffffaa;color:#5b2a86;}
div.stButton>button,div.stFormSubmitButton>button{background:#e86fc2;color:white;border-radius:14px;font-size:1.1rem;border:none;}
</style>
""",
    unsafe_allow_html=True,
)

st.title("🦄 Las tablas mágicas ✨🧚")

tab1, tab2, tab3 = st.tabs(["📖 Aprender", "🎯 Practicar", "🧩 Completa"])

# ---------- APRENDER ----------
with tab1:
    t = st.select_slider("Elige la tabla", options=list(range(1, 11)), value=5, key="aprender")
    audios = buscar_audios()
    if t in audios:
        st.markdown("🎧 **Escucha la tabla**")
        st.audio(audios[t].read_bytes(), format="audio/mp3")
    else:
        st.warning(
            f"No encuentro el audio de la tabla del {t}. "
            f"Busco archivos .mp3 en: {BASES[0]} — encontrados: {len(audios)}"
        )
    for i in range(1, 11):
        st.markdown(f'<div class="fila">{t} × {i} = <b>{t*i}</b></div>', unsafe_allow_html=True)
    if t == 1:
        st.info("💡 La tabla del 1: ¡todo número multiplicado por 1 se queda igual!")
    elif t == 5:
        st.info("💡 La tabla del 5: los resultados acaban siempre en 0 o en 5.")
    elif t == 10:
        st.info("💡 La tabla del 10: ¡añade un 0 al número!")

# ---------- PRACTICAR ----------
with tab2:
    tablas = st.multiselect("¿Qué tablas quieres practicar?", list(range(1, 11)), default=[1, 5, 10])
    n = st.slider("Número de preguntas", 5, 20, 10)
    if st.button("¡Empezar! 🚀"):
        if tablas:
            st.session_state.q = [(random.choice(tablas), random.randint(1, 10)) for _ in range(n)]
            st.session_state.i = 0
            st.session_state.ok = 0
            st.session_state.fb = ""
        else:
            st.warning("Elige al menos una tabla 🧚")

    q = st.session_state.get("q")
    if q:
        i = st.session_state.i
        if st.session_state.fb:
            st.write(st.session_state.fb)
        if i < len(q):
            a, b = q[i]
            st.progress(i / len(q))
            st.markdown(f'<div class="big">{a} × {b} = ?</div>', unsafe_allow_html=True)
            with st.form("respuesta", clear_on_submit=True):
                r = st.number_input("Tu respuesta", min_value=0, max_value=100, step=1, value=None)
                enviar = st.form_submit_button("Comprobar ✅")
            if enviar and r is not None:
                if r == a * b:
                    st.session_state.ok += 1
                    st.session_state.fb = f"🌟 ¡Correcto! {a} × {b} = {a*b}"
                else:
                    st.session_state.fb = f"🦄 Casi... {a} × {b} = {a*b}"
                st.session_state.i += 1
                st.rerun()
        else:
            ok = st.session_state.ok
            st.progress(1.0)
            st.markdown(f'<div class="big">{ok} / {len(q)} ✨</div>', unsafe_allow_html=True)
            if ok == len(q):
                st.balloons()
                st.success("¡Perfecto! Eres una maga de las tablas 🧙‍♀️")
            elif ok >= len(q) * 0.7:
                st.success("¡Muy bien! Un poquito más y lo clavas 🦄")
            else:
                st.info("¡Sigue practicando, vas a conseguirlo! 🧚")

# ---------- COMPLETA ----------
with tab3:
    t2 = st.select_slider("Tabla a completar", options=list(range(1, 11)), value=5, key="completa")
    with st.form(f"form_{t2}"):
        resp = {}
        for i in range(1, 11):
            resp[i] = st.number_input(f"{t2} × {i} =", min_value=0, max_value=100, step=1, value=None, key=f"c_{t2}_{i}")
        comprobar = st.form_submit_button("Comprobar tabla ✅")
    if comprobar:
        fallos = [i for i, v in resp.items() if v != t2 * i]
        if not fallos:
            st.balloons()
            st.success("¡Tabla perfecta! 🌈")
        else:
            st.warning("Repasa: " + ", ".join(f"{t2}×{i}" for i in fallos))
