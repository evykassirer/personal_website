var turn, boxwin, haswon, makeBox, makeRow;
var nums = ["one", "two", "thr", "fou", "fiv", "six", "sev", "eig", "nin"]; //all are three leters so I can do string manipulations


//FUNCTIONS FOR CREATING THE BOARD************
makeBox = function(n){ //n is the index of the box number
	var newb, s, i; //s is html string, short variable name because will be used a lot
	newb = document.createElement("div");
	newb.className = "box";
	newb.id = nums[n];
	s = "";
	i = 0;
	while(i < 9){
		s += "<div class = \"row\">\n";
		s +=  "<div class= \"block\" id=" + nums[n] + nums[i] + "></div>\n";
		i++;
		s +=  "<div class= \"block\" id=" + nums[n] + nums[i] + "></div>\n";
		i++;
		s +=  "<div class= \"block\" id=" + nums[n] + nums[i] + "></div>\n";
		i++;
		s += "</div>\n"
	}
	newb.innerHTML = s;
	return newb;
}

makeRow = function(n){ //n is the index of the leftmost box number
	var newr;
	newr = document.createElement("div");
	newr.className = "row";
	newr.appendChild(makeBox(n));
	n++;
	newr.appendChild(makeBox(n));
	n++;
	newr.appendChild(makeBox(n));
	return newr;
}

//******************END BOARD FUNCTIONS


boxwin = function(player, n){ //n is the box we're checking
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
	if(checkWin(nums[n] + "one", nums[n] + "two", nums[n] + "thr")) return true;
	else if(checkWin(nums[n] + "fou", nums[n] + "fiv", nums[n] + "six")) return true;
	else if(checkWin(nums[n] + "sev", nums[n] + "eig", nums[n] + "nin")) return true;
	else if(checkWin(nums[n] + "one", nums[n] + "fou", nums[n] + "sev")) return true;
	else if(checkWin(nums[n] + "two", nums[n] + "fiv", nums[n] + "eig")) return true;
	else if(checkWin(nums[n] + "thr", nums[n] + "six", nums[n] + "nin")) return true;
	else if(checkWin(nums[n] + "one", nums[n] + "fiv", nums[n] + "nin")) return true;
	else if(checkWin(nums[n] + "thr", nums[n] + "fiv", nums[n] + "sev")) return true;
	return false;
}

haswon = function(player){
	var checkWin, cname;
	cname = "box " + player + "on";
	checkWin = function(first, second, third){
		first = document.getElementById(first);
		second = document.getElementById(second);
		third = document.getElementById(third);
		if(first.className === cname && second.className === cname && third.className === cname){
			return true;
		}
		return false;
	}
	if(checkWin("one", "two", "thr")) return true;
	else if(checkWin("fou", "fiv", "six")) return true;
	else if(checkWin("sev", "eig", "nin")) return true;
	else if(checkWin("one", "fou", "sev")) return true;
	else if(checkWin("two", "fiv", "eig")) return true;
	else if(checkWin("thr", "six", "nin")) return true;
	else if(checkWin("one", "fiv", "nin")) return true;
	else if(checkWin("thr", "fiv", "sev")) return true;
	return false;
}

