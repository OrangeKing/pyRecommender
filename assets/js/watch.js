var b1 = document.getElementById("watchedbtn");
var b2 = document.getElementById("watchedico");


b1.onclick = function() {
    b1.className = "btn btn-success btn-lg"; 
    b1.innerHTML = '<span id="watchedico" class="glyphicon glyphicon-star" aria-hidden="true"></span> Watched!'
}
