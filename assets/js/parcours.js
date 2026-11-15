/* =====================================================================
   LIGHT ON BIKE - carte et profil altimétrique des parcours
   Données : assets/data/routes.js (générées par tools/build_routes.py à
   partir des tracés OpenRunner). Carte : Leaflet + fond OpenStreetMap.
   Le profil est dessiné à la largeur de l'écran ; survoler ou toucher le
   profil déplace un repère sur la carte.
   ===================================================================== */
(function () {
  'use strict';
  var R = window.LOB_ROUTES;
  if (!R) return;

  function decode(str) {
    var out = [], i = 0, lat = 0, lng = 0;
    while (i < str.length) {
      for (var k = 0; k < 2; k++) {
        var shift = 0, res = 0, b;
        do { b = str.charCodeAt(i++) - 63; res |= (b & 31) << shift; shift += 5; } while (b >= 32);
        var d = (res & 1) ? ~(res >> 1) : (res >> 1);
        if (k === 0) lat += d; else lng += d;
      }
      out.push([lat / 1e5, lng / 1e5]);
    }
    return out;
  }
  function hav(a, b) {
    var r = Math.PI / 180, p1 = a[0] * r, p2 = b[0] * r, dl = (b[1] - a[1]) * r;
    var h = Math.pow(Math.sin((p2 - p1) / 2), 2) + Math.cos(p1) * Math.cos(p2) * Math.pow(Math.sin(dl / 2), 2);
    return 12742000 * Math.asin(Math.sqrt(h));
  }
  function frNum(n, d) { return n.toFixed(d).replace('.', ','); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

  document.querySelectorAll('[data-route]').forEach(function (root) {
    var r = R[root.getAttribute('data-route')];
    if (!r) return;
    var pts = decode(r.line), cum = [0];
    for (var i = 1; i < pts.length; i++) cum.push(cum[i - 1] + hav(pts[i - 1], pts[i]));
    var totalKm = cum[cum.length - 1] / 1000;
    var el = r.el, stepKm = r.step / 1000;

    function pointAt(km) {
      var d = km * 1000, lo = 0, hi = cum.length - 1;
      while (lo < hi) { var m = (lo + hi) >> 1; if (cum[m] < d) lo = m + 1; else hi = m; }
      return pts[lo];
    }
    function altAt(km) {
      var x = Math.min(Math.max(km / stepKm, 0), el.length - 1), a = Math.floor(x), b = Math.min(a + 1, el.length - 1);
      return el[a] + (el[b] - el[a]) * (x - a);
    }

    /* ---------- Carte ---------- */
    var mapEl = root.querySelector('.rm-map'), map = null, cursor = null;
    if (mapEl && window.L) {
      mapEl.innerHTML = '';
      map = L.map(mapEl, { scrollWheelZoom: true, wheelPxPerZoomLevel: 120, minZoom: 8, zoomSnap: 0.25 });   // la molette zoome dès que le pointeur est sur la carte
      // Trois fonds de carte au choix, de gauche à droite : sombre (par défaut), plan, satellite
      var osm = '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>';
      var bases = [
        { id: 'sombre', label: 'Sombre', layer: L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 17, attribution: osm }) },
        { id: 'plan', label: 'Plan', layer: L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 17, attribution: osm }) },
        { id: 'satellite', label: 'Satellite', layer: L.tileLayer('https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&STYLE=normal&FORMAT=image/jpeg&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}', { maxZoom: 17, attribution: '&copy; <a href="https://www.ign.fr/" target="_blank" rel="noopener">IGN</a>' }) }
      ];
      var current = null, buttons = [];
      var setBase = function (id, remember) {
        var next = bases.filter(function (x) { return x.id === id; })[0] || bases[0];
        if (current) map.removeLayer(current.layer);
        current = next; next.layer.addTo(map); next.layer.bringToBack();
        mapEl.setAttribute('data-fond', next.id);
        buttons.forEach(function (btn) { btn.setAttribute('aria-pressed', btn.getAttribute('data-fond') === next.id ? 'true' : 'false'); });
        if (remember) { try { localStorage.setItem('lob-fond', next.id); } catch (e) {} }
      };
      var Switch = L.Control.extend({
        options: { position: 'topright' },
        onAdd: function () {
          var box = L.DomUtil.create('div', 'rm-fonds');
          box.setAttribute('role', 'group'); box.setAttribute('aria-label', 'Fond de carte');
          bases.forEach(function (x) {
            var btn = L.DomUtil.create('button', '', box);
            btn.type = 'button'; btn.textContent = x.label; btn.setAttribute('data-fond', x.id);
            L.DomEvent.on(btn, 'click', function (e) { L.DomEvent.stop(e); setBase(x.id, true); });
            buttons.push(btn);
          });
          L.DomEvent.disableClickPropagation(box);
          return box;
        }
      });
      map.addControl(new Switch());
      var saved = null; try { saved = localStorage.getItem('lob-fond'); } catch (e) {}
      setBase(saved || 'sombre', false);
      // Tracé : orange de marque bordé d'un fin liseré blanc, lisible sur les trois fonds
      var round = { lineJoin: 'round', lineCap: 'round', interactive: false };
      L.polyline(pts, L.extend({ color: '#fff', weight: 7.5 }, round)).addTo(map);
      var line = L.polyline(pts, L.extend({ color: '#ed5f3e', weight: 4.5 }, round)).addTo(map);
      map.fitBounds(line.getBounds(), { padding: [28, 28] });
      var pin = function (ll, label, cls, tip) {
        L.marker(ll, { icon: L.divIcon({ className: '', html: '<span class="rm-pin ' + cls + '">' + label + '</span>', iconSize: [24, 24], iconAnchor: [12, 12] }), keyboard: false })
          .addTo(map).bindTooltip(tip, { className: 'rm-tip', direction: 'top', offset: [0, -12] });
      };
      r.cols.forEach(function (c, n) { pin(c.ll, n + 1, '', esc(c.n) + ' · ' + c.alt + ' m · km ' + frNum(c.km, 1)); });
      if (hav(pts[0], pts[pts.length - 1]) < 150) {
        pin(pts[0], 'D', 'se', 'Départ et arrivée');   // boucle : un seul repère
      } else {
        pin(pts[pts.length - 1], 'A', 'se', 'Arrivée');
        pin(pts[0], 'D', 'se', 'Départ');
      }
      cursor = L.circleMarker(pts[0], { radius: 7, color: '#ed5f3e', weight: 3, fillColor: '#fff', fillOpacity: 1, opacity: 0, interactive: false }).addTo(map);
      cursor.setStyle({ fillOpacity: 0 });
    }

    /* ---------- Profil ---------- */
    var profEl = root.querySelector('.rm-profile'), readEl = root.querySelector('.rm-read');
    if (!profEl) return;
    var readDefault = readEl ? readEl.innerHTML : '';
    var geom = null;

    function draw() {
      var W = Math.max(280, Math.round(profEl.clientWidth)), small = W < 620;
      var H = small ? 190 : Math.min(300, Math.round(W * 0.24));
      var mL = small ? 34 : 46, mR = 8, mT = small ? 30 : 66, mB = 24;
      var lo = Math.floor(Math.min.apply(null, el) / 100) * 100, hi = Math.ceil((Math.max.apply(null, el) + 20) / 100) * 100;
      var X = function (km) { return mL + (km / totalKm) * (W - mL - mR); };
      var Y = function (a) { return mT + (1 - (a - lo) / (hi - lo)) * (H - mT - mB); };
      var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="Profil altimétrique du parcours">';
      var gStep = (hi - lo) > 500 ? 200 : 100;
      for (var a = lo; a <= hi; a += gStep) {
        s += '<line class="p-grid" x1="' + mL + '" x2="' + (W - mR) + '" y1="' + Y(a) + '" y2="' + Y(a) + '"/>' +
             '<text class="p-axis" x="' + (mL - 6) + '" y="' + (Y(a) + 4) + '" text-anchor="end">' + a + '</text>';
      }
      var kStep = totalKm > 100 ? (small ? 40 : 20) : (small ? 20 : 10);
      for (var k = 0; k <= totalKm; k += kStep) {
        s += '<text class="p-axis" x="' + X(k) + '" y="' + (H - 6) + '" text-anchor="' + (k === 0 ? 'start' : 'middle') + '">' + (k === 0 ? '0 km' : k) + '</text>';
      }
      var d = '', n = el.length;
      for (var j = 0; j < n; j++) d += (j ? 'L' : 'M') + X(Math.min(j * stepKm, totalKm)).toFixed(1) + ' ' + Y(el[j]).toFixed(1);
      s += '<path class="p-area" d="' + d + 'L' + X(totalKm).toFixed(1) + ' ' + Y(lo) + 'L' + X(0) + ' ' + Y(lo) + 'Z"/><path class="p-line" d="' + d + '"/>';
      var rowEnd = [-1e9, -1e9];   // fin du dernier libellé sur chaque ligne (les noms voisins passent sur deux lignes)
      r.cols.forEach(function (c, idx) {
        var x = X(c.km), y = Y(altAt(c.km));
        var label = c.n.replace(/^Col (de la |des |du |de )/, '') + ' ' + c.alt + ' m';
        var w = label.length * 7.2 + 22, row = 0, shown = !small;
        if (shown) {
          if (x - 12 < rowEnd[0]) row = 1;
          if (row === 1 && x - 12 < rowEnd[1]) shown = false;
          if (shown && x + w > W) shown = false;
          if (shown) rowEnd[row] = x + w;
        }
        var by = mT - 26 - (shown ? row * 20 : 0);
        s += '<line class="p-col" x1="' + x + '" x2="' + x + '" y1="' + (by + 18) + '" y2="' + y + '"/>' +
             '<g class="p-badge"><rect x="' + (x - 9) + '" y="' + by + '" width="18" height="18"/><text x="' + x + '" y="' + (by + 13) + '">' + (idx + 1) + '</text></g>';
        if (shown) s += '<text class="p-name" x="' + (x + 14) + '" y="' + (by + 13) + '">' + esc(label) + '</text>';
      });
      s += '<line class="p-cur" x1="0" x2="0" y1="' + (mT - 8) + '" y2="' + (H - mB) + '" style="display:none"/><circle class="p-curdot" r="5" style="display:none"/></svg>';
      profEl.innerHTML = s;
      geom = { W: W, mL: mL, mR: mR, X: X, Y: Y };
    }

    function show(clientX) {
      if (!geom) return;
      var box = profEl.getBoundingClientRect();
      var x = (clientX - box.left) * (geom.W / box.width);
      var km = Math.min(Math.max((x - geom.mL) / (geom.W - geom.mL - geom.mR), 0), 1) * totalKm;
      var alt = altAt(km), cur = profEl.querySelector('.p-cur'), dot = profEl.querySelector('.p-curdot');
      cur.style.display = dot.style.display = '';
      cur.setAttribute('x1', geom.X(km)); cur.setAttribute('x2', geom.X(km));
      dot.setAttribute('cx', geom.X(km)); dot.setAttribute('cy', geom.Y(alt));
      if (readEl) readEl.innerHTML = '<b>km ' + frNum(km, 1) + '</b> · ' + Math.round(alt) + ' m d’altitude';
      if (cursor) { cursor.setLatLng(pointAt(km)); cursor.setStyle({ opacity: 1, fillOpacity: 1 }); }
    }
    function hide() {
      var cur = profEl.querySelector('.p-cur'), dot = profEl.querySelector('.p-curdot');
      if (cur) cur.style.display = dot.style.display = 'none';
      if (readEl) readEl.innerHTML = readDefault;
      if (cursor) cursor.setStyle({ opacity: 0, fillOpacity: 0 });
    }
    profEl.addEventListener('pointermove', function (e) { show(e.clientX); });
    profEl.addEventListener('pointerdown', function (e) { show(e.clientX); });
    profEl.addEventListener('pointerleave', hide);

    draw();
    var t = null, lastW = profEl.clientWidth;
    window.addEventListener('resize', function () {
      clearTimeout(t);
      t = setTimeout(function () { if (profEl.clientWidth !== lastW) { lastW = profEl.clientWidth; draw(); } if (map) map.invalidateSize(); }, 150);
    });
  });
})();
