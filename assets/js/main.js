(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  if (window.location.search.indexOf("sent=1") !== -1) {
    var success = document.getElementById("form-success");
    var form = document.querySelector(".contact-form");
    if (success) {
      success.hidden = false;
    }
    if (form) {
      form.hidden = true;
    }
  }
})();
