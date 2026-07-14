(function () {
  var chips = document.getElementById("chips");
  if (!chips) return;
  chips.addEventListener("click", function (ev) {
    var btn = ev.target.closest(".chip");
    if (!btn) return;
    var pane = btn.getAttribute("data-pane");
    chips.querySelectorAll(".chip").forEach(function (c) {
      c.classList.toggle("on", c === btn);
    });
    document.querySelectorAll(".pane").forEach(function (p) {
      p.classList.toggle("hidden", p.id !== "pane-" + pane);
    });
  });
})();
