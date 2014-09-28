var dropdown = document.getElementsByClassName('clickopen');
var list = document.getElementsByClassName('clicklist');
if (list)
	var parent = list[0]
	var links = parent.children; 
if (dropdown && list && links) {
	dropdown[0].onclick = function() {
		var open = parent.className.indexOf("open");
		if (open == -1) {
			for(var i = 0; i < links.length; i++) {
				if ((window.innerHeight < 400 && links[i].className == "removefirst")){
					links[i].style.display = "none";
				} 
				else if ((window.innerHeight < 360 && links[i].className == "removesecond")){
					links[i].style.display = "none";
				} else { 
					links[i].style.display = "block";
				}
			}
			parent.className = parent.className + " open";
		}
		else {
			for(var i = 0; i < links.length; i++) {
				links[i].style.display = "none";
			}
			parent.className =  parent.className.substring(0,open); 
		}
	}
}