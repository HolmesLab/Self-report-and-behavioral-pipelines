 #!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files

@author: Bradley Wise
@edited by: David Gruskin
@email: david.gruskin@yale.edu
@version: 2.0
@date: 2017.07.06
"""
import pandas as pd
import numpy as np
import sys 

# BEHAVIORAL INHIBITION SCALE / BEHAVIORAL ACTIVATION SCALE

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/1fmoogofz2gmsict6jtl3gjmpfdi9htv
Scoring:https://yale.box.com/s/5ps8pmv3ip0m93iofgraa89au6s72rb3
"""

# SCORING:
"""
1. Scores are the sum of each subscale. Questions that should be reverse scored are reverse scored.

2. How to handle missing values is not explicitly mentioned in the primary resources above, so
if any value is left blank or prefer not to answer, those missing values will be replaced with the average
score on that particular subscale and then added to the final subscore total (Avram).
"""

# VERY TRUE - SOMEWHAT TRUE - SOMEWHAT FALSE - VERY FALSE - PREFER NOT TO ANSWER
#     1             2               3               4               YOUR #

# BAS_DRIVE		min:4 max:16
# BAS_FUN 		min:4 max:16	
# BAS_REWARD	min:5 max:20
# BIS 			min:7 max:28																
# ------------------------------------------------------------------------------
# Data Preparation 
def bisbas_analysis(df):
	# These are the different headers and their corresponding questions
	# ALL bisbas scoreS ARE REVERSE CODED EXCEPT the BIS HEADER
	drive_headers = ["bisbas_3", "bisbas_9", "bisbas_12", "bisbas_21"]
	funseeking_headers = ["bisbas_5", "bisbas_10", "bisbas_15", "bisbas_20"]
	reward_headers = ["bisbas_4", "bisbas_7", "bisbas_14", "bisbas_18","bisbas_23"]
	forward_code_bis = ["bisbas_2", "bisbas_22"]
	reverse_code_bis = ["bisbas_8", "bisbas_13", "bisbas_16","bisbas_19", "bisbas_24"]
	fillerheaders = ["bisbas_1", "bisbas_6", "bisbas_11", "bisbas_17"]

	bisbas_tot_keys=drive_headers+funseeking_headers+reward_headers+forward_code_bis+reverse_code_bis+fillerheaders

	# Replace Qualtrics text answers with numerical values
	df[bisbas_tot_keys]= df[bisbas_tot_keys].replace(['very true', 'somewhat true', 'somewhat false', 'very false'], [1,2,3,4])

	# Check for values that don't match parameters 
	bisbas_check=df[bisbas_tot_keys].apply(pd.to_numeric,args=('raise',))
	bisbas_check=bisbas_check[(bisbas_check !=1) & (bisbas_check !=2) & (bisbas_check !=3) & (bisbas_check !=4) & (bisbas_check !=999)].sum()
	for x in bisbas_check:
		if x!=0:
			df['bisbas_error']=np.nan
			df.bisbas_error=df.bisbas_error.replace([np.nan],["Your BIS/BAS responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			bisbas_result=df['bisbas_error']
			
		else:
			# ------------------------------------------------------------------------------
			# FILLERS

			# Change the numbers in drive headers to numeric floats
			fillers = df[fillerheaders].apply(pd.to_numeric, args=('raise',))

			# ------------------------------------------------------------------------------
			# DRIVE score - ALL REVERSE, NO FORWARD

			# Change the numbers in drive headers to numeric floats
			drive=df[drive_headers].apply(pd.to_numeric,args=('raise',))

			# Count the number of drive questions answered as "prefer to not answer" or left blank
			drive_prefernotanswer= drive.apply(lambda x: sum(x==999), axis=1)
			drive_leftblank = drive.apply(lambda x: sum(x.isnull().values), axis=1)
			drive_unanswered= drive_prefernotanswer+drive_leftblank

			# Reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
			# A score of 999 is "prefer not to answer" and will not be scored.
			# Adds up the reverse scores
			drive_score = drive[drive[drive_headers] <= 4].rsub(5).sum(axis=1, skipna=True)

			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			drive_score = drive_score + (drive_unanswered * drive_score / (len(drive_headers)-drive_unanswered))

			driveall = pd.DataFrame({'BAS_D_Left_Blank' : drive_leftblank, 'BAS_D_Prefer_Not_to_Answer': drive_prefernotanswer, 'BAS_D_Score' : drive_score,})

			# Check for scores that are outside acceptable values 
			for x in drive_score:
				if (x<4 or x>16) and x!=np.nan:
					drive_score=drive_score.replace([x],["Warning: This BAS_drive score (%d) falls outside of the accepted range (4 to 16). Please check your data and try again."  % x])


			# ------------------------------------------------------------------------------
			# Funseeking score - ALL REVERSE, NO FORWARD

			# Change the numbers in funseeking headers to numeric floats
			funseeking=df[funseeking_headers].apply(pd.to_numeric,args=('raise',))

			# Count the number of funseeking questions answered as "prefer to not answer" or left blank
			funseeking_prefernotanswer= funseeking.apply(lambda x: sum(x==999), axis=1)
			funseeking_leftblank = funseeking.apply(lambda x: sum(x.isnull().values), axis=1)
			funseeking_unanswered= funseeking_prefernotanswer+funseeking_leftblank

			# Reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
			# A score of 999 is "prefer not to answer" and will not be scored.
			# Adds up the reverse scores
			funseeking_score = funseeking[funseeking[funseeking_headers] <= 4].rsub(5).sum(axis=1, skipna=True)

			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			funseeking_score = funseeking_score + (funseeking_unanswered * funseeking_score / (len(funseeking_headers)-funseeking_unanswered))

			funseekingall = pd.DataFrame({'BAS_F_Left_Blank' : funseeking_leftblank, 'BAS_F_Prefer_Not_to_Answer': funseeking_prefernotanswer, 'BAS_F_Score' : funseeking_score,})

			# Check for scores that are outside acceptable values 
			for x in funseeking_score:
				if x<4 or x>16:
					funseeking_score=funseeking_score.replace([x],["Warning: This BAS_funseeking score (%d) falls outside of the accepted range (4 to 16). Please check your data and try again."  % x])

			# ------------------------------------------------------------------------------
			# REWARD score - ALL REVERSE, NO FORWARD

			# Change the numbers in reward headers to numeric floats
			reward=df[reward_headers].apply(pd.to_numeric,args=('raise',))

			# Count the number of reward questions answered as "prefer to not answer" or left blank
			reward_prefernotanswer= reward.apply(lambda x: sum(x==999), axis=1)
			reward_leftblank = reward.apply(lambda x: sum(x.isnull().values), axis=1)
			reward_unanswered= reward_prefernotanswer+reward_leftblank

			# Reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
			# A score of 999 is "prefer not to answer" and will not be scored.
			# Adds up the reverse scores
			reward_score = reward[reward[reward_headers] <= 4].rsub(5).sum(axis=1, skipna=True)

			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			reward_score = reward_score + (reward_unanswered * reward_score / (len(reward_headers)-reward_unanswered))

			rewardall = pd.DataFrame({'BAS_R_Left_Blank' : reward_leftblank, 'BAS_R_Prefer_Not_to_Answer': reward_prefernotanswer, 'BAS_R_Score' : reward_score,})

			# Check for scores that are outside acceptable values 
			for x in reward_score:
				if x<5 or x>20:
					reward_score=reward_score.replace([x],["Warning: This BAS_reward score (%d) falls outside of the accepted range (5 to 20). Please check your data and try again."  % x])

			# ------------------------------------------------------------------------------
			# BIS Score

			# Change the numbers in reverse_code_bis to numeric floats
			bis_reverse = df[reverse_code_bis].apply(pd.to_numeric, args=('raise',))

			# Count the number of reverse BIS questions answered as 'prefer not to answer' or left blank
			bis_reverse_prefernotanswer= bis_reverse.apply(lambda x: sum(x==999), axis=1)
			bis_reverse_leftblank = bis_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

			# Reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4. Sum the reversed scores together to get the BIS Reverse score
			reverse_bis_score = bis_reverse[bis_reverse[reverse_code_bis] <= 4].rsub(5).sum(axis=1, skipna=True)

			# Change the numbers in forward_code_bis to numeric floats
			bis_forward = df[forward_code_bis].apply(pd.to_numeric, args=('raise',))

			# Count the number of reverse BIS questions answered as 'prefer not to answer' or left blank
			bis_forward_prefernotanswer = bis_forward.apply(lambda x: sum(x==999), axis=1)
			bis_forward_leftblank = bis_forward.apply(lambda x: sum(x.isnull().values), axis=1)

			# Sum the forward items together to get the BIS Forward score and keeps anything over 4 from the sum.
			forward_bis_score = bis_forward[(bis_forward[forward_code_bis] >= 1) & (bis_forward[forward_code_bis] <= 4)].sum(axis=1)

			# Get the total BIS Score
			total_bis_score = reverse_bis_score + forward_bis_score
			bis_prefernotanswer = bis_reverse_prefernotanswer + bis_forward_prefernotanswer
			bis_leftblank= bis_forward_leftblank+bis_reverse_leftblank
			bis_unanswered= bis_leftblank+bis_prefernotanswer

			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			total_bis_score = (total_bis_score + (bis_unanswered * total_bis_score / (len(reverse_code_bis)+len(forward_code_bis)-bis_unanswered)))

			bisall = pd.DataFrame({'BIS_Left_Blank' : bis_leftblank, 'BIS_Prefer_Not_to_Answer': bis_prefernotanswer, 'BIS_Score': total_bis_score})

			# Check for scores that are outside acceptable values 
			for x in total_bis_score:
				if x<7 or x>28:
					total_bis_score=total_bis_score.replace([x],["Warning: This BIS score (%d) falls outside of the accepted range (7 to 28). Please check your data and try again."  % x])

			# -----------------------------------------------------------------------------
			# Generate Output

			# Put the scores into one frame
			bisbas_frames = [df.SUBJECT_ID, driveall, funseekingall, rewardall, bisall]
			bisbas_result = pd.concat(bisbas_frames, axis=1)
	return bisbas_result
	
			#bisbas_result.to_csv(raw_input("Save your BIS/BAS output as: "))
