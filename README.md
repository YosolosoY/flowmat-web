# flowmat-web

Sitio de FlowMat: flowmat.monsalve.com.co (GitHub Pages). HTML a mano + CSS propio (identidad de la app: Onest y Martian Mono locales, esquinas rectas, naranja solo para «cuidar»).

- `index.html`, `en/index.html`: portada en español e inglés (sin redirección automática).
- `pilates-para/` y `en/pilates-for/`: guías por condición (42 × 2 idiomas + índices). **Se generan** desde el catálogo de la app:
  `cd ~/Projects/flowmat && npx tsx scripts/tienda/sitio-paginas-condiciones.ts ../flowmat-web` (deja también `datos-paginas.json`).
- `condiciones.js`: datos de la demostración «Elige una condición» (`scripts/tienda/sitio-condiciones.ts`). `img/mapa.svg`: `scripts/tienda/sitio-mapa.ts`.
- `prensa/`: kit de prensa; gráfico destacado y capturas de Play salen de `scripts/tienda/grafico.mjs` y `capturas-nuevas.mjs`.
- `generar_sitemap.py`: sitemap con hreflang (correrlo tras cambiar páginas). `auditar_seo.py`: títulos, descripciones, H1, canonical, hreflang, JSON-LD, enlaces y sitemap (debe dar 0 errores).
- Antes de publicar: `python3 generar_sitemap.py && python3 auditar_seo.py`, y Lighthouse (hoy 95–97 rendimiento, 100 en SEO, accesibilidad y buenas prácticas).
