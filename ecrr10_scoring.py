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

# Experiences in Close Relationships-Revised (10-item)

# RESOURCES USED:
""" 
Scale: https://yale.box.com/s/2ctgz3ysqpjggypty88qqgmd0iy64v9q  (first ten items)
Scoring: https://yale.box.com/s/va4ia1odtz55bd08if3hrz5ckzb14mqt
"""

# SCORING:
"""
1. The Scale is typically 1-7, and the score is the sum of all answers. 

2. How to handle missing values is not explicitly mentioned in the primary resources above, so
if any value is left blank or prefer not to answer, those missing values will be replaced with the average
score on that particular subscale and then added to the final subscore total (Avram).

3. Any Question left blank was not counted toward the final score.
"""

# Anxiety/Avoidance scores:	min= 7	max= 35
# ------------------------------------------------------------------------------
# Data Preparation 
def ecrr10_analysis(df):
	# These are the different headers and their corresponding questions
	avoidance_forward_keys = ['ecrr10_1', 'ecrr10_3','ecrr10_5', 'ecrr10_7','ecrr10_9']
	anxiety_forward_keys = ['ecrr10_4', 'ecrr10_8','ecrr10_10']
	anxiety_reverse_keys = ['ecrr10_2', 'ecrr10_6']
	ecrr10_tot_keys=avoidance_forward_keys+anxiety_forward_keys+anxiety_reverse_keys

	# Replace Qualtrics text answers with numerical values
	df[ecrr10_tot_keys]= df[ecrr10_tot_keys].replace(['strongly disagree', 'somewhat disagree',  'slightly disagree', 'neither agree nor disagree','slightly agree', 'somewhat agree', 'strongly agree'], [1,2,3,4,5,6,7])

	# Check for values that don't match parameters 
	ecrr10_check=df[ecrr10_tot_keys].apply(pd.to_numeric,args=('raise',))
	ecrr10_check=ecrr10_check[(ecrr10_check !=1) & (ecrr10_check !=2) & (ecrr10_check !=3) & (ecrr10_check !=4) & (ecrr10_check !=5) & (ecrr10_check !=6) & (ecrr10_check !=7) & (ecrr10_check !=999)].sum()
	for x in ecrr10_check:
		if x!=0:
			df['ecrr10_error']=np.nan
			df.ecrr10_error=df.ecrr10_error.replace([np.nan],["Your ECR-R10 responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			ecrr10_result=df['ecrr10_error']
			
		else:
			# ------------------------------------------------------------------------------
			# Avoidance Scoring

			# change the numbers to numeric floats
			avoidance_forward = df[avoidance_forward_keys].apply(pd.to_numeric, args=('coerce',))

			# These count the number of questions answered as prefer not to answer and left blank
			avoidance_prefernotanswer= avoidance_forward.apply(lambda x: sum(x==999), axis=1)
			avoidance_leftblank = avoidance_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			avoidance_unanswered= avoidance_prefernotanswer+avoidance_leftblank 

			# Sum the forward scores together to get the Avoidance score and keeps anything less than or equal to 7
			avoidance_score = avoidance_forward[avoidance_forward[avoidance_forward_keys] <= 7].sum(axis=1)

			# Replace missing scores with subscale averages
			avoidance_score = avoidance_score + (avoidance_unanswered * avoidance_score / (len(avoidance_forward_keys)-avoidance_unanswered))

			# Check for scores that are outside acceptable values
			for x in avoidance_score:
				if (x<5 or x>35) and x!=np.nan:
					avoidance_score=avoidance_score.replace([x],["Warning: This ECR-R10_avoidance score (%d) falls outside of the accepted range (5 to 35). Please check your data and try again."  % x])
		
			# Condense summary scores into dataframe
			avoidanceall = pd.DataFrame({'ECRR10_Avoidance_Left_Blank' : avoidance_leftblank, 'ECRR10_Avoidance_Prefer_Not_to_Answer': avoidance_prefernotanswer,'ECRR10_Avoidance_Score': avoidance_score})

			# ------------------------------------------------------------------------------
			# Anxiety Scoring

			# change the numbers to numeric floats
			anxiety_forward = df[anxiety_forward_keys].apply(pd.to_numeric, args=('coerce',))
			anxiety_reverse = df[anxiety_reverse_keys].apply(pd.to_numeric, args=('coerce',))
			anxiety_total= anxiety_forward+anxiety_reverse

			# These count the number of questions answered as prefer not to answer and left blank
			anxiety_forward_prefernotanswer= anxiety_forward.apply(lambda x: sum(x==999), axis=1)
			anxiety_forward_leftblank = anxiety_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			anxiety_reverse_prefernotanswer= anxiety_reverse.apply(lambda x: sum(x==999), axis=1)
			anxiety_reverse_leftblank = anxiety_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

			anxiety_prefernotanswer= anxiety_forward_prefernotanswer + anxiety_reverse_prefernotanswer
			anxiety_leftblank= anxiety_forward_leftblank+anxiety_reverse_leftblank
			anxiety_unanswered=anxiety_prefernotanswer+anxiety_leftblank

			# Sum the forward scores together to get the anxiety score and keeps anything less than or equal to 7
			anxiety_forward_score = anxiety_forward[anxiety_forward[anxiety_forward_keys] <= 7].sum(axis=1)
			anxiety_reverse_score = anxiety_reverse[anxiety_reverse[anxiety_reverse_keys] <= 7].rsub(8).sum(axis=1, skipna=False)
			anxiety_score= anxiety_forward_score+anxiety_reverse_score

			# Replace missing scores with subscale averages
			anxiety_score = anxiety_score + (anxiety_unanswered * anxiety_score / (len(anxiety_forward_keys)-anxiety_unanswered))

			# Check for scores that are outside acceptable values 
			for x in anxiety_score:
				if (x<5 or x>35) and x!=np.nan:
					anxiety_score=anxiety_score.replace([x],["Warning: This ECR-R10_anxiety score (%d) falls outside of the accepted range (5 to 35). Please check your data and try again."  % x])
					
			# Condense summary scores into dataframe
			anxietyall = pd.DataFrame({'ECRR10_Anxiety_Left_Blank' : anxiety_leftblank, 'ECRR10_Anxiety_Prefer_Not_to_Answer': anxiety_prefernotanswer,'ECRR10_Anxiety_Score': anxiety_score})

			# ------------------------------------------------------------------------------
			# Generate Output

			# Put the scores into one frame
			ecrr10_frames = [df.SUBJECT_ID, avoidanceall, anxietyall]
			ecrr10_result = pd.concat(ecrr10_frames, axis=1)
	return ecrr10_result
	
	# Save result to csv
	#ecrr10_result.to_csv(raw_input("Save your ECR-R-10 output as: "))