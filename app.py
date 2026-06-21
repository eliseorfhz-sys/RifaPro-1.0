"""RifaPro-1.0 — aplicación de sorteos justos y transparentes."""

import random
import time
from datetime import datetime

import streamlit as st

from wheel_component import render_wheel

APP_NAME = "RifaPro-1.0"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6C63FF, #FF6584);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header { color: #888; font-size: 1rem; margin-bottom: 2rem; }
    .spin-machine {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        text-align: center;
        box-shadow: inset 0 0 40px rgba(0,0,0,0.4), 0 12px 40px rgba(108,99,255,0.35);
        border: 3px solid #6C63FF;
        max-width: 620px;
        margin: 1.5rem auto;
    }
    .spin-label {
        color: #a78bfa;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .spin-window {
        height: 72px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        background: rgba(0,0,0,0.25);
        border-radius: 12px;
    }
    .spin-window::before, .spin-window::after {
        content: '';
        position: absolute;
        left: 0; right: 0;
        height: 28px;
        z-index: 2;
        pointer-events: none;
    }
    .spin-window::before {
        top: 0;
        background: linear-gradient(to bottom, rgba(26,26,46,0.95), transparent);
    }
    .spin-window::after {
        bottom: 0;
        background: linear-gradient(to top, rgba(26,26,46,0.95), transparent);
    }
    .spin-name {
        font-size: 2rem;
        font-weight: 800;
        color: #fff;
        z-index: 1;
    }
    .spin-blur {
        animation: nameRoll 0.07s linear;
        filter: blur(1.5px);
        color: #c4b5fd;
        transform: perspective(200px) rotateX(25deg);
    }
    .spin-final {
        color: #FFD700 !important;
        filter: none !important;
        transform: scale(1.08);
        text-shadow: 0 0 24px rgba(255,215,0,0.9);
        animation: winnerPulse 0.5s ease;
    }
    @keyframes nameRoll {
        0%   { transform: perspective(200px) rotateX(-40deg) translateY(-18px); opacity: 0.2; }
        100% { transform: perspective(200px) rotateX(0deg) translateY(0); opacity: 1; }
    }
    @keyframes winnerPulse {
        0%   { transform: scale(0.6); opacity: 0; }
        60%  { transform: scale(1.15); }
        100% { transform: scale(1.08); opacity: 1; }
    }
    .winner-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 16px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0.6rem 0;
        box-shadow: 0 8px 32px rgba(102,126,234,0.4);
        animation: slideIn 0.45s ease;
    }
    @keyframes slideIn {
        0%   { transform: translateY(20px) scale(0.9); opacity: 0; }
        100% { transform: translateY(0) scale(1); opacity: 1; }
    }
    .winners-list-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #6C63FF;
        margin: 1.5rem 0 0.5rem 0;
    }
    .winners-panel {
        background: #f8f7ff;
        border: 2px solid #6C63FF;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }
    .winner-item {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.55rem 0;
        border-bottom: 1px solid #e8e5ff;
        font-size: 1.05rem;
    }
    .winner-item:last-child { border-bottom: none; }
    .winner-rank {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-weight: 700;
        width: 32px; height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 0.85rem;
    }
    .cert-box {
        border: 2px dashed #6C63FF;
        border-radius: 12px;
        padding: 1.5rem;
        background: #f8f7ff;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def parse_lines(text: str) -> list[str]:
    return [line.strip() for line in text.strip().splitlines() if line.strip()]


def apply_filters(
    entries: list[str],
    require_hashtag: str = "",
    require_mention: bool = False,
    remove_duplicates: bool = False,
    blocked: list[str] | None = None,
) -> list[str]:
    result = entries[:]
    if require_hashtag:
        tag = require_hashtag if require_hashtag.startswith("#") else f"#{require_hashtag}"
        result = [e for e in result if tag.lower() in e.lower()]
    if require_mention:
        result = [e for e in result if "@" in e]
    if remove_duplicates:
        seen: set[str] = set()
        unique: list[str] = []
        for e in result:
            key = e.lower()
            if key not in seen:
                seen.add(key)
                unique.append(e)
        result = unique
    if blocked:
        blocked_lower = {b.lower() for b in blocked}
        result = [e for e in result if e.split()[0].lower() not in blocked_lower]
    return result


def pick_winners(pool: list[str], count: int) -> list[str]:
    if not pool:
        return []
    count = min(count, len(pool))
    return random.sample(pool, count)


def _spin_html(name: str, label: str, is_final: bool) -> str:
    css_class = "spin-final" if is_final else "spin-blur"
    return f"""
    <div class="spin-machine">
        <div class="spin-label">{label}</div>
        <div class="spin-window">
            <div class="spin-name {css_class}">{name}</div>
        </div>
    </div>
    """


def spin_carousel(
    placeholder,
    pool: list[str],
    winner: str,
    label: str = "Girando...",
    spins: int = 35,
) -> None:
    """Animación de nombres giratorios que desacelera hasta el ganador."""
    if len(pool) <= 1:
        placeholder.markdown(_spin_html(winner, label, is_final=True), unsafe_allow_html=True)
        time.sleep(0.6)
        placeholder.empty()
        return

    sequence: list[str] = []
    for _ in range(spins - 1):
        sequence.append(random.choice(pool))
    sequence.append(winner)

    for i, name in enumerate(sequence):
        is_final = i == len(sequence) - 1
        progress = i / max(len(sequence) - 1, 1)
        delay = 0.025 + (0.28 * progress**2.2)
        placeholder.markdown(_spin_html(name, label, is_final), unsafe_allow_html=True)
        time.sleep(delay)

    time.sleep(0.4)
    placeholder.empty()


def reveal_winners_one_by_one(
    pool: list[str],
    count: int,
    label: str = "🏆 Ganador",
    animate: bool = True,
) -> list[str]:
    """Sortea y revela ganadores uno a uno con animación giratoria."""
    if not pool:
        st.warning("No hay participantes elegibles.")
        return []

    count = min(count, len(pool))
    winners = pick_winners(pool, count)
    remaining = pool[:]
    revealed: list[str] = []

    spin_slot = st.empty()
    results_slot = st.container()

    for i, winner in enumerate(winners):
        spin_pool = [p for p in remaining if p != winner or len(remaining) == 1]
        if not spin_pool:
            spin_pool = [winner]

        position_label = (
            f"🎰 Sorteando ganador {i + 1} de {count}..."
            if count > 1
            else "🎰 Girando nombres..."
        )

        if animate:
            spin_carousel(spin_slot, spin_pool, winner, label=position_label)
        else:
            spin_slot.empty()

        revealed.append(winner)
        remaining = [p for p in remaining if p != winner]

        prefix = f"{label} #{i + 1}" if count > 1 else label
        with results_slot:
            if i == 0 and count > 1:
                st.markdown('<p class="winners-list-title">🏆 Ganadores revelados</p>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="winner-box">{prefix}: {winner}</div>',
                unsafe_allow_html=True,
            )

        if i < count - 1:
            time.sleep(0.8)

    spin_slot.empty()
    return revealed


def show_certificate(winners: list[str], tool: str, total: int, filtered: int):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.markdown('<div class="cert-box">', unsafe_allow_html=True)
    st.markdown("### 📜 Certificado de Sorteo")
    st.markdown(f"**Herramienta:** {tool}")
    st.markdown(f"**Fecha:** {now}")
    st.markdown(f"**Participantes totales:** {total} | **Elegibles:** {filtered}")
    st.markdown("**Ganador(es):**")
    for i, w in enumerate(winners, 1):
        st.markdown(f"{i}. **{w}**")
    st.caption(
        f"Sorteo realizado con {APP_NAME} (algoritmo aleatorio random.sample). Resultado verificable."
    )
    st.markdown("</div>", unsafe_allow_html=True)


def show_winners_list(winners: list[str], title: str = "🏆 Ganadores del sorteo"):
    if not winners:
        return
    items = "".join(
        f'<div class="winner-item">'
        f'<span class="winner-rank">{i}</span>'
        f'<span>{w}</span></div>'
        for i, w in enumerate(winners, 1)
    )
    st.markdown(
        f'<p class="winners-list-title">{title} ({len(winners)})</p>'
        f'<div class="winners-panel">{items}</div>',
        unsafe_allow_html=True,
    )


def init_wheel_state(options: list[str], source_key: str) -> None:
    if st.session_state.get("wheel_source_key") != source_key:
        reset_wheel_state(options, source_key)


def reset_wheel_state(options: list[str], source_key: str) -> None:
    st.session_state.wheel_source_key = source_key
    st.session_state.wheel_remaining = options.copy()
    st.session_state.wheel_winners = []
    st.session_state.pop("wheel_do_spin", None)
    st.session_state.pop("wheel_last_revealed", None)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## 🎁 {APP_NAME}")
    st.divider()
    tool = st.radio(
        "Elige una herramienta",
        [
            "🎯 Ganador aleatorio (nombres)",
            "💬 Sorteo de comentarios",
            "🎡 Ruleta de la fortuna",
            "🔢 Números aleatorios",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    animate = st.checkbox("Animación giratoria", value=True)
    st.divider()
    st.markdown("**Cómo funciona**")
    st.markdown("1. Elige la herramienta\n2. Ingresa participantes\n3. Aplica filtros (opcional)\n4. ¡Sortea!")


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(f'<p class="main-header">{APP_NAME}</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Crea sorteos justos y transparentes — gratis y sin registro</p>',
    unsafe_allow_html=True,
)


# ════════════════════════════════════════════════════════════════════════════
# HERRAMIENTA 1 — Ganador aleatorio (nombres)
# ════════════════════════════════════════════════════════════════════════════
if tool == "🎯 Ganador aleatorio (nombres)":
    st.header("🎯 Ganador aleatorio")
    st.markdown("Pega una lista de nombres (uno por línea) y elige al ganador al azar.")

    col1, col2 = st.columns([2, 1])
    with col1:
        names_text = st.text_area(
            "Lista de participantes",
            placeholder="Juan Pérez\nMaría García\nCarlos López\nAna Martínez",
            height=220,
        )
    with col2:
        num_winners = st.number_input("Número de ganadores", min_value=1, max_value=100, value=1)
        remove_dup = st.checkbox("Eliminar duplicados", value=True)

    names = parse_lines(names_text)

    if st.button("🎲 ¡SORTear!", type="primary", use_container_width=True):
        if not names:
            st.error("Ingresa al menos un participante.")
        else:
            pool = apply_filters(names, remove_duplicates=remove_dup)
            winners = reveal_winners_one_by_one(pool, num_winners, animate=animate)
            if winners:
                show_certificate(winners, "Ganador aleatorio", len(names), len(pool))


# ════════════════════════════════════════════════════════════════════════════
# HERRAMIENTA 2 — Sorteo de comentarios
# ════════════════════════════════════════════════════════════════════════════
elif tool == "💬 Sorteo de comentarios":
    st.header("💬 Sorteo de comentarios")
    st.markdown(
        "Pega los comentarios de tu publicación (uno por línea). "
        "Ideal para sorteos de Instagram, Facebook, TikTok, etc."
    )

    comments_text = st.text_area(
        "Comentarios (uno por línea)",
        placeholder="@usuario1 ¡Quiero ganar! #sorteo\n@usuario2 Me encanta #sorteo\n@usuario3 Tag a @amigo",
        height=200,
    )

    with st.expander("⚙️ Filtros avanzados", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            hashtag = st.text_input("Requerir hashtag", placeholder="#sorteo")
            require_mention = st.checkbox("Requerir mención (@)")
        with fc2:
            remove_dup = st.checkbox("Eliminar comentarios duplicados", value=True)
            num_winners = st.number_input("Número de ganadores", min_value=1, max_value=50, value=1)
        with fc3:
            blocked_text = st.text_area(
                "Usuarios bloqueados (uno por línea)",
                placeholder="spam_user\nbot_account",
                height=80,
            )

    comments = parse_lines(comments_text)
    blocked = parse_lines(blocked_text) if blocked_text else []

    if comments:
        filtered = apply_filters(
            comments,
            require_hashtag=hashtag,
            require_mention=require_mention,
            remove_duplicates=remove_dup,
            blocked=blocked,
        )
        st.info(f"📊 {len(comments)} comentarios → **{len(filtered)} elegibles** tras filtros")

    if st.button("🎲 ¡SORTear comentario!", type="primary", use_container_width=True):
        if not comments:
            st.error("Pega al menos un comentario.")
        else:
            filtered = apply_filters(
                comments,
                require_hashtag=hashtag,
                require_mention=require_mention,
                remove_duplicates=remove_dup,
                blocked=blocked,
            )
            if not filtered:
                st.error("Ningún comentario cumple los filtros. Ajusta las reglas.")
            else:
                winners = reveal_winners_one_by_one(
                    filtered, num_winners, label="💬 Comentario ganador", animate=animate
                )
                if winners:
                    show_certificate(winners, "Sorteo de comentarios", len(comments), len(filtered))


# ════════════════════════════════════════════════════════════════════════════
# HERRAMIENTA 3 — Ruleta de la fortuna
# ════════════════════════════════════════════════════════════════════════════
elif tool == "🎡 Ruleta de la fortuna":
    st.header("🎡 Ruleta de la fortuna")
    st.markdown(
        "Gira la ruleta varias veces. Cada ganador se elimina automáticamente "
        "y los resultados se acumulan en la lista."
    )

    options_text = st.text_area(
        "Opciones de la ruleta (una por línea)",
        placeholder="Premio 1\nPremio 2\nPremio 3\nPremio 4\nPremio 5",
        height=160,
    )
    options = parse_lines(options_text)
    source_key = options_text.strip()
    init_wheel_state(options, source_key)

    remaining: list[str] = st.session_state.wheel_remaining
    winners_so_far: list[str] = st.session_state.wheel_winners
    total_original = len(options)

    cfg1, cfg2, cfg3 = st.columns([1, 1, 1])
    with cfg1:
        num_winners = st.number_input(
            "Número de ganadores",
            min_value=1,
            max_value=max(total_original, 1),
            value=min(1, total_original) if total_original else 1,
        )
    with cfg2:
        st.metric("En la ruleta", len(remaining))
    with cfg3:
        st.metric("Ya sorteados", len(winners_so_far))

    sorteo_completo = len(winners_so_far) >= num_winners

    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col2:
        if st.button("🔄 Reiniciar", use_container_width=True):
            reset_wheel_state(options, source_key)
            st.rerun()

    with btn_col1:
        spin_clicked = st.button(
            "🎡 ¡GIRAR RULETA!",
            type="primary",
            use_container_width=True,
            disabled=sorteo_completo or len(remaining) == 0 or bool(st.session_state.get("wheel_do_spin")),
        )

    # Fase 1: usuario pulsa girar → guardar datos y recargar para animar
    if spin_clicked:
        if len(options) < 2 and len(winners_so_far) == 0:
            st.error("Ingresa al menos 2 opciones.")
        elif len(remaining) == 0:
            st.error("No quedan participantes en la ruleta.")
        else:
            winner_idx = random.randrange(len(remaining))
            st.session_state.wheel_do_spin = {
                "pool": remaining.copy(),
                "winner_idx": winner_idx,
                "winner": remaining[winner_idx],
            }
            st.rerun()

    # Fase 2: mostrar SOLO la animación, luego recargar con el resultado
    if st.session_state.get("wheel_do_spin"):
        spin_data = st.session_state.wheel_do_spin
        render_wheel(spin_data["pool"], winner_index=spin_data["winner_idx"], spin=True)
        time.sleep(5.5)
        st.session_state.wheel_winners = winners_so_far + [spin_data["winner"]]
        st.session_state.wheel_remaining = [
            x for i, x in enumerate(spin_data["pool"]) if i != spin_data["winner_idx"]
        ]
        st.session_state.wheel_last_revealed = spin_data["winner"]
        st.session_state.pop("wheel_do_spin")
        st.rerun()

    # Fase 3: pantalla normal — una sola ruleta estática
    winners_so_far = st.session_state.wheel_winners
    remaining = st.session_state.wheel_remaining
    sorteo_completo = len(winners_so_far) >= num_winners

    if st.session_state.get("wheel_last_revealed"):
        winner = st.session_state.wheel_last_revealed
        st.markdown(
            f'<div class="winner-box">🎡 Ganador #{len(winners_so_far)}: {winner}</div>',
            unsafe_allow_html=True,
        )
        st.session_state.pop("wheel_last_revealed")

    if winners_so_far:
        show_winners_list(winners_so_far)

    if sorteo_completo:
        st.success(f"✅ Sorteo completado — {len(winners_so_far)} ganador(es).")
        show_certificate(winners_so_far, "Ruleta de la fortuna", total_original, total_original)
    elif len(remaining) >= 1:
        if winners_so_far:
            st.markdown(f"**Quedan {len(remaining)} opción(es) en la ruleta** — listo para el siguiente giro:")
        else:
            st.markdown("**Ruleta lista para girar:**")
        render_wheel(remaining, spin=False, height=400 if len(remaining) == 1 else 520)
        if winners_so_far and len(winners_so_far) < num_winners:
            st.caption(
                f"Pulsa **¡GIRAR RULETA!** para elegir al ganador "
                f"#{len(winners_so_far) + 1} de {num_winners}."
            )


# ════════════════════════════════════════════════════════════════════════════
# HERRAMIENTA 4 — Números aleatorios
# ════════════════════════════════════════════════════════════════════════════
elif tool == "🔢 Números aleatorios":
    st.header("🔢 Generador de números aleatorios")
    st.markdown("Genera una secuencia de números aleatorios para sorteos numéricos.")

    nc1, nc2, nc3 = st.columns(3)
    with nc1:
        min_num = st.number_input("Número mínimo", value=1, step=1)
    with nc2:
        max_num = st.number_input("Número máximo", value=100, step=1)
    with nc3:
        count = st.number_input("Cantidad de números", min_value=1, max_value=1000, value=1)

    no_repeat = st.checkbox("Sin repetición", value=True)

    if st.button("🔢 Generar números", type="primary", use_container_width=True):
        if min_num > max_num:
            st.error("El mínimo no puede ser mayor que el máximo.")
        elif no_repeat and count > (max_num - min_num + 1):
            st.error(f"No hay suficientes números únicos en el rango ({max_num - min_num + 1} disponibles).")
        else:
            pool = [str(n) for n in range(int(min_num), int(max_num) + 1)]
            if no_repeat:
                winners = reveal_winners_one_by_one(
                    pool, int(count), label="🔢 Número ganador", animate=animate
                )
                result = [int(w) for w in winners]
            else:
                result = [random.randint(int(min_num), int(max_num)) for _ in range(int(count))]
                for i, n in enumerate(result, 1):
                    st.markdown(
                        f'<div class="winner-box">🔢 Número #{i}: {n}</div>',
                        unsafe_allow_html=True,
                    )

            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            st.markdown(
                f'<div class="cert-box"><b>📜 Certificado — {APP_NAME}</b><br>'
                f"Rango: {min_num}–{max_num} | Sin repetición: {'Sí' if no_repeat else 'No'}<br>"
                f"Números: {', '.join(map(str, sorted(result)))}<br>"
                f"Fecha: {now}</div>",
                unsafe_allow_html=True,
            )
