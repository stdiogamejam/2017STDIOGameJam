/*
Video Poker

Copyright (c) 2017 James Williams

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*/

import groovy.json.JsonSlurper


class Deck {
    // Stores card data
    def file = new File("cards.json")

    private ArrayList cards = new ArrayList<>();
    private int numDecks = 2;

    public Deck(int numDecks) {
        initCards();
    }

    void initCards() {
        def deckOfCards = new JsonSlurper().parse(file)
        cards = new ArrayList()
        numDecks.times { cards.addAll(deckOfCards) }
    }

    // Shuffle cards
    int rand(int max) { return (int) Math.floor(Math.random() * max); }

    void shuffleDecks() {
        for (int j = 0; j < numDecks; j++) {
            for (int i = (numDecks * 51); i >= 0; i--) {
                int r = rand(i);
                cards.swap(i, r)
            }
        }
    }

    Map dealCard() {
        if (cards.size() == 0)
            initCards()
        return (Map) cards.remove(0)
    }

    ArrayList dealCards(int num) {
        ArrayList cards = new ArrayList<Map>();
        for (int i = 0; i < num; i++) {
            cards.add(dealCard());
        }
        return cards;
    }

}

class Hand {
    ArrayList<Map> cards = new ArrayList<>()
    private int position = 0    //position to insert card

    Map findCardToReplace() {
        for (Map card in cards) {
            boolean replaceCard = (boolean) card.get("replaceCard")
            if (replaceCard == true) return card;
        }
    }

    void addToHand(Map card) {
        if (cards.size() < 5) {
            card.putAll(["positionInHand": position++, "replaceCard": true])
            cards.add(card)
        } else {
            Map cardToReplace = findCardToReplace()
            if (cardToReplace != null) {
                card.put("positionInHand", cardToReplace.get("positionInHand"))
                cards.set(cardToReplace.get("positionInHand"), card)
            }
        }
    }

    int cardsNeeded() {
        if (cards.size() == 0) return 5
        else return cards.findAll { it.replaceCard == true }.collect { it.positionInHand }.size()
    }

    void printHand() {
        println "-------"
        cards.eachWithIndex { Map entry, int i ->
            def replace = entry.replaceCard == true ? " Replace " : " Keep "
            println("[${i}${replace}]:" + entry.face + " of " + entry.suit + "s")
        }

        println "-------"
    }

    void clearCards() {
        cards.clear()
        position = 0
    }

}

class Evaluator {
    ArrayList payouts = new JsonSlurper().parse(new File("base_payouts.json"))
    // basically this handles cards' face value
    ArrayList ordinalHandler(ArrayList<Map> cards) { cards.collect { it.get("value") } }

    ArrayList suitHandler(ArrayList<Map> cards) { cards.collect { it.get("suit") } }

    Integer checkSize(ArrayList cards, int sizeToCheck) {
        def cardsValues = ordinalHandler(cards)
        HashMap<Integer, Integer> map = new HashMap<>()
        for (cardsValue in cardsValues) {
            if (map.get(cardsValue) == null) map.put(cardsValue, 1)
            else map.put(cardsValue, map.get(cardsValue) + 1)
        }
        map.findAll { it.value == sizeToCheck }.size()
    }

    boolean checkJacksOrBetter(Hand hand) {
        def cardsValues = ordinalHandler(hand.getCards())
        HashMap<Integer, Integer> map = new HashMap<>()
        for (cardsValue in cardsValues) {
            if (map.get(cardsValue) == null) map.put(cardsValue, 1)
            else map.put(cardsValue, map.get(cardsValue) + 1)
        }
        def pairs = map.findAll { it.value == 2 }
        def v = [1, 11, 12, 13]
        for (pair in pairs) {
            if (pair.key == 1 || pair.key == 11 || pair.key == 12 || pair.key == 13)
                return true
        }
        return false
    }

    boolean checkPair(Hand hand) { return checkSize(hand.getCards(), 2) }

    boolean checkTwoPair(Hand hand) { return checkSize(hand.getCards(), 2) == 2 }

    boolean checkThreeKind(Hand hand) { return checkSize(hand.getCards(), 3) }

    boolean checkFullHouse(Hand hand) { return checkPair(hand) && checkThreeKind(hand) }

    boolean checkFourKind(Hand hand) { return checkSize(hand.getCards(), 4) }

    boolean checkStraight(Hand hand) {
        def values = ordinalHandler(hand.getCards()).sort()
        if (values == [1, 10, 11, 12, 13])      // handle 10-A condition
            return true
        else {
            Integer startValue = (Integer) values.get(0);
            for (int i = 0; i < 5; i++) {
                Integer currentValue = (Integer) values.get(i)
                if ((startValue + i) != currentValue)
                    return false
            }
            return true
        }
    }

