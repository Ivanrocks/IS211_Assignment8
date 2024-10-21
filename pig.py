import random
import argparse
import time
from xmlrpc.client import Boolean


class Player:
    """
        The Player class represents a player in the Pig game.

        Attributes:
            name (str): The name of the player.
            score (int): The player's current score, initialized to 0.

        Methods:
            rollDie(): Simulates rolling a six-sided die.
            resetScore(): Resets the player's score to 0.
            addToScore(points): Adds the given points to the player's score.
            getName(): Returns the player's name.
            isComputer(): Returns False (overridden by the ComputerPlayer).
            getScore(): Returns the player's current score.
        """

    def __init__(self):
        """
               Initializes a new Player object with the given name and sets the score to 0.

               """
        self.name = self.askName()
        self.score = 0
    def rollDie(self):
        """
        Simulates rolling a six-sided die and returns the result.

        Returns:
            int: A random number between 1 and 6 (inclusive).
        """
        maxNumber = 6
        minNumber = 1
        return random.randint(minNumber, maxNumber)

    def askName(self):
        """
                Prompts the user to input their name and ensures the input is valid.

                Returns:
                    str: The player's name.
                """
        while True:
            name = input("Enter name of player: ")
            if name:
                return name
            else:
                print("Enter a valid name")

    def resetScore(self):
        """Resets the player's score to 0."""

        self.score = 0

    def addToScore(self, points):
        """
                Adds the given number of points to the player's current score.
                Args:
                    points (int): The number of points to add.
        """
        self.score += points

    def getName(self):
        """Returns the player's name."""

        return self.name
    def isComputer(self):
        """Returns False, indicating this is not a computer player."""

        return False

    def getScore(self):
        """Returns the player's current score."""

        return self.score
class HumanPlayer(Player):
    """Represents a human player in the game."""

    pass

class ComputerPlayer(Player):
    """
        Represents a computer player in the Pig game.

        Methods:
            isComputer(): Returns True to indicate the player is controlled by the computer.
            shouldHold(score_total, turnScore): Implements the strategy for when the computer should hold.
            decideMove(turn_score_total, turnScore): Decides whether to roll or hold based on the computer's strategy.
        """


    def isComputer(self):
        """Returns True to indicate this is a computer player."""

        return True
    def shouldHold(self,score_total, turnScore):
        """
                Determines if the computer should hold based on its score and the turn score.

                Args:
                    score_total (int): The total score of the computer.
                    turnScore (int): The score accumulated during the current turn.

                Returns:
                    bool: True if the computer should hold, False otherwise.
                """
        target_hold_value = min(25, 100 - self.getScore())
        print("Turn_total" + str(score_total))
        print("target: " + str(target_hold_value))
        return turnScore  >= target_hold_value

    def decideMove(self, turn_score_total, turnScore):
        """
                Decides whether the computer should roll or hold.

                Args:
                    turn_score_total (int): The computer's total score for the turn.
                    turnScore (int): The points accumulated in the current turn.

                Returns:
                    str: 'h' for hold or 'r' for roll.
                """
        if self.shouldHold(turn_score_total, turnScore):
            return 'h'
        else:
            return 'r'


class PlayerFactory:
    """
        A factory class to create Player objects.

        Methods:
            createPlayer(player_type): Creates a ComputerPlayer or HumanPlayer based on the input.
        """
    @staticmethod
    def createPlayer(player_type):
        """
                Creates and returns a player object based on the provided type.

                Args:
                    player_type (str): The type of player ('computer' or 'human').

                Returns:
                    Player: An instance of ComputerPlayer or HumanPlayer.
                """
        if player_type == "computer" or player_type == "c":
            return ComputerPlayer()
        else:
            return HumanPlayer()
