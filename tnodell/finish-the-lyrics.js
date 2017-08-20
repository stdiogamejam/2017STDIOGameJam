// Require the lyrics from the JSON file, an object
var song = require("./lyrics.js");
// Require the utilities file,
var util = require('util');

// First provide instructions to the player
console.log("In finish the lyrics, you must finish the lyrics! \n The first half of the lyrics will be provided to you. \n You must finish the line.");
console.log("The song you will be completing is: " + song.name);
console.log("Type quit to end.");
console.log("Game will start in 1.5 seconds");

function start() {
		var line = getRandomLine(song.lyrics);
		var lineObj = splitLine(line);

		console.log("Line: "+ line);
		console.log("First Half: "+ lineObj.firstHalf);
		console.log("Finish the line: ");

	// Not every node program needs process, so it is paused by default. We must resume it.
	process.stdin.resume();
	// Set our encoding
	process.stdin.setEncoding('utf8');

	// process is our environment
	// stdin is our input, and on provides a listener
	// on 'data', apply this function using the text from the input
	process.stdin.on('data', function (text) {
		//console.log("Compare string: "+ compareString(lineObj.firstHalf, lineObj.secondHalf));

		if (text == 'quit\r\n') {
		      done();
		    }
	});
}

setTimeout(start, 1500);



/* Function definitions */

function done() {
	console.log('\nBye!');
    process.exit();
}

function getRandomLine(){
	// song.lyrics is an array, get the total number of lines
	var numOfSongLines = song.lyrics.length;
	// round to the lowest number of 0-1 * the total number of lines in a song
	var randomLine = Math.floor(Math.random()*numOfSongLines);
	return song.lyrics[randomLine];
}

// @param {string} line - line from the song
function splitLine(line){
	// create an object to return
	var obj = {};
	//turn the string into an array, split on spaces
	var arr = line.split(' ');
	// find the middle index
	var middleIndex = Math.ceil(arr.length / 2);

	// Slice the first half from beginning to middle index, slice returns an array
	var firstHalfArr = arr.slice(0, middleIndex);
	// Slice the second half starting on the element after the middle one.
	var secondHalfArr = arr.slice(middleIndex);

	// join the array again, putting a space between each element
	obj.firstHalf = firstHalfArr.join(" ");
	obj.secondHalf = secondHalfArr.join(" ");

	// return an object with the two halfs, put back together as strings
	return obj;
}

// @param {string} str1 - line from the song
// @param {string} str2 - user entered text
function compareString(str1, str2){
	// fancy regex to simplify strings to compare them. For more info https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions
	// remove any punctuation
	var punctuationless1 = str1.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"");
	// remove any excess space
	var extraSpaceless1 = punctuationless1.replace(/\s{2,}/g," ");
	// make the whole string lowercase
	var finalString1 = extraSpaceless1.toLowerCase();

	//repeat for the user inputed string
	var punctuationless2 = str2.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"");
	var extraSpaceless2 = punctuationless2.replace(/\s{2,}/g," ");
	var finalString2 = extraSpaceless2.toLowerCase();

	// compare them, if they're the same return true
	if( finalString1 == finalString2 ){
		return true;
	}
	//otherwise return false
	return false;
}