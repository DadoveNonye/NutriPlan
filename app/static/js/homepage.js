const toggleButton = document.querySelector(".nav-toggle");
const mobiNav = document.querySelector(".btt");
console.log(toggleButton);

toggleButton.addEventListener("click", function () {
  this.classList.toggle("open");
  mobiNav.classList.toggle("show");
  console.log("showww");
});

const about = document.getElementById("about-us");
const about_us = document.getElementById("about-page");
about.addEventListener("click", function (e) {
  e.preventDefault();
  smoothScroll();
});
const smoothScroll = () => {
  targetOffset = about_us.offsetTop;

  window.scrollTo({
    top: targetOffset,
    behavior: "smooth",
  });
};
