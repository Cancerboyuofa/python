import random

while True:
    possible_options = ["rock", "paper", "scissors"]
    rand_choice = random.choice(possible_options)
    player_choice = input("Please choose your play: rock, paper, or scissors\n")
    player_choice = player_choice.lower()

    if rand_choice == player_choice:
        print("We tied!")
    else:
        if rand_choice == "rock" and player_choice == "scissors":
            print("I win, Rock beats scissors")
        elif rand_choice == "rock" and player_choice == "paper":
            print("You win, Paper covers Rock")
        elif rand_choice == "paper" and player_choice == "rock":
            print("I win, Paper covers rock")
        elif rand_choice == "paper" and player_choice == "scissors": 
            print("You win, Scissors cuts Paper")
        elif rand_choice == "scissors" and player_choice == "rock":
            print("You win, Rock crushes Scissors")
        elif rand_choice == "scissors" and player_choice == "paper":
            print("I win, Scissors cuts Paper!")

    play_again = input("Want to play again? Y or N?\n")
    if play_again.lower() != "y":
        break