##############################  LU TABLE TENNIS ADMINISTRATION  ###############################
### Name:   Fangxin Tang
### Student ID: 1155764
################################################################################################## 

import lutt_admin_data       #lutt_admin_data.py contains the data lists and must be in the same folder as this file
import datetime
import random

# The list variables
colTeams = lutt_admin_data.colTeams
dbTeams = lutt_admin_data.dbTeams


# These dictionaries define the columns for display for the different functions.
colPlayers = {'Team_Name':str,'Player_Name':str}
colDraw = {'First_Team': str, 'First_Score':int,'Second_Team': str, 'Second_Score':int}
colPlayersbyAlpha = {"First Name": str, "Surname": str}
colMatchInfo = {'Match_ID': int, 'First_Team': str, 'First_Score':int,'Second_Team': str, 'Second_Score':int, 'Winner': str}


# Create global variables here
draw_info = [] ## Create a list of dict for creating draw. Each dict contains four key: value pairs with the info about the names of the current team and the opponent team and their scores
# draw_info=[{'First Team': versus[0], 'First Score': 0, 'Second Team': versus[1], 'Second Score': 0}]

##############################################################################################

# create utility functions:
def GetAllPlayersList():
    # to get a list of tuples, each tuple is a player's name in (firstname, surname) format
    AllPlayersList = []
    for team_players in list(dbTeams.values()):
        AllPlayersList.append(team_players[0])
        AllPlayersList.append(team_players[1])
    return AllPlayersList


def PlayerNameIsUnique(new_player_firstname, new_player_surname) -> bool:
    isUnique = True
    AllPlayersList = GetAllPlayersList()
    for (firstname, surname) in AllPlayersList:
        if new_player_firstname == firstname and new_player_surname == surname:
            IsUnique = False
            break
    return isUnique


def TeamNameIsUnique(new_team_ID:str) -> bool:
    for team_ID in dbTeams.keys():
        if new_team_ID == team_ID:
            return False
    return True


def GetListDrawInfo() -> list:
    # this function is support to list draw
    # only 4 items will be list: first name, first score, second name, second score
    # to get a list of tuples from a global variable draw_info
    draw_info_lst_of_tup = []
    for i in range(len(draw_info)):
        row = draw_info[i]
        match_info = (row['First Team'], row['First Score'], row['Second Team'], row['Second Score'])
        draw_info_lst_of_tup.append(match_info)
    # print(draw_info_lst_of_tup)
    return draw_info_lst_of_tup


def GetAllMatchInfo() -> list:
    # to get more match info including match id and winner info
    # get a list of tuples from a global variable draw_info
    # create a list of tuple includes all match info so it can pass to columOutput()
    draw_info_lst_of_tup = []
    winner = '' # create a placeholder column for "winners"
    for i in range(len(draw_info)):
        match_ID = i + 1
        row = draw_info[i]
        match_info = (match_ID, row['First Team'], row['First Score'], row['Second Team'], row['Second Score'], winner)
        draw_info_lst_of_tup.append(match_info)
    # print(draw_info_lst_of_tup)
    return draw_info_lst_of_tup


def CheckMatchIDValid(match_id:str) -> bool:
    total_match = len(draw_info)
    if not match_id.isdigit():
        return False
    match_id = int(match_id)
    if match_id < 1 or match_id > total_match:
        return False
    else:
        return True


def CheckScoreValid(first_score:str, second_score:str) -> bool:
    try:
        first_score_int = int(first_score)
        second_score_int = int(second_score)
        if first_score.isdigit() and second_score.isdigit():
            score_sum = first_score_int + second_score_int
            if score_sum > 5 or score_sum < 3:
                return False
            elif first_score_int == second_score_int:
                return False
            else:
                return True
        else:
            return False
    except ValueError:
        return False
    

def AddWinner():
    if len(draw_info) == 0:
        print("Please generate draw first.")
        return[]
    
    draw_info_lst_of_tup = GetAllMatchInfo() #winners column needs to be updated
    for i, match_info in enumerate(draw_info):
        first_score_int = int(match_info["First Score"])
        second_score_int = int(match_info["Second Score"])
        for j, match_info_tup in enumerate(draw_info_lst_of_tup):
            if i == j:
                match_info_lst = list(match_info_tup)
                if first_score_int == 0 and second_score_int == 0:
                    match_info_lst[5] = "Not Available"
                elif first_score_int > second_score_int:
                    match_info_lst[5] = match_info["First Team"]
                elif first_score_int < second_score_int:
                    match_info_lst[5] = match_info["Second Team"]
                draw_info_lst_of_tup[j] = tuple(match_info_lst)

    return(draw_info_lst_of_tup)


