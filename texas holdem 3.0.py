## This is a Texas Hold'em game where a player faces a Computer AI
## Computer AI has a detailed betting strategy that is explained further down
## The aim of this program was to help me practise python, with special emphasis
##  on abstraction techniques, lambda functions, handling edge cases, and efficiency


import random
import math


cards_full = ["Ah","2h","3h","4h","5h","6h","7h","8h","9h","Th","Jh","Qh","Kh","As",\
         "2s","3s","4s","5s","6s","7s","8s","9s","Ts","Js","Qs","Ks","Ac","2c",\
         "3c","4c","5c","6c","7c","8c","9c","Tc","Jc","Qc","Kc","Ad","2d","3d",\
         "4d","5d","6d","7d","8d","9d","Td","Jd","Qd","Kd"]

def random_card (cards):
    index = random.randrange (0, len(cards))
    card = cards [index]
    cards.remove (cards[index])
    return card
    
def numerical_value (card_input):
    card = card_input[0]
        
    if card == "A":
        return 14
    if card == "K":
        return 13
    if card == "Q":
        return 12
    if card == "J":
        return 11
    if card == "T":
        return 10
    else:
        return int (card)
    
def card_value (number):
    if number == 14:
        return "A"
    if number == 13:
        return "K"
    if number == 12:
        return "Q"
    if number == 11:
        return "J"
    if number == 10:
        return "T"
    else:
        return str (number)

def random_hand(cards):    
    
    card1 = random_card(cards)
    card2 = random_card(cards)
    
    return [card1, card2]

########################################################################
## Highest hand checking algorithm:

## Function 1
## checks for flush,
## checks for straight
## checks for straight flush

## Function 2
## checks for quad
## checks for trip
## checks for pair
## checks for full house
## checks for two pair

## Function 3
## checks for highest card
########################################################################


## checks if there's a flush or a straight
def flush_straight (pool):
    
    ## check for flush
    flush = [-1, -1, -1]
    for card in pool:
        if len(list(filter(lambda x: x[1] == card[1], pool))) >= 5:
            flush_list = list(filter(lambda x: x[1] == card[1], pool))
            flush_suit = card[1]
            highest_card = max(list(map(numerical_value, flush_list)))
            flush = [1, highest_card, flush_suit]
            break
    
    ## check for straight
    sorted_pool = sorted(list(map(numerical_value, pool)))
    distinct_sorted_pool = []
    for card in sorted_pool:
        if card not in distinct_sorted_pool:
            distinct_sorted_pool += [card]
    
    straight = [-1, -1]
    length = len(distinct_sorted_pool)
    if length >= 5:
        while (length - 5) >= 0:
            if distinct_sorted_pool[length-1] == distinct_sorted_pool[length - 5] + 4:
                straight = [1, distinct_sorted_pool[length - 1]]
                break
            length -= 1
            
    ## if neither straight nor flush, then it can't be a straight flush    
    if straight[0] == -1 and flush[0] == -1:
        return [-1]
    
    ## check for straight flush    
    straight_flush = [-1, -1, -1]
    if flush[0] == 1 and straight[0] == 1:
        num_value_flush_list = list(map(numerical_value, flush_list))
        counter = 0
        for i in range(straight[1], straight[1] - 5, -1):
            if i in num_value_flush_list:
                counter += 1
        if counter == 5:
            straight_flush = [1, straight[1], flush[2]]
    
        
    ## return what it was
    if straight_flush[0] == 1:
        return [9] + straight_flush[1:]
    elif flush[0] == 1:
        return [6] + flush[1:] 
    else:
        return [5] + straight[1:]
    

