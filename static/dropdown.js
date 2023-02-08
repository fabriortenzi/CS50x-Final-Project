const optionMenu = document.querySelector(".select-menu"),
       selectBtn = optionMenu.querySelector(".select-btn"),
       options = optionMenu.querySelectorAll(".option"),
       sBtn_text = optionMenu.querySelector(".sBtn-text");

selectBtn.addEventListener("click", () => optionMenu.classList.toggle("active"));       

options.forEach(option =>{
    option.addEventListener("click", ()=>{
        let selectedOption = option.querySelector(".option-text").innerText;
        sBtn_text.innerText = selectedOption;

        optionMenu.classList.remove("active");

        document.getElementById('input-category').value = selectedOption;

    });
});


// Focus effect on dropdown
let inputCategory = document.querySelector("#categories-dropdown");
inputCategory.addEventListener('click', function() {
    // Change the class of the dropdown to make the focus effect
    inputCategory.className = "input-category-focus";
});
let notDropdown = document.querySelectorAll('*:not(#categories-dropdown)');
console.log(notDropdown);
for (element in notDropdown)
{
    element.addEventListener('click', function(){    
        // Return to normal class
        inputCategory.className = "form-item";
    });
}