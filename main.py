import random
c_score = 0
p_score = 0
while p_score < 3 or c_score < 3:
    possible_options = ["rock", "paper", "scissors"]
    cpu_choice = random.choice(possible_options)
    player_choice = input("Please choose your play: rock, paper, or scissors\n")
    player_choice = player_choice.lower()

    if cpu_choice == player_choice:
        print("We tied!")
    else:
        if cpu_choice == "rock" and player_choice == "scissors":
            print("I win, Rock beats scissors")
            c_score += 1
        elif cpu_choice == "rock" and player_choice == "paper":
            print("You win, Paper covers Rock")
            p_score += 1
        elif cpu_choice == "paper" and player_choice == "rock":
            print("I win, Paper covers rock")
            c_score += 1
        elif cpu_choice == "paper" and player_choice == "scissors": 
            print("You win, Scissors cuts Paper")
            p_score += 1
        elif cpu_choice == "scissors" and player_choice == "rock":
            print("You win, Rock crushes Scissors")
            p_score += 1
        elif cpu_choice == "scissors" and player_choice == "paper":
            print("I win, Scissors cuts Paper!")
            c_score += 1
    if p_score == 3:
        print("\nYou win. Boohoo\n")
        break
    elif c_score == 3:
        print("\nI win, sucker!\n")
        break
    else:
        print("My score is currently: ",c_score)
        print("Your score is currently: ",p_score)
        want_continue = input("Ready for the next round? Y or N?\n")
       
    if want_continue.lower() != "y":
        print("Sorry to hear you quit! See you later...")
        break