def multiples_hands (pool):
    num_val_pool = sorted(list(map(numerical_value, pool)))
    distinct_list = []
    
    ## create a distinct list and if there are 7 distinct, then no multiples 
    for card in num_val_pool:
        if card not in distinct_list:
            distinct_list += [card]
    if len(distinct_list) == 7:
        return [-1]
    
    ## create a list mirroring distinct_list but with the associated entry 
    ##  showing how many of that card there is
    count_list = []
    for card in distinct_list:
        count_list += [num_val_pool.count(card)]
    
    max_count_list = max(count_list)
    ## quad
    if max_count_list == 4:
        i = count_list.index(4)
        quad_card = distinct_list[i]
        for i in range(0,4):
            num_val_pool.remove(quad_card)
        highest_card = max(num_val_pool)
        return [8, quad_card, high_card]
    
    ## triple and full house
    if max_count_list == 3:
        ## check how many triples there are
        if count_list.count(3) == 2:
            num_val_pool.remove(distinct_list[count_list.index(1)])
            trip_high = max(num_val_pool)
            for i in range(0,3):
                num_val_pool.remove(trip_high)
            pair_high = num_val_pool[0]
            return [7, trip_high, pair_high]
        else:
            trip_high = distinct_list[count_list.index(3)]
            
            ## check if there's a full house
            for i in range(0,3):
                num_val_pool.remove(trip_high)
            list_of_pairs = []
            for card in num_val_pool:
                if len(list(filter (lambda x: x == card, num_val_pool))) == 2 and \
                   card not in list_of_pairs:
                    list_of_pairs += [card]
            if list_of_pairs == []:
                high_cards = num_val_pool[2:4][::-1]
                return [4, trip_high] + high_cards
            
            else:
                highest_pair = max(list_of_pairs)
                return[7, trip_high, highest_pair]
        
    ## pairs, two pairs 
    if max_count_list == 2:
        list_of_pairs = []
        for card in num_val_pool:
            if len(list(filter (lambda x: x == card, num_val_pool))) == 2 and \
               card not in list_of_pairs:
                list_of_pairs += [card]      
        
        ## check for two pair
        if len(list_of_pairs) >= 2:
            high_pair = max(list_of_pairs)
            list_of_pairs.remove(high_pair)
            low_pair = max(list_of_pairs)
            
            ## find the high card
            for i in range(0,2):
                num_val_pool.remove(high_pair)
                num_val_pool.remove(low_pair)
            high_card = max(num_val_pool)
            
            return[3, high_pair, low_pair, high_card]
        
        else:
            pair_num = distinct_list[count_list.index(2)]
            num_val_pool.remove(pair_num)
            num_val_pool.remove(pair_num)
            high_cards = num_val_pool[2:5][::-1]
            
            return [2, pair_num] + high_cards
            
## high_card
def high_card(pool):
    num_val_pool = sorted(list(map(numerical_value, pool)))
    highest_five = num_val_pool[2:7][::-1]
    return [1] + highest_five

## Converts the number ranking of a hand to it's name
def convert_to_name (number_ranking):
    if number_ranking == 9:
        return "Straight Flush!"
    elif number_ranking == 8:
        return "Four Of A Kind!"
    elif number_ranking == 7:
        return "Full House!"
    elif number_ranking == 6:
        return "Flush!"   
    elif number_ranking == 5:
        return "Straight!"   
    elif number_ranking == 4:
        return "Triple!"   
    elif number_ranking == 3:
        return "Two Pair!"   
    elif number_ranking == 2:
        return "Pair!"   
    elif number_ranking == 1:
        return "High Card!"   
    
    
## check what the highest rank of that hand is and return the name for that
def highest_in_pool (pool):  
    highest_hand = max([flush_straight(pool)[0], multiples_hands(pool)[0],
                        high_card(pool)[0]])
    if highest_hand in [9,6,5]:
        return_list = flush_straight(pool)
    elif highest_hand in [1]:
        return_list = high_card(pool)
    else:
        return_list = multiples_hands(pool)
    
    return([convert_to_name(highest_hand)] + return_list)
        
