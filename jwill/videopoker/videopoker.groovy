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

/**
 * Class that stores a representation of decks of cards.
 *
 */
class Deck {
    /** File on disk that stores the definition of the cards. */
    def file = new File("cards.json")

    /** Collection of all the cards in this set of decks. */
    private ArrayList cards = new ArrayList<>();

    /** Number of decks to generate. */
    private int numDecks = 2;

    Deck(int numDecks) {
        initCards();
    }

    /** Using the numDecks variable, add the full set of cards to the cards collection that many times.
     * The default value of numDecks is 2 so you can call this function with initCards() or initCards(<someNumber>).
     *
     * In Groovy, a JSON file is parsed into a collection of ArrayLists and Maps(dictionaries in Python).
     * In an app with more space, you could wrap the representation of a card in a class.
     * @param numDecks
     */
    void initCards(int numDecks = 2) {
        def deckOfCards = new JsonSlurper().parse(file)
        cards = new ArrayList()
        numDecks.times { cards.addAll(deckOfCards) }
    }

    /**
     * Produces a random number under a certain value. Math.random generates a number between 0.0 and 1.0.
     * Multiplying that by max turns it into a whole number.
     * @param max
     * @return an integer
     */
    int rand(int max) { return (int) Math.floor(Math.random() * max); }

    /** Shuffles the deck of cards.
     *  Starting at the end of the cards, swap the positions of the selected card and one that
     *  appears in the collection of cards. Do this numDecks times.
     */
    void shuffleDecks() {
        for (int j = 0; j < numDecks; j++) {
            for (int i = (numDecks * 51); i >= 0; i--) {
                int r = rand(i);
                cards.swap(i, r)
            }
        }
    }

    /**
     * Removes a card from the card from the collection of cards. If there are no cards left,
     * the deck is reshuffled before returning a card.
     * @return a (Hash)Map of a card
     */
    Map dealCard() {
        if (cards.size() == 0)
            initCards()
        return (Map) cards.remove(0)
    }

    /**
     * Deals a number of cards
     * @param num the number of cards to return
     * @return an arraylist holding the cards
     */
    ArrayList dealCards(int num) {
        ArrayList cards = new ArrayList<Map>();
        for (int i = 0; i < num; i++) {
            cards.add(dealCard());
        }
        return cards;
    }

}

/**
 * Class that stores a representation of a poker hand. In this case, 5 cards.
 */
class Hand {
    /**
     * Holds the cards in a hand
     */
    ArrayList<Map> cards = new ArrayList<>()

    /**
     * Position to insert the next card.
     */
    private int position = 0

    /**
     * Iterates through the cards and looks for one that has the replaceCard property
     * set to true in it.
     *
     * This can return null.
     * @return Map representing a playing card
     */
    Map findCardToReplace() {
        for (Map card in cards) {
            boolean replaceCard = (boolean) card.get("replaceCard")
            if (replaceCard == true) return card;
        }
    }

    /**
     * Add a card represented by a map to a hand.
     * It attempts to replace the first card that findCardToReplace has found.
     * @param card
     */
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

    /**
     * Returns an integer indicating the number of cards that are flagged as replaceCard.
     * @return
     */
    int cardsNeeded() {
        if (cards.size() == 0) return 5
        else return cards.findAll { it.replaceCard == true }.collect { it.positionInHand }.size()
    }

    /**
     * Prints out a representation of a hand.
     */
    void printHand() {
        println "-------"
        cards.eachWithIndex { Map entry, int i ->
            def replace = entry.replaceCard == true ? " Replace " : " Keep "
            println("[${i}${replace}]:" + entry.face + " of " + entry.suit + "s")
        }

        println "-------"
    }

    /**
     * Clears all cards from the hand, sets the position to insert the next card to 0.
     */
    void clearCards() {
        cards.clear()
        position = 0
    }

}

/**
 * Class that evaluates a poker hand to see if it has won or lost
 */
class Evaluator {

    /** Stores the payout chart and descriptions. */
    ArrayList payouts = new JsonSlurper().parse(new File("base_payouts.json"))
    /**
     * Retrieves the numeric value of each card. Groovy's collect closure tells the cards ArrayList that on every card,
     * run the code get("value"), collect those items into a list and return it.
     * @param cards
     * @return
     */
    ArrayList ordinalHandler(ArrayList<Map> cards) { cards.collect { it.get("value") } }

    /**
     * Retrieves the suit of each card. Also uses Groovy's collect closure.
     * @param cards
     * @return
     */
    ArrayList suitHandler(ArrayList<Map> cards) { cards.collect { it.get("suit") } }

    /**
     * Returns the number of cards that whose values show up in the hand multiple times
     * @param cards
     * @param sizeToCheck the number of matches to check for.
     * @return
     */
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

    /**
     * Cycles through all the check functions to see if the game should pay out for a win.
     * Starts from the end of the results array to make sure the highest possible payout is used.
     * @param hand
     * @param round
     * @return
     */
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

/**
 * Class where our main game logic lives.
 */
class VideoPoker {
    /** Streams user input to the game. */
    Scanner scanner = new Scanner(System.in)

    Hand hand = new Hand()
    Deck deck = new Deck(2)
    Evaluator evaluator = new Evaluator()
    /** Starting number of tokens */
    int tokens = 500
    int maxBet = 5
    int currentBet = 1
    int roundState = 0
    /** When the player hits Q, this is toggled to true and the game ends. */
    boolean quitGame = false

    /**
     * Show the initialization screen and shuffle the decks.
     */
    void init() {
        println "Welcome to Video Poker!\n"
        println(new File("how_to_play.txt").getText())
        deck.shuffleDecks()
        processInput()
    }

    /**
     * Deal the cards and handle cleanup and evaluation of a player's hand as well as
     * awarding and reserving tokens.
     */
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
                println "You lost. Play again? \nUse i to set your bet or hit d to continue with the last bet."
            }
            roundState++
        }
    }

    /**
     * Deal the needed cards.
     * If it is after the player has selected a bet, 5 cards are drawn.
     * At any other point, it's the number of cards the player has elected to replace.
     */
    void dealHand() {
        int numCards = hand.cardsNeeded()
        numCards.times { hand.addToHand(deck.dealCard()) }
    }

    /**
     * Increment the players bet by one. It rolls over to 1 when the maximum bet is reached.
     */
    void incrementBet() {
        if (roundState != 1) {
            currentBet >= maxBet ? currentBet = 1 : currentBet++
            println "Your bet is now: ${currentBet}"
        } else { println "You can't change your bet right now."}
    }

    /**
     * Display a representation of the game state.
     * @param showEvaluator whether or now to tell the player what hand they are holding.
     */
    void drawScreen(boolean showEvaluator = true) {
        println "Bet: ${currentBet}\nTokens: ${tokens}"
        hand.printHand()
        if (showEvaluator && !hand.getCards().isEmpty()) {
            def result = evaluator.evaluate(hand, roundState)
            if (!result.isEmpty()) println("You have a " + result.label)
            println "Enter the number of the cards you would like to keep or replace. Deal when done."
        }
    }

    /**
     * Process the input from a user.
     */
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
                    println("Payout Chart and Descriptions")
                    for (item in evaluator.payouts) {
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

    // This is run in the application is run from inside a jar file.
    public static void main(String[] args) {
        def poker = new VideoPoker()
        poker.init()
    }
}

// This is run if the file is run as a script
def poker = new VideoPoker()
poker.init()