/* Shared behavior for every page: mobile nav toggle + active-link marking. */

(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Mark the current page's nav link. Each <body> declares data-page,
  // and each nav link declares data-page it represents, so pages can
  // live in subdirectories without path comparisons.
  var current = document.body.getAttribute("data-page");
  if (current) {
    document.querySelectorAll(".site-nav a[data-page]").forEach(function (a) {
      if (a.getAttribute("data-page") === current) a.classList.add("active");
    });
  }
})();
