"""Generate fig-additions.tex: staggered additions for 1/49 (forward) and 1/19 (backward).

Run: python3 make_fig.py   (writes fig-additions.tex next to this script)
"""
import os
W = 0.34   # cell width (cm)
H = 0.46   # row height (cm)
BASE = 0.10  # digits and labels share a baseline this far below the row centre
out = []
def cell(x, y, d, over):
    style = "ovf" if over else "dig"
    out.append(f"\\node[{style}] at ({x:.3f},{-y - BASE:.3f}) {{{d}}};")

# ---------- forward 1/49: term k = 2^(k+1) ends at decimal position 2(k+1)
out.append("\\begin{scope}")
K = 8
for k in range(K):
    v = str(2 ** (k + 1)).zfill(2)
    end = 2 * (k + 1)
    start = end - len(v) + 1
    for i, d in enumerate(v):
        pos = start + i
        cell(pos * W, (k + 1) * H, d, pos < 2 * k + 1)
    # light bracket under own block
    out.append(f"\\draw[blk] ({(2*k+1)*W - W/2:.3f},{-(k+1)*H - 0.21:.3f}) -- ({(2*k+2)*W + W/2:.3f},{-(k+1)*H - 0.21:.3f});")
    out.append(f"\\node[lab] at ({-0.55:.3f},{-(k+1)*H - BASE:.3f}) {{$2^{{{k+1}}}$}};")
true49 = "02040816326530"
ROWS = K + 1
ysum = ROWS * H + 0.25
out.append(f"\\draw ({0.5*W:.3f},{-(ROWS*H - 0.12):.3f}) -- ({(len(true49)+0.5)*W:.3f},{-(ROWS*H - 0.12):.3f});")
out.append(f"\\node[dig, anchor=base east] at ({0.5*W:.3f},{-ysum - BASE:.3f}) {{0.}};")
for i, d in enumerate(true49):
    cell((i + 1) * W, ysum, d, False)
out.append(f"\\node[dig, anchor=base west] at ({(len(true49)+0.5)*W:.3f},{-ysum - BASE:.3f}) {{\\dots}};")
out.append(f"\\node[ttl] at ({8.5*W:.3f},{0.75:.3f}) {{$1/49$: forward, blocks of 2 digits}};")
out.append("\\end{scope}")

# ---------- backward 1/19: term k = 2^k, last digit at column k from the right
X0 = 10.0  # right edge (cm) of the second panel
out.append("\\begin{scope}")
K2 = 9
for k in range(K2):
    v = str(2 ** k)
    for j, d in enumerate(reversed(v)):
        col = k + j
        cell(X0 - col * W, k * H, d, col > k)
    out.append(f"\\node[lab] at ({X0 + 0.6:.3f},{-k*H - BASE:.3f}) {{$2^{{{k}}}$}};")
true19 = "947368421"
ysum2 = K2 * H + 0.25
out.append(f"\\draw ({X0 - (len(true19)+1)*W + W/2:.3f},{-(K2*H - 0.12):.3f}) -- ({X0 + W/2:.3f},{-(K2*H - 0.12):.3f});")
for j, d in enumerate(reversed(true19)):
    cell(X0 - j * W, ysum2, d, False)
out.append(f"\\node[dig, anchor=base east] at ({X0 - (len(true19)-0.5)*W:.3f},{-ysum2 - BASE:.3f}) {{\\dots}};")
out.append(f"\\node[ttl] at ({X0 - 5*W:.3f},{0.75:.3f}) {{$1/19$: backward, 1 digit}};")
out.append("\\end{scope}")

hdr = r"""\begin{tikzpicture}[
  dig/.style={font=\ttfamily\small, inner sep=0pt, minimum width=3.2mm, anchor=base},
  ovf/.style={dig, text=ovfcol, font=\ttfamily\small\bfseries},
  lab/.style={font=\scriptsize, text=gray, anchor=base},
  ttl/.style={font=\small},
  blk/.style={gray!60, line width=0.4pt}]
"""
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig-additions.tex"), "w").write(hdr + "\n".join(out) + "\n\\end{tikzpicture}\n")
# sanity: partial sums match shown digits
from fractions import Fraction
s = sum(Fraction(2 ** (k + 1), 100 ** (k + 1)) for k in range(K))
print("fwd partial", str(int(s * 10**14)).zfill(14), "shown", true49)
s2 = sum(2 ** k * 10 ** k for k in range(K2))
print("bwd partial", str(s2)[-9:], "shown", true19, "period end", str((10**18 - 1)//19)[-9:])