class Game:
    """
    Represents the Pig dice game.

    Attributes:
        players (list of Player): A list of Player objects participating in the game.
        scoreToWin (int): The score required to win the game (default is 100).
        current_player (int): The index of the current player in the players list.
        rulesMessage (str): A message displaying the rules of the game.

    Methods:
        switchPlayer(): Switches to the next player.
        turn(player): Handles the player's turn, including rolling or holding.
        is_winner(player, turnScore=0): Checks if a player has won.
        printScores(): Prints the current scores of all players.
        play(): Starts and manages the game until a winner is determined.
    """
    rulesMessage = '''The rules of Pig are simple. The game features two players, whose goal is to reach 100 points first. 
    Each turn, a player repeatedly rolls a die until either a 1 is rolled or the player holds and scores the sum of the
rolls (i.e. the turn total). At any time during a player's turn, the player is faced with two decisions:
- roll: If the player rolls a
    1: the player scores nothing and it becomes the opponent's turn.
    2 - 6: the number is added to the player's turn total and the player's turn continues.
- hold: The turn total is added to the player's score and it becomes the opponent's turn.'''

    def __init__(self, players):
        """
        Initializes a new Game object with the given players.

        Args:
            players (list of Player): A list of Player objects.
        """
        self.players = players
        self.scoreToWin = 100
        self.current_player = 0



    def switchPlayer(self):
        """
                Switches to the next player in the list. Cycles back to the first player if necessary.
                """
        # Using module to cycle back to the beginning of the list
        self.current_player = (self.current_player + 1) % len(self.players)

    def turn(self, player):
        """
                Handles the player's turn by rolling the die or holding.

                The player can keep rolling until a 1 is rolled (in which case their turn ends with no points)
                or decide to hold and add the accumulated points to their score.

                Args:
                    player (Player): The player whose turn it is.
                """
        print("It's {0} player's turn".format(player.getName()))
        turn_score = 0

        while True:
            roll = player.rollDie()
            print("You rolled: {0}".format(roll))
            if roll == 1:
                print("No points for you!")
                print("Your turn is over")
                break
            else:
                turn_score += roll
                print("Your turn score is: {0}".format(turn_score))
                print("Your total score is: {0}".format(turn_score + player.score))

                # Ask user if they want to hold or continue rolling
                if self.is_winner(player, turn_score):
                    print("Winner")
                    break
                while True:
                    #if
                    if player.isComputer():
                        userInput= player.decideMove(turn_score+player.getScore(), turn_score)
                    else:
                        userInput = input("Do you want to Hold or Roll the die again? Enter 'h' or 'r': ").strip()
                    if userInput.lower() in ['h', 'r', 'hold', 'roll']:
                        # we want to exit the while loop
                        break
                    else:
                        print('Your input is invalid. Enter "h", "hold" to hold or "r", "roll" to roll the die again.')

                if userInput.lower() in ['h', 'hold']:
                    player.addToScore(turn_score)
                    print("{0} is holding. Total Score is: {1}".format(player.name, player.score))
                    break

    def is_winner(self, player, turnScore=0):
        """
                Checks if the player has reached or exceeded the score required to win.

                Args:
                    player (Player): The player whose score is being checked.
                    turnScore (int, optional): The score accumulated during the current turn. Default is 0.

                Returns:
                    bool: True if the player has won, otherwise False.
                """
        if player.score >= self.scoreToWin:
            return True
        elif (turnScore + player.score) >= self.scoreToWin:
            player.score = turnScore + player.score
            return True
        else:
            return False

    def printScores(self):
        """Prints the current scores of all players."""

        print("*********** Score Card ***********")

        for player in self.players:
            print("{0} : {1} points".format(player.name, player.score))

        print("*********** Score Card ***********")

    def play(self):
        """Starts the game, allowing players to take turns until a winner is determined."""

        print("Starting game of Pig.............")
        print("-" * 50)
        print(self.rulesMessage)
        print("-" * 50)
        keepGoing = True
        while keepGoing:
            currentPlayer = self.players[self.current_player]
            self.turn(currentPlayer)

            if self.is_winner(currentPlayer):
                keepGoing = False
            # if no winner yet
            self.printScores()

            self.switchPlayer()

class TimedGameProxy:
    """
      A proxy class for the Game that introduces a timed aspect.

      The game follows the same rules as Pig, but it ends either when someone reaches 100 points
      or when one minute has elapsed since the start of the game.

      Attributes:
          game (Game): The original Game object being proxied.
          time_limit (int): The time limit in seconds (default is 60 seconds).
          start_time (float): The time when the game started.

      Methods:
          play(): Starts the game and enforces the time limit.
          has_time_elapsed(): Checks whether the time limit has been exceeded.
      """

    def __init__(self, game, time_limit=60):
        """
        Initializes the TimedGameProxy with a reference to the original Game object and a time limit.

        Args:
            game (Game): The original Game object.
            time_limit (int): The time limit in seconds (default is 60 seconds).
        """
        self.game = game
        self.time_limit = time_limit
        self.start_time = time.time()

    def has_time_elapsed(self):
        """
        Checks whether the time limit has been exceeded.

        Returns:
            bool: True if the time limit has been exceeded, False otherwise.
        """
        elapsed_time = time.time() - self.start_time
        return elapsed_time > self.time_limit

    def play(self):
        """
        Starts the game and keeps checking if the time limit has been exceeded.
        If the time exceeds the limit, the game will end without a winner.
        """
        print("Starting timed game of Pig...")
        print("Time limit: 1 minute")
        print("-" * 50)

        keepGoing = True
        while keepGoing:
            if self.has_time_elapsed():
                print("Time's up! No one wins.")
                break

            currentPlayer = self.game.players[self.game.current_player]
            self.game.turn(currentPlayer)

            if self.game.is_winner(currentPlayer):
                keepGoing = False

            self.game.printScores()
            self.game.switchPlayer()

        print("Game over!")
class NotValidValue(Exception):
    pass

if __name__ == "__main__":
    """
        Main entry point for the game. Handles command-line arguments and game loop.
        """
    # Getting players info
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", help="Specify player 1 type (human or computer)", type=str, required=True)
    parser.add_argument("--player2", help="Specify player 2 type (human or computer)", type=str, required=True)
    parser.add_argument("--timed", help="Play the timed version of the game True or False", type=str, required=False, default=False)


    args = parser.parse_args()
    acceptedValues = ["c", "computer", "h", "human"]

    player1 = args.player1.lower()
    player2 = args.player2.lower()
    isTimedGamed = False
    if args.timed.lower() == "true" or args.times.lower() == "t":
        isTimedGamed = True

    print(args)
    try:
        if player1 not in acceptedValues:
            raise NotValidValue
        if player2 not in acceptedValues:
            raise NotValidValue
    except:
        print("not a valid Value")
        raise SystemExit


    keepPlaying = True
    players = []
    while keepPlaying:

        players.append(PlayerFactory.createPlayer(player1))
        players.append(PlayerFactory.createPlayer(player2))
        game = Game(players)
        if isTimedGamed:
            timedGamed = TimedGameProxy(game)
            timedGamed.play()
        else:
            game.play()
        userInput = input("Do you want to start a new game? y/n").strip().lower()
        players = []
        if userInput not in ["y", "yes"]:

            print("Good Bye.........")
            print("See you soon-------------------")
            keepPlaying = False




