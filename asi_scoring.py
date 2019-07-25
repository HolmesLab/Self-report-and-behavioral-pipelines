#!/usr/bin/python
"""
Battery Scores Package for Processing Qualtrics CSV Files

@author: David Gruskin
@email: david.gruskin@yale.edu
@version: 1.0
@date: 2017.07.06
"""
import pandas as pd
import numpy as np
import sys 

# Anxiety Sensitivity Index

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/3jf0nntidzii8inb07xn6b267o93a5gb
Scoring: https://yale.box.com/s/ikyauawaoi2za4ht1bfd2s6719zt82qb
"""

# SCORING:
"""
1. The Scale is typically 0-4, and the score is the sum of all answers. 

2. How to handle missing values is not explicitly mentioned in the primary resources above, so
if any value is left blank or prefer not to answer, those missing values will be replaced with the average
score and then added to the final score (Avram).
"""

# very little     a little             some            much          very much	Prefer not to answer
#   0                1                  2                3               4				999

# Total score:	min= 0	max= 64
# ------------------------------------------------------------------------------
# Data Preparation 
def asi_analysis(df):
	# Group all ASI questions under list asi_tot_keys
	asi_tot_keys =['asi_1', 'asi_2','asi_3','asi_4','asi_5','asi_6','asi_7','asi_8','asi_9','asi_10','asi_11','asi_12','asi_13','asi_14','asi_15','asi_16']

	# Replace Qualtrics text answers with numerical values
	df[asi_tot_keys]= df[asi_tot_keys].replace(['very little', 'a little',  'some', 'much','very much'], [0,1,2,3,4])

	# Check for values that fall outside parameter ranges
	asi_check=df[asi_tot_keys].apply(pd.to_numeric,args=('raise',))
	asi_check=asi_check[(asi_check !=0) & (asi_check !=1) & (asi_check !=2) & (asi_check !=3) & (asi_check !=4) & (asi_check !=999)].sum()
	for x in asi_check:
		if x!=0:
			df['asi_error']=np.nan
			df.asi_error=df.asi_error.replace([np.nan],["Your ASI responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			asi_result=df['asi_error']
		
		else:
			# ------------------------------------------------------------------------------
			# ASI Scoring

			# Change the numbers to numeric floats
			asi_forward = df[asi_tot_keys].apply(pd.to_numeric, args=('coerce',))

			# These count the number of questions answered as prefer not to answer and left blank
			asi_prefernotanswer= asi_forward.apply(lambda x: sum(x==999), axis=1)
			asi_leftblank = asi_forward.apply(lambda x: sum(x.isnull().values), axis=1)

			# Sum the forward scores together to get the ASI Forward score and keeps anything less than or equal to 4
			asi_score = asi_forward[asi_forward[asi_tot_keys] <= 4].sum(axis=1)

			# Total questions left unanswered 
			asi_unanswered = asi_leftblank + asi_prefernotanswer

			# Replace unanswered items with the average and recalculate
			asi_score = asi_score + (asi_unanswered * asi_score / (len(asi_tot_keys)-asi_unanswered))

			# Check for scores that are outside acceptable values 
			for x in asi_score:
				if (x<0 or x>64) and x!=np.nan:
					asi_score=asi_score.replace([x],["Warning: This ASI score (%d) falls outside of the accepted range (0 to 64). Please check your data and try again."  % x])

			# Condense summary scores into dataframe
			asiall = pd.DataFrame({'ASI_Left_Blank': asi_leftblank,'ASI_Prefer_Not_to_Answer': asi_prefernotanswer,'ASI_Score': asi_score})

			# ------------------------------------------------------------------------------
			# Generate Output

			# Put the scores into one frame
			asi_frames = [df.SUBJECT_ID, asiall]
			asi_result = pd.concat(asi_frames, axis=1)
	return asi_result

		# Save result to csv
		#asi_result.to_csv(raw_input("Save your ASI output as: "))