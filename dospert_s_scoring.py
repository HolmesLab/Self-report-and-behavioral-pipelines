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

# DOMAIN-SPECIFIC RISK-TAKING SCALE (social items only)

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/89t2eo21x2v2yf6elpkekd38tg4yfgs8 (social items only)
Scoring:https://yale.box.com/s/4a839o0noil6v547ksjbmd8jp558bsis
"""

# SCORING:
"""
1. Scores are the sum of each subscale (Risk-Taking and Risk-Perception).
This version uses only "Social" items from the 2003 DOSPERT (https://sites.google.com/a/decisionsciences.columbia.edu/cds-wiki/home/dospert/DOSPERT_40_English_2003.doc?attredirects=0)

2. Any left blank/prefer to not answer response will be replaced with the mean response from the corresponding subscale.
"""

# RISK TAKING MODULE
# EXTREMELY UNLIKELY - MODERATELY UNLIKELY - SOMEWHAT UNLIKELY - NOT SURE - SOMEWHAT LIKELY - MODERATELY LIKELY - EXTREMELY LIKELY - PREFER NOT TO ANSWER
#           1                   2                   3               4             5                    6               7                    999
# RISK PERCEPTION MODULE
# NOT AT ALL RISKY - SLIGHTLY RISKY - SOMEWHAT RISKY - MODERATELY RISKY - RISKY - VERY RISKY - EXTREMELY RISKY - PREFER NOT TO ANSWER
#           1              2                3                  4            5          6            7                   999

# Subscale scores: min= 8  max= 56
# ------------------------------------------------------------------------------
# Data Preparation
def dospert_s_analysis(df):
	# These are the different headers and their corresponding questions
	risktaking_keys = ['dospert_s_1', 'dospert_s_2', 'dospert_s_3', 'dospert_s_4', 'dospert_s_5', 'dospert_s_6', 'dospert_s_7',
	'dospert_s_8']
	
	riskperception_keys = ['dospert_s_9', 'dospert_s_10', 'dospert_s_11', 'dospert_s_12', 'dospert_s_13', 'dospert_s_14', 'dospert_s_15', 'dospert_s_16']
	
	dospert_s_tot_keys=risktaking_keys+riskperception_keys
				   
	# Replace Qualtrics text answers with numerical values
	df[dospert_s_tot_keys]= df[dospert_s_tot_keys].replace(['very unlikely', 'unlikely','not sure','likely', 'very likely'], [1,2,3,4,5])
	df[dospert_s_tot_keys]= df[dospert_s_tot_keys].replace(['not at all risky', 'slightly risky', 'moderately risky', 'very risky', 'extremely risky'], [1,2,3,4,5])

	# Check for values that don't match parameters 
	dospert_s_check=df[dospert_s_tot_keys].apply(pd.to_numeric,args=('raise',))
	dospert_s_check=dospert_s_check[(dospert_s_check !=1) & (dospert_s_check !=2) & (dospert_s_check !=3) & (dospert_s_check !=4) & (dospert_s_check !=5) & (dospert_s_check !=999)].sum()
	for x in dospert_s_check:
		if x!=0:
			df['dospert_s_error']=np.nan
			df.dospert_s_error=df.dospert_s_error.replace([np.nan],["Your DOSPERT(S) responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			dospert_s_result=df['dospert_s_error']	
		else:
			# ------------------------------------------------------------------------------
			# DOSPERT(S) Risktaking Score 

			# Scores and questions unanswered
			risktaking = df[risktaking_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_socialonly_prefernotanswer = risktaking[risktaking[risktaking_keys] == 999].count(axis=1)
			risktaking_socialonly_leftblank = risktaking.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_socialonly_unanswered = risktaking_socialonly_prefernotanswer + risktaking_socialonly_leftblank

			# Total score
			risktaking_socialonly_score = risktaking[risktaking[risktaking_keys] <=7].sum(axis=1)
			risktaking_socialonly_score = risktaking_socialonly_score + (risktaking_socialonly_unanswered * risktaking_socialonly_score / (8-risktaking_socialonly_unanswered))

			risktakingall = pd.DataFrame({'DOSPERT(S)_Risktaking_Left_Blank' : risktaking_socialonly_leftblank,'DOSPERT(S)_Risktaking_Prefer_Not_to_Answer': risktaking_socialonly_prefernotanswer,'DOSPERT(S)_Risktaking_Score': risktaking_socialonly_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_socialonly_score:
				if (x<8 or x>56) and x!=np.nan:
					risktaking_socialonly_score=risktaking_socialonly_score.replace([x],["Warning: This DOSPERT(S)_risktaking score (%d) falls outside of the accepted range (8 to 56). Please check your data and try again."  % x])


			# ------------------------------------------------------------------------------
			# DOSPERT(S) Riskperception Score 


			# Scores and questions unanswered
			riskperception = df[riskperception_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_socialonly_prefernotanswer = riskperception[riskperception[riskperception_keys] == 999].count(axis=1)
			riskperception_socialonly_leftblank = riskperception.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_socialonly_unanswered = riskperception_socialonly_prefernotanswer + riskperception_socialonly_leftblank

			# Total score
			riskperception_socialonly_score = riskperception[riskperception[riskperception_keys] <=7].sum(axis=1)
			riskperception_socialonly_score = riskperception_socialonly_score + (riskperception_socialonly_unanswered * riskperception_socialonly_score / (8-riskperception_socialonly_unanswered))

			riskperceptionall = pd.DataFrame({'DOSPERT(S)_Riskperception_Left_Blank' : riskperception_socialonly_leftblank,'DOSPERT(S)_Riskperception_Prefer_Not_to_Answer': riskperception_socialonly_prefernotanswer,'DOSPERT(S)_Riskperception_Score': riskperception_socialonly_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_socialonly_score:
				if (x<8 or x>56) and x!=np.nan:
					riskperception_socialonly_score=riskperception_socialonly_score.replace([x],["Warning: This DOSPERT(S)_riskperception score (%d) falls outside of the accepted range (8 to 56). Please check your data and try again."  % x])

			# ------------------------------------------------------------------------------
			# Generate Output

			# Put the scores into one frame
			dospert_s_frames = [df.SUBJECT_ID, risktakingall, riskperceptionall]
			dospert_s_result = pd.concat(dospert_s_frames, axis=1)
	return dospert_s_result
	#dospert_s_result.to_csv(raw_input("Save your dospert_s Output csv as: "))
