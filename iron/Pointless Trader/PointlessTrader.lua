-- STDIO gamejam entry

--In LUA, you can only call functions if you made them first, so the actual start point will be last in this script.
--You can ofcourse also load in other scripts, but I will not be doing that because you will need to be able to run this in a webbrowser lua demo.

--Lets create some variables here, in LUA you don't need to tell the computer which type your variable is(string, integer, etc..), the computer will sort that out based
--on the actual content of your variable.

gameTitle = "Pointless Trader" --Why not make it easy to change the game's title?
gameDescription = "In this text game, your goal is to become as rich as possible. Sell and buy gold at the right prices, \nonce a place has no gold left or is too expensive, you can leave in search for a better location.\n\nThis game is written in LUA, and was made for the STDIO game jam \nhosted by the \"Museum of Art and Digital Entertainment\""-- Same for the description.

turn = 0 --This is used to count in which turn the user is.
playerInput = "" --This will later be used to set the player's last input.
playerInutYesNoScore = 0 --This will be used to understand what the player meant if a typo is made.
playerInputTravelScore = 0
playerInputBuyScore = 0
playerInputSellScore = 0

playerMoney = 100 --Just adding some game variables
playerLocation = "Brabant"

locationBuyPrice = 10
locationSellPrice = 10

playerInventory = {["wood"] = 0, ["bronze"] = 0, ["iron"] = 0, ["copper"] = 0, ["clothes"] = 0, ["tin"] = 0, ["wool"] = 0, ["pots"] = 0, ["hemp"] = 0}
price = {["wood"] = 12.5, ["bronze"] = 12.5, ["iron"] = 12.5, ["copper"] = 12.5, ["clothes"] = 12.5, ["tin"] = 12.5, ["wool"] = 12.5, ["pots"] = 12.5, ["hemp"] = 12.5}

event = "" --Optional, to add flavour to the game.

--This is the buy function, it will buy goods.
function buy(good, ammount)
	
	if (playerMoney - (ammount * price[good])) >= 0 then --if the player can afford it, BUY
		playerMoney = playerMoney - (ammount * price[good])
		playerInventory[good] = playerInventory[good] + ammount
	else
		graphics("you can't afford this...", "noOptions", "buy")
		io.read()
	end

end

--This is the sell function, it will sell goods.
function sell(good, ammount)
	
	if (playerInventory[good] >=  ammount) then --If the player can sell it, SELL
		playerInventory[good] = playerInventory[good] - ammount
		playerMoney = playerMoney + (ammount * price[good])
	else
		graphics("you can't sell what you don't own...", "noOptions", "sell")
		io.read()
	end
	
	

end

--This is the travel function, it will travel the player to a random "location".
function travel()
	locations = {"Brabant", "MicroPose", "Snijder", "New Kork", "North Dorea", "Timland", "Jakka", "Placebo", "Dubra", "Ugla"}
	math.randomseed(os.time()) --change the gold prices to a random value
	math.random(6,20)

	if (playerMoney - 20) >= 0 then
		for key,value in pairs(price) do
			price[key] = math.random(5, 30)
		end
		playerLocation = locations[math.random(1,10)]
		playerMoney = playerMoney - 20
	else
		graphics("You can't afford to travel..", "noOptions", "travel")
		io.read()
	end

end

