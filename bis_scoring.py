#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files
@author: David Gruskin
@email: david.gruskin@yale.edu
@version: 1.0
@date: 2017.08.04
"""

import pandas as pd
import numpy as np
import sys 

# BARRATT IMPULSIVITY SCALE

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/qxs0mtznkdujnpks6hkl80ru3om62p1u
Scoring: https://yale.box.com/s/ln823cuqe5deqow0n09wf964nu52gwuv
"""

# SCORING:
"""
1. Scores are the sum of each subscale. Questions that should be reverse scored are reverse scored.

2. How to handle missing values is not explicitly mentioned in the primary resources above, so
if any value is left blank or prefer not to answer, those missing values will be replaced with the average
score on that particular subscale and then added to the final subscore total (Avram).
"""

# SCORING:
# RARELY/NEVER - OCCASIONALLY - OFTEN - ALMOST ALWAYS/ALWAYS - PREFER NOT TO ANSWER
#     1               2           3             4                       999

# BIS attention 				min:5 max:20
# BIS cognitive instability 	min:3 max:12
# BIS motor 					min:7 max:28
# BIS self-control				min:6 max:24
# BIS cognitive complexity 		min:5 max:20
# BIS perseverance 				min:4 max:16
# BIS attentional impulsiveness min:8 max:32
# BIS motor impulsiveness 		min:11 max:44
# BIS nonplanning impulsiveness min:11 max:44
	# ------------------------------------------------------------------------------
