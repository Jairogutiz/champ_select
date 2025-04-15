#Who am i

im new to web development, i've been coding for a few months now and i'm trying to learn how to build a web application, so give me instructions that someone that's learning web development can understand.

You shouldn't try to build the entire application, just help me with what i'm asking for, since im learning web development i need to go step by step and understand each part of the application.


#What im trying to build

I Want to build a web application that shows recommendations to league of legends players in a webpage while they are in champ select, the reason i want it on a webpage is so that the person can share a link in the champ select chat and it will show a a menu where the visitors can pick a role, and view the recommendations for that role so that it can become viral.




#How we get the data

inside zClient/client.py we have a function called get_champ_select_data that gets the data from the lockfile and sends it to the api gateway.

the data the api gets is in the test_api_event.json file. it's unwrapped from the api gateway event format.

the Data of the interactions is in the models.



#How are we going to do the calculations.

let's use the test_api_event.json file to explain. how we are going to calculate the recommendations.

Assigned role = jungle

The enemy team consists of Aatrox (top), Ahri (middle), Akali (middle), Alistar (support), and Amumu (jungle).
The ally team consists of Anivia (middle), Annie (middle), Aphelios (bottom), Ashe (bottom), and Aurelion Sol (middle).


inside the champion interactions model we have the winrate, delta_wr, sample_size of each champion interaction.

it follows this format

	Zyra	Support	Aurelion Sol	Bottom	Synergy	54.21215580248283	/0.3578441975171678	16
	Zyra	Support	Cassiopeia	Bottom	Synergy	54.77146082295388	0.5714608229538752	25

the recommendations page should show a table with the following columns:

remember the number of locked in champions varies trough the champ select, so we are going to be recieving updates, and so the table should be updated to reflect the new data.


this is when 1 champion is locked in.
Enemy champion 1 (Aatrox) - Matchup Wr - Overall Wr - Synergy Wr 

This is when just 2 champions are locked in.
Enemy champion 2 (Aatrox) - Matchup Wr - Overall Wr - Synergy Wr - Ally champion 1 (Anivia)


This is when all champions are locked in.
Enemy champion 1 (Aatrox) - Enemy champion 2 (Ahri) - Enemy champion 3 (Akali) - Enemy champion 4 (Alistar) - Enemy champion 5 (Amumu) - Matchup Wr - Overall Wr - Synergy Wr - Ally champion 1 (Anivia) - Ally champion 2 (Annie) - Ally champion 3 (Aphelios) - Ally champion 4 (Ashe) - Ally champion 5 (Aurelion Sol)


since our assigned role is jungle, we are going to get a list of all the distinct jungle champions in the champion interactions model on champion1 column.

when we have a list of distinct jungle champions, we are going to use the champion interactions model to get the winrate, delta_wr, sample_size of each champion interaction.

so let's say the distinct jungle champions are leesin, elise, and jarvan. and the enemy team has locked aatrox, and the ally team has locked anivia.

we are going to get the winrate, delta_wr, sample_size of the interactions between leesin and the enemy team and the ally team.

let's say we get this data:

	Lee Sin	Jungle	Aatrox	Top	Matchup	49.83	-0.98	9696
    Lee Sin	Jungle	Anivia	Middle	Matchup	49.148519336063046	0.7385193360630465	2196


The recommendations page should show the following:

Enemy champion 1 (Aatrox) / Matchup Wr / Overall Wr / Synergy Wr / Ally champion 1 (Anivia) 
(winrate of lee sin vs aatrox) 49.83 (delta_wr of lee sin vs aatrox) 0.98 (sample_size of lee sin vs aatrox) 9696 / (average winrate of lee sin vs enemy team) 49.83 (the sum of all the delta_wr of lee sin vs enemy team) 0.7385193360630465 (the number of low sample size values vs enemy team if it's less than 300) / (average of the values of winrate in the matchup and synergy columns) 49.48 / (sum of the values of delta_wr in the matchup and synergy columns) 0.25 / (the sum of the sample sizes of the values in the matchup and synergy columns) 0 / (average  winrate of lee sin with ally team) 49.148519336063046 (the sum of all the delta_wr of lee sin with ally team) 0.7385193360630465 (the number of low sample size values in the ally team if it's less than 300) / (winrate of lee sin with anivia) 49.148519336063046 (delta_wr of lee sin with anivia) 0.7385193360630465 (sample_size of lee sin with anivia) 2196

and on each row we show the values for each distinct champion in their respective columns.

there's an image in zclient/recommendations.png that shows the recommendations page as i want it to look like.


# Recommendations Page Functionality

## Table Structure
The recommendations page displays a dynamic table that shows champion matchup and synergy data. The table adapts its columns based on the number of champions locked in during champion select.

### Table Headers
- Enemy champion columns (showing champion icon and role icon)
- Matchup Statistics column
- Champion Statistics column (showing recommended champion icon)
- Synergy Statistics column  
- Ally champion columns (showing champion icon and role icon)

### Data Display
Each cell in the table shows:
- Winrate (displayed as a percentage)
- Delta (change in winrate, shown with + or - prefix)
- Sample size (shown in parentheses)

## Visual Features

### Color Coding
- Winrates are color coded on a gradient:
  - Below 47%: Red (#FF4444)
  - 47-50%: Red to Yellow gradient
  - 50-53%: Yellow to Green gradient
  - Above 53%: Blue (#00BFFF)

- Delta values use a similar gradient:
  - Below -3%: Red
  - -3% to 0%: Red to Yellow
  - 0% to 3%: Yellow to Green
  - Above 3%: Blue

### Champion Icons
- Champion icons in the main column have colored borders indicating data reliability:
  - Green: Less than 30% low sample matchups
  - Yellow: 30-40% low sample matchups
  - Red: Over 50% low sample matchups
  - Gradients between these colors for values in between

### Sample Size Indicators
- Sample sizes below 300 are marked in orange
- The percentage of low sample matchups is displayed below each recommended champion

## Sorting Functionality
The table can be sorted by different metrics:
- Matchup WR and Matchup Delta
- Combined Score (default), Overall WR, and Overall Delta
- Synergy WR and Synergy Delta

## Dynamic Updates
- The page automatically polls for updates every 500ms
- Updates stop when all 10 champions are locked in
- Only updates when there are actual changes to the team composition
- Maintains sort order when data updates

## Debug Features
- Debug logging (when DEBUG = true)
- Detailed logging of data changes and sorting operations
- Error tracking for champion ID mapping

## Responsive Design
- Consistent cell heights (80px)
- Flexible layout that adapts to different screen sizes
- Centered alignment of content
- Clear visual hierarchy with champion icons and statistics

## Page Title
- Shows the assigned role with both text and role icon
- Updates dynamically when role changes















