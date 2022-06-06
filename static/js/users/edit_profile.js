$.fn.cropper(

$('#image').cropper({
 	aspectRatio: 16 / 9,
 	crop: function(event) {
 		console.log(event.detail.x);
 		console.log(event.detail.y);
 		console.log(event.detail.width);
 		console.log(event.detail.height);
 	}
    })




);






