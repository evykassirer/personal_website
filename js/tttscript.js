var turn, haswon;

haswon = function(player){
	var checkWin, cname;
	cname = "block " + player + "on";
	checkWin = function(first, second, third){
		first = document.getElementById(first);
		second = document.getElementById(second);
		third = document.getElementById(third);
		if(first.className === cname && second.className === cname && third.className === cname){
			return true;
		}
		return false;
	}
	if(checkWin("one", "two", "three")) return true;
	else if(checkWin("four", "five", "six")) return true;
	else if(checkWin("sev", "eight", "nine")) return true;
	else if(checkWin("one", "four", "sev")) return true;
	else if(checkWin("two", "five", "eight")) return true;
	else if(checkWin("three", "six", "nine")) return true;
	else if(checkWin("one", "five", "nine")) return true;
	else if(checkWin("three", "five", "sev")) return true;
	return false;
}

turn = function(){
	var board, target, old, player, elem, oneMove, newGame;
	
	//start with player one
	document.getElementById("currentplayer").style.color = 'blue'
	document.getElementById("currentplayer").innerHTML="Player 1";
	player = "p1";
	
	//executes one move and changes the colour of one block
	oneMove = function(e){
		if(player == "win") return;
		e = e || event;  
		target =  e.target || e.srcElement; 		
		if(target.className === "block"){
			target.setAttribute("class", "block " + player + "on");							
			e.cancelBubble = true;
			if (e.stopPropagation) {
				e.stopPropagation();
			}
			//next turn
			if(haswon(player)){
				elem  = document.getElementById("winner");
				if(player == "p1"){
					elem.style.color = 'blue'
					elem.innerHTML=" PLAYER 1 WINS! ";
				}else if(player == "p2"){
					elem.style.color = 'red'
					elem.innerHTML=" PLAYER 2 WINS! ";
				}
				player = "win";
			}else if(player === "p1"){
				document.getElementById("currentplayer").style.color = 'red'
				document.getElementById("currentplayer").innerHTML="Player 2";
				player = "p2";
			}else{
				document.getElementById("currentplayer").style.color = 'blue'
				document.getElementById("currentplayer").innerHTML="Player 1";
				player = "p1";
			}
		}
	}
	
	//adds the listener to the board
	board = document.getElementById("board");
	board.addEventListener("click", oneMove, false);
	
	//sets the New Game button to reset the board
	newGame = function(){
		var divs, i;
		
		divs = document.getElementsByClassName("block");
		for(i = 0; i < divs.length; i++){
			divs[i].className = "block";
		}
		
		document.getElementById("winner").innerHTML = "";
		
		//start with player one
		document.getElementById("currentplayer").style.color = 'blue'
		document.getElementById("currentplayer").innerHTML="Player 1";
		player = "p1";
		oneMove();
	}
	
	elem = document.getElementById("new");
	elem.addEventListener("click", newGame, false);
};
turn();