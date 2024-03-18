// this js files won't be here, i am currently having issues with connecting the right path on my html, its here on a temporary basis to enable it work for now
// Also, in this main js file I will be doing all my js work for now, i will split to different files when i sort the path

// inputForm.js
const mealFormDirection = document.getElementById("mealPlanDirection");
const mealPlanForm = document.getElementById("mealPlanForm");

mealFormDirection.addEventListener('click', function(){
    targetOffset = mealPlanForm.offsetTop;

    window.scrollTo({
        top: targetOffset,
        behavior: 'smooth'
    });
})


// mealDetail.js

const InputForm = document.getElementById("inputForm");
const ShowMeal = document.getElementById("showMeal");
const ShowMealDetail = document.getElementById("showMealDetail");

let storedMeal = [];

InputForm.addEventListener("submit", function(e){
    e.preventDefault()

    const mealName = document.querySelector("#inputForm input[name='mealName']").value;
    const mealDescription = document.querySelector("#inputForm textarea[name='mealDescription']").value;

    const mealFormData = {
        mealName,
        mealDescription
    }

    storedMeal.push(mealFormData)
    localStorage.setItem('mealFormData', JSON.stringify(storedMeal))
});

ShowMeal.document.addEventListener('click', function(){
    ShowMealDetail.innerHTML = ''

    if(storedMeal.length){
        for (const meal of storedMeal){
            const eachMeal = document.createElement('li');
            eachMeal.textContent = `Name: ${meal.mealName}, Description: ${meal.mealDescription}`;
            ShowMealDetail.appendChild(eachMeal);
        }
    }else{
        ShowMealDetail.textContent = "you don't have any stored meal yet"
    }
})
