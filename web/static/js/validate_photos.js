function image_result(status){
    //return p1 * p2;   // The function returns the product of p1 and p2
    console.log("Sending validation for a photo");
    
    var data = { "photo": document.getElementById("image_view").src, "positive": status};
    var strJSONData = JSON.stringify(data);
    $.ajax({
        url: '/result_analyze',
        data: strJSONData,
        dataType : 'json',
        type: "post",
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
