// this js files won't be here, i am currently having issues with connecting the right path on my html, its here on a temporary basis to enable it work for now
// Also, in this main js file I will be doing all my js work for now, i will split to different files when i sort the path

// inputForm.js
const mealFormDirection = document.getElementById("mealPlanDirection");
const mealPlanForm = document.getElementById("mealPlanForm");

mealFormDirection.addEventListener("click", function () {
  smoothScroll();
});

const smoothScroll = () => {
  targetOffset = mealPlanForm.offsetTop;

  window.scrollTo({
    top: targetOffset,
    behavior: "smooth",
  });
};

// mealDetail.js

const InputForm = document.getElementById("inputForm");
const ShowMeal = document.getElementById("showMeal");
const ShowMealDetail = document.getElementById("showMealDetail");

let storedMeal = [];

InputForm.addEventListener("submit", function (e) {
  e.preventDefault();

  let mealName = document.querySelector(
    "#inputForm input[name='mealName']"
  ).value;
  let mealDescription = document.querySelector(
    "#inputForm textarea[name='mealDescription']"
  ).value;

  const mealFormData = {
    mealName,
    mealDescription,
  };

  storedMeal.push(mealFormData);
  localStorage.setItem("mealFormData", JSON.stringify(storedMeal));

  InputForm.reset();
});

ShowMeal.addEventListener("click", function (e) {
  e.preventDefault();
  ShowMealDetail.innerHTML = "";
  smoothScroll();

  if (storedMeal.length) {
    for (const meal of storedMeal) {
      const eachMeal = document.createElement("li");
      const viewDescription = document.createElement("a");
      viewDescription.href = "#";
      viewDescription.textContent = "view";
      viewDescription.addEventListener("click", function (e) {
        e.preventDefault();
        mealPlanDisplay(meal.mealDescription);
        // toggleCloseBtn();
      });
      eachMeal.textContent = `Name: ${meal.mealName} `;
      eachMeal.appendChild(viewDescription);
      ShowMealDetail.appendChild(eachMeal);
    }
  } else {
    ShowMealDetail.textContent = "You don't have any stored meal yet";
  }
});
function mealPlanDisplay(mealDescription) {
  viewDescriptionBox.textContent = mealDescription;
}

const viewDescriptionBox = document.getElementById("viewDescriptionBox");
const descCloseBtn = document.getElementById("descCloseBtn");
// ]Next working on the edit description function
