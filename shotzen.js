// All translations are in the HTML. No network requests are needed to switch.
// Choice: URL → saved language → browser preference → English.
(function () {
  "use strict";
  var LANGS = ["en", "zh-Hans", "zh-Hant", "ja", "ko", "de", "fr", "es", "pt-BR"];

  function normalise(tag) {
    if (typeof tag !== "string") return null;
    tag = tag.trim().replace(/_/g, "-").toLowerCase();
    var base = tag.split("-")[0];
    if (base === "zh") {
      if (/-hant\b/.test(tag)) return "zh-Hant";
      if (/-hans\b/.test(tag)) return "zh-Hans";
      return /-(tw|hk|mo)\b/.test(tag) ? "zh-Hant" : "zh-Hans";
    }
    // Brazilian Portuguese is the app's Portuguese locale.
    if (base === "pt") return "pt-BR";
    return LANGS.indexOf(base) >= 0 ? base : null;
  }

  function preferred() {
    var query = normalise(new URLSearchParams(location.search).get("lang"));
    if (query) return query;
    try {
      var saved = normalise(localStorage.getItem("shotzen.lang"));
      if (saved) return saved;
    } catch (error) { /* Storage may be disabled. */ }
    var list = navigator.languages || [navigator.language];
    for (var i = 0; i < list.length; i++) {
      var match = normalise(list[i]);
      if (match) return match;
    }
    return "en";
  }

  function show(lang) {
    if (LANGS.indexOf(lang) < 0) return;
    var active;
    document.querySelectorAll("article[lang]").forEach(function (article) {
      var selected = article.getAttribute("lang") === lang;
      article.hidden = !selected;
      article.classList.toggle("on", selected);
      if (selected) active = article;
    });
    if (!active) return;
    document.querySelectorAll(".langs button").forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.lang === lang));
    });
    document.documentElement.lang = lang;
    document.title = active.dataset.title;
    document.querySelector('meta[name="description"]').content = active.dataset.description;
    document.querySelector(".tagline").textContent = active.dataset.tagline;
    document.querySelector(".langs").setAttribute("aria-label", active.dataset.languageLabel);
    var footer = document.querySelector("[data-page-link]");
    var target = new URL(footer.getAttribute("href"), location.href);
    target.searchParams.set("lang", lang);
    footer.setAttribute("href", target.pathname + target.search);
    footer.textContent = active.dataset.footer;
    try { localStorage.setItem("shotzen.lang", lang); } catch (error) {}
    try {
      var url = new URL(location.href);
      url.searchParams.set("lang", lang);
      history.replaceState(null, "", url.pathname + url.search + url.hash);
    } catch (error) { /* Readable even if history updates are unavailable. */ }
  }

  document.querySelectorAll(".langs button").forEach(function (button) {
    button.addEventListener("click", function () { show(button.dataset.lang); });
  });
  show(preferred());
})();
