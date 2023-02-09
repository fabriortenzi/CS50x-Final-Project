// Dropdown
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


// Change active dropdown to normal
let fields = new Array();
let field1 = document.getElementById('1');
fields[0] = field1;
let field3 = document.getElementById('3');
fields[1] = field3;
fields.forEach(function(element){
    element.addEventListener('click', function(){    
        // Return to normal class
        let inputCategory2 = document.querySelector("#categories-dropdown");
        inputCategory2.className = "select-menu";

        let inputCategory3 = document.getElementById('2');
        inputCategory3.className = "select-menu";
    });
});


