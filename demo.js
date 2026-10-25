// Demostración «Elige una condición»: con datos reales del catálogo (condiciones.js, generado desde la app).
(function () {
  var caja = document.querySelector('[data-demo]');
  if (!caja || !window.FM_CONDICIONES) return;
  var idioma = document.documentElement.lang === 'en' ? 'en' : 'es';
  var T = idioma === 'en'
    ? { de: 'of', nunca: 'never proposed', cuidado: 'with a warning and a gentler option', resto: 'available as usual',
        tituloNunca: 'Never in the class', tituloCuidado: 'In the class, with a warning', marcaNunca: 'Not proposed',
        marcaCuidado: 'Careful', sinNunca: 'No exercise is ruled out for this condition: the care is in how each one is done.',
        dosis: 'Reps and times are also lowered automatically.', ejercicios: 'exercises in the catalog' }
    : { de: 'de', nunca: 'nunca se proponen', cuidado: 'con aviso y opción más suave', resto: 'disponibles como siempre',
        tituloNunca: 'Nunca entran en la clase', tituloCuidado: 'Entran con aviso', marcaNunca: 'No se propone',
        marcaCuidado: 'Con cuidado', sinNunca: 'Ningún ejercicio queda fuera por esta condición: el cuidado está en cómo se hace cada uno.',
        dosis: 'Además, se bajan solas las repeticiones y los tiempos.', ejercicios: 'ejercicios en el catálogo' };
  var lista = caja.querySelector('.demo-elegir');
  var res = caja.querySelector('.demo-resultado');

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function ficha(e, tipo) {
    return '<div class="ej"><div class="dibujo">' + e.svg + '</div><div><span class="marca ' + tipo + '">' +
      (tipo === 'no' ? T.marcaNunca : T.marcaCuidado) + '</span><strong>' + esc(e.nombre[idioma]) + '</strong>' +
      (e.nota ? '<p>' + esc(e.nota[idioma]) + '</p>' : '') + '</div></div>';
  }

  function mostrar(c) {
    var resto = c.total - c.nunca - c.cuidado;
    var html = '<p class="nota" style="margin:0 0 10px">' + esc(c.nombre[idioma]) + ' · ' + c.total + ' ' + T.ejercicios + '</p><div class="demo-cifras">' +
      '<div class="cifra no"><strong>' + c.nunca + '</strong><span>' + T.nunca + '</span></div>' +
      '<div class="cifra aviso"><strong>' + c.cuidado + '</strong><span>' + T.cuidado + '</span></div>' +
      '<div class="cifra ok"><strong>' + resto + '</strong><span>' + T.resto + '</span></div></div>';
    if (c.aviso) html += '<div class="demo-aviso">⚠️ ' + esc(c.aviso[idioma]) + (c.dosis < 1 ? ' ' + T.dosis : '') + '</div>';
    html += '<div class="demo-columnas"><div><h3>' + T.tituloNunca + '</h3>' +
      (c.ejemplosNunca.length ? c.ejemplosNunca.map(function (e) { return ficha(e, 'no'); }).join('') : '<p class="nota">' + T.sinNunca + '</p>') +
      '</div><div><h3>' + T.tituloCuidado + '</h3>' + c.ejemplosCuidado.map(function (e) { return ficha(e, 'aviso'); }).join('') + '</div></div>';
    res.innerHTML = html;
    Array.prototype.forEach.call(lista.children, function (b) { b.setAttribute('aria-pressed', String(b.dataset.codigo === c.codigo)); });
  }

  window.FM_CONDICIONES.forEach(function (c) {
    var b = document.createElement('button');
    b.type = 'button';
    b.dataset.codigo = c.codigo;
    b.textContent = c.corto[idioma];
    b.title = c.nombre[idioma];
    b.addEventListener('click', function () { mostrar(c); });
    lista.appendChild(b);
  });
  mostrar(window.FM_CONDICIONES[0]);
})();
