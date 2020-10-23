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
            document.getElementById("name").innerHTML = response['name'];
            document.getElementById("header-time").innerHTML = response['header']['time'];
            document.getElementById("header-exposition").innerHTML = response['header']['exposition'];
            document.getElementById("header-gain").innerHTML = response['header']['gain'];
            document.getElementById("header-img_type").innerHTML = response['header']['img_type'];
            document.getElementById("header-comment").innerHTML = response['header']['comment'];
        },
        error: function(error){
            console.log(error);
        }
    });
    create_url_for_download()
}


function create_url_for_download(){
    console.debug("Computando url para descarga");

    let image = document.getElementById("image_view").src;
    let raw_url = image.replace('jpg', 'fit');
    document.getElementById("download-raw").href = raw_url;

}




window.onload = function() {
    create_url_for_download();

};