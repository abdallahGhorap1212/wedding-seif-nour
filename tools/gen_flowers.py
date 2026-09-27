# -*- coding: utf-8 -*-
"""باقة ورد ركنية (ورد أبيض + ورق أخضر هادي + ورد الجبس) — بتطلع SVG بإحداثيات 0..400
الركن بتاعها فوق على الشمال (0,0)، والـ CSS بيقلبها لباقي الأركان.
الاستخدام: python3 tools/gen_flowers.py > tools/bouquet.svg
"""
import math, random
R = random.Random(11)
P = []
def a(s): P.append(s)

SAGE, SAGE2, SAGE3 = '#8FA081', '#A9B79C', '#72846A'
STEM = '#9AA88C'
PET = ['#FFFDF9', '#FBF4EA', '#F4E8D8', '#EBDCC7']
EDGE = '#D9C6AA'

def leaf(x, y, rot, L, w, col):
    a('<g transform="translate(%.1f %.1f) rotate(%.1f)">'
      '<path d="M0,0 C%.1f,%.1f %.1f,%.1f %.1f,0 C%.1f,%.1f %.1f,%.1f 0,0Z" fill="%s"/>'
      '<path d="M1,0 L%.1f,0" stroke="%s" stroke-width=".8" opacity=".55"/></g>'
      % (x, y, rot, L*.3, -w, L*.75, -w*.8, L, L*.75, w*.8, L*.3, w, col, L*.85, SAGE3))