##############################################################################################

def columnOutput(dbData,cols,formatStr):
    print(formatStr.format(*cols))
    for row in dbData:
        rowList=list(row)
        for index,item in enumerate(rowList):
            if item==None:      # Removes any None values from the rowList, which would cause the print(*rowList) to fail
                rowList[index]=""       # Replaces them with an empty string
            elif type(item)==datetime.date:    # If item is a date, convert to a string to avoid formatting issues
                rowList[index]=str(item)
        print(formatStr.format(*rowList))   


def listDraw():
    # Print out a copy of the draw  
    if len(draw_info) == 0:
         print("The draw has not been generated yet.")
         return
    
    draw_info_lst_of_tup = GetListDrawInfo()
    columnOutput(draw_info_lst_of_tup, colDraw, ' {:^20} | {:^15} | {:^20} | {:^15} ')   
    input("\nPress Enter to continue.")     # End function with this line


def listAllMatchInfo():
    draw_info_lst_of_tup = GetAllMatchInfo()
    columnOutput(draw_info_lst_of_tup, colMatchInfo, '{:^15} | {:^20} | {:^15} | {:^20} | {:^15} | {:^20}')



def listTeams():
    # Print a list of the teams
    displayList = []
    for team in dbTeams.keys():
        displayList.append((team,f'{dbTeams[team][0][0]} {dbTeams[team][0][1]}',f'{dbTeams[team][1][0]} {dbTeams[team][1][1]}'))
    print(displayList)
    columnOutput(displayList,colTeams,"{: ^18} | {: ^18} | {: ^18}") #example of how to call columnOutput function
    input("\nPress Enter to continue.")     # End function with this line
    

def listMembersSurnameAlpha():
    # print team member details in alphabetical order by last name then first name 
    AllPlayersList = GetAllPlayersList()
    players_surname_alpha = sorted(AllPlayersList, key = lambda team_players: (team_players[1], team_players[0]))
    # print(players_surname_alpha)
    
    columnOutput(players_surname_alpha, colPlayersbyAlpha, "{: ^18} | {: ^18}")
    input("\nPress Enter to continue.")     # End function with this line
        

def listMembersFirstnameAlpha():
    # print team member details in alphabetical order by first name then last name 
    AllPlayersList = GetAllPlayersList()
    players_surname_alpha = sorted(AllPlayersList, key = lambda team_players: (team_players[0], team_players[1]))
    # print(players_surname_alpha)
    columnOutput(players_surname_alpha, colPlayersbyAlpha, "{: ^18} | {: ^18}")
    input("\nPress Enter to continue.")     # End function with this line


def addTeam():
    # add a team. Check a Player does not already exist.
    # Generate the team name and check that it does not already exist
    # Team Name is First Surname and Second Surname joined together each with an initial capital letter
    while True:
        # check if new player1's name is unique
        new_player1_firstname = input("Enter the firstname of player 1: ").capitalize()
        new_player1_surname = input("Enter the surname of player 1: ").capitalize()
        
        if len(new_player1_surname) == 0 or len(new_player1_firstname) == 0:
            print("The player's name cannot be empty.")
            continue

        if not PlayerNameIsUnique(new_player1_firstname, new_player1_surname):
            print("The name already exists.")
            continue

        # check if new player2's name is unique
        new_player2_firstname = input("Enter the firstname of player 2: ").capitalize()
        new_player2_surname = input("Enter the surname of player 2: ").capitalize()

        if len(new_player2_surname) == 0 or len(new_player2_firstname) == 0:
            print("The player's name cannot be empty.")
            continue

        if new_player1_firstname == new_player2_firstname and new_player1_surname == new_player2_surname:
            print("Player2's name is same as player1's name.")
            continue

        if not PlayerNameIsUnique(new_player2_firstname, new_player2_surname):
            print("The name already exists.")
            continue
            
        # check if new team name is unique
        new_team_name = new_player1_surname + new_player2_surname
        if not TeamNameIsUnique(new_team_name):
            print("The team name already exists.")
            continue
        else:
            new_player1_full_name_tuple = (new_player1_firstname, new_player1_surname)
            new_player2_full_name_tuple = (new_player2_firstname, new_player2_surname)
            break

    # the above ensure that the names of the team and its players are unique
    # then we add this team name and players' names in to the dbTeam in the format of: "ChartersMelton":[("Stuart","Charters"),("Craig","Melton")],
    dbTeams[new_team_name] = [new_player1_full_name_tuple, new_player2_full_name_tuple]
    print(f"New team is added successfully!, Team ID is {new_team_name}")
    input("\nPress Enter to continue.")


