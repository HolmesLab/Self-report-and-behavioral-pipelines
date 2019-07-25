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

# State-Trait ANXIETY INVENTORY FOR ADULTS

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/tnprt0ny7mm8hbapbk4wjkdg27qj5x5k
Scoring: https://yale.box.com/s/yu1tmkqohty8nn2wewbaoc0nklila2mo
"""

# SCORING:
"""
1. Score of each item typically ranges from 1-4 with a prefer not to answer choice.

2. Scores are the sum of each subscale. Questions that should be reverse scored are reverse scored.

3. How to handle missing values is not explicitly mentioned in the primary resources above, so
if any value is left blank or prefer not to answer, those missing values will be replaced with the average
score on that particular subscale and then added to the final subscore total (Avram).
"""

# State/Trait scores:	min= 20	  max= 80
# ------------------------------------------------------------------------------
# Data Preparation 

def stai_analysis(df):
	# These are the different headers and their corresponding questions
	stai_trait_keys = ['stai_3', 'stai_4', 'stai_6', 'stai_7', 'stai_9', 'stai_12', 'stai_13', 'stai_14', 'stai_17','stai_18']
	stai_trait_rev_keys = ['stai_1', 'stai_2', 'stai_5', 'stai_8', 'stai_10', 'stai_11', 'stai_15', 'stai_16','stai_19','stai_20']
	stai_state_keys = ['stai_22', 'stai_24', 'stai_25', 'stai_28', 'stai_29', 'stai_31', 'stai_32', 'stai_35','stai_37','stai_38', 'stai_40']
	stai_state_rev_keys = ['stai_21', 'stai_23', 'stai_26', 'stai_27', 'stai_30', 'stai_33', 'stai_34', 'stai_36','stai_39']
	stai_tot_keys= stai_trait_keys+stai_trait_rev_keys+stai_state_keys+stai_state_rev_keys

	# Replace Qualtrics text answers with numerical values
	df[stai_tot_keys]= df[stai_tot_keys].replace(['not at all', 'almost never', 'somewhat', 'sometimes', 'moderately so', 'often','very much so', 'almost always'], [1,1,2,2,3,3,4,4])

	# Check for values that don't match parameters 
	stai_check=df[stai_tot_keys].apply(pd.to_numeric,args=('raise',))
	stai_check=stai_check[(stai_check !=1) & (stai_check !=2) & (stai_check !=3) & (stai_check !=4) & (stai_check !=999)].sum()
	for x in stai_check:
		if x!=0:
			df['stai_error']=np.nan
			df.stai_error=df.stai_error.replace([np.nan],["Your STAI responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			stai_result=df['stai_error']
			
		else:
			# ------------------------------------------------------------------------------

			# ------------------------------------------------------------------------------
			# STAI Trait score

			# Change the numbers in forward stai Trait headers to numeric floats
			stai_trait_forward = df[stai_trait_keys].apply(pd.to_numeric, args=('coerce',))

			# Sum the number of forward questions left blank or preferred not to answer
			stai_trait_forward_leftblank = stai_trait_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			stai_trait_forward_prefernotanswer = stai_trait_forward[stai_trait_forward[stai_trait_keys] == 999].count(axis=1)
			stai_trait_forward_unanswered = stai_trait_forward_leftblank + stai_trait_forward_prefernotanswer

			# Sum all the forward scores
			stai_trait_forward_score = stai_trait_forward[stai_trait_forward[stai_trait_keys] < 5].sum(axis=1)

			# Change the numbers in reverse stai Trait headers to numeric floats
			stai_trait_rev =df[stai_trait_rev_keys].apply(pd.to_numeric, args=('coerce',))

			# Sum the number of reverse questions left blank or preferred not to answer
			stai_trait_reverse_leftblank = stai_trait_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			stai_trait_reverse_prefernotanswer = stai_trait_rev[stai_trait_rev[stai_trait_rev_keys] == 999].count(axis=1)
			stai_trait_reverse_unanswered = stai_trait_reverse_leftblank + stai_trait_reverse_prefernotanswer

			# Sum all the reverse scores
			stai_trait_reverse_score = stai_trait_rev.rsub(5)[stai_trait_rev[stai_trait_rev_keys] < 5].sum(axis=1)

			# Total STAI Trait score
			total_stai_trait_score = stai_trait_forward_score + stai_trait_reverse_score
			total_stai_trait_score= total_stai_trait_score.replace([0], [np.nan])

			# Total STAI Trait answers unanswered
			total_stai_trait_unanswered = stai_trait_forward_unanswered + stai_trait_reverse_unanswered

			# Total answers left blank
			total_stai_trait_leftblank = stai_trait_forward_leftblank + stai_trait_reverse_leftblank

			# Total answers PREFER NOT TO ANSWER
			total_stai_trait_prefernotanswer = stai_trait_forward_prefernotanswer + stai_trait_reverse_prefernotanswer

			# Replace missing values with subscale averages
			total_stai_trait_score = total_stai_trait_score + (total_stai_trait_unanswered * total_stai_trait_score / (20-total_stai_trait_unanswered))

			# Check for scores that are outside acceptable values 
			for x in total_stai_trait_score:
				if (x<20 or x>80) and x!=np.nan:
					total_stai_trait_score=total_stai_trait_score.replace([x],["Warning: This STAI_trait score (%d) falls outside of the accepted range (20 to 80). Please check your data and try again."  % x])

			staitraitall = pd.DataFrame({'STAI_Trait_Left_Blank': total_stai_trait_leftblank,'STAI_Trait_Prefer_Not_to_Answer': total_stai_trait_prefernotanswer,'STAI_Trait_Score': total_stai_trait_score,})

			# ------------------------------------------------------------------------------
			# STAI State score

			# Change the numbers in forward stai State headers to numeric floats
			stai_state_forward = df[stai_state_keys].apply(pd.to_numeric, args=('coerce',))
			# sum the number of forward questions left blank or preferred not to answer
			stai_state_forward_leftblank = stai_state_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			stai_state_forward_prefernotanswer = stai_state_forward[stai_state_forward[stai_state_keys] == 999].count(axis=1)
			stai_state_forward_unanswered = stai_state_forward_leftblank + stai_state_forward_prefernotanswer

			# Sum all the forward scores
			stai_state_forward_score = stai_state_forward[stai_state_forward[stai_state_keys] < 5].sum(axis=1)

			# Change the numbers in forward stai State headers to numeric floats
			stai_state_rev = df[stai_state_rev_keys].apply(pd.to_numeric, args=('coerce',))

			# Sum the number of reverse questions left blank or preferred not to answer
			stai_state_reverse_leftblank = stai_state_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			stai_state_reverse_prefernotanswer = stai_state_rev[stai_state_rev[stai_state_rev_keys] == 999].count(axis=1)
			stai_state_reverse_unanswered = stai_state_reverse_leftblank + stai_state_reverse_prefernotanswer

			# Sum all the reverse scores
			stai_state_reverse_score = stai_state_rev.rsub(5)[stai_state_rev[stai_state_rev_keys] < 5].sum(axis=1)

			# Total STAI State score
			total_stai_state_score = stai_state_forward_score + stai_state_reverse_score
			total_stai_state_score= total_stai_state_score.replace([0], [np.nan])

			# Total STAI Trait answers unanswered
			total_stai_state_unanswered = stai_state_forward_unanswered + stai_state_reverse_unanswered

			# Total answers left blank
			total_stai_state_leftblank = stai_state_forward_leftblank + stai_state_reverse_leftblank
			
			#Total answers PREFER NOT TO ANSWER
			total_stai_state_prefernotanswer = stai_state_forward_prefernotanswer + stai_state_reverse_prefernotanswer

			# Replace missing values with subscale averages
			total_stai_state_score = total_stai_state_score + (total_stai_state_unanswered * total_stai_state_score / (20-total_stai_state_unanswered))
			
			# Check for scores that are outside acceptable values 
			for x in total_stai_state_score:
				if (x<20 or x>80) and x!=np.nan:
					total_stai_state_score=total_stai_state_score.replace([x],["Warning: This STAI_state score (%d) falls outside of the accepted range (20 to 80). Please check your data and try again."  % x])

			staistateall = pd.DataFrame({'STAI_State_Left_Blank': total_stai_state_leftblank,'STAI_State_Prefer_Not_to_Answer': total_stai_state_prefernotanswer,'STAI_State_Score': total_stai_state_score})
			
			# ------------------------------------------------------------------------------
			# Generate Output

			# Put the scores into one frame

			stai_frames = [df.SUBJECT_ID, staitraitall, staistateall]
			stai_result = pd.concat(stai_frames, axis=1)
	return stai_result

	# saves output to csv
	# stai_result.to_csv(raw_input("Save your stai output as: "))
