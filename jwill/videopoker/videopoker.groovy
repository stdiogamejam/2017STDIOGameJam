import groovy.json.JsonSlurper


public class Deck {
    // Stores card data
    def file = new File("cards.json")

    private ArrayList cards = new ArrayList<>();
    private int numDecks;

    public Deck(int numDecks) {
        this.numDecks = numDecks;
        initCards();
    }

    void initCards() {
        def deckOfCards = new JsonSlurper().parse(file)
        cards = new ArrayList()
        numDecks.times {cards.addAll(deckOfCards)}
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
        if (cards.size() > 0) {
            return (Map)cards.remove(0)
        } else {
            initCards();
            return (Map)cards.remove(0);
        }
    }

    ArrayList dealCards(int num) {
        ArrayList cards = new ArrayList<Map>();
        for (int i = 0; i < num; i++) {
            cards.add(dealCard());
        }
        print "dealCards:" + cards
        return cards;
    }

}

public class Hand {
    ArrayList<Map> cards = new ArrayList<>()
    private int position = 0    //position to insert card

    Map findCardToReplace() {
        int i = 0
        for (Map card in cards) {
            boolean replaceCard = (boolean) card.get("replaceCard")
            if (state == true)
                return card;
        }
    }

    void addToHand(Map card) {
        if (cards.size() < 5) {
            card.putAll(["positionInHand": position++, "replaceCard": false])
            cards.add(card)
        } else {
            Map cardToReplace = findCardToReplace()
            if (cardToReplace != null) {
                card.put("positionInHand", cardToReplace.get("positionInHand"))
                cards.set(cardToReplace.get("positionInHand"), card)
            }
        }
    }

    void printHand() {
        for (c in cards) {
            println(c)
        }
    }

    void clearCards() {
        cards.clear()
        pos = 0
    }

}

class Evaluator {

    // rename to something simpler
    // basically this handles cards' face value
    ArrayList ordinalHandler(ArrayList<Map> cards) {
        cards.collect { it.get("value") }
    }

    ArrayList suitHandler(ArrayList<Map> cards) {
        cards.collect { it.get("suit") }
    }

    Integer checkSize(ArrayList cards, int sizeToCheck) {
        def cardsValues = ordinalHandler(cards)
        HashMap<Integer, Integer> map = new HashMap<>()
        for (cardsValue in cardsValues) {
            if (map.get(cardsValue) == null)
                map.put(cardsValue, 1)
            else map.put(cardsValue, map.get(cardsValue) + 1)
        }
        map.findAll{ it.value == sizeToCheck }.size()
    }

    boolean checkJacksOrBetter(Hand hand) {
        def cardsValues = ordinalHandler(hand.getCards())
        HashMap<Integer, Integer> map = new HashMap<>()
        for (cardsValue in cardsValues) {
            if (map.get(cardsValue) == null)
                map.put(cardsValue, 1)
            else map.put(cardsValue, map.get(cardsValue) + 1)
        }
        map.findAll{ it.value == 2 }.each {
            def v = [1,11,12,13]
            if (v.contains(it.key)) {
                return true
            }
        }
    }

    boolean checkPair(Hand hand) {
        return checkSize(hand.getCards(), 2)
    }

    boolean checkTwoPair(Hand hand) {
        return checkSize(hand.getCards(), 2) == 2
    }

    boolean checkThreeKind(Hand hand) {
        return checkSize(hand.getCards(), 3)
    }

    boolean checkFullHouse(Hand hand) {
        return checkPair(hand) && checkThreeKind(hand)
    }

    boolean checkFourKind(Hand hand) {
        return checkSize(hand.getCards(), 4)
    }

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
}

class VideoPoker {
    Scanner scanner = new Scanner(System.in)

    Hand hand = new Hand()
    Deck deck = new Deck(1)
    // Evaluator evaluator
    int tokens
    int maxBet = 5
    int currentBet = 1
    int roundState = 2
    boolean quitGame = false

    void init() {
        println "Welcome!"
        // deal throwaway hand
        deck.shuffleDecks()
        def cards = deck.dealCards(5)

        cards.each {hand.addToHand((Map)it)}
        println hand
        //evaluator = new Evaluator()
    }

    void deal() {
        // Round is over
        if (roundState == 2) {
            hand.clearCards()
            roundState = 0
        }
        if (roundState == 0) {
            tokens -= currentBet
            // TODO Update bet and tokens
        }
        dealHand()
        // TODO Show the cards
        // TODO Run evaluator

        if (roundState == 1) {
            // TODO Award winning hand if applicable
            // Display message
        }
        roundState++
    }

    void dealHand() {
        int numCards = hand.cardsNeeded()
        numCards.times {hand.addToHand(deck.dealCard())}
    }

    void incrementBet() {
        if (roundState != 1) {
            currentBet++
            if (currentBet > maxBet) currentBet = 1
        }
        // TODO drawBetAndTokens
    }

    void drawScreen() {
        
    }

    void processInput(){
        while(quitGame != true) {
            String input = scanner.nextLine()
            switch(input) {
                case "Q":case "Quit":case "quit": case "q":   // Quit the game
                    quitGame = true
                    break
                case "H": // Show how to play
                    println("how to play")
                    break
                case "I":case "i":  // Increment bet
                    incrementBet()
                    break
                case "D":case "d":  // Deal
                    break

            }
            println input
        }
    }
}

def poker = new VideoPoker()
poker.init()
poker.processInput()

// Screen options
// 1. How to play
// 2. Show pay table
// 3. Deal
// Select cards to hold
// Increment bet

