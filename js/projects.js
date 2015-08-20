/*
AN ATTEMPT TO MAKE THE HOVER THING WORK ON MOBILE (touch to read information)


var projects = document.getElementsByClassName('project');
var images = document.getElementsByClassName('projectimage');
if (projects && images) {
	function f(i) {
		images[i].style.display = "block";
	}
	for(var i = 0; i < projects.length && i < images.length; i++) {
		projects[i].onclick = f(i);
	}
}

/* Add links to projects */
/*
var project = document.getElementsByClassName('codenext');
if (project) {
	console.log("got it");
	project[0].onclick = function(){
		window.open('http://davepagurek.com/yc/', '_blank');
	}
}

*/