    boolean checkFlush(Hand hand) { return suitHandler(hand.cards).unique().size() == 1 }

    boolean checkStraightFlush(Hand hand) {
        if (checkFlush(hand) && checkStraight(hand))
            return true
        return false
    }

    boolean checkRoyalFlush(Hand hand) {
        def values = ordinalHandler(hand.getCards()).sort()
        if (values == [1, 10, 11, 12, 13] && suitHandler(hand.getCards()).unique().size() == 1)
            return true
        else return false
    }

    Map evaluate(Hand hand, int round) {
        def results = []
        results.addAll([checkJacksOrBetter(hand), checkTwoPair(hand), checkThreeKind(hand), checkStraight(hand), checkFlush(hand),
                        checkFullHouse(hand), checkFourKind(hand), checkStraightFlush(hand), checkRoyalFlush(hand)])
        for (int i = payouts.size() - 1; i >= 0; i--) {
            if (results[i] == true && round != 2) {
                return payouts.get(i)
                break
            }
        }
        return [:]
    }
}

class VideoPoker {
    Scanner scanner = new Scanner(System.in)

    Hand hand = new Hand()
    Deck deck = new Deck(2)
    Evaluator evaluator = new Evaluator()
    int tokens = 500
    int maxBet = 5
    int currentBet = 1
    int roundState = 0
    boolean quitGame = false

    void init() {
        println "Welcome to Video Poker!\n"
        println(new File("how_to_play.txt").getText())
        deck.shuffleDecks()
        processInput()
    }

    void deal() {
        if (roundState == 2)
            roundState = 0
        if (roundState == 0) {
            hand.clearCards()
            tokens -= currentBet
            dealHand()
            roundState++
            return
        }

        if (roundState == 1) {
            dealHand()
            drawScreen(false)
            Map result = evaluator.evaluate(hand, roundState)
            if (result.isEmpty() != true) {
                println "You win ${currentBet * result.payout} tokens! You had a ${result.label}!"
                tokens += currentBet * result.payout
            } else {
                println "You lost. Play again? \n Use i to set your bet or hit d to continue with the last bet."
            }
            roundState++
        }
    }

    void dealHand() {
        int numCards = hand.cardsNeeded()
        numCards.times { hand.addToHand(deck.dealCard()) }
    }

    void incrementBet() {
        if (roundState != 1) {
            currentBet >= maxBet ? currentBet = 1 : currentBet++
            println "Your bet is now: ${currentBet}"
        } else { println "You can't change your bet right now."}
    }

    void drawScreen(boolean showEvaluator = true) {
        println "Bet: ${currentBet}\nTokens: ${tokens}"
        hand.printHand()
        if (showEvaluator && !hand.getCards().isEmpty()) {
            def result = evaluator.evaluate(hand, roundState)
            if (!result.isEmpty()) println("You have a " + result.label)
            println "Enter the number of the cards you would like to keep or replace. Deal when done."
        }
    }

    void processInput() {
        while (quitGame != true) {
            String input = scanner.nextLine()
            try {
                Integer.valueOf(input)
                for (number in input) {
                    Map card = hand.getCards().get(number as Integer)
                    card.put("replaceCard", !card.replaceCard)
                }
                drawScreen()
            } catch (NumberFormatException ex) { /* This isn't a number process it otherwise */}

            switch (input) {
                case "Q": case "Quit": case "quit": case "q":   // Quit the game
                    quitGame = true
                    break
                case "H": case "h": // Show how to play
                    println(new File("how_to_play.txt").getText())
                    break
                case "I": case "i": case "+": case "=":  // Increment bet
                    incrementBet()
                    break
                case "D": case "d":  // Deal
                    println "Dealing cards."
                    deal()
                    if (roundState != 2)
                        drawScreen()
                    break
                case "p": case "P":
                    def items = new JsonSlurper().parse(new File("base_payouts.json"))
                    println("Payout Chart and Descriptions")
                    for (item in items) {
                        def msg = ["Hand: ${item.label}",
                                   "Payout: ${item.payout}", "Description: \n${item.description}\n"].join("\n")
                        println msg
                    }
                    break
                case "r": case "R":
                    drawScreen()
                    break
                default:
                    break
            }
        }
    }
}

def poker = new VideoPoker()
poker.init()

//def hand = new Hand()
//hand.addToHand(["face": "ace", "value": 1, "suit": "club"])
//hand.addToHand(["face": "8", "value": 8, "suit": "heart"])
//hand.addToHand(["face": "2", "value": 2, "suit": "club"])
//hand.addToHand(["face": "3", "value": 3, "suit": "club"])
//hand.addToHand(["face": "ace", "value": 1, "suit": "club"])
//
//def eval = new Evaluator()
//
//println eval.evaluate(hand,1)