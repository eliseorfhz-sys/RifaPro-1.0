import html
import json

import streamlit.components.v1 as components

WHEEL_COLORS = [
    "#FF6584", "#6C63FF", "#43e97b", "#fa709a",
    "#fee140", "#4facfe", "#f093fb", "#ff9a56",
    "#a18cd1", "#84fab0", "#fbc2eb", "#667eea",
]


def _truncate(text: str, max_len: int = 18) -> str:
    text = text.strip()
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def build_wheel_html(
    options: list[str],
    winner_index: int | None = None,
    spin: bool = False,
) -> str:
    labels = [_truncate(o) for o in options]
    colors = [WHEEL_COLORS[i % len(WHEEL_COLORS)] for i in range(len(options))]
    win_idx = winner_index if winner_index is not None else 0
    spin_flag = "true" if spin else "false"

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: transparent;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px 0;
  }}
  .wheel-wrap {{
    position: relative;
    width: 380px;
    height: 380px;
  }}
  .wheel {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    transform: rotate(0deg);
    filter: drop-shadow(0 8px 24px rgba(0,0,0,0.35));
  }}
  .wheel.spinning {{
    transition: transform 5s cubic-bezier(0.17, 0.67, 0.12, 0.99);
  }}
  .pointer {{
    position: absolute;
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 0; height: 0;
    border-left: 16px solid transparent;
    border-right: 16px solid transparent;
    border-top: 32px solid #FFD700;
    filter: drop-shadow(0 3px 6px rgba(0,0,0,0.4));
    z-index: 10;
  }}
  .hub {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 52px; height: 52px;
    background: radial-gradient(circle, #fff 30%, #ddd 100%);
    border-radius: 50%;
    border: 4px solid #333;
    z-index: 5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }}
  .result {{
    margin-top: 1.2rem;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 14px;
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    opacity: 0;
    transform: scale(0.8);
    transition: opacity 0.5s, transform 0.5s;
    max-width: 420px;
    word-break: break-word;
  }}
  .result.show {{
    opacity: 1;
    transform: scale(1);
  }}
  .legend {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    justify-content: center;
    margin-top: 1rem;
    max-width: 420px;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.78rem;
    color: #555;
    background: #f4f4f8;
    padding: 3px 8px;
    border-radius: 6px;
  }}
  .legend-dot {{
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
</style>
</head>
<body>
<div class="wheel-wrap">
  <div class="pointer"></div>
  <svg id="wheel" class="wheel" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg"></svg>
  <div class="hub"></div>
</div>
<div id="result" class="result"></div>
<div id="legend" class="legend"></div>

<script>
(function() {{
  const options = {json.dumps(labels, ensure_ascii=False)};
  const colors  = {json.dumps(colors)};
  const winIdx  = {win_idx};
  const shouldSpin = {spin_flag};
  const fullLabels = {json.dumps([html.escape(o) for o in options], ensure_ascii=False)};

  const svg = document.getElementById("wheel");
  const cx = 200, cy = 200, r = 185;
  const n = options.length;
  const seg = 360 / n;

  function polar(angleDeg) {{
    const rad = (angleDeg - 90) * Math.PI / 180;
    return {{ x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) }};
  }}

  function segmentPath(i) {{
    const start = i * seg;
    const end = start + seg;
    const p1 = polar(start);
    const p2 = polar(end);
    const large = seg > 180 ? 1 : 0;
    return `M ${{cx}} ${{cy}} L ${{p1.x}} ${{p1.y}} A ${{r}} ${{r}} 0 ${{large}} 1 ${{p2.x}} ${{p2.y}} Z`;
  }}

  options.forEach((label, i) => {{
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", segmentPath(i));
    path.setAttribute("fill", colors[i]);
    path.setAttribute("stroke", "#fff");
    path.setAttribute("stroke-width", "2");
    svg.appendChild(path);

    const mid = i * seg + seg / 2;
    const tr = polar(mid);
    const textR = r * 0.62;
    const rad = (mid - 90) * Math.PI / 180;
    const tx = cx + textR * Math.cos(rad);
    const ty = cy + textR * Math.sin(rad);

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", tx);
    text.setAttribute("y", ty);
    text.setAttribute("fill", "#fff");
    text.setAttribute("font-size", n > 12 ? "9" : n > 8 ? "11" : "13");
    text.setAttribute("font-weight", "700");
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("dominant-baseline", "middle");
    text.setAttribute("transform", `rotate(${{mid}}, ${{tx}}, ${{ty}})`);
    text.textContent = label;
    svg.appendChild(text);
  }});

  const legend = document.getElementById("legend");
  options.forEach((label, i) => {{
    const item = document.createElement("div");
    item.className = "legend-item";
    item.innerHTML = `<span class="legend-dot" style="background:${{colors[i]}}"></span>${{label}}`;
    legend.appendChild(item);
  }});

  if (shouldSpin) {{
    const extraTurns = 5 + Math.floor(Math.random() * 3);
    const finalDeg = 360 * extraTurns - (winIdx + 0.5) * seg;
    requestAnimationFrame(() => {{
      svg.classList.add("spinning");
      svg.style.transform = `rotate(${{finalDeg}}deg)`;
    }});
    setTimeout(() => {{
      const el = document.getElementById("result");
      el.textContent = "🏆 " + fullLabels[winIdx];
      el.classList.add("show");
    }}, 5200);
  }}
}})();
</script>
</body>
</html>
"""


def render_wheel(
    options: list[str],
    winner_index: int | None = None,
    spin: bool = False,
    height: int = 520,
) -> None:
    components.html(
        build_wheel_html(options, winner_index, spin),
        height=height,
        scrolling=False,
    )
