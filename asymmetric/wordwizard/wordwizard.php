<?
$wordlist=file_get_contents("./words.txt");
$words=explode("\n",$wordlist);
$usedwords=array();
$level=1; // starting difficulty level
$player=array();
makenewplayer();

echo "\n\n\nWelcome to WORD WIZARD.  You are a powerful WORD WIZARD.";
echo "\nFight monsters by typing words.  You can only use each word once!";
echo "\nYou will grow more powerful after each monster you defeat,";
echo "\nbut beware, for the monsters will also grow stronger!";

$monster=makemonster($level);

while ($gameover==false) {
	$gameover=false;
	clear;
	echo "\n\n********\n\nYou're fighting ".$monster["name"].".";
	echo "\nOnly words beginning with ".strtoupper($monster["adjective"][0])." will hurt this monster.";
	echo "\nYour HP: ".$player["hp"];
	echo "\nEnemy HP: ".$monster["hp"];
	$playerword = readline("\nWhat word will you attack with: ");
	$playerword=strtoupper($playerword); // upper-case the input for processing
	if ($playerword=="XXX") $player["hp"]=0; 
	if (!isword($playerword)) {
		if ($playerword=="XXX") echo "\nYou surrender to the monster.";
		else echo "\n\nThat's not a word!";
	} else {
		if (in_array($playerword,$usedwords)) {
			echo "\nYou've used that word before!";
		} else {
			if ($playerword[0]!=strtoupper($monster["adjective"][0])) {
				echo "\nThat doesn't begin with ".strtoupper($monster["adjective"][0])."!";
			} else {
				$damage=strlen($playerword)+$player["bonus"];
				echo "\nYou attack with the word $playerword, dealing $damage damage.";
				$monster["hp"]-=$damage;
				array_push($usedwords,$playerword);
			}
		}
	}
	if ($monster["hp"]<1) {
		echo "\nYou beat the monster!";
		$level++;
		levelup();
		$monster=makemonster($level);
	} else {
		echo "\nThe monster attacks you for ".$monster["damage"]." damage!";
		$player["hp"]-=$monster["damage"];
	}
	if ($player["hp"]<1) {
		echo "\nYou have fallen...";
		$score=floor(pow($level,1.2));
		echo "\nYou defeated $level monsters, giving you a final score of $score.";
		$gameover=true;
	}
}
function isword($word_to_check) {
  global $words;
  if (in_array(strtoupper($word_to_check),$words)) return true; else return false;
}
function pickone($array_to_pick_from) {
	return $array_to_pick_from[mt_rand(0,sizeof($array_to_pick_from)-1)];
}
function aan($phrase) {
	if (in_array(strtolower($phrase[0]),array("a","e","i","o","u"))) return "an $phrase";
	else return "a $phrase";
}
function levelup() {
	global $player;
	echo "\nYou level up!  Choose one:";
	echo "\n1. Increase the damage of your words by 1.";
	echo "\n2. Increase your maximum HP by 5.";
	echo "\n3. Rest and restore all of your HP.";
	$input = readline("\nType 1, 2, or 3: ");
	if ($input==1) {
		$player["bonus"]++;
		echo "\nYour word damage bonus is now ".$player["bonus"].".";
	} else if ($input==2) {
		$player["maxhp"]+=5;
		echo "\nYour maximum HP is now ".$player["maxhp"].".";
	} else if ($input==3) {
		$player["hp"]=$player["maxhp"];
		echo "\nYour HP have been restored.";
	} else echo "\nPeople who don't follow instructions don't deserve to level up.";
	echo "\n\nYou find a new monster to fight.";
}
function makemonster($difficulty=1) {
	global $monster;
	$monster=array();
	$adjectives=array("apathetic","belligerent","cruel","dastardly","eerie","flaming","giant","horrific","insolent","jubilant","knife-wielding","lemon-scented","mouthy","nearsighted","orange","purple","quick","red","sideways","thick-skinned","ugly","venomous","wide-mouthed","xenophobic","yellow","zealous");
	$monster["hp"]=7+($difficulty+3);
	$monster["name"]=pickone(array("goblin","skeleton","ooze","bat","rat","cultist","ghoul","troglodyte","ogre"));
	$monster["adjective"]=pickone($adjectives);
	if (in_array($monster["adjective"][0],array("k","j","q","x","z","y"))) $monster["adjective"]=pickone($adjectives);
	$monster["name"]=$monster["adjective"]." ".$monster["name"];
	$monster["name"]=aan($monster["name"]); // add an indefinite article
	$monster["damage"]=3+$difficulty;
	return $monster;
}
function makenewplayer() {
	global $player;
	$player["maxhp"]=30;
	$player["hp"]=30;
	$player["bonus"]=0;
}
echo "\n\n\n";
exit();
?>