test=['2s','2d','2s','Js','Jd','Js','3d']
test2 = ["3s", "4d", "5c", "2s", "6d", "9s", "Js"]
test3 = ["2s", "2s", "2s", "4s", "4s", "5s", "5s",]
test4 = ["4s","5s","6s","7s","8s","9s", "Qh"]
            
 
## Compare two pools, check which pool is higher, and print what they won with
## Computer is always pool2
def compare_pools(pool1, pool2):
    pool1_high = highest_in_pool (pool1)
    pool2_high = highest_in_pool (pool2)
    
    len1 = len(pool1_high)
    len2 = len(pool2_high)
    
    string1 = ""
    string2 = ""
    
    ## Create a string for the cards associated with the hand
    for i in range(2, len1):
        if i == 2:
            string1 += (card_value(pool1_high[i]))
        else:
            string1 += (", " + card_value(pool1_high[i])) 
    
    for i in range(2, len2):
        if i == 2:
            string2 += (card_value(pool2_high[i]))
        else:
            string2 += (", " + card_value(pool2_high[i]))             
    
    ## Print what each player got
    print("\nPlayer Name got a " + pool1_high[0] + " " + string1)
    print("\nComputer got a " + pool2_high[0] + " " + string2)
    
    if pool1_high[1] > pool2_high[1]:
        print("\nPlayer Name beat Computer with a " + pool1_high[0])
    elif pool1_high[1] < pool2_high[1]:
        print("\nComputer beat Player Name with a " + pool2_high[0])
    else:
        for i in range(2, len1):
            if isinstance(pool1_high[i], str):
                print("\nBoth players tied! Split the pot.")
                break
            else:
                if pool1_high[i] > pool2_high[i]:
                    print("\nPlayer Name beat Computer with a higher " + pool1_high[0])
                    break
                elif pool1_high[i] < pool2_high[i]:
                    print("\nComputer beat Player Name with a higher " + pool2_high[0])
                    break
            if i == len1 - 1:
                print ("\nBoth players tied! Split the pot.")

## Function that determines who wins
def determine_winner(pool1, pool2):
    pool1_high = highest_in_pool (pool1)
    pool2_high = highest_in_pool (pool2)
    
    len1 = len(pool1_high)
    len2 = len(pool2_high)

    if pool1_high[1] > pool2_high[1]:
        return 1
    elif pool1_high[1] < pool2_high[1]:
        return 2
    else:
        for i in range(2, len1):
            if isinstance(pool1_high[i], str):
                return 0
            else:
                if pool1_high[i] > pool2_high[i]:
                    return 1
                elif pool1_high[i] < pool2_high[i]:
                    return 2
            if i == len1 - 1:
                return 0

## Computer AI Betting Decision
## This is the Texas Hold'em computer betting algorithm

## 1) A numerical value is assigned to the starting hand of the computer. This
##    numerical value ranks the strength of the hand.
## 2) If the value is above a certain threshold, the computer will play. 
##    Otherwise, it will fold.
##      - if it's above an even high threshold, the computer will raise
## 3) Every single time cards are revealed in the flop, the computer's hand rank
##    will be recalculated. This is done by adding or subtracting the rank
##    by a number depending on whether the hand gets stronger or weaker (based
##    on the possible cards that would be advantageous for the computer).
##      - for example, if the card revealed is within 5 cards to one of the 
##        cards in the computer's hand, a straight is more likely so the value 
##        rises. 
## 4) The computer will either check, fold, or raise depending on this newly 
##    calculated score.
##      - there will be a certain threshold where the computer will/won't play
##        if the player raises by a certain amount.
## 5) There are risk tolerance safety nets in place to make sure the computer 
##    doesn't make too risky bets.

## To display what the computer's hand was, we have a block of ###### displayed
## with the computer's hand cards midway through so the player can't see it. 


################################################################################

