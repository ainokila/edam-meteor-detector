function image_result(status){
    //return p1 * p2;   // The function returns the product of p1 and p2
    console.log("LLama a la api");
    
    $.ajax({
        url: '/result_analyze',
        data: {"photo": document.getElementById("image_view").src, "positive": status},
        dataType: "json",
        type: 'POST',
        success: function(response){
            console.log(response);
            document.getElementById("image_view").src = response['new_photo'];
            // ACTUALIZAR LA INFORMACION DE LA IMAGEN
        },
        error: function(error){
            console.log(error);
        }
    });
}
