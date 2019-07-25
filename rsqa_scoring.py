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

# Rejection Sensitivity Questionnaire (Adult Version) 

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/wqm12bmazgoizmh8wzksk361dma8ltpe
Scoring: https://yale.box.com/s/wqm12bmazgoizmh8wzksk361dma8ltpe
"""

# SCORING:
"""
1. The Scale is typically 1-6, and the score is the average of the 9 rejection sensitivity scores 
	   (which are calculated by multiplying together items 1 and 2, 3 and 4, etc.).  

2. Any Prefer Not To Answer selection was not counted toward the final score.

3. Any Question left blank was not counted toward the final score.
"""

# Total score:	min= 1	max= 36
# ------------------------------------------------------------------------------
#Data Preparation 
def rsqa_analysis(df):
	# These are the different headers and their corresponding questions
	rsqa_concern_key= ['rsqa_1', 'rsqa_3', 'rsqa_5', 'rsqa_7','rsqa_9', 'rsqa_11', 'rsqa_13', 'rsqa_15','rsqa_17']
	rsqa_expect_key= ['rsqa_2', 'rsqa_4', 'rsqa_6', 'rsqa_8','rsqa_10', 'rsqa_12', 'rsqa_14', 'rsqa_16','rsqa_18']

	rsqa_tot_key=['rsqa_1', 'rsqa_3', 'rsqa_5', 'rsqa_7','rsqa_9', 'rsqa_11', 'rsqa_13', 'rsqa_15','rsqa_17','rsqa_2', 'rsqa_4', 'rsqa_6', 'rsqa_8','rsqa_10', 'rsqa_12', 'rsqa_14', 'rsqa_16','rsqa_18']

	df[rsqa_tot_key]= df[rsqa_tot_key].replace(['very unconcerned', 'unconcerned',  'somewhat unconcerned', 'somewhat concerned','concerned', 'very concerned'], [1,2,3,4,5,6])
	df[rsqa_tot_key]= df[rsqa_tot_key].replace(['very unlikely', 'unlikely',  'somewhat unlikely', 'somewhat likely','likely', 'very likely'], [6,5,4,3,2,1])
	df.rsqa_7
	df.rsqa_8

	# Check for values that don't match parameters 
	rsqa_check=df[rsqa_tot_key].apply(pd.to_numeric,args=('raise',))
	rsqa_check=rsqa_check[(rsqa_check !=1) & (rsqa_check !=2) & (rsqa_check !=3) & (rsqa_check !=4) & (rsqa_check !=5) & (rsqa_check !=6) & (rsqa_check !=999)].sum()
	for x in rsqa_check:
		if x!=0:
			df['rsqa_error']=np.nan
			df.rsqa_error=df.rsqa_error.replace([np.nan],["Your RSQA responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			rsqa_result=df['rsqa_error']
			
		else:
			# ------------------------------------------------------------------------------
			# RSQA Scoring

			# change the numbers to numeric floats
			rsqaconcern = df[rsqa_concern_key].apply(pd.to_numeric, args=('coerce',))
			rsqaexpect = df[rsqa_expect_key].apply(pd.to_numeric, args=('coerce',))
			rsqa = df[rsqa_tot_key].apply(pd.to_numeric, args=('coerce',))

			# These count the number of questions answered as prefer not to answer and left blank
			rsqa_prefernotanswer= df[rsqa_tot_key].apply(lambda x: sum(x==999), axis=1)
			rsqa_leftblank = rsqa.apply(lambda x: sum(x.isnull().values), axis=1)
			rsqa=rsqa.replace(np.nan,999)

			# Multiply together the corresponding concern and expect responses 
			df['rsqa1']= df.rsqa_1*df.rsqa_2
			df['rsqa2']= df.rsqa_3*df.rsqa_4
			df['rsqa3']= df.rsqa_5*df.rsqa_6
			df['rsqa4']= df.rsqa_7*df.rsqa_8
			df['rsqa5']= df.rsqa_9*df.rsqa_10
			df['rsqa6']= df.rsqa_11*df.rsqa_12
			df['rsqa7']= df.rsqa_13*df.rsqa_14
			df['rsqa8']= df.rsqa_15*df.rsqa_16
			df['rsqa9']= df.rsqa_17*df.rsqa_18

			# Exclude 'Prefer to not answer' responses from the final sum 
			rsqa_sum_keys= ['rsqa1','rsqa2','rsqa3','rsqa4','rsqa5','rsqa6','rsqa7','rsqa8','rsqa9']
			df[rsqa_sum_keys]=df[rsqa_sum_keys].replace(np.nan,999)
			rsqa_sum_df = df[rsqa_sum_keys].apply(pd.to_numeric, args=('coerce',))
			rsqa_exclude= df[rsqa_sum_keys].apply(lambda x: sum(x>100), axis=1)

			# Divide the sum by the number of answered questions to get the score 
			rsqa_sum = rsqa_sum_df[rsqa_sum_df[rsqa_sum_keys] < 100].sum(axis=1)
			rsqa_score= rsqa_sum/(9-rsqa_exclude)

			# Check for scores that are outside acceptable values 
			for x in rsqa_score:
				if (x<1 or x>36) and x!=np.nan:
					rsqa_score=rsqa_score.replace([x],["Warning: This RSQA score (%d) falls outside of the accepted range (1 to 36). Please check your data and try again."  % x])

			# Condense summary scores into dataframe
			rsqaall = pd.DataFrame({'RSQA_Left_Blank' : rsqa_leftblank, 'RSQA_Prefer_Not_to_Answer': rsqa_prefernotanswer,'RSQA_Score': rsqa_score})

			# ------------------------------------------------------------------------------
			# Generate Output

			# Put the scores into one frame
			rsqa_frames = [df.SUBJECT_ID, rsqaall]
			rsqa_result = pd.concat(rsqa_frames, axis=1)
	return rsqa_result
	
	#save result to csv
	#rsqa_result.to_csv(raw_input("Save your RSQ-A output as: "))