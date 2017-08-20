'''
Penalty Fever

MIT License
-----------

Copyright (c) 2017 Fabián Alfredo Arias
Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
'''

# Import the random module. This module is used to generate random numbers
import random 

# This constant contains the probability of success of the penalty kick 
# depending on the sector.
PENALTY_KICKS_PPROBABILITY = [86, 93, 86, 90, 97, 90, 80, 87, 80]

# This constant contains the probability that the goalkeeper 
# will save the penalty.
GOALKEEPER_SAVE_PROBABILITY = [[76, 14, 2], [13, 83, 13], [2, 14, 76], 
																[87, 18, 3], [17, 91, 17], [3, 18, 87], 
																[72, 12, 1], [11, 79, 11], [1, 12, 72]]

def menu():
  # This function show the menu.
  
  print('______                _ _          ______                  ')
  print('| ___ \              | | |         |  ___|                 ')
  print('| |_/ /__ _ __   __ _| | |_ _   _  | |_ _____   _____ _ __ ')
  print("|  __/ _ \ '_ \ / _` | | __| | | | |  _/ _ \ \ / / _ \ '__|")
  print('| | |  __/ | | | (_| | | |_| |_| | | ||  __/\ V /  __/ |   ')
  print('\_|  \___|_| |_|\__,_|_|\__|\__, | \_| \___| \_/ \___|_|   ')
  print('                             __/ |                         ')
  print('    by Fabián A. Arias      |___/    Released under MIT License ')
  print()
  print('1) Play')
  print('2) How to Play')
  print('3) Exit')
  print()
  
  
    
    
def getPlayerPenaltyKicks():
	# Let the player enter his penalty kicks.
	
  print('\n' * 10)
  print('Penalty kicks')
  print(' _____________________ ')
  print('|  _________________  | Choose the place where you want to kick')
  print('| |  6  |  7  |  8  | | each of the 5 penalties.')
  print('| |-----+-----+-----| | For example: 61682 means that the 1st penalty will go to ')
  print('| |  3  |  4  |  5  | | the upper left corner, 2nd to the lower middle,')
  print('| |-----+-----+-----| | 3rd to the same place as the 1st, 4th to the upper')
  print('| |  0  |  1  |  2  | | right corner and the 5th equal to the 2nd.')
  print()
  
  while True:
    playerPenaltyKicks= input('Enter your 5 penalty kicks: ')
    
		# Validate that the player enters 5 penalty kicks.
    if len(playerPenaltyKicks) != 5:       
      print('You must enter 5 penalty kicks.\n')
    else:
				# Validate that the player enters valid numbers.
        validPenaltyKicks = set('012345678')
        if not set(playerPenaltyKicks).issubset(validPenaltyKicks):
          print('You must enter only numbers from 0 to 8.\n')
        else:
          break
  
  return list(playerPenaltyKicks)

def getPlayerGoalKeeperDives():
		# Let the player enter his goalkeeper dives.
		
  print('\n' * 5)
  print('Goalkeeper')
  print(' _____________________')
  print('|  _________________  |')
  print('| |     |     |     | | Choose the sector where your goalkeeper will dive')
  print('| |     |     |     | | into each penalty.')
  print('| |  0  |  1  |  2  | | For example: 01121')
  print('| |     |     |     | |')
  print('| |     |     |     | |')
  print()
  
  while True:
    playerGoalKeeperDives= input('Enter your 5 goalkeeper dives: ')
    
		# Validate that the player enters 5 goalkeeper dives.
    if len(playerGoalKeeperDives) != 5:       
      print('You must enter 5 goalkeeper dives.\n')
    else:
				# Validate that the player enters valid numbers.
        validGoalKeeperDives = set('012')
        if not set(playerGoalKeeperDives).issubset(validGoalKeeperDives):
          print('You must enter only numbers from 0 to 2.\n')
        else:
          break
  
  return list(playerGoalKeeperDives)

def getAiPenaltyKicks():
	# The program generate its penalty kicks.
	
  aiPenaltyKicks = ''
  for i in range(5):
		# Use randint from random module to generate an integer between 0 and 8.
    aiPenaltyKicks += str(random.randint(0, 8))
  
  return list(aiPenaltyKicks)
  
