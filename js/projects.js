var projects = document.getElementsByClassName('project');
var images = document.getElementsByClassName('projectimage');
if (projects && images) {
	function f(i) {
		if (images[i].style.display == "none") {
			images[i].style.display = "block";
		}
		else {
			images[i].style.display = "none";
		}
	}
	for(var i = 0; i < projects.length && i < images.length; i++) (function(i) {
		projects[i].onclick = function() {
			f(i);
		};
	})(i);
}