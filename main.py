import random
import os


def clear_con():
    os.system('cls')


name = input("What is your name?\n")
name = name.capitalize()
play_to = input ("First to how many? Enter 1, 3, 5, or 7\n")
play_to = int(play_to)
c_score = 0
p_score = 0
while p_score < play_to or c_score < play_to:
    possible_options = ["rock", "paper", "scissors"]
    cpu_choice = random.choice(possible_options)
    clear_con()
    player_choice = input("Please choose your play: rock, paper, or scissors\n")
    player_choice = player_choice.lower()

    if cpu_choice == player_choice:
        print("\nWe tied!\n")
    else:
        if cpu_choice == "rock" and player_choice == "scissors":
            print("I win, Rock beats scissors\n")
            c_score += 1
        elif cpu_choice == "rock" and player_choice == "paper":
            print("You win, Paper covers Rock\n")
            p_score += 1
        elif cpu_choice == "paper" and player_choice == "rock":
            print("I win, Paper covers rock\n")
            c_score += 1
        elif cpu_choice == "paper" and player_choice == "scissors": 
            print("You win, Scissors cuts Paper\n")
            p_score += 1
        elif cpu_choice == "scissors" and player_choice == "rock":
            print("You win, Rock crushes Scissors\n")
            p_score += 1
        elif cpu_choice == "scissors" and player_choice == "paper":
            print("I win, Scissors cuts Paper!\n")
            c_score += 1
    if p_score == play_to:
        print("\nYou win. Boohoo\n")
        break
    elif c_score == play_to:
        print("\nI win, sucker!\n")
        break
    else:
        print("My score is currently: " + str(c_score) + "    <--|-->   " + name + "'s score is currently: " + str(p_score) + "\n")
        want_continue = input("\nReady for the next round? Y or N?\n")
       
    if want_continue.lower() != "y":
        print("Sorry to hear you quit! See you later...")
        break