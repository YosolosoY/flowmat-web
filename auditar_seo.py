#!/usr/bin/env python3
"""Auditoría SEO del sitio: títulos y descripciones (únicos y de buen largo), un solo H1, canonical a sí misma, hreflang
recíproco, JSON-LD válido, imágenes con alt y medidas, enlaces internos que existen y sitemap completo. python3 auditar_seo.py"""
import glob, json, os, re, collections
B = 'https://flowmatapp.com'
pags = [p for p in glob.glob('**/index.html', recursive=True)]
errores = []; avisos = []
def ruta(p): return '/' + p[:-len('index.html')] if p != 'index.html' else '/'
datos = {}
for p in pags:
    s = open(p).read(); r = ruta(p)
    t = re.search(r'<title>(.*?)</title>', s, re.S); t = t.group(1).strip() if t else ''
    d = re.search(r'<meta name="description" content="(.*?)">', s)
    d = d.group(1) if d else ''
    h1 = len(re.findall(r'<h1\b', s))
    can = re.search(r'<link rel="canonical" href="(.*?)">', s)
    datos[r] = dict(t=t, d=d, h1=h1, can=can.group(1) if can else None, s=s)
    if not t: errores.append(f'{r}: sin título')
    elif len(t) > 70: avisos.append(f'{r}: título largo ({len(t)})')
    if not d: errores.append(f'{r}: sin descripción')
    elif len(d) < 70 or len(d) > 175: avisos.append(f'{r}: descripción de {len(d)} caracteres')
    if h1 != 1: errores.append(f'{r}: {h1} H1')
    if not can: errores.append(f'{r}: sin canonical')
    elif can.group(1) != B + r: errores.append(f'{r}: canonical {can.group(1)}')
    for m in re.finditer(r'<img\b([^>]*)>', s):
        a = m.group(1)
        if 'alt=' not in a: errores.append(f'{r}: imagen sin alt')
        if ('width=' not in a or 'height=' not in a) and 'class="dibujo"' not in a and 'mapa.svg' not in a: avisos.append(f'{r}: imagen sin width/height ({re.search(r"src=.([^ ]*)", a).group(1)[:40]})')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j)
        except Exception as e: errores.append(f'{r}: JSON-LD inválido ({e})')
    for h in re.findall(r'href="(/[^"#]*)', s):
        if h.endswith('/') or h == '/':
            if not os.path.exists('.' + h + 'index.html') and h != '/': errores.append(f'{r}: enlace roto {h}')
        elif not os.path.exists('.' + h): errores.append(f'{r}: enlace roto {h}')
# duplicados
for campo, nombre in (('t', 'título'), ('d', 'descripción')):
    c = collections.Counter(v[campo] for k, v in datos.items() if v[campo])
    for v, n in c.items():
        if n > 1: errores.append(f'{nombre} repetido {n} veces: {v[:70]}')
# hreflang recíproco
for r, v in datos.items():
    hs = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', v['s']))
    for l, u in hs.items():
        if l == 'x-default': continue
        dest = datos.get(u.replace(B, ''))
        if not dest: errores.append(f'{r}: hreflang a página inexistente {u}'); continue
        back = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', dest['s']))
        if not any(x == B + r for x in back.values()): errores.append(f'{r}: {u} no devuelve el hreflang')
# sitemap
sm = set(re.findall(r'<loc>(.*?)</loc>', open('sitemap.xml').read()))
for r in datos:
    if B + r not in sm: avisos.append(f'{r}: no está en el sitemap')
for u in sm:
    if u.replace(B, '') not in datos and not u.endswith('prensa/'): errores.append(f'sitemap apunta a {u}')
print(len(pags), 'páginas;', len(sm), 'URL en el sitemap')
for e in errores: print('ERROR', e)
for a in avisos[:40]: print('aviso', a)
print(len(errores), 'errores,', len(avisos), 'avisos')
