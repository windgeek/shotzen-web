// Language switching for the ShotZen pages.
//
// The six translations ship in the page itself rather than as six URLs, so a
// single Support URL and a single Privacy Policy URL cover every localisation
// the app has. Choice order: an explicit ?lang=, then whatever was picked last
// time, then the browser's own preference, then English.

(function () {
  var LANGS = ["en", "zh-Hans", "zh-Hant", "ja", "de", "fr"];

  function normalise(tag) {
    if (!tag) return null;
    tag = tag.toLowerCase();
    if (tag.indexOf("zh") === 0) {
      // Script subtag first; failing that, the regions that use traditional.
      if (tag.indexOf("hant") >= 0) return "zh-Hant";
      if (tag.indexOf("hans") >= 0) return "zh-Hans";
      return /-(tw|hk|mo)\b/.test(tag) ? "zh-Hant" : "zh-Hans";
    }
    var base = tag.split("-")[0];
    return LANGS.indexOf(base) >= 0 ? base : null;
  }

  function preferred() {
    var q = normalise(new URLSearchParams(location.search).get("lang"));
    if (q) return q;

    try {
      var saved = localStorage.getItem("shotzen.lang");
      if (LANGS.indexOf(saved) >= 0) return saved;
    } catch (e) { /* private browsing — fall through to the browser's list */ }

    var list = navigator.languages || [navigator.language];
    for (var i = 0; i < list.length; i++) {
      var hit = normalise(list[i]);
      if (hit) return hit;
    }
    return "en";
  }

  function show(lang) {
    document.querySelectorAll("article[lang]").forEach(function (a) {
      a.classList.toggle("on", a.getAttribute("lang") === lang);
    });
    document.querySelectorAll(".langs button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.lang === lang));
    });
    // Keeps the page's own lang honest, which is what a screen reader and the
    // browser's translate prompt both read.
    document.documentElement.setAttribute("lang", lang);
    try { localStorage.setItem("shotzen.lang", lang); } catch (e) {}
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".langs button").forEach(function (b) {
      b.addEventListener("click", function () { show(b.dataset.lang); });
    });
    show(preferred());
  });
})();