## Assign a rank to the computer's initial hand
def assign_init_rank(comp_init_hand):
    
    rank_hand = 0
    
    ## Give value for pairs
    if comp_init_hand[0][0] == comp_init_hand[1][0]:
        ## higher pair yields higher value
        rank_hand += 2 * numerical_value(comp_init_hand[0]) + 30
    
    ## Give value for same suit
    if comp_init_hand[0][1] == comp_init_hand[1][1]:
        rank_hand += 15
    
    ## Give value for proximity (straight)
    abs_diff = abs(numerical_value(comp_init_hand[0]) - numerical_value(comp_init_hand[1]))
    if abs_diff != 0 and abs_diff <= 4:
        rank_hand += 10
           
    ## Give value for high card
    higher_card = max(numerical_value(comp_init_hand[0]), numerical_value(comp_init_hand[1]))
    lower_card = min(numerical_value(comp_init_hand[0]), numerical_value(comp_init_hand[1]))
    rank_hand += 2 * higher_card + lower_card
    
    print("computer_hand: " + str(comp_init_hand))
    return rank_hand

## Determines (based on the rank of the initial hand) whether the computer plays
##  or not.
## flop_num is which round the game is at currently. 
##  pre-flop = 0
##  flop = 1
##  4th = 2
##  5th = 3

def does_comp_play(rank, current_wager, total_money, opponent_raise, flop_num):
    current_wager_fraction = current_wager / total_money 
    
    ## higher the risk_value, more risk-averse the AI becomes
    if current_wager_fraction >= 0.5:
        risk_value = 5
    elif current_wager_fraction <= 0.05:
        risk_value = 1
    else:
        risk_value = 10 * round(current_wager_fraction, 1)
        
    ## higher the opponent_raise is, the less likely computer will play
    relative_raise_change = round((opponent_raise / total_money), 2)
    raise_value = relative_raise_change * 30 + 1
    
    ## higher the flop_num, the less risk-averse the computer becomes
    
    ## Calculate the play threshold
    play_threshold = 20 + 5 * risk_value + raise_value - 1.5 * flop_num 
    
    print("risk_value: " + str(5 * risk_value))
    print("raise_value: " + str(raise_value))
    print("flop_value: " + str(-1.5 * flop_num))
    print("play_threshold: " + str(play_threshold))
    print("rank: " + str(rank))
    
    ## Determine if computer plays
    if rank >= play_threshold:
        ## If computer's hand is much better than the play threshold
        if rank >= play_threshold + 10:
            if current_wager_fraction <= .2:
                return round(.10 * total_money)
            else:
                return round(.10 * (total_money - current_wager))
        else:
            return 0
    else:
        return -1

## Test case    
#does_comp_play(assign_init_rank(random_hand()), 20, 300, 15, 2)


## Change the rank of the computer's hand based on what card is revealed
def change_rank_reveal_card(card_revealed, rank, init_hand, pool):
    your_cards_num_val = list(map(lambda x: numerical_value(x[0]), pool))
    your_cards_suit = list(map(lambda x: x[1], pool))
    rank_increased = 0
    
    ## Add the new card revealed to the pool
    new_pool = pool + [card_revealed]
    
    
    ## If the card is the same as a card that you have
    if numerical_value(card_revealed) in your_cards_num_val:
        if your_cards_num_val[0] == your_cards_num_val[1]:
            rank += 40
        elif (numerical_value(card_revealed) in your_cards_num_val[:2]) and \
             (numerical_value(card_revealed) in your_cards_num_val[2:]):
            rank += 30
        else:
            rank += 20
        rank_increased = 1
            
    ## If the card revealed is the same suit as a card that you have, only if 
    ##  you have the potential for a flush
    suits_list = ['s','h','c','d']
    num_each_suit = [0,0,0,0]
    counter = 0
    for suit in suits_list:
        num_each_suit[counter] = len(list(filter(lambda x: x[1] == suits_list[counter], pool)))
        counter += 1
    
    ## create a suits list for all suits that have >=3 cards in the pool
    num_suits_list = []
    for i in range(0, 4): 
        if num_each_suit[i] >= 3:
            num_suits_list += [suits_list[i]] 
        
    ## if card revealed is in the num_suits_list, increase rank 
    if card_revealed[1] in num_suits_list:
        rank += 10
        rank_increased = 1
    
    ## if card revealed has the potential of a straight, increase rank
    sorted_hand = sorted(your_cards_num_val)
    for i in range(0, len(sorted_hand) - 1):
        if (sorted_hand[i + 1] - sorted_hand[i] <= 4 and 
           numerical_value(card_revealed) > sorted_hand[i] and  
           numerical_value(card_revealed) < sorted_hand[i+1]):
            rank += 5
            rank_increased = 1
            break
        
        elif abs(numerical_value(card_revealed) - sorted_hand[i]) <= 4 and \
             abs(numerical_value(card_revealed) - sorted_hand[i]) > 0:
            rank += 2
            rank_increased = 1
            break
        
    ## if the revealed card is not any of the above, rank goes down
    if rank_increased == 0:
        rank -= 5
            
    ## Return the new rank and the current pool
    return [rank, new_pool]


