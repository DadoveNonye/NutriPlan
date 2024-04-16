/**
 * This file contains the JavaScript code for the homepage functionality.
 */

/**
 * The toggle button element.
 * @type {HTMLElement}
 */
const toggleButton = document.querySelector(".nav-toggle");

/**
 * The mobile navigation element.
 * @type {HTMLElement}
 */
const mobiNav = document.querySelector(".btt");

console.log(toggleButton);

/**
 * Event listener for the toggle button click event.
 */
toggleButton.addEventListener("click", function () {
  this.classList.toggle("open");
  mobiNav.classList.toggle("show");
  console.log("showww");
});

/**
 * The about button element.
 * @type {HTMLElement}
 */
const about = document.getElementById("about-us");

/**
 * The about page element.
 * @type {HTMLElement}
 */
const about_us = document.getElementById("about-page");

/**
 * Event listener for the about button click event.
 * @param {Event} e - The click event object.
 */
about.addEventListener("click", function (e) {
  e.preventDefault();
  smoothScroll();
});

/**
 * Smoothly scrolls to the about page.
 */
const smoothScroll = () => {
  targetOffset = about_us.offsetTop;

  window.scrollTo({
    top: targetOffset,
    behavior: "smooth",
  });
};
