#!/usr/bin/python

"""Battery Scores Package for Processing Qualtrics CSV Files

@author: David Gruskin
@email: david.gruskin@yale.edu
@version: 1.0
@date: 2017.07.06
"""
import pandas as pd
import numpy as np
import sys 

# Retrospective Self-Report of Inhibition

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/uspejcf4s3l805o6vyzdkzb4buf2v9r4
Scoring: https://yale.box.com/s/lqamrtn0azblbiofy4e76z4m680zz5ck
"""

# SCORING:
"""
1. The RSRI is scored from 1 to 5 with a 'prefer not to answer option'. The final score is calculated by averaging all of the response,
and subscale scores are calculated by averaging all of the responses within each subscale.  

2. Any Prefer Not To Answer/Left Blank selection was not counted toward the final score (as per scoring sheet instructions).
"""

# Subscale scores:	min= 1	max= 5
# Total score:		min= 1	max= 5
# ------------------------------------------------------------------------------
def rsri_analysis(df):
	# For some questions, the numerical value assigned to each text response is flipped (i.e. sometimes 'never' should be scored as 1, sometimes it should be scored as 5). The lines below reverse problematic questions.
	flip_scores= ['rsri_13','rsri_14','rsri_20','rsri_21','rsri_22','rsri_23', 'rsri_25', 'rsri_28','rsri_30']
	df[flip_scores]=df[flip_scores].replace(['always', 'very often', 'often', 'sometimes', 'rarely','never', 'moderately'], [1,1,2,3,4,5,2])

	# These are the RSRI Headers
	school_social= ['rsri_15', 'rsri_17', 'rsri_18', 'rsri_19', 'rsri_20', 'rsri_21', 'rsri_22', 'rsri_23', 'rsri_24', 'rsri_25', 'rsri_28', 'rsri_30']
	fear_illness= ['rsri_1', 'rsri_2', 'rsri_3', 'rsri_4', 'rsri_5', 'rsri_6', 'rsri_7', 'rsri_10', 'rsri_12', 'rsri_16', 'rsri_26', 'rsri_27']
	rsri_tot= ['rsri_1', 'rsri_2', 'rsri_3', 'rsri_4', 'rsri_5', 'rsri_6', 'rsri_7','rsri_8', 'rsri_9', 'rsri_10', 'rsri_11', 'rsri_12', 'rsri_13', 'rsri_14', 'rsri_15', 'rsri_16', 'rsri_17', 'rsri_18', 'rsri_19', 'rsri_20', 'rsri_21', 'rsri_22', 'rsri_23', 'rsri_24', 'rsri_25','rsri_26', 'rsri_27', 'rsri_28', 'rsri_29', 'rsri_30']

	# Replace other RSRI text answers with numerical answers       
	df[rsri_tot]=df[rsri_tot].replace(["0-4 days","0-4 days","never","eagerly","not at all","5-9 days","agreeably","rarely","once a year","slightly","moderately","with coaxing","10-14 days","sometimes","once a month","average","often","only if pressured","very","below average","once a week","15-19 days","20 or more days","very often","once a night","always","terrified"],[1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5])


	# Check for values that don't match parameters 
	rsri_check=df[rsri_tot].apply(pd.to_numeric,args=('raise',))
	rsri_check=rsri_check[(rsri_check !=1) & (rsri_check !=2) & (rsri_check !=3) & (rsri_check !=4) & (rsri_check !=5) & (rsri_check !=999)].sum()
	for x in rsri_check:
		if x!=0:
			df['rsri_error']=np.nan
			df.rsri_error=df.rsri_error.replace([np.nan],["Your RSRI responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			rsri_result=df['rsri_error']
			
		else:
			# ------------------------------------------------------------------------------
			# Count number of "prefer to not answer" responses and number of questions left blank 
			rsri = df[rsri_tot].apply(pd.to_numeric, args=('ignore',), axis=1)
			rsri_prefernotanswer= rsri.apply(lambda x: sum(x==999), axis=1)
			rsri_leftblank = rsri.apply(lambda x: sum(x.isnull().values), axis=1)
			rsri_unanswered= rsri_leftblank+rsri_prefernotanswer

			# School/Social Subscale
			school_social_ss = df[school_social].apply(pd.to_numeric, args=('ignore',), axis=1)
			school_social_subscale_prefernotanswer= school_social_ss.apply(lambda x: sum(x==999), axis=1)
			school_social_subscale_leftblank = school_social_ss.apply(lambda x: sum(x.isnull().values), axis=1)
			school_social_unanswered= school_social_subscale_leftblank+school_social_subscale_prefernotanswer
			school_social_sum = school_social_ss[school_social_ss < 6].sum(axis=1)
			school_social_score=school_social_sum/(12-school_social_unanswered)

			# Fear/Illness Subscale
			fear_illness_ss = df[fear_illness].apply(pd.to_numeric, args=('ignore',), axis=1)
			fear_illness_subscale_prefernotanswer= fear_illness_ss.apply(lambda x: sum(x==999), axis=1)
			fear_illness_subscale_leftblank = fear_illness_ss.apply(lambda x: sum(x.isnull().values), axis=1)
			fear_illness_unanswered= fear_illness_subscale_leftblank+fear_illness_subscale_prefernotanswer
			fear_illness_sum = fear_illness_ss[fear_illness_ss < 6].sum(axis=1)
			fear_illness_score=fear_illness_sum/(12-fear_illness_unanswered)

			# ------------------------------------------------------------------------------
			# Averages all scored responses to compute RSRI score 
			rsri_sum = rsri[rsri < 6].sum(axis=1)
			rsri_score=rsri_sum/(30-rsri_prefernotanswer)

			# Check for scores that are outside acceptable values 
			for x in rsri_score:
				if (x<1 or x>5) and x!=np.nan:
					rsri_score=rsri_score.replace([x],["Warning: This RSRI score (%d) falls outside of the accepted range (1 to 5). Please check your data and try again."  % x])
					
			# Shifts columns to properly align data
			rsriall = pd.DataFrame({'RSRI_SS_Left_Blank': school_social_subscale_leftblank,'RSRI_SS_Prefer_to_Not_Answer': school_social_subscale_prefernotanswer, 'RSRI_SS_Score': school_social_score, 'RSRI_FI_Left_Blank': fear_illness_subscale_leftblank, 'RSRI_FI_Prefer_to_Not_Answer': fear_illness_subscale_prefernotanswer, 'RSRI_FI_Score': fear_illness_score, 'RSRI_Left_Blank': rsri_leftblank,'RSRI_Prefer_to_not_answer': rsri_prefernotanswer, 'RSRI_Score': rsri_score})
			cols= rsriall.columns.tolist()
			cols=cols[-4:]+cols[:-4]
			rsriall=rsriall[cols]

			# ------------------------------------------------------------------------------
			# Generate Output 
			rsri_frames = [df.SUBJECT_ID, rsriall]
			rsri_result = pd.concat(rsri_frames, axis=1)
		return rsri_result
			#rsri_result.to_csv(raw_input("Save your RSRI output as: "))

