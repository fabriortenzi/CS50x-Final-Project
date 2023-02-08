function sumbitCategory(){

    const dict_values = {'selectedOption': selectedOption} //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
    $.ajax({
        url:"/expense",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify(s)});
}
