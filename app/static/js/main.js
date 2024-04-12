// this js files won't be here, i am currently having issues with connecting the right path on my html, its here on a temporary basis to enable it work for now
// Also, in this main js file I will be doing all my js work for now, i will split to different files when i sort the path

// inputForm.js
const mealFormDirection = document.getElementById("mealPlanDirection");
const mealPlanForm = document.getElementById("mealPlanForm");
const descCloseBtn = document.getElementById("descCloseBtn");
const confirmDeleteButton = document.getElementById("confirmDeleteButton");
const deleteConfirmationModal = document.getElementById(
  "deleteConfirmationModal"
);
const cancelDeleteButton = document.getElementById("cancelDeleteButton");
const InputForm = document.getElementById("inputForm");
const ShowMeal = document.getElementById("showMeal");
const ShowMealDetail = document.getElementById("showMealDetail");

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

confirmDeleteButton.addEventListener("click", (e) => {
  e.preventDefault();
  deleteConfirmationModal.style.display = "none";
  const mealIndex = parseInt(
    deleteConfirmationModal.getAttribute("data-meal-index")
  );
  deleteMeal(mealIndex);
});

ShowMeal.addEventListener("click", function (e) {
  e.preventDefault();
  ShowMealDetail.innerHTML = "";
  smoothScroll();

  if (storedMeal.length) {
    for (let i = 0; i < storedMeal.length; i++) {
      const meal = storedMeal[i];
      const eachMeal = document.createElement("li");
      const viewDescription = document.createElement("a");
      const editButton = document.createElement("button");
      const deleteButton = document.createElement("button");

      editButton.textContent = "Edit";
      deleteButton.textContent = "Delete";
      editButton.classList.add("edit-btn");
      deleteButton.classList.add("delete-btn");

      viewDescription.href = "#";
      viewDescription.textContent = "View";

      // Set data attributes to store the index of the meal
      editButton.setAttribute("data-meal-index", i);
      deleteButton.setAttribute("data-meal-index", i);

      // Add event listener to the edit button
      editButton.addEventListener("click", function (e) {
        e.preventDefault();
        const mealIndex = parseInt(editButton.getAttribute("data-meal-index"));
        editDescription(mealIndex);
      });

      // Add event listener to the delete button
      deleteButton.addEventListener("click", function (e) {
        e.preventDefault();
        const mealIndex = parseInt(
          deleteButton.getAttribute("data-meal-index")
        );
        deleteConfirmationModal.style.display = "block";
        deleteConfirmationModal.setAttribute("data-meal-index", mealIndex);
      });

      viewDescription.addEventListener("click", function (e) {
        e.preventDefault();
        mealPlanDisplay(meal.mealDescription);
      });

      eachMeal.textContent = `Name: ${meal.mealName} `;
      eachMeal.appendChild(viewDescription);
      eachMeal.appendChild(editButton);
      eachMeal.appendChild(deleteButton);
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

// edit.js
function editDescription(mealIndex) {
  if (mealIndex >= 0 && mealIndex < storedMeal.length) {
    const mealToEdit = storedMeal[mealIndex];
    const mealNameInput = document.querySelector(
      "#inputForm input[name='mealName']"
    );
    const mealDescriptionInput = document.querySelector(
      "#inputForm textarea[name='mealDescription']"
    );

    mealNameInput.value = mealToEdit.mealName;
    mealDescriptionInput.value = mealToEdit.mealDescription;
    mealDescriptionInput.focus();
  } else {
    console.log("invalid meal index");
  }
}

// delete.js

function deleteMeal(mealIndex) {
  storedMeal.splice(mealIndex, 1);
  localStorage.setItem("mealFormData", JSON.stringify(storedMeal));
  viewDescriptionBox.textContent = "";
}

cancelDeleteButton.addEventListener("click", () => {
  deleteConfirmationModal.style.display = "none";
});

confirmDeleteButton.addEventListener("click", () => {
  deleteConfirmationModal.style.display = "none";
});

const createMealPlanBtn = document.getElementById("create-mealplan-btn");

createMealPlanBtn.addEventListener("click", async () => {
  const name = document.getElementById("meal-plan-name").value;
  const description = document.getElementById("meal-plan-description").value;

  const response = await fetch("/mealplans", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, description }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    console.error("Error creating meal plan:", errorData.error);
    // Display error message to the user
  } else {
    const data = await response.json();
    console.log("Meal plan created:", data);
    // Update UI to show success message or redirect to view the new plan
  }
});
const toggleButton = document.querySelector(".nav-toggle");
const mobiNav = document.querySelector(".btt");
const logout = document.querySelector(".mlogin");
console.log(mobiNav);

toggleButton.addEventListener("click", function () {
  this.classList.toggle("open");
  mobiNav.classList.toggle("show");
  logout.classList.toggle("show");

  console.log(mobiNav);
});
