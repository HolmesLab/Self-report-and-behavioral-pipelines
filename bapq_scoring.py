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

# BROAD AUTISM PHENOTYPE QUESTIONNAIRE

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/1y3iudybvh7oyi1xrjktiic3ko8jwr75
Scoring: https://yale.box.com/s/74inyvau1n305b2dentczu2f8rc6499d
"""

# SCORING:
"""
1. Summary score for each of three subscales were computed by reverse scoring the appropriate items,
averaging across the 12 items for each subscale and averaging across all 36 items to create a total score.
All summary scores therefore have a range 1-6. (Hurley et al., 2007).

2. Questions that should be reverse scored are reverse scored.

3. Participant who chooses Prefer Not To Answer selection is not discarded, but is not counted toward the average on subscales or final score (Avram).

4. Any Question that is left completely blank is not discarded, but not counted toward the average on subscales or final score (Avram).
"""

# VERY RARELY - RARELY - OCCASIONALLY - SOMEWHAT OFTEN - OFTEN - VERY OFTEN - PREFER NOT TO ANSWER
#     1           2           3              4             5          6             999

# Subscale scores:	 min= 1   max= 6
# Total score:		 min= 1	  max= 6
# ------------------------------------------------------------------------------
# Data Preparation 

def bapq_analysis(df):
	# THESE KEYS ARE READ BY THE COLUMN DICTIONARY -> Question_Name
	bapq_aloof_keys = ['bapq_5', 'bapq_18', 'bapq_27', 'bapq_31']
	bapq_aloof_reverse_keys = ['bapq_1', 'bapq_9', 'bapq_12', 'bapq_16', 'bapq_23', 'bapq_25', 'bapq_28', 'bapq_36']
	bapq_rigid_keys = ['bapq_6', 'bapq_8', 'bapq_13', 'bapq_22', 'bapq_24', 'bapq_26', 'bapq_33', 'bapq_35']
	bapq_rigid_reverse_keys = ['bapq_3', 'bapq_15', 'bapq_19', 'bapq_30']
	bapq_pragmatic_keys = ['bapq_2', 'bapq_4', 'bapq_10', 'bapq_11', 'bapq_14', 'bapq_17', 'bapq_20', 'bapq_29','bapq_32']
	bapq_pragmatic_reverse_keys = ['bapq_7', 'bapq_21', 'bapq_34']
	bapq_tot_keys= bapq_aloof_keys+bapq_aloof_reverse_keys+bapq_rigid_keys+bapq_rigid_reverse_keys+bapq_pragmatic_keys+bapq_pragmatic_reverse_keys

	# Replace Qualtrics text answers with numerical values
	df[bapq_tot_keys]= df[bapq_tot_keys].replace(['very rarely', 'rarely',  'occasionally', 'somewhat often','often', 'very often' ], [1,2,3,4,5,6])

	# Check for values that fall outside parameter ranges
	bapq_check=df[bapq_tot_keys].apply(pd.to_numeric,args=('raise',))
	bapq_check=bapq_check[(bapq_check !=0) & (bapq_check !=1) & (bapq_check !=2) & (bapq_check !=3) & (bapq_check !=4) & (bapq_check !=5) & (bapq_check !=6) & (bapq_check !=999)].sum()
	for x in bapq_check:
		if x!=0:
			df['bapq_error']=np.nan
			df.bapq_error=df.bapq_error.replace([np.nan],["Your BAPQ responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			bapq_result=df['bapq_error']
			
		else:
			# ------------------------------------------------------------------------------
			# Aloof score

			# Forward scores and questions unanswered
			aloof_forward = df[bapq_aloof_keys].apply(pd.to_numeric, args=('raise',))
			aloof_forward_leftblank = aloof_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			aloof_forward_prefernotanswer = aloof_forward.apply(lambda x: sum(x==999), axis=1)

			# Sum all the forward scores
			aloof_forward_score = aloof_forward[(aloof_forward[bapq_aloof_keys] >= 1) & (aloof_forward[bapq_aloof_keys] <= 6)].sum(axis=1)

			# Reverse scores and questions unanswered
			aloof_reverse = df[bapq_aloof_reverse_keys].apply(pd.to_numeric, args=('raise',))

			# Sum the number of reverse questions left blank or preferred not to answer
			aloof_reverse_prefernotanswer = aloof_reverse.apply(lambda x: sum(x==999), axis=1)
			aloof_reverse_leftblank = aloof_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

			# Sum all the reverse scores
			aloof_reverse_score = aloof_reverse[aloof_reverse[bapq_aloof_reverse_keys] <= 6].rsub(7).sum(axis=1, skipna=True)

			# Total prefer to not answer and left blank 
			total_aloof_prefernotanswer = aloof_forward_prefernotanswer + aloof_reverse_prefernotanswer
			total_aloof_leftblank = aloof_forward_leftblank+aloof_reverse_leftblank
			total_aloof_unanswered= total_aloof_prefernotanswer+total_aloof_leftblank

			# Total score
			total_aloof_score = (aloof_forward_score + aloof_reverse_score)/(12-total_aloof_unanswered)

			aloofall = pd.DataFrame({'BAPQ_A_Left_Blank' : total_aloof_leftblank, 'BAPQ_A_Prefer_Not_to_Answer': total_aloof_prefernotanswer,'BAPQ_A_Score': total_aloof_score,})

			# Check for scores that are outside acceptable values 
			for x in total_aloof_score:
				if (x<1 or x>6) and x!=np.nan:
					total_aloof_score=total_aloof_score.replace([x],["Warning: This BAPQ_aloof score (%d) falls outside of the accepted range (1 to 6). Please check your data and try again."  % x])


			# ------------------------------------------------------------------------------
			# Rigid score

			# Forward scores and questions unanswered
			rigid_forward = df[bapq_rigid_keys].apply(pd.to_numeric, args=('raise',))
			rigid_forward_leftblank = rigid_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			rigid_forward_prefernotanswer = rigid_forward.apply(lambda x: sum(x==999), axis=1)

			# Sum all the forward scores
			rigid_forward_score = rigid_forward[(rigid_forward[bapq_rigid_keys] >= 1) & (rigid_forward[bapq_rigid_keys] <= 6)].sum(axis=1)

			# Reverse scores and questions unanswered
			rigid_reverse = df[bapq_rigid_reverse_keys].apply(pd.to_numeric, args=('raise',))

			# Sum the number of reverse questions left blank or preferred not to answer
			rigid_reverse_prefernotanswer = rigid_reverse.apply(lambda x: sum(x==999), axis=1)
			rigid_reverse_leftblank = rigid_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

			# Sum all the reverse scores
			rigid_reverse_score = rigid_reverse[rigid_reverse[bapq_rigid_reverse_keys] <= 6].rsub(7).sum(axis=1, skipna=True)

			# Total prefer to not answer and left blank 
			total_rigid_prefernotanswer = rigid_forward_prefernotanswer + rigid_reverse_prefernotanswer
			total_rigid_leftblank = rigid_forward_leftblank+rigid_reverse_leftblank
			total_rigid_unanswered= total_rigid_prefernotanswer+total_rigid_leftblank

			# Total score
			total_rigid_score = (rigid_forward_score + rigid_reverse_score)/(12-total_rigid_unanswered)

			rigidall = pd.DataFrame({'BAPQ_R_Left_Blank' : total_rigid_leftblank, 'BAPQ_R_Prefer_Not_to_Answer': total_rigid_prefernotanswer,'BAPQ_R_Score': total_rigid_score,})

			# Check for scores that are outside acceptable values 
			for x in total_rigid_score:
				if (x<1 or x>6) and x!=np.nan:
					total_rigid_score=total_rigid_score.replace([x],["Warning: This BAPQ_rigid score (%d) falls outside of the accepted range (1 to 6). Please check your data and try again."  % x])


			# ------------------------------------------------------------------------------
			# Pragmatic score

			# Forward scores and questions unanswered
			pragmatic_forward = df[bapq_pragmatic_keys].apply(pd.to_numeric, args=('raise',))
			pragmatic_forward_leftblank = pragmatic_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			pragmatic_forward_prefernotanswer = pragmatic_forward.apply(lambda x: sum(x==999), axis=1)

			# Sum all the forward scores
			pragmatic_forward_score = pragmatic_forward[(pragmatic_forward[bapq_pragmatic_keys] >= 1) & (pragmatic_forward[bapq_pragmatic_keys] <= 6)].sum(axis=1)

			# Reverse scores and questions unanswered
			pragmatic_reverse = df[bapq_pragmatic_reverse_keys].apply(pd.to_numeric, args=('raise',))

			# Sum the number of reverse questions left blank or preferred not to answer
			pragmatic_reverse_prefernotanswer = pragmatic_reverse.apply(lambda x: sum(x==999), axis=1)
			pragmatic_reverse_leftblank = pragmatic_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

			# Sum all the reverse scores
			pragmatic_reverse_score = pragmatic_reverse[pragmatic_reverse[bapq_pragmatic_reverse_keys] <= 6].rsub(7).sum(axis=1, skipna=True)

			# Total prefer to not answer and left blank 
			total_pragmatic_prefernotanswer = pragmatic_forward_prefernotanswer + pragmatic_reverse_prefernotanswer
			total_pragmatic_leftblank = pragmatic_forward_leftblank+pragmatic_reverse_leftblank
			total_pragmatic_unanswered= total_pragmatic_prefernotanswer+total_pragmatic_leftblank

			# Total score
			total_pragmatic_score = (pragmatic_forward_score + pragmatic_reverse_score)/(12-total_pragmatic_unanswered)

			pragmaticall = pd.DataFrame({'BAPQ_P_Left_Blank' : total_pragmatic_leftblank, 'BAPQ_P_Prefer_Not_to_Answer': total_pragmatic_prefernotanswer,'BAPQ_P_Score': total_pragmatic_score,})

			# Check for scores that are outside acceptable values 
			for x in total_pragmatic_score:
				if (x<1 or x>6) and x!=np.nan:
					total_pragmatic_score=total_pragmatic_score.replace([x],["Warning: This BAPQ_pragmatic score (%d) falls outside of the accepted range (1 to 6). Please check your data and try again."  % x])


			# ------------------------------------------------------------------------------
			# TOTAL score

			# Add the subscale scores, then divide by the total number of subscales
			total_prefernottoanswer = total_aloof_prefernotanswer + total_rigid_prefernotanswer + total_pragmatic_prefernotanswer

			total_leftblank = total_aloof_leftblank+total_rigid_leftblank+total_pragmatic_leftblank

			total_unanswered= total_aloof_unanswered+total_rigid_unanswered+total_pragmatic_unanswered

			total_score = ((((total_aloof_score*(12-total_aloof_unanswered)) + (total_rigid_score*(12-total_rigid_unanswered)) + (total_pragmatic_score*(12-total_pragmatic_unanswered))) / (36-total_prefernottoanswer)))

			totalall = pd.DataFrame({'BAPQ_Left_Blank' : total_leftblank, 'BAPQ_Prefer_Not_To_Answer': total_prefernottoanswer,'BAPQ_Score': total_score})
			for x in total_score:
				if (x<1 or x>6) and x!=np.nan:
					total_score=total_score.replace([x],["Warning: This BAPQ score (%d) falls outside of the accepted range (1 to 6). Please check your data and try again."  % x])


			# ------------------------------------------------------------------------------
			#Generate Output 

			# Put the scores into one frame
			bapq_frames = [df.SUBJECT_ID, aloofall, rigidall, pragmaticall, totalall]
			bapq_result = pd.concat(bapq_frames, axis=1)
	return bapq_result
	
	#bapq_result.to_csv(raw_input("Save your BAPQ Output as: "))
