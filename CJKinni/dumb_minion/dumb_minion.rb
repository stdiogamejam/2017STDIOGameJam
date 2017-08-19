def prompt
	print "> "
	gets.chomp
end

class Card
	attr_accessor :victory, :treasure, :cost, :description, :action
	def initialize(victory, treasure, cost=0, description="Basic Card", action=lambda {|state| state})
		@victory = victory
		@treasure = treasure
		@cost = cost
		@action = action
		@description = description
	end
end

def discard_hand(state)
	state[:hand].each_with_index do |c, i|
		discard_card(state, i) unless c.nil?
	end
	state
end

def discard_card(state, position)
	state[:discard] << state[:hand][position]
	state[:hand][position] = nil
	state
end

def draw_hand(state)
	state = discard_hand(state)
	state[:hand].clear
	state = draw_card(state) while state[:hand].size < 5
	state
end

def draw_card(state)
	if state[:deck].size == 0
		state[:deck] = state[:discard].shuffle 
		state[:discard] = []
		puts ">>> Shuffling discard pile back into deck."
	end
	state[:hand] << state[:deck][0]
	state[:deck].delete_at(0)
	state
end

def setup_next_turn(state)
	game_win(state) if get_vp(state) >= 20
	state = draw_hand(state)
	state[:turn_count] += 1
	state[:turn_order] = 0
	state[:round_treasure] = 0
	state[:round_treasure_inc] = 0
	state[:round_treasure_mult] = 0
	state
end

def get_vp(state)
	vp = 0
	state[:deck].each do |c|
		vp += c.victory
	end
	state[:hand].each do |c|
		vp += c.victory unless c.nil?
	end
	state[:discard].each do |c|
		vp += c.victory
	end
	vp
end

def show_board(state)
	puts " - - - - - - - - - - - - - TURN #{state[:turn_count]} - - - - - - - - - - - - -"
	puts " - #{state[:discard].size} cards in discard pile."
	puts " - #{state[:deck].size} cards in deck."
	puts " - #{get_vp(state)} total Victory Points in Deck."
	puts " - #{state[:round_treasure]} gold available this turn."
	puts " - SKIP ~ Skip turn and discard your current hand."
	state[:board].each_with_index do |c, i|
		puts " - Buy B#{i+1} ~ Board: #{c[0]} in stock, #{c[1].victory} VP, #{c[1].treasure} Treasure, #{c[1].cost} Price ~ #{c[1].description}"
	end
end

def show_hand(hand)
	hand.each_with_index do |c, i|
		puts " - Use U#{i+1} ~ In Hand: #{c.victory} VP, #{c.treasure} Treasure ~ #{c.description}" unless c.nil?
		puts " - Use U#{i+1} ~ Card already used or trashed this turn.  Skip or buy a card to continue." if c.nil?
	end
end

def use_card(position, state)
	used_card = state[:hand][position]
	state = discard_card(state, position)
	state[:round_treasure] += used_card.treasure
	if (used_card.treasure > 0)
		while state[:round_treasure_mult] != 0
			state[:round_treasure] += used_card.treasure
			state[:round_treasure_mult] -= 1
			puts ">>> gained #{used_card.treasure} extra treasure from the Gold Multiplier Special Card"
		end
		(1..state[:round_treasure_inc]).each do |i|
			state[:round_treasure] += 2
			puts ">>> gained 2 treasure from Additional Gold Special Card"
		end
	end
	puts ">>> Gained #{used_card.treasure} treasure and discarded card from your hand."
	state = used_card.action.call(state)
	state
end

def parse_input(prompt, state)
	if prompt.downcase[0] == 'u' && !prompt[1..-1].to_i.nil? && prompt[1..-1].to_i > 0 && prompt[1..-1].to_i <= state[:hand].size  && !state[:hand][prompt[1].to_i-1].nil?
		state = use_card(prompt[1..-1].to_i - 1, state)
	elsif prompt.downcase == 'bono' || prompt.downcase == 'the edge'
		state = use_card(1, state)
	elsif prompt.downcase[0] == 'b'
		if state[:board][prompt[1].to_i-1][1].cost <= state[:round_treasure]
			if state[:board][prompt[1].to_i-1][0] > 0
				state[:discard] << state[:board][prompt[1].to_i-1][1]
				state[:board][prompt[1].to_i-1][0] -= 1
				puts ">>> Bought card."
				state[:turn_order] = -1
			else
				puts ">>> There are no more copies of that card on the board."
			end
		else
			puts ">>> That card costs #{state[:board][prompt[1].to_i-1][1].cost}, but you only have #{state[:round_treasure]}."
		end
	elsif prompt.downcase == "exit"
		puts "Was it something I said?"
		exit
	elsif prompt.downcase == "help"
		puts state[:help_text]
	elsif prompt.downcase == "skip"
		state[:turn_order] = -1
	else
		puts ">>> Uknown Command."
	end
	state