turn = function(){
	var board, target, old, player, nextBox, elem, string, i, instr_on;
	var oneMove, newGame, instructions; //the functions
	
	//add the elements to the board
	board = document.getElementById("board");
	board.appendChild(makeRow(0));
	board.appendChild(makeRow(3));
	board.appendChild(makeRow(6));
	
	//start with player one
	document.getElementById("currentplayer").style.color = 'blue'
	document.getElementById("currentplayer").innerHTML="Player 1";
	player = "p1";
	nextBox = "";
	instr_on = false;
	
	//executes one move and changes the colour of one block
	oneMove = function(e){
		if(player == "win") return;
		if(instr_on) return;
		
		e = e || event;  
		target =  e.target || e.srcElement; 
		
		//invalid move if we've added "p1/2 on" to the block 
		if(target.className !== "block") return; 

		//if there's a box highlighted yellow make sure it's in that box
		if(nextBox !== "" && target.parentNode.parentNode.className !== "box turn") return; 
		
		
		//HERE IS WHERE BUSINESS STARTS
		
		//change the specific element where the player made a move
		target.setAttribute("class", "block " + player + "on");		
		
		//this catches the click after newgame - don't think I need it now
		//if(!document.getElementById(nextBox)) return; 
		
		//unhighlight the box
		elem = document.getElementsByClassName("turn");
		if(elem.length) {
			string = elem[0].className;
			string = string.substr(0, string.length-5);
			elem[0].className = string;
		}
		
		//this is the subbox that will rule which big box will be used next
		nextBox = target.id.substring(3, 6); 
		
		//if the next box has already been won, nextbox is freed
		if(document.getElementById(nextBox).className === "box p1on" || document.getElementById(nextBox).className === "box p2on") {
			nextBox = "";
		}
		//otherwise make the next highlighted box
		else{		
			elem = document.getElementById(nextBox); 
			elem.className = elem.className + " turn";
		}		
		
		//stop the bubbling
		e.cancelBubble = true;
		if (e.stopPropagation) {
			e.stopPropagation();
		}
		
		//update any individual box wins
		for(i = 0; i < 9; i++){
			elem = document.getElementById(nums[i]);
			if(elem.className !== "box p1on" && elem.className !== "box p2on" && boxwin(player, i)){
				elem.className = "box " + player + "on";	
				elem.innerHTML = "";
				if(elem.id === nextBox) { //this is when the nextbox is now a filled won box, 
					nextBox = "";         //so we must reset to default
				}
			}
		}		
		
		//big win
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
			
		}

		//next turn 
		else if(player === "p1"){
			document.getElementById("currentplayer").style.color = 'red'
			document.getElementById("currentplayer").innerHTML="Player 2";
			player = "p2";
		}else{
			document.getElementById("currentplayer").style.color = 'blue'
			document.getElementById("currentplayer").innerHTML="Player 1";
			player = "p1";
		}
	}
	
	//adds the turn listener to the board
	board = document.getElementById("board");
	board.addEventListener("click", oneMove, false);
	
	
	//sets the New Game button to reset the board
	newGame = function(){
		board = document.getElementById("board");
		board.innerHTML = "";
		board.appendChild(makeRow(0));
		board.appendChild(makeRow(3));
		board.appendChild(makeRow(6));
		
		document.getElementById("winner").innerHTML = "";
		
		//start with player one
		document.getElementById("currentplayer").style.color = 'blue'
		document.getElementById("currentplayer").innerHTML="Player 1";
		player = "p1";
		nextBox = "";
		instr_on = false;
		oneMove();
	}
	//listener for the new game button
	elem = document.getElementById("new");
	elem.addEventListener("click", newGame, false);
	
	
	//set listener for instructions
	instructions = function(){
		if(instr_on) {
			return;
		}
		var back, e;
		elem = document.getElementById("instructions");
		elem.innerHTML = "Instructions: <br> <br> The first player can go any where on the board that they would like. " +
						"The move of the first player will limit where the next player can go. " +
						"Bold lines indicate divisions of the large board. " +
						"Non bold lines indicate divisions of the smaller boards. " +
						"Wherever the first player goes in a small board translates to where the next player can go in the large board. " +
						"Within the smaller tic tac toe boards, game play works the same as regular tic tac toe. " +
						"If a player wins a small board, their color fills that box. " +
						"If a player is redirected to a board that has already been filled, " + 
						"then they will be allowed to play anywhere that is unoccupied on the board." +
						"<br><br>" +
						"Objective: win on the larger board. " +
						"<br><br>" +
						"<em> (click anywhere to go back to the game) </em>";
		elem.style.backgroundColor = "powderblue";
		elem.style.position = "fixed";
		instr_on = true;
		
		e = e || event;  
		e.cancelBubble = true;
		if (e.stopPropagation) {
			e.stopPropagation();
		}
		
		//to turn instructions off
		back = function(){
			elem = document.getElementById("instructions");
			elem.innerHTML = "";
			elem.style.backgroundColor = "transparent";
			elem.style.position = "static";
			instr_on = false;
			
			elem = document.getElementsByClassName("body");
			elem = elem[0];
			elem.removeEventListener("click", back, false);
			
			e = e || event;  
			e.cancelBubble = true;
			if (e.stopPropagation) {
				e.stopPropagation();
			}
		}
		
		elem = document.getElementsByClassName("body");
		elem = elem[0];
		elem.addEventListener("click", back, false);
	}
	
	//listener or instructions
	elem = document.getElementById("instr_button");
	elem.addEventListener("click", instructions, false);
	
};
turn();