def round_leaf(x, y, r, col):
    a('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x, y, r, col))

def stem(pts, w=1.6, col=STEM):
    (x0,y0),(x1,y1),(x2,y2),(x3,y3) = pts
    a('<path d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
      % (x0,y0,x1,y1,x2,y2,x3,y3, col, w))

def bez(pts, t):
    (x0,y0),(x1,y1),(x2,y2),(x3,y3) = pts; m = 1-t
    x = m**3*x0 + 3*m*m*t*x1 + 3*m*t*t*x2 + t**3*x3
    y = m**3*y0 + 3*m*m*t*y1 + 3*m*t*t*y2 + t**3*y3
    dx = 3*m*m*(x1-x0) + 6*m*t*(x2-x1) + 3*t*t*(x3-x2)
    dy = 3*m*m*(y1-y0) + 6*m*t*(y2-y1) + 3*t*t*(y3-y2)
    return x, y, math.degrees(math.atan2(dy, dx))

def pt(cx, cy, r, deg):
    t = math.radians(deg)
    return cx + math.cos(t)*r, cy + math.sin(t)*r

def rose(cx, cy, r, turn=0):
    """وردة مفتوحة: طبقات حوافها متموّجة (كل موجة بتلة) وجوّه كل بتلة خط منحني يدّي عمق"""
    a('<g transform="rotate(%.0f %.1f %.1f)">' % (turn, cx, cy))
    layers = [(.86, 6, 0, '#FFFFFF'), (.72, 6, 30, '#FDF8EF'), (.57, 5, 8, '#F9EFE1'),
              (.42, 5, 44, '#F4E6D2'), (.28, 4, 15, '#EEDCC3')]
    for k, n, off, col in layers:
        pr = r*k; step = 360.0/n
        angs = [off + i*step + R.uniform(-5, 5) for i in range(n)]
        d = 'M%.1f,%.1f' % pt(cx, cy, pr, angs[0])
        for i in range(n):
            a1 = angs[i]; a2 = angs[(i+1) % n] + (360 if i == n-1 else 0)
            qx, qy = pt(cx, cy, pr*1.3, (a1+a2)/2)
            x2, y2 = pt(cx, cy, pr, a2)
            d += ' Q%.1f,%.1f %.1f,%.1f' % (qx, qy, x2, y2)
        a('<path d="%sZ" fill="%s" stroke="%s" stroke-width=".9" stroke-linejoin="round"/>' % (d, col, EDGE))
        for i in range(n):
            m = angs[i] + step/2
            x1, y1 = pt(cx, cy, pr*.86, m - step*.3); x2, y2 = pt(cx, cy, pr*.86, m + step*.3)
            qx, qy = pt(cx, cy, pr*.68, m)
            a('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width=".8" opacity=".75"/>'
              % (x1, y1, qx, qy, x2, y2, EDGE))
    c = r*.15
    a('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#E6CFAE"/>' % (cx, cy, c))
    a('<path d="M%.1f,%.1f a%.1f,%.1f 0 1,1 %.1f,%.1f" fill="none" stroke="#C9AB82" stroke-width="1.1" stroke-linecap="round"/>'
      % (cx - c*.6, cy + c*.2, c*.6, c*.6, c*.9, c*.5))
    a('</g>')

def gypsophila(pts, n):
    """ورد الجبس: فرع رفيع عليه نقط بيضا صغيرة"""
    stem(pts, .9, SAGE2)
    for i in range(n):
        x, y, ang = bez(pts, .35 + .65*i/max(n-1, 1))
        for _ in range(3):
            dx, dy = R.uniform(-9, 9), R.uniform(-9, 9)
            a('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="%s" stroke-width=".6"/>' % (x, y, x+dx, y+dy, SAGE2))
            a('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFFFFF" stroke="%s" stroke-width=".5"/>' % (x+dx, y+dy, R.uniform(2, 3.2), EDGE))

# ── فروع طويلة بورق (ورا كل حاجة) ──
BRANCHES = [
  [(0, 30), (90, 30), (170, 60), (250, 40)],
  [(30, 0), (30, 90), (60, 170), (40, 250)],
  [(0, 110), (70, 120), (120, 160), (150, 220)],
  [(110, 0), (120, 70), (160, 120), (220, 150)],
  [(10, 10), (120, 20), (220, 90), (330, 70)],
  [(10, 10), (20, 120), (90, 220), (70, 330)],
]
for bi, br in enumerate(BRANCHES):
    stem(br, 1.8)
    n = 9 if bi >= 4 else 7
    for i in range(n):
        x, y, ang = bez(br, (i + .7)/n)
        side = 1 if i % 2 else -1
        col = [SAGE, SAGE2, SAGE3][(i + bi) % 3]
        leaf(x, y, ang + side*(50 + R.uniform(-12, 12)), R.uniform(20, 32), R.uniform(6, 9), col)
    x, y, ang = bez(br, 1)
    leaf(x, y, ang, 26, 7, SAGE2)

# ورق دائري (زي الكافور اللي في الصورة)
for pts in ([(40, 60), (110, 70), (180, 110), (230, 180)], [(60, 40), (70, 110), (110, 180), (180, 230)]):
    stem(pts, 1.1, SAGE2)
    for i in range(6):
        x, y, ang = bez(pts, (i + 1)/6.5)
        side = 1 if i % 2 else -1
        round_leaf(x + side*7*math.sin(math.radians(ang)), y - side*7*math.cos(math.radians(ang)), R.uniform(6, 8.5), SAGE2 if i % 2 else SAGE)

# ورد الجبس
gypsophila([(20, 40), (120, 60), (210, 110), (275, 110)], 7)
gypsophila([(40, 20), (60, 120), (110, 210), (110, 275)], 7)
gypsophila([(60, 60), (130, 120), (170, 170), (200, 205)], 5)

# ── الورد نفسه ──
for (x, y, r, t) in [(52, 52, 50, 0), (135, 38, 36, 20), (38, 135, 36, 50),
                     (118, 112, 30, 10), (205, 60, 22, 40), (60, 205, 22, 70)]:
    rose(x, y, r, t)

DEFS = ('<defs><radialGradient id="rg"><stop offset="0" stop-color="#F1E1C8"/>'
        '<stop offset="1" stop-color="#FFFFFF"/></radialGradient></defs>')
print('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">' + DEFS + ''.join(P) + '</svg>')