end

def game_win(state)
	puts "\n\nYOU WIN!\n\nScore:\n- Turns: #{state[:turn_count]}\n- Cards in Deck: #{state[:deck].size + state[:hand].size + state[:discard].size}\n\nThanks for playing!\n"
	exit
end

treasure_multiplier_inc = Proc.new do |state|
	state[:round_treasure_mult] += 1
	state
end

treasure_incrementer_inc = Proc.new do |state|
	state[:round_treasure_inc] += 1
	state
end

trash_remaining_cards = Proc.new do |state|
	state[:hand] = [nil, nil, nil, nil, nil]
	state
end

state = {:hand => [], :deck => [], :discard => [], :board => [], :round_treasure => 0, :round_treasure_inc => 0, :round_treasure_mult => 0, :turn_order => 0, :turn_count => 0}
state[:help_text] = "DUMB MINION\nA quick and dirty deck building game.\n\n HOW TO PLAY\n\nYour goal is to have 20 Victory Points (VP) in your deck as quickly as possible.  You can achieve this goal through two actions: \n - Using cards in your hand by typing 'u' and the number of the card. e.g. 'u2'.  Card you use go into your discard pile.\n - Buying cards that will then go into your deck.\n\n PILES OF CARDS\n\n Your cards are split between three piles:\n- Deck\n- Hand\n- Discard \n\n TURN ORDER\n\n 1. Draw five cards from your Deck to your Hand.  At the start of your turn, you draw five cards from your deck.  If you don't have enough cards in your deck, your discard pile will be shuffled back into your deck.\n 2. Use Cards.  You may use as many cards from your hand as you would like.\n 3. Buy Cards.  You may only buy one card each turn, once you buy your card, your turn will be over.\n 4. Discard Hand.  Your hand will be automatically discarded into the discard pile.\n\n NOTES\n\nYou can type multiple commands in one line.  E.g. 'u1 u2 u4 u5 b1' will use cards 1, 2, 4, and 5, then buy card 1.\nAt the beginning of the game you start with 5 Victory scoring cards that have no other use, and 5 Treasure cards that grant 1 gold when used.  You may use gold to buy additional cards from the shop, they will be deposited into your discard pile so they may be used in future turns.  There are 8 copies of each card available at the shop.\n The game is about managing what you have in your hand so that you can build an engine to efficiently buy VP.\n\nIf your lost, but want to give it a try, try Dominion instead.  It's an amazing card game.\n\n The game ends when you have more than 20 VP.\n\nGood Luck!\n\n"

print state[:help_text]
# turn_order is just an integer that loops through the order of the game:
# 0 - Use Cards.  You can keep using cards that have a use.
# 1 - Buy Cards.  You can buy one card per turn, unless you get some additional buys.
# -1 - Prepare to Draw.  This is the last stage of the turn, and triggers prep for the next turn.

(0..4).each { state[:deck] << Card.new(0, 1) }
(0..4).each { state[:deck] << Card.new(1, 0, 2) }
state[:deck] = state[:deck].shuffle

state[:board] << [8, Card.new(0, 1, 0)]
state[:board] << [8, Card.new(0, v = rand(2) + 2, v + 1)]
state[:board] << [8, Card.new(0, v = rand(2) + 4, v + 1)]
state[:board] << [8, Card.new(v = rand(4) + 2, 0, v * 2)]
state[:board] << [8, Card.new(v = rand(4) + 7, 0, v * 2)]
state[:board] << [8, Card.new(0, v = rand(2), v, "Special: The all treasures you play this turn gains you an extra 2 gold.", treasure_incrementer_inc)]
state[:board] << [8, Card.new(0, v = rand(4), v + 5, "Special: The next treasure you play this turn gains you 2 times as much gold.", treasure_multiplier_inc)]
state[:board] << [8, Card.new(0, v = rand(1), v + 1, "Special: All cards in your hand after playing this card are permenantly trashed.", trash_remaining_cards)]

state = draw_hand(state)

while true
	state = setup_next_turn(state) if state[:turn_order] == -1
	show_board(state)
	show_hand(state[:hand])
	prompt.split(" ").each do |command|
		state = parse_input(command, state)
	end
end
