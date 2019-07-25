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

# PERCEIVED STRESS SCALE

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/647c65w4651dm6r2vzob43dmf2644153
Scoring: https://yale.box.com/s/647c65w4651dm6r2vzob43dmf2644153
"""

# SCORING:
"""
1. The Scale is typically 0-4, and the score is the sum of all answers.  Questions that should be reverse scored are reverse scored.

3. Any response left blank or prefer not to answer will be replaced with the average
score on the corresponding subscale and then added to the final score (Avram).
"""

# NEVER         ALMOST NEVER        SOMETIMES       FAIRLY OFTEN    VERY OFTEN
#   0                1                  2                3               4

# Total score:	min= 0	max= 40
# ------------------------------------------------------------------------------
# Data Preparation
def pss_analysis(df):
	# These are the different headers and their corresponding questions
	pss_negative_keys_for =['pss_1', 'pss_2', 'pss_3', 'pss_6', 'pss_9', 'pss_10']
	pss_positive_keys_reverse =['pss_4', 'pss_5', 'pss_7', 'pss_8']
	pss_tot_keys= ['pss_1', 'pss_2', 'pss_3', 'pss_6', 'pss_9', 'pss_10', 'pss_4', 'pss_5', 'pss_7', 'pss_8']

	# Replace Qualtrics text answers with numerical values
	df[pss_tot_keys]= df[pss_tot_keys].replace(['never', 'almost never',  'sometimes', 'fairly often','very often'], [0,1,2,3,4])

	# Check for values that don't match parameters 
	pss_check=df[pss_tot_keys].apply(pd.to_numeric,args=('raise',))
	pss_check=pss_check[(pss_check !=0) & (pss_check !=1) & (pss_check !=2) & (pss_check !=3) & (pss_check !=4) & (pss_check !=999)].sum()
	for x in pss_check:
		if x!=0:
			df['pss_error']=np.nan
			df.pss_error=df.pss_error.replace([np.nan],["Your PSS responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			pss_result=df['pss_error']
			
		else:
			# ------------------------------------------------------------------------------
			# PSS Reverse Scoring

			# Change the numbers to numeric floats
			pss_reverse = df[pss_positive_keys_reverse].apply(pd.to_numeric, args=('coerce',))

			# These count the number of questions answered as prefer not to answer or left blank
			pss_reverse_prefernotanswer= pss_reverse.apply(lambda x: sum(x==999), axis=1)
			pss_reverse_leftblank = pss_reverse.apply(lambda x: sum(x.isnull().values), axis=1)
			pss_reverse_unanswered= pss_reverse_prefernotanswer + pss_reverse_leftblank

			# Sum the reverse scored items
			reverse_pss_score = pss_reverse.rsub(5)[pss_reverse[pss_positive_keys_reverse] <= 4].sum(axis=1)


			# ------------------------------------------------------------------------------
			# PSS Forward Scoring

			# change the numbers to numeric floats
			pss_forward = df[pss_negative_keys_for].apply(pd.to_numeric, args=('coerce',))

			# These count the number of questions answered as prefer not to answer or left blank
			pss_forward_prefernotanswer= pss_forward.apply(lambda x: sum(x==999), axis=1)
			pss_forward_leftblank = pss_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			pss_forward_unanswered= pss_forward_prefernotanswer+pss_forward_leftblank

			# sum the forward scores together to get the PSS Forward score and keeps anything less than or equal to 4
			forward_pss_score = pss_forward[pss_forward[pss_negative_keys_for] <= 4].sum(axis=1)
			
			# ------------------------------------------------------------------------------
			# PSS Total Scoring

			# Get the total PSS Score
			total_pss_score = reverse_pss_score + forward_pss_score
			
			# TOTAL ANSWERS LEFT BLANK
			total_pss_prefernotanswer = pss_reverse_prefernotanswer + pss_forward_prefernotanswer
			total_pss_leftblank= pss_reverse_leftblank+pss_forward_leftblank
			total_pss_unanswered= pss_reverse_unanswered+pss_forward_unanswered
			
			# Replace missing values with subscale averages
			total_pss_score = total_pss_score + (total_pss_unanswered * total_pss_score/ (10-total_pss_unanswered))

			# Check for scores that are outside acceptable values 
			for x in total_pss_score:
				if (x<0 or x>40) and x!=np.nan:
					total_pss_score=total_pss_score.replace([x],["Warning: This PSS score (%d) falls outside of the accepted range (0 to 40). Please check your data and try again."  % x])

			pssall = pd.DataFrame({'PSS_Left_Blank' : total_pss_leftblank, 'PSS_Prefer_Not_to_Answer': total_pss_prefernotanswer, 'PSS_Score': total_pss_score})

			# ------------------------------------------------------------------------------
			# Generate Output

			# Put the scores into one frame
			pss_frames = [df.SUBJECT_ID, pssall]
			pss_result = pd.concat(pss_frames, axis=1)
	return pss_result
	#pss_result.to_csv(raw_input("Save your PSS output as: "))