def bis_analysis(df):
	bis_1atten_keys = ['bis_5', 'bis_11', 'bis_28']
	bis_1atten_rev_keys = ['bis_9', 'bis_20']
	bis_1instability_keys = ['bis_6', 'bis_24', 'bis_26']
	bis_1mot_keys = ['bis_2', 'bis_3', 'bis_4', 'bis_17', 'bis_19', 'bis_22', 'bis_25']
	bis_1persever_keys = ['bis_16', 'bis_21', 'bis_23']
	bis_1persever_rev_keys = ['bis_30']
	bis_1selfcontrol_keys = ['bis_14']
	bis_1selfcontrol_rev_keys = ['bis_1', 'bis_7', 'bis_8', 'bis_12', 'bis_13']
	bis_1complex_keys = ['bis_18', 'bis_27']
	bis_1complex_rev_keys = ['bis_10', 'bis_15', 'bis_29']
	bis_2attentionalimpulsiveness_keys = ["bis_5", "bis_6", "bis_11", "bis_24", "bis_26", "bis_28"]
	bis_2attentionalimpulsiveness_rev_keys =["bis_9", "bis_20"]
	bis_2motorimpulsiveness_keys = ["bis_2", "bis_3", "bis_4", "bis_16", "bis_17", "bis_19", "bis_21", "bis_22", "bis_23", "bis_25"]
	bis_2motorimpulsiveness_rev_keys = ["bis_30"]
	bis_2nonplanningimpulsiveness_keys = [ "bis_14", "bis_18", "bis_27"]
	bis_2nonplanningimpulsiveness_rev_keys = ["bis_1", "bis_7", "bis_8", "bis_10", "bis_12", "bis_13", "bis_15", "bis_29"]
									
	bis_tot_keys= bis_1atten_keys + bis_1atten_rev_keys+bis_1instability_keys+bis_1mot_keys+bis_1persever_keys+bis_1persever_rev_keys+bis_1selfcontrol_keys+bis_1selfcontrol_rev_keys+bis_1complex_keys+bis_1complex_rev_keys

	df[bis_tot_keys]=df[bis_tot_keys].replace(['Rarely/Never', 'Occasionally', 'Often', 'Almost Always/Always','Prefer not to answer'], [1,2,3,4,999])

	# Check for values outside of parameter ranges 
	bis_check=df[bis_tot_keys].apply(pd.to_numeric,args=('raise',))
	bis_check=bis_check[(bis_check !=1) & (bis_check !=2) & (bis_check !=3) & (bis_check !=4) & (bis_check !=999)].sum()
	for x in bis_check:
		if x!=0:
			df['bis_error']=np.nan
			df.bis_error=df.bis_error.replace([np.nan],["Your BIS responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			bis_result=df['bis_error']
		else:
	
	
		# ------------------------------------------------------------------------------
		# BIS ATTENTION
	
		# Change the numbers in forward bis 1atten headers to numeric floats
			bis_1atten_forward = df[bis_1atten_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			bis_1atten_forward_leftblank = bis_1atten_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1atten_forward_prefernotanswer = bis_1atten_forward[bis_1atten_forward[bis_1atten_keys] == 999].count(axis=1)
			bis_1atten_forward_unanswered = bis_1atten_forward_leftblank + bis_1atten_forward_prefernotanswer
		
			# Sum all the forward scores
			bis_1atten_forward_score = bis_1atten_forward[bis_1atten_forward[bis_1atten_keys] < 5].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			bis_1atten_rev =df[bis_1atten_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			bis_1atten_reverse_leftblank = bis_1atten_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1atten_reverse_prefernotanswer = bis_1atten_rev[bis_1atten_rev[bis_1atten_rev_keys] == 999].count(axis=1)
			bis_1atten_reverse_unanswered = bis_1atten_reverse_leftblank + bis_1atten_reverse_prefernotanswer
		
			# Sum all the reverse scores
			bis_1atten_reverse_score = bis_1atten_rev.rsub(5)[bis_1atten_rev[bis_1atten_rev_keys] < 5].sum(axis=1)
		
			# Total bis 1atten score
			total_bis_1atten_score = bis_1atten_forward_score + bis_1atten_reverse_score
			total_bis_1atten_score=total_bis_1atten_score.replace([0],[np.nan])
		
			# TOTAL bis 1atten ANSWERS UNANSWERED
			total_bis_1atten_unanswered = bis_1atten_forward_unanswered + bis_1atten_reverse_unanswered
		
			# TOTAL ANSWERS LEFT BLANK
			total_bis_1atten_leftblank = bis_1atten_forward_leftblank + bis_1atten_reverse_leftblank
		
			# TOTAL ANSWERS PREFER NOT TO ANSWER
			total_bis_1atten_prefernotanswer = bis_1atten_forward_prefernotanswer + bis_1atten_reverse_prefernotanswer
		
			# Replace missing values with subscore averages 
			total_bis_1atten_score = total_bis_1atten_score + (total_bis_1atten_unanswered * total_bis_1atten_score / (5-total_bis_1atten_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_bis_1atten_score:
				if (x<5 or x>20) and x!=np.nan:
					total_bis_1atten_score=total_bis_1atten_score.replace([x],["Warning: This BIS_Attention score (%d) falls outside of the accepted range (5 to 20). Please check your data and try again."  % x])
		
			attentionall = pd.DataFrame({'BIS_Attention_Left_Blank': total_bis_1atten_leftblank,'BIS_Attention_Prefer_Not_to_Answer': total_bis_1atten_prefernotanswer,'BIS_Attention_Score': total_bis_1atten_score,})
		
			# ------------------------------------------------------------------------------
			# BIS COGNITIVE INSTABILITY - ALL FORWARD, NO REVERSE
		
			# Change the numbers in forward bis 1instability headers to numeric floats
			bis_1instability_forward = df[bis_1instability_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			bis_1instability_forward_leftblank = bis_1instability_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1instability_forward_prefernotanswer = bis_1instability_forward[bis_1instability_forward[bis_1instability_keys] == 999].count(axis=1)
			bis_1instability_forward_unanswered = bis_1instability_forward_leftblank + bis_1instability_forward_prefernotanswer
		
			# Sum all the forward scores
			bis_1instability_forward_score = bis_1instability_forward[bis_1instability_forward[bis_1instability_keys] < 5].sum(axis=1)
		
			# Total bis 1instability score
			total_bis_1instability_score = bis_1instability_forward_score 
			total_bis_1instability_score=total_bis_1instability_score.replace([0],[np.nan])
		
			# TOTAL bis 1instability ANSWERS UNANSWERED
			total_bis_1instability_unanswered = bis_1instability_forward_unanswered 
		
			# TOTAL ANSWERS LEFT BLANK
			total_bis_1instability_leftblank = bis_1instability_forward_leftblank
		
			# TOTAL ANSWERS PREFER NOT TO ANSWER
			total_bis_1instability_prefernotanswer = bis_1instability_forward_prefernotanswer 
		
			# Replace missing values with subscore averages 
			total_bis_1instability_score = total_bis_1instability_score + (total_bis_1instability_unanswered * total_bis_1instability_score / (3-total_bis_1instability_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_bis_1instability_score:
				if (x<3 or x>12) and x!=np.nan:
					total_bis_1instability_score=total_bis_1instability_score.replace([x],["Warning: This BIS_Cognitive_Instability score (%d) falls outside of the accepted range (3 to 12). Please check your data and try again."  % x])
		
			coginstall = pd.DataFrame({'BIS_Cognitive_Instability_Left_Blank': total_bis_1instability_leftblank,'BIS_Cognitive_Instability_Prefer_Not_to_Answer': total_bis_1instability_prefernotanswer,'BIS_Cognitive_Instability_Score': total_bis_1instability_score,})
			# ------------------------------------------------------------------------------
			# BIS MOTOR - ALL FORWARD, NO REVERSE
			# Change the numbers in forward bis 1instability headers to numeric floats
			bis_1mot_forward = df[bis_1mot_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			bis_1mot_forward_leftblank = bis_1mot_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1mot_forward_prefernotanswer = bis_1mot_forward[bis_1mot_forward[bis_1mot_keys] == 999].count(axis=1)
			bis_1mot_forward_unanswered = bis_1mot_forward_leftblank + bis_1mot_forward_prefernotanswer
		
			# Sum all the forward scores
			bis_1mot_forward_score = bis_1mot_forward[bis_1mot_forward[bis_1mot_keys] < 5].sum(axis=1)
		
			# Total bis 1mot score
			total_bis_1mot_score = bis_1mot_forward_score 
			total_bis_1mot_score=total_bis_1mot_score.replace([0],[np.nan])
		
			# TOTAL bis 1mot ANSWERS UNANSWERED
			total_bis_1mot_unanswered = bis_1mot_forward_unanswered 
		
			# TOTAL ANSWERS LEFT BLANK
			total_bis_1mot_leftblank = bis_1mot_forward_leftblank
		
			# TOTAL ANSWERS PREFER NOT TO ANSWER
			total_bis_1mot_prefernotanswer = bis_1mot_forward_prefernotanswer 
		
			# Replace missing values with subscore averages 
			total_bis_1mot_score = total_bis_1mot_score + (total_bis_1mot_unanswered * total_bis_1mot_score / (7-total_bis_1mot_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_bis_1mot_score:
				if (x<7 or x>28) and x!=np.nan:
					total_bis_1mot_score=total_bis_1mot_score.replace([x],["Warning: This BIS_Motor score (%d) falls outside of the accepted range (7 to 28). Please check your data and try again."  % x])
	
			motorall = pd.DataFrame({'BIS_Motor_Left_Blank': total_bis_1mot_leftblank,'BIS_Motor_Prefer_Not_to_Answer': total_bis_1mot_prefernotanswer,'BIS_Motor_Score': total_bis_1mot_score,})
			# ------------------------------------------------------------------------------
			# BIS SELF-CONTROL
		
			# Change the numbers in forward bis 1selfcontrol headers to numeric floats
			bis_1selfcontrol_forward = df[bis_1selfcontrol_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			bis_1selfcontrol_forward_leftblank = bis_1selfcontrol_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1selfcontrol_forward_prefernotanswer = bis_1selfcontrol_forward[bis_1selfcontrol_forward[bis_1selfcontrol_keys] == 999].count(axis=1)
			bis_1selfcontrol_forward_unanswered = bis_1selfcontrol_forward_leftblank + bis_1selfcontrol_forward_prefernotanswer
		
			# Sum all the forward scores
			bis_1selfcontrol_forward_score = bis_1selfcontrol_forward[bis_1selfcontrol_forward[bis_1selfcontrol_keys] < 5].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			bis_1selfcontrol_rev =df[bis_1selfcontrol_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			bis_1selfcontrol_reverse_leftblank = bis_1selfcontrol_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1selfcontrol_reverse_prefernotanswer = bis_1selfcontrol_rev[bis_1selfcontrol_rev[bis_1selfcontrol_rev_keys] == 999].count(axis=1)
			bis_1selfcontrol_reverse_unanswered = bis_1selfcontrol_reverse_leftblank + bis_1selfcontrol_reverse_prefernotanswer
		
			# Sum all the reverse scores
			bis_1selfcontrol_reverse_score = bis_1selfcontrol_rev.rsub(5)[bis_1selfcontrol_rev[bis_1selfcontrol_rev_keys] < 5].sum(axis=1)
		
			# Total bis 1selfcontrol score
			total_bis_1selfcontrol_score = bis_1selfcontrol_forward_score + bis_1selfcontrol_reverse_score
			total_bis_1selfcontrol_score=total_bis_1selfcontrol_score.replace([0],[np.nan])
		
			# TOTAL bis 1selfcontrol ANSWERS UNANSWERED
			total_bis_1selfcontrol_unanswered = bis_1selfcontrol_forward_unanswered + bis_1selfcontrol_reverse_unanswered
		
			# TOTAL ANSWERS LEFT BLANK
			total_bis_1selfcontrol_leftblank = bis_1selfcontrol_forward_leftblank + bis_1selfcontrol_reverse_leftblank
		
			# TOTAL ANSWERS PREFER NOT TO ANSWER
			total_bis_1selfcontrol_prefernotanswer = bis_1selfcontrol_forward_prefernotanswer + bis_1selfcontrol_reverse_prefernotanswer
		
			# Replace missing values with subscore averages 
			total_bis_1selfcontrol_score = total_bis_1selfcontrol_score + (total_bis_1selfcontrol_unanswered * total_bis_1selfcontrol_score / (6-total_bis_1selfcontrol_unanswered))
		
		
			# Check for scores that are outside acceptable values 
			for x in total_bis_1selfcontrol_score:
				if (x<6 or x>24) and x!=np.nan:
					total_bis_1selfcontrol_score=total_bis_1selfcontrol_score.replace([x],["Warning: This BIS_Self_Control score (%d) falls outside of the accepted range (6 to 24). Please check your data and try again."  % x])
		
			selfcontrolall = pd.DataFrame({'BIS_Self_Control_Left_Blank': total_bis_1selfcontrol_leftblank,'BIS_Self_Control_Prefer_Not_to_Answer': total_bis_1selfcontrol_prefernotanswer,'BIS_Self_Control_Score': total_bis_1selfcontrol_score,})
		
			# ------------------------------------------------------------------------------
			# BIS COGNITIVE COMPLEXITY
		
			# Change the numbers in forward bis 1atten headers to numeric floats
			bis_1complex_forward = df[bis_1complex_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			bis_1complex_forward_leftblank = bis_1complex_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1complex_forward_prefernotanswer = bis_1complex_forward[bis_1complex_forward[bis_1complex_keys] == 999].count(axis=1)
			bis_1complex_forward_unanswered = bis_1complex_forward_leftblank + bis_1complex_forward_prefernotanswer
		
			# Sum all the forward scores
			bis_1complex_forward_score = bis_1complex_forward[bis_1complex_forward[bis_1complex_keys] < 5].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			bis_1complex_rev =df[bis_1complex_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			bis_1complex_reverse_leftblank = bis_1complex_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1complex_reverse_prefernotanswer = bis_1complex_rev[bis_1complex_rev[bis_1complex_rev_keys] == 999].count(axis=1)
			bis_1complex_reverse_unanswered = bis_1complex_reverse_leftblank + bis_1complex_reverse_prefernotanswer
		
			# Sum all the reverse scores
			bis_1complex_reverse_score = bis_1complex_rev.rsub(5)[bis_1complex_rev[bis_1complex_rev_keys] < 5].sum(axis=1)
		
			# Total bis 1complex score
			total_bis_1complex_score = bis_1complex_forward_score + bis_1complex_reverse_score
			total_bis_1complex_score=total_bis_1complex_score.replace([0],[np.nan])
		
			# TOTAL bis 1complex ANSWERS UNANSWERED
			total_bis_1complex_unanswered = bis_1complex_forward_unanswered + bis_1complex_reverse_unanswered
		
			# TOTAL ANSWERS LEFT BLANK
			total_bis_1complex_leftblank = bis_1complex_forward_leftblank + bis_1complex_reverse_leftblank
		
			# TOTAL ANSWERS PREFER NOT TO ANSWER
			total_bis_1complex_prefernotanswer = bis_1complex_forward_prefernotanswer + bis_1complex_reverse_prefernotanswer
		
			# Replace missing values with subscore averages 
			total_bis_1complex_score = total_bis_1complex_score + (total_bis_1complex_unanswered * total_bis_1complex_score / (5-total_bis_1complex_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_bis_1complex_score:
				if (x<5 or x>20) and x!=np.nan:
					total_bis_1complex_score=total_bis_1complex_score.replace([x],["Warning: This BIS_Cognitive_Complexity score (%d) falls outside of the accepted range (5 to 20). Please check your data and try again."  % x])
			cogcomplexall = pd.DataFrame({'BIS_Cognitive_Complexity_Left_Blank': total_bis_1complex_leftblank,'BIS_Cognitive_Complexity_Prefer_Not_to_Answer': total_bis_1complex_prefernotanswer,'BIS_Cognitive_Complexity_Score': total_bis_1complex_score,})
		
			# ------------------------------------------------------------------------------
			# BIS PERSEVERANCE
		
			# Change the numbers in forward bis 1persever headers to numeric floats
			bis_1persever_forward = df[bis_1persever_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			bis_1persever_forward_leftblank = bis_1persever_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1persever_forward_prefernotanswer = bis_1persever_forward[bis_1persever_forward[bis_1persever_keys] == 999].count(axis=1)
			bis_1persever_forward_unanswered = bis_1persever_forward_leftblank + bis_1persever_forward_prefernotanswer
		
			# Sum all the forward scores
			bis_1persever_forward_score = bis_1persever_forward[bis_1persever_forward[bis_1persever_keys] < 5].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			bis_1persever_rev =df[bis_1persever_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			bis_1persever_reverse_leftblank = bis_1persever_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_1persever_reverse_prefernotanswer = bis_1persever_rev[bis_1persever_rev[bis_1persever_rev_keys] == 999].count(axis=1)
			bis_1persever_reverse_unanswered = bis_1persever_reverse_leftblank + bis_1persever_reverse_prefernotanswer
		
			# Sum all the reverse scores
			bis_1persever_reverse_score = bis_1persever_rev.rsub(5)[bis_1persever_rev[bis_1persever_rev_keys] < 5].sum(axis=1)
		
			# Total bis 1persever score
			total_bis_1persever_score = bis_1persever_forward_score + bis_1persever_reverse_score
			total_bis_1persever_score=total_bis_1persever_score.replace([0],[np.nan])
		
			# TOTAL bis 1persever ANSWERS UNANSWERED
			total_bis_1persever_unanswered = bis_1persever_forward_unanswered + bis_1persever_reverse_unanswered
		
			# TOTAL ANSWERS LEFT BLANK
			total_bis_1persever_leftblank = bis_1persever_forward_leftblank + bis_1persever_reverse_leftblank
		
			# TOTAL ANSWERS PREFER NOT TO ANSWER
			total_bis_1persever_prefernotanswer = bis_1persever_forward_prefernotanswer + bis_1persever_reverse_prefernotanswer
		
			# Replace missing values with subscore averages 
			total_bis_1persever_score = total_bis_1persever_score + (total_bis_1persever_unanswered * total_bis_1persever_score / (4-total_bis_1persever_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_bis_1persever_score:
				if (x<4 or x>16) and x!=np.nan:
					total_bis_1persever_score=total_bis_1persever_score.replace([x],["Warning: This BIS_Perseverance score (%d) falls outside of the accepted range (4 to 16). Please check your data and try again."  % x])
		
			perseverall = pd.DataFrame({'BIS_Perseverance_Left_Blank': total_bis_1persever_leftblank,'BIS_Perseverance_Prefer_Not_to_Answer': total_bis_1persever_prefernotanswer,'BIS_Perseverance_Score': total_bis_1persever_score,})
			# ------------------------------------------------------------------------------
			# ATTENTIONAL IMPULSIVENESS
		
			# Change the numbers in forward bis attentionalimpulsiveness headers to numeric floats
			bis_2attentionalimpulsiveness_forward = df[bis_2attentionalimpulsiveness_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			bis_2attentionalimpulsiveness_forward_leftblank = bis_2attentionalimpulsiveness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_2attentionalimpulsiveness_forward_prefernotanswer = bis_2attentionalimpulsiveness_forward[bis_2attentionalimpulsiveness_forward[bis_2attentionalimpulsiveness_keys] == 999].count(axis=1)
			bis_2attentionalimpulsiveness_forward_unanswered = bis_2attentionalimpulsiveness_forward_leftblank + bis_2attentionalimpulsiveness_forward_prefernotanswer
		
			# Sum all the forward scores
			bis_2attentionalimpulsiveness_forward_score = bis_2attentionalimpulsiveness_forward[bis_2attentionalimpulsiveness_forward[bis_2attentionalimpulsiveness_keys] < 5].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			bis_2attentionalimpulsiveness_rev =df[bis_2attentionalimpulsiveness_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			bis_2attentionalimpulsiveness_reverse_leftblank = bis_2attentionalimpulsiveness_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_2attentionalimpulsiveness_reverse_prefernotanswer = bis_2attentionalimpulsiveness_rev[bis_2attentionalimpulsiveness_rev[bis_2attentionalimpulsiveness_rev_keys] == 999].count(axis=1)
			bis_2attentionalimpulsiveness_reverse_unanswered = bis_2attentionalimpulsiveness_reverse_leftblank + bis_2attentionalimpulsiveness_reverse_prefernotanswer
		
			# Sum all the reverse scores
			bis_2attentionalimpulsiveness_reverse_score = bis_2attentionalimpulsiveness_rev.rsub(5)[bis_2attentionalimpulsiveness_rev[bis_2attentionalimpulsiveness_rev_keys] < 5].sum(axis=1)
		
			# Total bis 2attentionalimpulsiveness score
			total_bis_2attentionalimpulsiveness_score = bis_2attentionalimpulsiveness_forward_score + bis_2attentionalimpulsiveness_reverse_score
			total_bis_2attentionalimpulsiveness_score=total_bis_2attentionalimpulsiveness_score.replace([0],[np.nan])
		
			# TOTAL bis 2attentionalimpulsiveness ANSWERS UNANSWERED
			total_bis_2attentionalimpulsiveness_unanswered = bis_2attentionalimpulsiveness_forward_unanswered + bis_2attentionalimpulsiveness_reverse_unanswered
		
			# TOTAL ANSWERS LEFT BLANK
			total_bis_2attentionalimpulsiveness_leftblank = bis_2attentionalimpulsiveness_forward_leftblank + bis_2attentionalimpulsiveness_reverse_leftblank
		
			# TOTAL ANSWERS PREFER NOT TO ANSWER
			total_bis_2attentionalimpulsiveness_prefernotanswer = bis_2attentionalimpulsiveness_forward_prefernotanswer + bis_2attentionalimpulsiveness_reverse_prefernotanswer
		
			# Replace missing values with subscore averages 
			total_bis_2attentionalimpulsiveness_score = total_bis_2attentionalimpulsiveness_score + (total_bis_2attentionalimpulsiveness_unanswered * total_bis_2attentionalimpulsiveness_score / (8-total_bis_2attentionalimpulsiveness_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_bis_2attentionalimpulsiveness_score:
				if (x<8 or x>32) and x!=np.nan:
					total_bis_2attentionalimpulsiveness_score=total_bis_2attentionalimpulsiveness_score.replace([x],["Warning: This BIS_Attentional_Impulsiveness score (%d) falls outside of the accepted range (8 to 32). Please check your data and try again."  % x])
			attenimpulsall= pd.DataFrame({'BIS_Attentional_Impulsiveness_Left_Blank': total_bis_2attentionalimpulsiveness_leftblank,'BIS_Attentional_Impulsiveness_Prefer_Not_to_Answer': total_bis_2attentionalimpulsiveness_prefernotanswer,'BIS_Attentional_Impulsiveness_Score': total_bis_2attentionalimpulsiveness_score,})
			# ------------------------------------------------------------------------------
			# MOTOR IMPULSIVENESS
		
			# Change the numbers in forward bis motorimpulsiveness headers to numeric floats
			bis_2motorimpulsiveness_forward = df[bis_2motorimpulsiveness_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			bis_2motorimpulsiveness_forward_leftblank = bis_2motorimpulsiveness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_2motorimpulsiveness_forward_prefernotanswer = bis_2motorimpulsiveness_forward[bis_2motorimpulsiveness_forward[bis_2motorimpulsiveness_keys] == 999].count(axis=1)
			bis_2motorimpulsiveness_forward_unanswered = bis_2motorimpulsiveness_forward_leftblank + bis_2motorimpulsiveness_forward_prefernotanswer
		
			# Sum all the forward scores
			bis_2motorimpulsiveness_forward_score = bis_2motorimpulsiveness_forward[bis_2motorimpulsiveness_forward[bis_2motorimpulsiveness_keys] < 5].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			bis_2motorimpulsiveness_rev =df[bis_2motorimpulsiveness_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			bis_2motorimpulsiveness_reverse_leftblank = bis_2motorimpulsiveness_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_2motorimpulsiveness_reverse_prefernotanswer = bis_2motorimpulsiveness_rev[bis_2motorimpulsiveness_rev[bis_2motorimpulsiveness_rev_keys] == 999].count(axis=1)
			bis_2motorimpulsiveness_reverse_unanswered = bis_2motorimpulsiveness_reverse_leftblank + bis_2motorimpulsiveness_reverse_prefernotanswer
		
			# Sum all the reverse scores
			bis_2motorimpulsiveness_reverse_score = bis_2motorimpulsiveness_rev.rsub(5)[bis_2motorimpulsiveness_rev[bis_2motorimpulsiveness_rev_keys] < 5].sum(axis=1)
		
			# Total bis 2motorimpulsiveness score
			total_bis_2motorimpulsiveness_score = bis_2motorimpulsiveness_forward_score + bis_2motorimpulsiveness_reverse_score
			total_bis_2motorimpulsiveness_score=total_bis_2motorimpulsiveness_score.replace([0],[np.nan])
		
			# TOTAL bis 2motorimpulsiveness ANSWERS UNANSWERED
			total_bis_2motorimpulsiveness_unanswered = bis_2motorimpulsiveness_forward_unanswered + bis_2motorimpulsiveness_reverse_unanswered
		
			# TOTAL ANSWERS LEFT BLANK
			total_bis_2motorimpulsiveness_leftblank = bis_2motorimpulsiveness_forward_leftblank + bis_2motorimpulsiveness_reverse_leftblank
		
			# TOTAL ANSWERS PREFER NOT TO ANSWER
			total_bis_2motorimpulsiveness_prefernotanswer = bis_2motorimpulsiveness_forward_prefernotanswer + bis_2motorimpulsiveness_reverse_prefernotanswer
		
			# Replace missing values with subscore averages 
			total_bis_2motorimpulsiveness_score = total_bis_2motorimpulsiveness_score + (total_bis_2motorimpulsiveness_unanswered * total_bis_2motorimpulsiveness_score / (11-total_bis_2motorimpulsiveness_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_bis_2motorimpulsiveness_score:
				if (x<11 or x>44) and x!=np.nan:
					total_bis_2motorimpulsiveness_score=total_bis_2motorimpulsiveness_score.replace([x],["Warning: This BIS_Attention score (%d) falls outside of the accepted range (11 to 44). Please check your data and try again."  % x])
		
			motorimpulsall = pd.DataFrame({'BIS_Motor_Impulsiveness_Left_Blank': total_bis_2motorimpulsiveness_leftblank,'BIS_Motor_Impulsiveness_Prefer_Not_to_Answer': total_bis_2motorimpulsiveness_prefernotanswer,'BIS_Motor_Impulsiveness_Score': total_bis_2motorimpulsiveness_score,})
			# ------------------------------------------------------------------------------
			# NONPLANNING IMPULSIVENESS
		
			# Change the numbers in forward bis 1atten headers to numeric floats
			bis_2nonplanningimpulsiveness_forward = df[bis_2nonplanningimpulsiveness_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			bis_2nonplanningimpulsiveness_forward_leftblank = bis_2nonplanningimpulsiveness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_2nonplanningimpulsiveness_forward_prefernotanswer = bis_2nonplanningimpulsiveness_forward[bis_2nonplanningimpulsiveness_forward[bis_2nonplanningimpulsiveness_keys] == 999].count(axis=1)
			bis_2nonplanningimpulsiveness_forward_unanswered = bis_2nonplanningimpulsiveness_forward_leftblank + bis_2nonplanningimpulsiveness_forward_prefernotanswer
		
			# Sum all the forward scores
			bis_2nonplanningimpulsiveness_forward_score = bis_2nonplanningimpulsiveness_forward[bis_2nonplanningimpulsiveness_forward[bis_2nonplanningimpulsiveness_keys] < 5].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			bis_2nonplanningimpulsiveness_rev =df[bis_2nonplanningimpulsiveness_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			bis_2nonplanningimpulsiveness_reverse_leftblank = bis_2nonplanningimpulsiveness_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			bis_2nonplanningimpulsiveness_reverse_prefernotanswer = bis_2nonplanningimpulsiveness_rev[bis_2nonplanningimpulsiveness_rev[bis_2nonplanningimpulsiveness_rev_keys] == 999].count(axis=1)
			bis_2nonplanningimpulsiveness_reverse_unanswered = bis_2nonplanningimpulsiveness_reverse_leftblank + bis_2nonplanningimpulsiveness_reverse_prefernotanswer
		
			# Sum all the reverse scores
			bis_2nonplanningimpulsiveness_reverse_score = bis_2nonplanningimpulsiveness_rev.rsub(5)[bis_2nonplanningimpulsiveness_rev[bis_2nonplanningimpulsiveness_rev_keys] < 5].sum(axis=1)
		
			# Total bis 2nonplanningimpulsiveness score
			total_bis_2nonplanningimpulsiveness_score = bis_2nonplanningimpulsiveness_forward_score + bis_2nonplanningimpulsiveness_reverse_score
			total_bis_2nonplanningimpulsiveness_score=total_bis_2nonplanningimpulsiveness_score.replace([0],[np.nan])
		
			# TOTAL bis 2nonplanningimpulsiveness ANSWERS UNANSWERED
			total_bis_2nonplanningimpulsiveness_unanswered = bis_2nonplanningimpulsiveness_forward_unanswered + bis_2nonplanningimpulsiveness_reverse_unanswered
		
			# TOTAL ANSWERS LEFT BLANK
			total_bis_2nonplanningimpulsiveness_leftblank = bis_2nonplanningimpulsiveness_forward_leftblank + bis_2nonplanningimpulsiveness_reverse_leftblank
		
			# TOTAL ANSWERS PREFER NOT TO ANSWER
			total_bis_2nonplanningimpulsiveness_prefernotanswer = bis_2nonplanningimpulsiveness_forward_prefernotanswer + bis_2nonplanningimpulsiveness_reverse_prefernotanswer
		
			# Replace missing values with subscore averages 
			total_bis_2nonplanningimpulsiveness_score = total_bis_2nonplanningimpulsiveness_score + (total_bis_2nonplanningimpulsiveness_unanswered * total_bis_2nonplanningimpulsiveness_score / (11-total_bis_2nonplanningimpulsiveness_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_bis_2nonplanningimpulsiveness_score:
				if (x<11 or x>44) and x!=np.nan:
					total_bis_2nonplanningimpulsiveness_score=total_bis_2nonplanningimpulsiveness_score.replace([x],["Warning: This BIS_Nonplanning_Impulsiveness score (%d) falls outside of the accepted range (11 to 44). Please check your data and try again."  % x])

			nonplanimpulsall = pd.DataFrame({'BIS_Nonplanning_Impulsiveness_Left_Blank': total_bis_2nonplanningimpulsiveness_leftblank,'BIS_Nonplanning_Impulsiveness_Prefer_Not_to_Answer': total_bis_2nonplanningimpulsiveness_prefernotanswer,'BIS_Nonplanning_Impulsiveness_Score': total_bis_2nonplanningimpulsiveness_score,})
		
			# ------------------------------------------------------------------------------
			# Put the scores into one frame
			bis_frames = [attentionall, coginstall, motorall, selfcontrolall, cogcomplexall, perseverall, attenimpulsall, motorimpulsall, nonplanimpulsall]
			bis_result = pd.concat(bis_frames, axis=1)
	return bis_result
		#bis_result.to_csv(raw_input("Save your Barratt (BIS) Output csv as: "))