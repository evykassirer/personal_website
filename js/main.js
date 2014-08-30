var dropdown = document.getElementsByClassName('clickopen');
var list = document.getElementsByClassName('clicklist');
if (list)
	var links = list[0].children; 
if (dropdown && list && links) {
	dropdown[0].onclick = function() {
		for(var i = 0; i < links.length; i++) {
			if (links[i].style.display == "block") {
				links[i].style.display = "none";
			} else { 
				links[i].style.display = "block";
			}
		}
	}
}