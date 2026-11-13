// UI strings by language (document.documentElement.lang)
  var SITE_LANG = (document.documentElement.lang || 'fr').slice(0, 2);
  var SITE_T = ({
    fr: {
      menuOpen: 'Ouvrir le menu',
      menuClose: 'Fermer le menu',
            newsInvalid: 'Entrez une adresse e-mail valide.',
      newsThanks: 'Merci ! Vérifiez votre boîte mail pour confirmer votre inscription.'
    },
    en: {
      menuOpen: 'Open menu',
      menuClose: 'Close menu',
      newsInvalid: 'Enter a valid email address.',
      newsThanks: 'Thanks! Check your inbox to confirm your subscription.'
    },
    de: {
      menuOpen: 'Menü öffnen',
      menuClose: 'Menü schließen',
      newsInvalid: 'Gib eine gültige E-Mail-Adresse ein.',
      newsThanks: 'Danke! Prüfe dein Postfach, um deine Anmeldung zu bestätigen.'
    }
  })[SITE_LANG] || null;
  function siteT(key, fallback) { return (SITE_T && SITE_T[key]) || fallback; }

  // Scroll reveal via IntersectionObserver (no scroll listeners)
  (function () {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var els = document.querySelectorAll('.reveal');
    if (reduce || !('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.16, rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (e) { io.observe(e); });
  })();

  // Mobile nav toggle
  (function () {
    var toggle = document.getElementById('navToggle');
    var links = document.getElementById('navLinks');
    function setOpen(open) {
      links.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? siteT('menuClose', 'Fermer le menu') : siteT('menuOpen', 'Ouvrir le menu'));
    }
    // Raccourcis de la barre du haut, repris en tête du menu mobile
    var quick = document.querySelector('.topbar-links');
    if (quick) {
      var box = document.createElement('div');
      box.className = 'nav-quick';
      quick.querySelectorAll('a').forEach(function (a) { box.appendChild(a.cloneNode(true)); });
      links.insertBefore(box, links.firstChild);
    }
    toggle.addEventListener('click', function () {
      setOpen(!links.classList.contains('open'));
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });
  })();

  // Newsletter: submit to Brevo via hidden iframe, inline confirmation
  (function () {
    var form = document.getElementById('newsForm');
    if (!form) return;
    var note = document.getElementById('newsNote');
    form.addEventListener('submit', function (e) {
      var input = form.querySelector('input[type="email"]');
      if (!input.value || !input.checkValidity()) {
        e.preventDefault();
        note.textContent = siteT('newsInvalid', 'Entrez une adresse e-mail valide.');
        input.focus();
        return;
      }
      note.textContent = siteT('newsThanks', 'Merci ! Vérifiez votre boîte mail pour confirmer votre inscription.');
      setTimeout(function () { form.reset(); }, 200);
    });
  })();
