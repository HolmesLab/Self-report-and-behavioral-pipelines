#!/usr/bin/python

"""
Battery Scores Package for Processing CSV Files	
@author: David Gruskin
@email: david.gruskin@yale.edu
@version: 1.0
@date: 2017.07.06
"""
import pandas as pd
import numpy as np
import sys 

# Social Anxiety Questionnaire for Adults

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/yc5rioap687yrelhxbyz3w9yykodyenj
Scoring: https://yale.box.com/s/yc5rioap687yrelhxbyz3w9yykodyenj
"""

# SCORING:
"""
1. Scores are the sum of each subscale (D1 through D5). 

2. How to handle missing values is not explicitly mentioned in the primary resources above, so
if any value is left blank or prefer not to answer, those missing values will be replaced with the average
score on that particular subscale and then added to the final subscore total (Avram).
"""

# Subscale scores:	min= 6	  max= 30
# Total scores:		min= 30	  max= 150
# ------------------------------------------------------------------------------
# Data Preparation 

def saqa_analysis(df):
	# These are are the different dimensions and their corresponding questions
	D1_headers = ["saqa_10","saqa_13","saqa_15","saqa_17","saqa_19","saqa_22"]
	D2_headers = ["saqa_3","saqa_7","saqa_12","saqa_18","saqa_25","saqa_29"]
	D3_headers = ["saqa_4","saqa_6","saqa_20","saqa_23","saqa_27","saqa_30"]
	D4_headers = ["saqa_1","saqa_8","saqa_16","saqa_21","saqa_24","saqa_28"]
	D5_headers = ["saqa_2","saqa_5","saqa_9","saqa_11","saqa_14","saqa_26"]
	saqa_headers= D1_headers+D2_headers+D3_headers+D4_headers+D5_headers

	# Replace Qualtrics text answers with numerical values
	df[saqa_headers]= df[saqa_headers].replace(['not at all or very slight', 'slight',  'moderate', 'high','very high or extremely high'], [1,2,3,4,5])

	# Check for values that don't match parameters 
	saqa_check=df[saqa_headers].apply(pd.to_numeric,args=('raise',))
	saqa_check=saqa_check[(saqa_check !=1) & (saqa_check !=2) & (saqa_check !=3) & (saqa_check !=4) & (saqa_check !=5) & (saqa_check !=999)].sum()
	for x in saqa_check:
		if x!=0:
			df['saqa_error']=np.nan
			df.saqa_error=df.saqa_error.replace([np.nan],["Your SAQ-A responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			saqa_result=df['saqa_error']
			
		else:
			# ------------------------------------------------------------------------------

			# Dimension 1: Interactions with strangers

			# Change the numbers in saqa headers to numeric floats
			D1 = df[D1_headers].apply(pd.to_numeric, args=('raise',))

			# These count the number of Dimension 1 questions that were left blank or answered with 'prefer not to answer' 
			D1_leftblank = D1.apply(lambda x: sum(x.isnull().values), axis=1)
			D1_prefernotanswer= D1.apply(lambda x: sum(x==999), axis=1)
			D1_unanswered = D1_leftblank + D1_prefernotanswer

			# Calculate the D1 score
			D1_score = D1[D1[D1_headers] < 6].sum(axis=1)

			# Replace blank or prefer to not answer responses with the average from the subscale
			D1_score = D1_score + (D1_unanswered * D1_score / (len(D1_headers)-D1_unanswered))

			D1all = pd.DataFrame({'SAQA_D1_Left_Blank': D1_leftblank, 'SAQA_D1_Prefer_Not_to_Answer': D1_prefernotanswer, 'SAQA_D1_Subscore' : D1_score})

			# Check for scores that are outside acceptable values 
			for x in D1_score:
				if (x<6 or x>30) and x!=np.nan:
					D1_score=D1_score.replace([x],["Warning: This SAQ-A D1 score (%d) falls outside of the accepted range (6 to 30). Please check your data and try again."  % x])

			# ------------------------------------------------------------------------------

			# Dimension 2: Speaking in public/Talking with people in authority 

			# Change the numbers in saqa headers to numeric floats
			D2 = df[D2_headers].apply(pd.to_numeric, args=('raise',))

			# These count the number of Dimension 1 questions that were left blank or answered with 'prefer not to answer' 
			D2_leftblank = D2.apply(lambda x: sum(x.isnull().values), axis=1)
			D2_prefernotanswer= D2.apply(lambda x: sum(x==999), axis=1)
			D2_unanswered = D2_leftblank + D2_prefernotanswer

			# Calculate the D2 score
			D2_score = D2[D2[D2_headers] < 6].sum(axis=1)

			# Replace blank or prefer to not answer responses with the average from the subscale
			D2_average= D2_score/(6-D2_unanswered)
			df[D2_headers].apply(str)
			D2=D2.replace(np.nan,999)
			D2=D2.replace([999], [D2_average])

			# Re-score, this time including average values 
			D2_score = D2[D2[D2_headers] < 6].sum(axis=1)

			D2all = pd.DataFrame({'SAQA_D2_Left_Blank': D2_leftblank, 'SAQA_D2_Prefer_Not_to_Answer': D2_prefernotanswer, 'SAQA_D2_Subscore' : D2_score})

			# Check for scores that are outside acceptable values 
			for x in D2_score:
				if (x<6 or x>30) and x!=np.nan:
					D2_score=D2_score.replace([x],["Warning: This SAQ-A D2 score (%d) falls outside of the accepted range (6 to 30). Please check your data and try again."  % x])

			# ------------------------------------------------------------------------------
			# Dimension 3: Interactions with the opposite sex

			# Change the numbers in saqa headers to numeric floats
			D3 = df[D3_headers].apply(pd.to_numeric, args=('raise',))

			# These count the number of Dimension 1 questions that were left blank or answered with 'prefer not to answer' 
			D3_leftblank = D3.apply(lambda x: sum(x.isnull().values), axis=1)
			D3_prefernotanswer= D3.apply(lambda x: sum(x==999), axis=1)
			D3_unanswered = D3_leftblank + D3_prefernotanswer

			# Calculate the D3 score
			D3_score = D3[D3[D3_headers] < 6].sum(axis=1)

			# Replace blank or prefer to not answer responses with the average from the subscale
			D3_average= D3_score/(6-D3_unanswered)
			df[D3_headers].apply(str)
			D3=D3.replace(np.nan,999)
			D3=D3.replace([999], [D3_average])

			# Re-score, this time including average values 
			D3_score = D3[D3[D3_headers] < 6].sum(axis=1)

			D3all = pd.DataFrame({'SAQA_D3_Left_Blank': D3_leftblank, 'SAQA_D3_Prefer_Not_to_Answer': D3_prefernotanswer, 'SAQA_D3_Subscore' : D3_score})

			# Check for scores that are outside acceptable values 
			for x in D3_score:
				if (x<6 or x>30) and x!=np.nan:
					D3_score=D3_score.replace([x],["Warning: This SAQ-A D3 score (%d) falls outside of the accepted range (6 to 30). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------

			# D4: Criticism and Embarrassment

			# Change the numbers in saqa headers to numeric floats
			D4 = df[D4_headers].apply(pd.to_numeric, args=('raise',))


			# These count the number of Dimension 1 questions that were left blank or answered with 'prefer not to answer' 
			D4_leftblank = D4.apply(lambda x: sum(x.isnull().values), axis=1)
			D4_prefernotanswer= D4.apply(lambda x: sum(x==999), axis=1)
			D4_unanswered = D4_leftblank + D4_prefernotanswer

			# Calculate the D4 score
			D4_score = D4[D4[D4_headers] < 6].sum(axis=1)

			# Replace blank or prefer to not answer responses with the average from the subscale
			D4_average= D4_score/(6-D4_unanswered)
			df[D4_headers].apply(str)
			D4=D4.replace(np.nan,999)
			D4=D4.replace([999], [D4_average])

			# Re-score, this time including average values 
			D4_score = D4[D4[D4_headers] < 6].sum(axis=1)

			D4all = pd.DataFrame({'SAQA_D4_Left_Blank': D4_leftblank, 'SAQA_D4_Prefer_Not_to_Answer': D4_prefernotanswer, 'SAQA_D4_Subscore' : D4_score})

			# Check for scores that are outside acceptable values 
			for x in D4_score:
				if (x<6 or x>30) and x!=np.nan:
					D4_score=D4_score.replace([x],["Warning: This SAQ-A D4 score (%d) falls outside of the accepted range (6 to 30). Please check your data and try again."  % x])

			# ------------------------------------------------------------------------------

			# Dimension 5: Assertive expression of annoyance, disgust, or displeasure 

			# Change the numbers in saqa headers to numeric floats
			D5 = df[D5_headers].apply(pd.to_numeric, args=('raise',))

			# These count the number of Dimension 1 questions that were left blank or answered with 'prefer not to answer' 
			D5_leftblank = D5.apply(lambda x: sum(x.isnull().values), axis=1)
			D5_prefernotanswer= D5.apply(lambda x: sum(x==999), axis=1)
			D5_unanswered = D5_leftblank + D5_prefernotanswer

			# Calculate the D5 score
			D5_score = D5[D5[D5_headers] < 6].sum(axis=1)

			# Replace blank or prefer to not answer responses with the average from the subscale
			D5_average= D5_score/(6-D5_unanswered)
			df[D5_headers].apply(str)
			D5=D5.replace(np.nan,999)
			D5=D5.replace([999], [D5_average])

			# Re-score, this time including average values 
			D5_score = D5[D5[D5_headers] < 6].sum(axis=1)

			D5all = pd.DataFrame({'SAQA_D5_Left_Blank': D5_leftblank, 'SAQA_D5_Prefer_Not_to_Answer': D5_prefernotanswer, 'SAQA_D5_Subscore' : D5_score})

			# Check for scores that are outside acceptable values 
			for x in D5_score:
				if (x<6 or x>30) and x!=np.nan:
					D5_score=D5_score.replace([x],["Warning: This SAQ-A D5 score (%d) falls outside of the accepted range (6 to 30). Please check your data and try again."  % x])

			# -----------------------------------------------------------------------------
			# Total score

			saqa_total= D1_score+D2_score+D3_score+D4_score+D5_score
			saqa_prefernotanswer= D1_prefernotanswer+D2_prefernotanswer+D3_prefernotanswer+D4_prefernotanswer+D5_prefernotanswer
			saqa_leftblank= D1_leftblank+D2_leftblank+D3_leftblank+D4_leftblank+D5_leftblank
			saqa_all = pd.DataFrame({'SAQA_Total_Left_Blank' : saqa_leftblank, 'SAQA_Total_Prefer_to_Not_Answer' : saqa_prefernotanswer,'SAQA_Total_Score' : saqa_total}) 

			# Check for scores that are outside acceptable values 
			for x in saqa_total:
				if (x<30 or x>150) and x!=np.nan:
					saqa_total_score=saqa_total_score.replace([x],["Warning: This SAQ-A score (%d) falls outside of the accepted range (30 to 150). Please check your data and try again."  % x])

			# -----------------------------------------------------------------------------
			# Generate Output 

			# Put the scores into one frame
			saqa_frames = [df.SUBJECT_ID, D1all, D2all, D3all, D4all, D5all,saqa_all]
			saqa_result = pd.concat(saqa_frames, axis=1)
	return saqa_result

	#saqa_result.to_csv(raw_input("Save your SAQ-A Output csv as: "))'''