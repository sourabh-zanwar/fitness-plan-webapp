const accordionBtns = document.querySelectorAll(".accordion-btn");

accordionBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const panel = btn.nextElementSibling;
    panel.classList.toggle("active");

    accordionBtns.forEach((item) => {
      if (item !== btn) {
        item.classList.remove("active");
        item.nextElementSibling.style.display = "none";
      }
    });
  });
});
