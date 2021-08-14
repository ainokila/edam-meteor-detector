function imageResult(status){
    
    var data = { "photo": document.getElementById("image_view").src, "positive": status};
    var strJSONData = JSON.stringify(data);

    $.ajax({
        url: '/result_analyze',
        data: strJSONData,
        dataType : 'json',
        type: "post",
        success: function(response){
            drawImageInformation(response);
            composeDownloadUrl();

        },
        error: function(error){
            console.log(error);
        }
    });
}

function drawImageInformation(response){
    document.getElementById("image_view").src = response['photo'];
    document.getElementById("name").innerHTML = response['name'];
    document.getElementById("header-time").innerHTML = response['header']['time'];
    document.getElementById("header-exposition").innerHTML = response['header']['exposition'];
    document.getElementById("header-gain").innerHTML = response['header']['gain'];
    document.getElementById("header-img_type").innerHTML = response['header']['img_type'];
    document.getElementById("header-comment").innerHTML = response['header']['comment'];
}


function composeDownloadUrl(){

    let image = document.getElementById("image_view").src;
    let raw_url = image.replace('jpg', 'fit');
    document.getElementById("download-raw").href = raw_url;

}

function fillGallery(endpoint, from, size){

    var data = { "offset": from, "size": size};
    var strJSONData = JSON.stringify(data);
    $.ajax({
        url: endpoint,
        data: strJSONData,
        dataType : 'json',
        type: "post",
        success: function(response){
            var photoPosition;
            for (photoPosition in response['data']) {
                var image = response['data'][photoPosition]['photo'];
                var imageUrl = '/repository/' + image.replace('/static/data/','').replace('.jpg', '');
                var photoGallery = [
                    '<div class="col-lg-4 col-md-4 col-6">',
                            '<img class="img-fluid img-thumbnail showImage" src="' + image +'" alt="">',
                    '</div>',
                ];
                $(photoGallery.join('')).appendTo("#gallery");
            }
            console.info(response['data'].length);
            if (response['data'].length < size){
                //Disable button btn-load-images
                $("#btn-load-images").prop("disabled",true);
            }
        },
        error: function(error){
            console.exception(error);
            alert('Failed connecting with the server'); 
        }
    });

}


function nextImages(){
    var numberPhotos = 3;
    var endpoint = "";
    if (window.location.href.includes("positives")){
        endpoint = '/repository/positives/search';
    }else{
        endpoint = '/repository/candidates/search';
    }
    fillGallery(endpoint, $('#gallery').children().length + 1, numberPhotos);
    $(document).on('click', '.showImage', showImage);
}


function showImage(){
    var sourcePhoto = $(this).attr('src');
    ///repository/<img_type>/<img_name>'
    var endPoint = '/repository/' + sourcePhoto.split('/')[2] + '/' + sourcePhoto.split('/')[3];
    console.log(endPoint);
    $.ajax({
        url: endPoint,
        dataType : 'json',
        type: "get",
        success: function(response){
            drawImageInformation(response);
            composeDownloadUrl();
            $("html, body").animate({ scrollTop: 0 }, "slow");
        },
        error: function(error){
            console.log(error);
        }
    });

}


$( document ).ready(function() {
    $("#btn-load-images").click(nextImages);
    composeDownloadUrl();
    nextImages();
});