def getAiGoalKeeperDives():
  aiGoalKeeperDives = ''
  for i in range(5):
    aiGoalKeeperDives += str(random.randint(0, 2))
  
  return list(aiGoalKeeperDives)

def processPenalties(shooter, goalkeeper):
	# Proccess the penalties.
	
	# contains the result of all penalties. 
	# Possible results: 1 = goal, 2 = saved, 3 = missed
  shooterPenaltyResults = '' 
  shooterGoals = 0
  
  for i in range(5):
		# Check if the penalty kick was missed.
    missProbability = random.randint(0, 100)
    if missProbability > PENALTY_KICKS_PPROBABILITY[int(shooter[i])]:
      shooterPenaltyResults += '3'
    else:
			# Check if the goalkeeper may save the penalty kick.
      canSaveProbability = random.randint(0, 100)
      if canSaveProbability > GOALKEEPER_SAVE_PROBABILITY[int(shooter[i])][int(goalkeeper[i])]:
        shooterPenaltyResults += '1'
        shooterGoals += 1
      else:
				# if the penalty was not missed and the goalkeeper may save it
        convertProbability = random.randint(0, 100)
        saveProbability = random.randint(0, 100)
        if convertProbability > saveProbability:
          # Goal
          shooterPenaltyResults += '1'
          shooterGoals += 1
        else:
					# Saved
          shooterPenaltyResults += '2'

  return shooterGoals, shooterPenaltyResults

def showResults(playerGoals, playerResults, aiGoals, aiResults):
	# Show the final score
	
  print('\n' * 8)
  if playerGoals > aiGoals: 
    print('Player wins!')
  elif playerGoals < aiGoals:
    print('AI wins!')
  else:
    print('It is a tie game')
  print('        ___________________________')
  print('       |   |   |   |   |   |       |')
  print('       | 1 | 2 | 3 | 4 | 5 | Goals |')
  print(' ______|___|___|___|___|___|_______|')
  print('|      |   |   |   |   |   |       |')
  print('|Player', end='')
  for i in range(5):
    if playerResults[i] == '1':
      print('| o ', end='')
    else:
      print('| x ', end='')
  print('|   ' + str(playerGoals) + '   |')
  print('|------|---+---+---+---+---|-------|')
  print('|    AI', end='')
  for i in range(5):
    if aiResults[i] == '1':
      print('| o ', end='')
    else:
      print('| x ', end='')
  print('|   ' + str(aiGoals) + '   |')
  print('|______|___|___|___|___|___|_______|')
  print('\n' * 6)
  
  
def playGame():
  playerPenaltyKicks = getPlayerPenaltyKicks()
  playerGoalKeeperDives = getPlayerGoalKeeperDives()
  
  aiPenaltyKicks = getAiPenaltyKicks()
  aiGoalKeeperDives = getAiGoalKeeperDives()
  
  playerGoals, playerPenaltyResults = processPenalties(playerPenaltyKicks, aiGoalKeeperDives)
  aiGoals,  aiPenaltyResults = processPenalties(aiPenaltyKicks, playerGoalKeeperDives)
  
  showResults(playerGoals, playerPenaltyResults, aiGoals, aiPenaltyResults)
  
  return 

def howToPlay():
  print('\n' * 5)
  print('How to play')
  print('-----------')
  print('For each play you must enter your instructions.')
  print('This is divided into two parts:')
  print('   Penalty kick: choose where you want to kick a particular penalty.')
  print('   Goalkeeper: you choose where your goalkeeper is thrown in a certain penalty.')
  print('You must enter the instructions for the 5 penalties.')
  print('\n' * 5)


while True:
	# Main loop
	
  menu()
  
  while True:
    # Let the player choose an option.
    menuOption = input('Choose an option: ')
    
    # Validate that the player enters a valid option.
    validMenuOptions = ['1', '2', '3']
    if menuOption in validMenuOptions:
      break
    
  if menuOption == '1':
	  #Play 
    playGame()
  elif menuOption == '2':
    #How to play
    howToPlay()
  else:
    break