## Position text
def your_position (position):
    if position == 1:
        print ("You are the small blind. You bet $2. You go first.")
    else: 
        print ("You are the big blind. Pay up.")

## Flop
def flop(cards):
    card3 = random_card (cards)
    card4 = random_card (cards)
    card5 = random_card (cards)
    card6 = random_card (cards)
    card7 = random_card (cards)    
    
    flop = [card3,card4,card5,card6,card7]
    return flop

## Your move
def your_move():
    your_choice = user_input()
    if your_choice == 'f' or your_choice == "F":
        return -1
    elif your_choice == 'c' or your_choice == 'C':
        return 0
    elif your_choice == 'r' or your_choice == 'R':
        your_raise = raise_input()
        return your_raise
    
## Function for the computer's decision text
def computer_decision_text (comp_bet, your_bet, computer_rank, ai_money, flop_num):
    opponent_raise = your_bet - comp_bet
    comp_decision = does_comp_play(computer_rank, comp_net, ai_money, opponent_raise, flop_num)
    
    if comp_decision == -1:
        print("\nComputer folds. You gain $" + str(comp_bet) + ".\n\n\n")
        play_round((player_pos + 1) %2, your_money + comp_bet, ai_money - comp_bet, round_num + 1)
        return        
    elif comp_decision == 0:
        print("\nComputer calls.")
        print("Both players have bet $" + str(your_bet) + ".\n")
        comp_bet = your_bet        
        
        if flop_num != 5:
            full_flop = flop(cards)
            ## AI calculates their hand
            pool = computer_hand
            for card in full_flop:
                rank_pool = change_rank_reveal_card(card,computer_init_rank, computer_hand, pool)
                computer_init_rank = rank_pool[0]
                pool = rank_pool[1]
            computer_rank = computer_init_rank
            
            print("The flop is: " + str(full_flop))
            
    elif comp_decision > 0:
        print("\nComputer raises by $" + str(comp_play_decision) + ".")
        comp_bet = your_bet + comp_play_decision
    # Need to return values pertaining to the computer's move

## User Input (Fold, Call, Raise)
def user_input():    
    accepted_responses = ['f','F','c','C','r','R']
    while True:
        try:
            user_response = input(str("\nWhat's your move? (f to fold, c to call, r to raise): "))
        except: 
            print("Sorry, I didn't understand that.")
            continue
        
        if user_response not in accepted_responses:
            print("Sorry, you can only fold, call or raise (f, c, r).")
            continue
        else:
            break
    
    return user_response

## Raise input (how much you want to raise)
def raise_input():
    while True:
        try:
            raise_amount = int(input("How much would you like to raise? $"))
        except ValueError:
            print("Sorry, you must input a number")
            continue
        else:
            break
    return raise_amount