def createDraw():
    global draw_info
    #each team should play each other team, but only once.
    draw_info.clear()
    versus_list = []
    team_IDs = list(dbTeams.keys())
    
    # creating two teams for a match
    for i, first_team in enumerate(team_IDs):
        for j, second_team in enumerate(team_IDs):
            if i < j:
                versus_list.append((first_team,second_team))
    random.shuffle(versus_list)
    #print(versus_list)

    # generating draw info as a list of dict
    for versus in versus_list:
        draw_info.append({'First Team': versus[0], 'First Score': 0, 'Second Team': versus[1], 'Second Score': 0})
    # print(draw_info)

    #Display the draw
    listDraw()


def addResult():
    #update the result of a match, hint use the enumerate function to identify which match to update
    global draw_info
    total_match = len(draw_info)
    if total_match == 0:
        print("Please create a draw first. ")
        return
    
    # display all match info
    listAllMatchInfo()

    while True:
        # check the selected match ID is valid
        selected_match_ID = input("Enter the match ID: ")
        ## all input string will be checked if they are valid integer by using two other functions
        if CheckMatchIDValid(selected_match_ID):
            print(f"You are updating the score of match ID {selected_match_ID}.")
            # check the scores are valid
            first_score = input("Enter the score of the First Team: ")
            second_score = input("Enter the score of the Second Team: ")

            if CheckScoreValid(first_score, second_score):
                # update scores in the original variable draw_info
                match_index = int(selected_match_ID) - 1
                first_score_int = int(first_score)
                second_score_int = int(second_score)
                draw_info[match_index]["First Score"] = first_score_int
                draw_info[match_index]["Second Score"] = second_score_int
                listAllMatchInfo()
                # print(draw_info)
                print(f"The two scores of Match ID {selected_match_ID} has been updated.")

                # checks if the user wants to add another match's result 
                while True:
                    add_another_result = input("Do you want to add another match's result? Y/N: " ).lower()
                    if add_another_result == "y":
                        break
                    elif add_another_result == "n":
                        dispMenu()
                        return
                    else:
                        print("Please enter a valid response (Y/N). ")
                        continue
            else:
                print("The score/scores you entered is/are NOT valid.")
                continue         
        else:
            print("The match ID you entered is NOT valid.")
            continue

        input("\nPress Enter to continue.")     # End function with this line


def dispWinner():
    draw_info_lst_of_tup = AddWinner()
    columnOutput(draw_info_lst_of_tup, colMatchInfo, '{:^10} | {:^20} | {:^15} | {:^20} | {:^15} | {:^15}')
   
 

#function to display the menu
def dispMenu():
    print("==== WELCOME TO LU TABLE TENNIS ===")
    print("1 - List Draw")
    print("2 - List Teams and Players")
    print("3 - List Players - alphabetical (by surname)")
    print("4 - List Players - alphabetical (by firstname)")
    print("5 - Add Team")
    print("6 - Add Match Result")
    print("7 - Create Draw")
    print("8 - Display Winners")
    print("Q - Quit")
    print("R - Repeat Menu")


# This is the main program


# Repeat this until user enters a "Q"
dispMenu()
response = input("Please select menu choice: ").upper()
while response.upper() != "Q":
    if response == "1":
        listDraw()
    elif response == "2":
        listTeams()
    elif response == "3":
        listMembersSurnameAlpha()
    elif response == "4":
        listMembersFirstnameAlpha()
    elif response == "5":
        addTeam()
    elif response == "6":
        addResult()
    elif response == "7":
        createDraw()
    elif response == "8":
        dispWinner()
    elif response == "R":
        dispMenu()
    else:
        print("invalid response, please re-enter")

    print("")
    dispMenu()
    response = input("Please select menu choice: ")

print("=== Thank you for using LU TABLE TENNIS ===")



