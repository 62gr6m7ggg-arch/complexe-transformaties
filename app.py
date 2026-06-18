import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURATIE & INITIALISATIE (Altijd bovenaan!) ---
st.set_page_config(page_title="Complexe Transformaties", layout="wide")



st.title("📐 Complexe Transformatie: $w = 1/z$")
st.caption("Voeg vormen toe in de sidebar. Ontwerp en bouw door Edwin van der Plas (Deeltijdstudent 2e graadswiskunde docent aan de HAN.")

if "originals" not in st.session_state:
    st.session_state.originals = [
        np.linspace(1 + 1j*(-10), 1 + 1j*10, 500),
        np.exp(1j * np.linspace(0, 2 * np.pi, 300))
    ]

if "labels" not in st.session_state:
    st.session_state.labels = [
        "Verticale lijn $x=1$",
        "Eenheidscirkel $|z|=1$"
    ]

# --- 2. HULPFUNCTIE VOOR PLOTTEN ---
def plot_complex(ax, curves, title, is_inv=False):
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axhline(0, color='black', lw=0.8, linestyle='--')
    ax.axvline(0, color='black', lw=0.8, linestyle='--')
    ax.grid(True, which='both', linestyle=':', alpha=0.6)
    
    # We gebruiken een vaste kleurenset zodat origineel en beeld exact matchen
    colors = plt.cm.tab10.colors
    
    for i, curve in enumerate(curves):
        color = colors[i % len(colors)]
        z = curve
        if is_inv:
            with np.errstate(divide='ignore', invalid='ignore'):
                w = 1 / z
                # Filter extreem grote waarden eruit voor een stabiele plot
                mask = np.isfinite(w) & (np.abs(w) < 100)
                pts = w[mask]
        else:
            pts = z
            
        if len(pts) > 0:
            ax.plot(pts.real, pts.imag, lw=2.5, color=color)

# --- 3. SIDEBAR: GEBRUIKERSINVOER ---
st.sidebar.header("➕ Voeg een vorm toe")
vlak_type = st.sidebar.radio("Kies type:", ["Lijn", "Cirkel"])

if vlak_type == "Lijn":
    st.sidebar.markdown("**Formule:** $y = ax + b$")
    a = st.sidebar.number_input("Helling (a)", value=1.0, step=0.5)
    b = st.sidebar.number_input("Intercept (b)", value=0.0, step=0.5)
    if st.sidebar.button("➕ Lijn toevoegen"):
        # Ruimer bereik (-10 tot 10) voor mooiere transformaties naar het oneindige
        x = np.linspace(-10, 10, 500)
        y = a * x + b
        z = x + 1j * y
        st.session_state.originals.append(z)
        st.session_state.labels.append(f"Lijn: $y = {a}x + {b}$")

elif vlak_type == "Cirkel":
    st.sidebar.markdown("**Formule:** Middelpunt $(c_x, c_y)$ en straal $r$")
    cx = st.sidebar.number_input("Middelpunt X (cx)", value=0.0, step=0.5)
    cy = st.sidebar.number_input("Middelpunt Y (cy)", value=0.0, step=0.5)
    r = st.sidebar.number_input("Straal (r)", value=1.0, min_value=0.01, step=0.25)
    if st.sidebar.button("➕ Cirkel toevoegen"):
        theta = np.linspace(0, 2 * np.pi, 300)
        z = (cx + r * np.cos(theta)) + 1j * (cy + r * np.sin(theta))
        st.session_state.originals.append(z)
        st.session_state.labels.append(f"Cirkel: MP=({cx}, {cy}), r={r}")

st.sidebar.markdown("---")
st.sidebar.header("🛠️ Beheer & Voorbeelden")

# Standaard voorbeelden
if st.sidebar.button("📌 Laad klassieke voorbeelden"):
    st.session_state.originals = [
        np.linspace(1 + 1j*(-10), 1 + 1j*10, 500),  # verticale lijn x=1
        np.exp(1j * np.linspace(0, 2 * np.pi, 300))  # eenheidscirkel
    ]
    st.session_state.labels = ["Verticale lijn $x=1$", "Eenheidscirkel $|z|=1$"]

# Laatste vorm verwijderen (Undo)
if st.sidebar.button("↩️ Verwijder laatste vorm"):
    if st.session_state.originals:
        st.session_state.originals.pop()
        st.session_state.labels.pop()

# Alles resetten
if st.sidebar.button("🗑️ Reset alles"):
    st.session_state.originals = []
    st.session_state.labels = []

# Toon huidige actieve vormen in de sidebar
if st.session_state.labels:
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Actieve vormen in plot:**")
    for i, label in enumerate(st.session_state.labels):
        st.sidebar.write(f"{i+1}. {label}")

# --- 4. PLOT GEDEELTE ---
if st.session_state.originals:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    plot_complex(ax1, st.session_state.originals, "Origineel (z-vlak)", is_inv=False)
    plot_complex(ax2, st.session_state.originals, "Beeld (w-vlak waar $w = 1/z$)", is_inv=True)
    st.pyplot(fig)
else:
    st.info("De plot is nog leeg. Voeg een vorm toe via de sidebar of klik op 'Laad klassieke voorbeelden'!")

st.markdown("---")
st.caption("💡 **Wiskundig hoogtepuntje:** Let op hoe een rechte lijn die *niet* door de oorsprong gaat (zoals $x=1$) getransformeerd wordt in een perfecte cirkel die *wel* de oorsprong raakt!")
