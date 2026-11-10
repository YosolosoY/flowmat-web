#!/usr/bin/env python3
"""sitemap.xml del sitio, con las alternativas de idioma (hreflang). Correr tras cambiar páginas:
   python3 generar_sitemap.py   (las guías por condición salen de datos-paginas.json, que deja
   flowmat/scripts/tienda/sitio-paginas-condiciones.ts)."""
import json

B = 'https://flowmat.monsalve.com.co'
HOY = '2026-11-10'
datos = json.load(open('datos-paginas.json'))
pares = [('/', '/en/'), (datos['indices']['es'], datos['indices']['en']), ('/privacidad/', '/en/privacy/'), ('/borrar-cuenta/', '/en/delete-account/')]
pares += [(c['es'], c['en']) for c in datos['condiciones']]

urls = []
for es, en in pares:
    alt = (f'\n    <xhtml:link rel="alternate" hreflang="es" href="{B}{es}"/>'
           f'\n    <xhtml:link rel="alternate" hreflang="en" href="{B}{en}"/>'
           f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{B}{en}"/>')
    for r in (es, en):
        urls.append(f'  <url><loc>{B}{r}</loc><lastmod>{HOY}</lastmod>{alt}</url>')
urls.append(f'  <url><loc>{B}/prensa/</loc><lastmod>{HOY}</lastmod></url>')

open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + '\n'.join(urls) + '\n</urlset>\n')
print(len(urls), 'URL')