--This is the graphics function, it will draw all information into the screen.
function graphics(writeSentence, options, case)
	--Lets clear the console first, this is OS dependant, so you need an if-statement.
	if not os.execute("clear") then
		os.execute("cls")
	elseif not os.execute("cls") then
		for i = 1,25 do
			print("\n\n")
		end
	end
	
	if case == "main" then
		
		--After that we have cleared the screen, lets print to our hearts content.
		io.write(gameTitle .. "\n")
		io.write("--------------------------------------------------------------------------------\n")
		io.write("Money: "..playerMoney.."\n") --Show the ammount of money.
		io.write("Location: ".. playerLocation .. "\n\n")	--Show the location. 
		
		for key,value in pairs(playerInventory) do
			io.write("owned " .. key .. ":" ..value.."\n")
		end
		
		 if not event == "" then io.write("\n" .. event .. "\n") end --maybe add some detail talk to it too.
		io.write("--------------------------------------------------------------------------------\n")
		if options == "showOptions" then --If options are requested, print those too.
		io.write ("Commands: Travel, Sell, Buy\n")
		end
		io.write(writeSentence .. "\n")
		io.write("--------------------------------------------------------------------------------\n")
		
	elseif case == "travel" then
		io.write(gameTitle .. "\n")
		io.write("--------------------------------------------------------------------------------\n")
		io.write("Money: "..playerMoney.."\n") --Show the ammount of money.
		io.write("Location: ".. playerLocation .. "\n\n")	--Show the location. 
		for key,value in pairs(playerInventory) do
			io.write("owned " .. key .. ":" ..value.."\n")
		end
		
		
		io.write("\n" .. writeSentence .. "\n")
	elseif case == "buy" then
		io.write(gameTitle .. "\n")
		io.write("--------------------------------------------------------------------------------\n")
		io.write("Money: "..playerMoney.."\n") --Show the ammount of money.
		io.write("Location: ".. playerLocation .. "\n\n")	--Show the location. 
		
		for key,value in pairs(playerInventory) do
			io.write("owned " .. key .. ":" ..value.."\n")
		end
		
		io.write("\n")
		
		for key,value in pairs(price) do
			io.write("price of " .. key .. ":" ..value.."\n")
		end
		
		io.write("\n" ..writeSentence .. "\n")
	elseif case == "sell" then
		io.write(gameTitle .. "\n")
		io.write("--------------------------------------------------------------------------------\n")
		io.write("Money: "..playerMoney.."\n") --Show the ammount of money.
		io.write("Location: ".. playerLocation .. "\n\n")	--Show the location. 
		
		for key,value in pairs(playerInventory) do
			io.write("owned " .. key .. ":" ..value.."\n")
		end
		
		io.write("\n")
		
		for key,value in pairs(price) do
			io.write("price of " .. key .. ":" ..value.."\n")
		end
		io.write("\n" ..writeSentence .. "\n")
	end
end

--This is the getInput function, it will use the input of the player and advance the turn correctly.
function getInput(case)
	if case == "turn" then --We'll will need to execute a turn.
		playerInput = io.read() --Getting the input.
		
		stringTable = {} --Creating a table, where all the characters of the players input will go into.
		for i = 1, #playerInput do --Using the gsub function we will convert the string into the table. #table Is the length of the string.
			stringTable[i] = playerInput:sub(i,i) --Every table entry = character from string
		end
		
		lookupTableTravel = {"T", "R", "A", "V", "E", "L", "t", "r", "a", "v", "e", "l"}
		lookupTableSell = {"S", "E", "L", "s", "e", "l"}
		lookupTableBuy  = {"B", "U", "Y", "b", "u", "y"}
		
		playerInputBuyScore = 0 --without doing this, our previous inputs keep counting...
		playerInputSellScore = 0
		playerInputTravelScore = 0
		
		for key,value in pairs(stringTable) do --Check for every character in the lookupTable If it is, change score. 
			for lookupKey,lookupValue in pairs(lookupTableTravel) do
				if value == lookupValue then playerInputTravelScore = playerInputTravelScore + 1 end
			end
			for lookupKey,lookupValue in pairs(lookupTableBuy) do
				if value == lookupValue then playerInputBuyScore = playerInputBuyScore + 1 end
			end
			for lookupKey,lookupValue in pairs(lookupTableSell) do
				if value == lookupValue then playerInputSellScore = playerInputSellScore + 1 end
			end
		end
		
		--now, check which score is the highest.
		valueSort = {playerInputBuyScore, playerInputSellScore, playerInputTravelScore}
		table.sort(valueSort) --sorting the table on value, from low to high.
		
		if valueSort[3] == playerInputTravelScore then playerInput = "travel" end --deciding the intended input
		if valueSort[3] == playerInputBuyScore then playerInput = "buy" end
		if valueSort[3] == playerInputSellScore then playerInput = "sell" end
		
	elseif case == "confirm" then --Is the players input yes or no, or something else?
		playerInput = io.read() -- Reading the player's input.
		playerInutYesNoScore = 0
		
		stringTable = {} --Creating a table, where all the characters of the players input will go into.
		for i = 1, #playerInput do --Using the gsub function we will convert the string into the table. #table Is the length of the string.
			stringTable[i] = playerInput:sub(i,i) --Every table entry = character from string
		end
		
		lookupTableYes = {"Y", "E", "S", "y", "e", "s"} --Table with possible character of yes.
		lookupTableNo = {"N", "O", "n", "o"} --The same for no.

		for key,value in pairs(stringTable) do --Check for every character if it is a "y","e","s","n" or "o". If it is, change score. 
			for lookupKey,lookupValue in pairs(lookupTableYes) do
				if value == lookupValue then playerInutYesNoScore = playerInutYesNoScore + 1 end
			end
			for lookupKey,lookupValue in pairs(lookupTableNo) do
				if value == lookupValue then playerInutYesNoScore = playerInutYesNoScore - 1 end
			end
		end
		
		--now, the only thing left to do is changing the player input to what the player meant.
		if playerInutYesNoScore > 0 then
			playerInput = "yes"
		elseif playerInutYesNoScore <= 0 then
			playerInput = "no"
		end	
	elseif case == "ammount" then
		playerInput = io.read()
		if (playerInput:match("%d")) then
			playerInput = tonumber(playerInput)
		else
			playerInput = 0
		end
		
	end
