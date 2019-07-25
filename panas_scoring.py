#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files
@author: David Gruskin
@email: david.gruskin@yale.edu
@version: 2.0
@date: 2017.08.04
"""
import pandas as pd
import numpy as np
import sys 

# Positive and Negative Affect Schedule 

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/13io2yje4trm5ode8acw6wsk0ip4ij25
Scoring:https://yale.box.com/s/13io2yje4trm5ode8acw6wsk0ip4ij25
"""

# SCORING:
"""
1. Positive and Negative affect scores range from 10-50 and are computed by summing the responses to relevant questions.

2. Prefer not to answer or blank responses will be replaced with the mean response from the relevant score. 
"""

# Positive/Negative scores:	min= 10	  max= 50
# ------------------------------------------------------------------------------
# Data Preparation 

def panas_analysis(df):
	# THESE KEYS ARE READ BY THE COLUMN DICTIONARY -> Question_Name
	panas_zero= ['panas_0']
	panas_positive_keys = ['panas_1', 'panas_3', 'panas_5', 'panas_9','panas_10', 'panas_12', 'panas_14', 'panas_16','panas_17', 'panas_19']
	panas_negative_keys = ['panas_2', 'panas_4', 'panas_6', 'panas_7','panas_8', 'panas_11', 'panas_13', 'panas_15','panas_18', 'panas_20']

	panas_tot_keys= panas_positive_keys+panas_negative_keys+panas_zero

	# Replace Qualtrics text answers with numerical values
	panas_zero
	df[panas_tot_keys]= df[panas_tot_keys].replace(['1', '2', 'very slightly or not at all', 'a little',  'moderately', 'quite a bit','extremely'], ["at_present","past_week",1,2,3,4,5])

	# Check for values that fall outside parameter ranges
	panas_check=df[panas_tot_keys].apply(pd.to_numeric,args=('raise',))
	panas_check=panas_check[(panas_check !=1) & (panas_check !=2) & (panas_check !=3) & (panas_check !=4) & (panas_check !=5) & (panas_check !=999)].sum()
	for x in panas_check:
		if x!=0:
			df['panas_error']=np.nan
			df.panas_error=df.panas_error.replace([np.nan],["Your PANAS responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			panas_result=df['panas_error']

		else:
	# ------------------------------------------------------------------------------
	# Positive score

	# Forward scores and questions unanswered
			panas_positive = df[panas_positive_keys].apply(pd.to_numeric, args=('raise'))
			panas_positive_leftblank = panas_positive.apply(lambda x: sum(x.isnull().values), axis=1)
			panas_positive_prefernotanswer = panas_positive.apply(lambda x: sum(x==999), axis=1)
			panas_positive_unanswered= panas_positive_leftblank+panas_positive_prefernotanswer
		
			# Sum all the forward scores
			panas_positive_score = panas_positive[(panas_positive[panas_positive_keys] >= 1) & (panas_positive[panas_positive_keys] <= 5)].sum(axis=1)
		
			# Total score
			panas_positive_score = panas_positive_score + (panas_positive_unanswered * panas_positive_score / (10-panas_positive_unanswered))
		
			positiveall = pd.DataFrame({'PANAS_Positive_Affect_Left_Blank' : panas_positive_leftblank, 'PANAS_Positive_Affect_Prefer_Not_to_Answer': panas_positive_prefernotanswer,'PANAS_Positive_Affect_Score': panas_positive_score})
		
			# Check for scores that are outside acceptable values 
			for x in panas_positive_score:
				if (x<10 or x>50) and x!=np.nan:
					panas_positive_score=panas_positive_score.replace([x],["Warning: This PANAS_positive score (%d) falls outside of the accepted range (10 to 50). Please check your data and try again."  % x])
	
			# ------------------------------------------------------------------------------
			# Negative score
		
			# Forward scores and questions unanswered
			panas_negative = df[panas_negative_keys].apply(pd.to_numeric, args=('raise',))
			panas_negative_leftblank = panas_negative.apply(lambda x: sum(x.isnull().values), axis=1)
			panas_negative_prefernotanswer = panas_negative.apply(lambda x: sum(x==999), axis=1)
			panas_negative_unanswered= panas_negative_leftblank+panas_negative_prefernotanswer
		
			# Sum all the forward scores
			panas_negative_score = panas_negative[(panas_negative[panas_negative_keys] >= 1) & (panas_negative[panas_negative_keys] <= 5)].sum(axis=1)
		
			# Total score
			panas_negative_score = panas_negative_score + (panas_negative_unanswered * panas_negative_score / (10-panas_negative_unanswered))
		
			negativeall = pd.DataFrame({'PANAS_Negative_Affect_Left_Blank' : panas_negative_leftblank, 'PANAS_Negative_Affect_Prefer_Not_to_Answer': panas_negative_prefernotanswer,'PANAS_Negative_Affect_Score': panas_negative_score})
		
			# Check for scores that are outside acceptable values 
			for x in panas_negative_score:
				if (x<10 or x>50) and x!=np.nan:
					panas_negative_score=panas_negative_score.replace([x],["Warning: This PANAS_negative score (%d) falls outside of the accepted range (10 to 50). Please check your data and try again."  % x])
			# ------------------------------------------------------------------------------
			#Generate Output 
		
			# Put the scores into one frame
			panas_frames = [df.SUBJECT_ID, df.panas_0, positiveall,negativeall]
			panas_result = pd.concat(panas_frames, axis=1)
	return panas_result

#panas_result.to_csv(raw_input("Save your PANAS Output as: "))