## Play Round
def play_round(player_pos, your_money, ai_money, round_num):
    cards = ["Ah","2h","3h","4h","5h","6h","7h","8h","9h","Th","Jh","Qh","Kh",
             "As","2s","3s","4s","5s","6s","7s","8s","9s","Ts","Js","Qs","Ks",
             "Ac","2c","3c","4c","5c","6c","7c","8c","9c","Tc","Jc","Qc","Kc",
             "Ad","2d","3d","4d","5d","6d","7d","8d","9d","Td","Jd","Qd","Kd"]
    
    player_money = your_money
    computer_money = ai_money
    
    card1 = random_card (cards)
    card2 = random_card (cards)
    your_hand = [card1, card2]
    
    card3 = random_card (cards)
    card4 = random_card (cards)
    computer_hand = [card3, card4]
    
    raise_amt = 0
    pot = 6
    
    #In the future, implement it so you can choose the blinds
    if player_pos == 1:
        your_bet = 2
        comp_bet = 4
    else:
        your_bet = 4
        comp_bet = 2
    
    print("Round " + str(round_num))
    your_position (player_pos)
    print("You have $" + str(player_money) + " left!")
    print ("Your hand is: " + card1 + ", " + card2 + ".\n")
    user_play = user_input()
    
    ## Fold
    if user_play == "f" or user_play == "F":
        print("You folded and lost $2.\n\n\n")
        play_round((player_pos + 1) %2, your_money - your_bet, ai_money + your_bet, round_num + 1)
        return

    ## Call    
    elif user_play == "c" or user_play == "C":
        print("You called. Pot is now $8.\n")
        your_bet = 4
    
    ## Raise    
    elif user_play == "r" or user_play == "R":
        raise_amt = raise_input()
        while raise_amt > your_money - your_bet:
            print("Sorry, you do not have that much money to raise.")
            print("You have $" + str(your_money - your_bet) + " left to bet.") 
            raise_amt = raise_input()
            
        your_bet = 4 + int(raise_amt)
        print("\nYou called and raised by $" + str(raise_amt) + ". The pot is now $" + str(8 + int(raise_amt)) + ".")
        
    ## Computer initial decision
    computer_init_rank = assign_init_rank(computer_hand)
    comp_play_decision = does_comp_play(computer_init_rank, comp_bet, ai_money, int(raise_amt), 0)
    print(comp_play_decision)
    
    ## computer folds
    if comp_play_decision == -1:
        print("\nComputer folds.")
        print("You gained $2.\n\n\n")
        play_round((player_pos + 1) %2, your_money + comp_bet, ai_money - comp_bet, round_num + 1)
    
    ## Computer calls    
    elif comp_play_decision == 0:
        print("\nComputer calls.")
        print("Both players have bet $" + str(your_bet) + ".\n")
        comp_bet = your_bet
        
        full_flop = flop(cards)
        ## AI calculates their hand
        pool = computer_hand
        for card in full_flop:
            rank_pool = change_rank_reveal_card(card,computer_init_rank, computer_hand, pool)
            computer_init_rank = rank_pool[0]
            pool = rank_pool[1]
        computer_rank = computer_init_rank
        
        print("The flop is: " + str(full_flop))
        
        
        decision = your_move()
        if decision == -1:
            print("\nYou folded and lost $" + str(your_bet) + ".\n\n\n")
            play_round((player_pos + 1) %2, your_money - your_bet, ai_money + your_bet, round_num + 1)
            return
        
        # Create case for when user raises instead of just calls
        # Change it so the order is based on player_pos. Right now player goes first every time
        elif decision == 0 or decision > 0: #Get rid of the decision > 0 part later
            comp_decision = does_comp_play(computer_rank, comp_bet, ai_money, 0, 3)
            if comp_decision == -1:
                print("\nComputer folds. You gain $" + str(comp_bet) + ".\n\n\n")
                play_round((player_pos + 1) %2, your_money + comp_bet, ai_money - comp_bet, round_num + 1)
                return                
            else:
                print("Both players decide to play!\n")
                
                ## Determine who wins
                your_pool = your_hand + full_flop
                comp_pool = computer_hand + full_flop
                
                compare_pools(your_pool, comp_pool)
                who_won = determine_winner(your_pool, comp_pool)
                print(who_won)
                print(your_bet)                
                print("\n\n\n")
                
                if who_won == 1:
                    play_round((player_pos + 1) %2, your_money + comp_bet, ai_money - comp_bet, round_num + 1)
                elif who_won == 2:
                    play_round((player_pos + 1) %2, your_money - your_bet, ai_money + your_bet, round_num + 1)
                else:
                    play_round((player_pos + 1) %2, your_money, ai_money, round_num + 1)
                return
                
    ## Computer raises
    elif comp_play_decision > 0:
        print("\nComputer raises by $" + str(comp_play_decision) + ".")
        comp_bet = your_bet + comp_play_decision
        your_new_decision = input("Do you call or fold? (c to call, f to fold): ")

        ## You fold
        if your_new_decision == "f" or your_new_decision == "F":
            print("\nYou folded and lost $" + str(your_bet) + ".\n\n\n")
            play_round((player_pos + 1) %2, your_money - your_bet, ai_money + your_bet, round_num + 1)
            return
        
        ## you call
        elif your_new_decision == "c" or your_new_decision == "C":
            print ("\nYou called. Your bet is now $" + str(comp_bet) + ".")
            your_bet = comp_bet
            print("Both players have bet $" + str(your_bet) + ".\n")
            
            full_flop = flop(cards)
        
            ## AI calculates their hand
            pool = computer_hand
            for card in full_flop:
                rank_pool = change_rank_reveal_card(card,computer_init_rank, computer_hand, pool)
                computer_init_rank = rank_pool[0]
                pool = rank_pool[1]
            computer_rank = computer_init_rank
            
            print("The flop is: " + str(full_flop))
            
            decision = your_move()
            if decision == -1:
                print("\nYou folded and lost $" + str(your_bet) + ".\n\n\n")
                play_round((player_pos + 1) %2, your_money - your_bet, ai_money + your_bet, round_num + 1)
                return
            
            # Create case for when user raises instead of just calls
            # Change it so the order is based on player_pos. Right now player goes first every time
            elif decision == 0 or decision > 0: #Get rid of the decision > 0 part later
                comp_decision = does_comp_play(computer_rank, comp_bet, ai_money, 0, 3)
                if comp_decision == -1:
                    print("\nComputer folds. You gain $" + str(comp_bet) + ".\n\n\n")
                    play_round((player_pos + 1) %2, your_money + comp_bet, ai_money - comp_bet, round_num + 1)
                    return                
                else:
                    print("Both players decide to play!\n")
                    
                    ## Determine who wins
                    your_pool = your_hand + full_flop
                    comp_pool = computer_hand + full_flop
                    
                    compare_pools(your_pool, comp_pool)
                    who_won = determine_winner(your_pool, comp_pool)
                    print(who_won)
                    print(your_bet)
                    print("\n\n\n")
                    
                    if who_won == 1:
                        play_round((player_pos + 1) %2, your_money + comp_bet, ai_money - comp_bet, round_num + 1)
                    elif who_won == 2:
                        play_round((player_pos + 1) %2, your_money - your_bet, ai_money + your_bet, round_num + 1)
                    else:
                        play_round((player_pos + 1) %2, your_money, ai_money, round_num + 1)
        else:
            print("Thank you for playing.")

## Initiate the game
def initiate_game():
    print ("Texas Hold'em v3.0\n")
    
    ## Both players start with $100
    play_round(1, 100, 100, 1)
    
    

    
    