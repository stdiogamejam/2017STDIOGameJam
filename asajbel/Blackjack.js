function print (text, where = "output") {
  document.getElementById(where).innerHTML += "<p>" + text + "</p>";
}

function read(e, value, id) {
  if (e.keyCode === 13) {
    e.preventDefault();
    playerAction(value);
    document.getElementById(id).value = '';
  }
}

var deck = [];
var state = ["Opening","Play","Resolve"];
var s = state[0];
var dealerCards = [0,0];
var playerCards = [0,0];
var playerMoney = 1000;
var bet = 100;
var numDecks = 1;

intro();

function intro() {
  s = state[0];
  var text =
  "This is a game of Blackjack. You start with $1000. The rules for the game can\
  be found at " +
  "<a href='http://www.bicyclecards.com/how-to-play/blackjack/'>\
  http://www.bicyclecards.com/how-to-play/blackjack/</a>"
  + ". To begin enter the number\
  of decks to play with. Then use the commands Hit, Stand, or \
  Double Down. To restart enter Restart. Split and insurance are not \
  implemented.";
  print(text);
}

function newDeck() {
  var cards = [];
  var suits = ['Hearts','Spades','Diamonds','Clubs'];
  for (var i = 0; i < 4; i++) {
    for (var j = 1; j <= 13; j++){
      switch (j){
        case 1:
          cards.push({value:j,name:'Ace',suit:suits[i]});
          break;
        default:
          cards.push({value:j,name:j,suit:suits[i]});
          break;
        case 11:
          cards.push({value:10,name:'Jack',suit:suits[i]});
          break;
        case 12:
          cards.push({value:10,name:'Queen',suit:suits[i]});
          break;
        case 13:
          cards.push({value:10,name:'King',suit:suits[i]});
          break;
        }
    }
  }
  return cards;
}

function shuffle(cards) {
  for (var i = cards.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var temp = cards[i];
    cards[i] = cards[j];
    cards[j] = temp;
  }
  return cards;
}

function makeBigDeck(size) {
  deck = newDeck();
  for (var i = 1; i < size; i++){
    deck = deck.concat(newDeck());
  }
  shuffle(deck);
  print( "There are " + deck.length + " cards in the deck.");
  print("The dealer has shuffled the deck and begins.");
}

function firstDeal() {
  playerCards = [0,0];
  dealerCards = [0,0];
  bet = 100;
  if (deck.length <= 11 * numDecks){
    print("Reshuffling deck");
    makeBigDeck(numDecks);
  }
  print("You have $" + playerMoney);
  print("You bet $" + bet);
  playerMoney -= bet;
  print("The dealer deals you a card");
  var card = deal();
  playerCards[0] = card;
  print("The dealer deals himself a card");
  var card = deal();
  dealerCards[0] = card;
  print("The dealer deals you a card");
  var card = deal();
  playerCards[1] = card;
  playerSum = sumCards(playerCards);
  printHand(playerCards);
  print("The dealer deals himself a card facedown");
  var card = deck.pop();
  dealerCards[1] = card;
  if (sumCards(playerCards) == 21){
    if(sumCards(dealerCards) == 21) {
        printHand(dealerCards, "The dealer")
        print("You and the dealer have have natural 21");
        print("You get your bet back");
        playerMone += bet;
        s = state[2];
    } else {
      print("You have a natural 21");
      print("You get one and a half your bet");
      playerMoney += bet*1.5;
      s = state[2];
    }
  } else
  s = state[1];
}

function sumCards(cards) {
  var sum = 0;
  var hasAce = false;
  for (var i = 0; i < cards.length; i++){
    if (cards[i].name == 'Ace') hasAce = true;
    sum += cards[i].value;
  }
  if (hasAce && (sum + 10) <= 21) sum +=10;
  return sum;
}

function printHand(cards, pronoun = 'Your') {
  var text = pronoun + ' hand is: <br />';
  for (var i = 0; i < cards.length; i++){
    text += cards[i].name + " ";
  }
  text += "<br />Totaling " + sumCards(cards);
  print(text);
}

function deal() {
  var card = deck.pop();
  print(card.name + " of " + card.suit);
  return card;
}

function hit() {
  var card  = deal();
  playerCards.push(card);
  printHand(playerCards);
  if (sumCards(playerCards) > 21) {
    print ("You busted");
    print ("Press Enter to continue")
    s = state[2];
  }
}

function stand() {
  print ("The dealer reveals their facedown card")
  print(dealerCards[1].name + " of " + dealerCards[1].suit);
  printHand(dealerCards, 'The dealers');
  while (sumCards(dealerCards) < 17){
    print("The dealer draws himself a card");
    dealerCards.push(deal());
    printHand(dealerCards, 'The dealers');
  }
  if (sumCards(dealerCards) > 21){
    print("Dealer busts");
    print("You get double your bet");
    playerMoney += bet*2;
  }
  else if (sumCards(dealerCards) < sumCards(playerCards)) {
    print("You win");
    print("You get double your bet");
    playerMoney += bet*2;
  } else if (sumCards(dealerCards) == sumCards(playerCards)) {
    print("You tie with the dealer");
    print("You get your bet back");
    playerMoney += bet;
  } else {
    print("Dealer wins");
  }
  print("Press Enter to continue");
  s = state[2];
}

function doubleDown() {
  print("You double your bet");
  print("The dealer deals you a card");
  playerMoney -= bet;
  bet = bet * 2;
  hit();
  if (s == "Play")
    stand();
}

function playerAction(act) {
  act = act.toLowerCase()
  var a = act[0];
  if (act == 'restart')
    intro();
  switch (s) {
    case "Opening":
    if (!isNaN(act)){
      if (act != 0) numDecks = act;
      makeBigDeck(act);
      firstDeal();
    }
    else
      print("Enter the number of decks to use");
    break;
    case "Play":
    var a = act[0];
    if (act[1] == 'p') {
      a = '/'
    }
    switch (a){
      case "d":
      print ("You double down");
      if (8 < sumCards(playerCards) &&
          sumCards(playerCards) < 12
          && playerCards.length == 2) {
        doubleDown();
      } else
      print("Your card total must be 9, 10, or 11 and only have 2 cards in a hand");
      break;
      case "h":
      print ("You hit");
      hit();
      break;
      case "s":
      print ("You stand");
      stand();
      break;
      case '/':
      print ("You split");
      break;
    }
    break;
    case "Resolve":
    firstDeal();
    break;
  }
}
