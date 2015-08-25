var dropdown = document.getElementsByClassName('clickopen');
var list = document.getElementsByClassName('clicklist');
var dropdown_button = document.getElementsByClassName('dropdown_button')[0];
if (list) {
	var parent = list[0];
	var links = parent.children; 
}
if (dropdown && list && links) {
	dropdown[0].onclick = function() {
		var open = parent.className.indexOf("open");
		console.log(dropdown_button);
		if (open == -1) {
			dropdown_button.style.backgroundColor = "#311B92";
			dropdown_button.style.color = "#FFFFFF";
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
			dropdown_button.style.backgroundColor = "#B39DDB";
			dropdown_button.style.color = "#000000";
			for(var i = 0; i < links.length; i++) {
				links[i].style.display = "none";
			}
			parent.className =  parent.className.substring(0,open); 
		}
	}
}