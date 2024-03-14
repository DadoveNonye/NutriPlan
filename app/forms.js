const mealFormDirection = document.getElementById("mealPlanDirection")
const mealPlanForm = document.getElementById("mealPlanForm")

mealFormDirection.addEventListener('click', function(){
    targetOffset = mealPlanForm.offsetTop;

    window.scrollTo({
        top: targetOffset,
        behavior: 'smooth'
    });
    console.log("button clicked")
})