end

-- This is the main function, it is started first, and will contain calls to other functions.
function main()
	if turn == 0 then	--Only display information the first turn aka. startup.
		--If the game started, its probably a good idea to introduce the player first.
		io.write("Welcome to " .. gameTitle .. "\n\n") -- In LUA, you can use .. to stitch two strings together in order to make one big string.
		--After we've written the title of the game, who not give some basic information aswell?
		print(gameDescription) --I am using \n to indicate that there needs to be a line break, you could also use the print function to do this automatically.
		
		io.write ("\ntype yes to start.\ninput: ")
		getInput("confirm") --lets ask the player to start
		
		if playerInput == "yes" then --Making sure we leave the intro.
			turn = turn + 1
		end
		
	else
		graphics("What would you like to do?", "showOptions", "main") --Printing the basic UI
		getInput("turn") --What does the player want?
		
		if playerInput == "travel" then --make the player travel
			graphics("Are you sure you want to travel? yes/no\nTraveling costs 20 coins", "noOptions", "travel")
			getInput("confirm")
			
			if playerInput == "yes" then
				travel()
			end
			
		elseif playerInput == "buy" then --offer the player to buy gold
			graphics("What would you wish to buy?", "noOptions", "buy")
			playerInput = io.read()
			for key,value in pairs(price) do
				if playerInput == key then
					accepted = true
					good = playerInput
				end
			end
			if accepted then
				graphics("How much " .. good .." would you like to buy?", "noOptions", "buy")
				getInput("ammount")
				buy(good, playerInput)
				accepted = false
			else
				graphics("That good does not exist...", "noOptions", "buy")
				io.read()
			end
			
		elseif playerInput == "sell" then --offer the player to sell geld.
			graphics("What would you wish to sell?", "noOptions", "sell")
			playerInput = io.read()
			for key,value in pairs(price) do
				if playerInput == key then
					accepted = true
					good = playerInput
				end
			end
			if accepted then
				graphics("How much " .. good .." would you like to sell?", "noOptions", "sell")
				getInput("ammount")
				sell(good, playerInput)
				accepted = false
			else
				graphics("That good does not exist...", "noOptions", "sell")
				io.read()
			end
			
		end
		
		turn = turn + 1 --At the end of the turn, turn up the turn ammount.
	end
end

--Actually starting the game, by calling the main function.
while true do

playerInput = ""
main()

end
