document.getElementById('imageInput').onchange = function () {
  var src = URL.createObjectURL(this.files[0]);
  var imageInput = document.getElementById('imageInput');
  
  document.getElementById('image').src = src;
  
  var isValidpng = /\.png?g$/i.test(imageInput.value);
  var isValidjpg = /\.jpg?g$/i.test(imageInput.value);
  
  if (!isValidpng && !isValidjpg) {
	document.getElementById('image').value = null;
	document.getElementById("submitButton").disabled = true;
    alert('Please use a png or jpg!');
  }
  else {
	document.getElementById("submitButton").disabled = false;
  };
}
