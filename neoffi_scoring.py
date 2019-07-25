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

# Neuroticism-Extroversion-Openness Five Factor Inventory

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/tiu9dcg02dfxcwrg5gec1eg32kaci48e
Scoring: https://yale.box.com/s/0acqjkfqw070zxr5ju0vd3j8mus13pe9
"""

# SCORING:
"""
1. Raw subscores are computed by summing each subscale. Questions that should be reverse scored are reverse scored.

2. Missing values are scored as Neutral (2) (as per the scoring instructions). 
"""

# STRONGLY DISAGREE - DISAGREE - NEUTRAL - AGREE - STRONGLY AGREE - PREFER NOT TO ANSWER
#        0               1         2        3          4                   999


# Subscale scores:	min= 0	max= 48
# ------------------------------------------------------------------------------
#Data Preparation

def neoffi_analysis(df): 
	# These are the different headers and their corresponding questions
	neoffi_neuroticism_keys = ['neoffi_6', 'neoffi_11', 'neoffi_21', 'neoffi_26', 'neoffi_36', 'neoffi_41', 'neoffi_51', 'neoffi_56']
	neoffi_neuroticism_reverse_keys = ['neoffi_1', 'neoffi_16', 'neoffi_31', 'neoffi_46']
	neoffi_extraversion_keys = ['neoffi_2', 'neoffi_7', 'neoffi_17', 'neoffi_22', 'neoffi_32', 'neoffi_37', 'neoffi_47', 'neoffi_52']
	neoffi_extraversion_reverse_keys = ['neoffi_12', 'neoffi_27', 'neoffi_42', 'neoffi_57']
	neoffi_openness_keys = ['neoffi_13', 'neoffi_28', 'neoffi_43', 'neoffi_53', 'neoffi_58']
	neoffi_openness_reverse_keys = ['neoffi_3', 'neoffi_8', 'neoffi_18', 'neoffi_23', 'neoffi_33', 'neoffi_38', 'neoffi_48']
	neoffi_agreeableness_keys = ['neoffi_4', 'neoffi_19', 'neoffi_34', 'neoffi_49']
	neoffi_agreeableness_reverse_keys = ['neoffi_9', 'neoffi_14', 'neoffi_24', 'neoffi_29', 'neoffi_39', 'neoffi_44', 'neoffi_54', 'neoffi_59']
	neoffi_conscientiousness_keys = ['neoffi_5', 'neoffi_10', 'neoffi_20', 'neoffi_25', 'neoffi_35', 'neoffi_40', 'neoffi_50', 'neoffi_60']
	neoffi_conscientiousness_reverse_keys = ['neoffi_15', 'neoffi_30', 'neoffi_45', 'neoffi_55']

	neoffi_negative_affect_keys = ['neoffi_11']
	neoffi_negative_affect_reverse_keys = ['neoffi_1', 'neoffi_16', 'neoffi_31', 'neoffi_46']
	neoffi_self_reproach_keys= ['neoffi_6', 'neoffi_21', 'neoffi_26', 'neoffi_36','neoffi_41', 'neoffi_51', 'neoffi_56']

	neoffi_positive_affect_keys = ['neoffi_7', 'neoffi_37']
	neoffi_positive_affect_reverse_keys = ['neoffi_12', 'neoffi_42']
	neoffi_sociability_keys = ['neoffi_2', 'neoffi_17']
	neoffi_sociability_reverse_keys = ['neoffi_27', 'neoffi_57']
	neoffi_activity_keys = ['neoffi_22', 'neoffi_32', 'neoffi_47', 'neoffi_52']

	neoffi_aesthetic_interests_keys = ['neoffi_13', 'neoffi_43']
	neoffi_aesthetic_interests_reverse_keys = ['neoffi_23']
	neoffi_intellectual_interests_keys = ['neoffi_53', 'neoffi_58']
	neoffi_intellectual_interests_reverse_keys = ['neoffi_48']
	neoffi_unconventionality_reverse_keys = ['neoffi_3', 'neoffi_8', 'neoffi_18', 'neoffi_38']

	neoffi_nonantagonistic_orientation_keys = ['neoffi_19']
	neoffi_nonantagonistic_orientation_reverse_keys= ['neoffi_9', 'neoffi_14', 'neoffi_24', 'neoffi_29','neoffi_44', 'neoffi_54', 'neoffi_59']
	neoffi_prosocial_orientation_keys = ['neoffi_4', 'neoffi_34', 'neoffi_49']
	neoffi_prosocial_orientation_reverse_keys= ['neoffi_39']


	neoffi_orderliness_keys = ['neoffi_5', 'neoffi_10']
	neoffi_orderliness_reverse_keys = ['neoffi_15', 'neoffi_30', 'neoffi_55']
	neoffi_goal_striving_keys = ['neoffi_25', 'neoffi_35', 'neoffi_60']
	neoffi_dependability_keys = ['neoffi_20', 'neoffi_40', 'neoffi_50']
	neoffi_dependability_reverse_keys = ['neoffi_45']

	neoffi_tot_keys = neoffi_neuroticism_keys+neoffi_neuroticism_reverse_keys+neoffi_extraversion_keys+neoffi_extraversion_reverse_keys+neoffi_openness_keys+neoffi_openness_reverse_keys+neoffi_agreeableness_keys+neoffi_agreeableness_reverse_keys+neoffi_conscientiousness_keys+neoffi_conscientiousness_reverse_keys



	# Replace Qualtrics text answers with numerical values
	df[neoffi_tot_keys]= df[neoffi_tot_keys].replace(['strongly disagree', 'disagree',  'neutral', 'agree', 'strongly agree'], [0,1,2,3,4])

	# Number of prefer to not answer responses are calculated first so that they can be later scored as "2" and added to the actual score

	neuroticism_forward = df[neoffi_neuroticism_keys].apply(pd.to_numeric, args=('raise',))
	neuroticism_reverse = df[neoffi_neuroticism_reverse_keys].apply(pd.to_numeric, args=('raise',))
	neuroticism_forward_prefernotanswer = neuroticism_forward.apply(lambda x: sum(x==999), axis=1)
	neuroticism_reverse_prefernotanswer = neuroticism_reverse.apply(lambda x: sum(x==999), axis=1)
	neuroticism_forward_leftblank = neuroticism_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	neuroticism_reverse_leftblank = neuroticism_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	negative_affect_forward = df[neoffi_negative_affect_keys].apply(pd.to_numeric, args=('raise',))
	negative_affect_reverse = df[neoffi_negative_affect_reverse_keys].apply(pd.to_numeric, args=('raise',))
	negative_affect_forward_prefernotanswer = negative_affect_forward.apply(lambda x: sum(x==999), axis=1)
	negative_affect_reverse_prefernotanswer = negative_affect_reverse.apply(lambda x: sum(x==999), axis=1)
	negative_affect_forward_leftblank = negative_affect_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	negative_affect_reverse_leftblank = negative_affect_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	self_reproach_forward = df[neoffi_self_reproach_keys].apply(pd.to_numeric, args=('raise',))
	self_reproach_forward_prefernotanswer = self_reproach_forward.apply(lambda x: sum(x==999), axis=1)
	self_reproach_forward_leftblank = self_reproach_forward.apply(lambda x: sum(x.isnull().values), axis=1)

	extraversion_forward = df[neoffi_extraversion_keys].apply(pd.to_numeric, args=('raise',))
	extraversion_reverse = df[neoffi_extraversion_reverse_keys].apply(pd.to_numeric, args=('raise',))
	extraversion_forward_prefernotanswer = extraversion_forward.apply(lambda x: sum(x==999), axis=1)
	extraversion_reverse_prefernotanswer = extraversion_reverse.apply(lambda x: sum(x==999), axis=1)
	extraversion_forward_leftblank = extraversion_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	extraversion_reverse_leftblank = extraversion_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	positive_affect_forward = df[neoffi_positive_affect_keys].apply(pd.to_numeric, args=('raise',))
	positive_affect_reverse = df[neoffi_positive_affect_reverse_keys].apply(pd.to_numeric, args=('raise',))
	positive_affect_forward_prefernotanswer = positive_affect_forward.apply(lambda x: sum(x==999), axis=1)
	positive_affect_reverse_prefernotanswer = positive_affect_reverse.apply(lambda x: sum(x==999), axis=1)
	positive_affect_forward_leftblank = positive_affect_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	positive_affect_reverse_leftblank = positive_affect_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	sociability_forward = df[neoffi_sociability_keys].apply(pd.to_numeric, args=('raise',))
	sociability_reverse = df[neoffi_sociability_reverse_keys].apply(pd.to_numeric, args=('raise',))
	sociability_forward_prefernotanswer = sociability_forward.apply(lambda x: sum(x==999), axis=1)
	sociability_reverse_prefernotanswer = sociability_reverse.apply(lambda x: sum(x==999), axis=1)
	sociability_forward_leftblank = sociability_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	sociability_reverse_leftblank = sociability_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	activity_forward = df[neoffi_activity_keys].apply(pd.to_numeric, args=('raise',))
	activity_forward_prefernotanswer = activity_forward.apply(lambda x: sum(x==999), axis=1)
	activity_forward_leftblank = activity_forward.apply(lambda x: sum(x.isnull().values), axis=1)

	openness_forward = df[neoffi_openness_keys].apply(pd.to_numeric, args=('raise',))
	openness_reverse = df[neoffi_openness_reverse_keys].apply(pd.to_numeric, args=('raise',))
	openness_forward_prefernotanswer = openness_forward.apply(lambda x: sum(x==999), axis=1)
	openness_reverse_prefernotanswer = openness_reverse.apply(lambda x: sum(x==999), axis=1)
	openness_forward_leftblank = openness_forward.apply(lambda x: sum(x==999), axis=1)
	openness_reverse_leftblank = openness_reverse.apply(lambda x: sum(x==999), axis=1)

	aesthetic_interests_forward = df[neoffi_aesthetic_interests_keys].apply(pd.to_numeric, args=('raise',))
	aesthetic_interests_reverse = df[neoffi_aesthetic_interests_reverse_keys].apply(pd.to_numeric, args=('raise',))
	aesthetic_interests_forward_prefernotanswer = aesthetic_interests_forward.apply(lambda x: sum(x==999), axis=1)
	aesthetic_interests_reverse_prefernotanswer = aesthetic_interests_reverse.apply(lambda x: sum(x==999), axis=1)
	aesthetic_interests_forward_leftblank = aesthetic_interests_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	aesthetic_interests_reverse_leftblank = aesthetic_interests_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	intellectual_interests_reverse = df[neoffi_intellectual_interests_reverse_keys].apply(pd.to_numeric, args=('raise',))
	intellectual_interests_forward = df[neoffi_intellectual_interests_keys].apply(pd.to_numeric, args=('raise',))
	intellectual_interests_forward_prefernotanswer = intellectual_interests_forward.apply(lambda x: sum(x==999), axis=1)
	intellectual_interests_reverse_prefernotanswer = intellectual_interests_reverse.apply(lambda x: sum(x==999), axis=1)
	intellectual_interests_forward_leftblank = intellectual_interests_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	intellectual_interests_reverse_leftblank = intellectual_interests_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	unconventionality_reverse = df[neoffi_unconventionality_reverse_keys].apply(pd.to_numeric, args=('raise',))
	unconventionality_reverse_prefernotanswer = unconventionality_reverse.apply(lambda x: sum(x==999), axis=1)
	unconventionality_reverse_leftblank = unconventionality_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	agreeableness_forward = df[neoffi_agreeableness_keys].apply(pd.to_numeric, args=('raise',))
	agreeableness_reverse = df[neoffi_agreeableness_reverse_keys].apply(pd.to_numeric, args=('raise',))
	agreeableness_forward_prefernotanswer = agreeableness_forward.apply(lambda x: sum(x==999), axis=1)
	agreeableness_reverse_prefernotanswer = agreeableness_reverse.apply(lambda x: sum(x==999), axis=1)
	agreeableness_forward_leftblank = agreeableness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	agreeableness_reverse_leftblank = agreeableness_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	nonantagonistic_orientation_forward = df[neoffi_nonantagonistic_orientation_keys].apply(pd.to_numeric, args=('raise',))
	nonantagonistic_orientation_reverse = df[neoffi_nonantagonistic_orientation_reverse_keys].apply(pd.to_numeric, args=('raise',))
	nonantagonistic_orientation_forward_prefernotanswer = nonantagonistic_orientation_forward.apply(lambda x: sum(x==999), axis=1)
	nonantagonistic_orientation_reverse_prefernotanswer = nonantagonistic_orientation_reverse.apply(lambda x: sum(x==999), axis=1)
	nonantagonistic_orientation_forward_leftblank = nonantagonistic_orientation_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	nonantagonistic_orientation_reverse_leftblank = nonantagonistic_orientation_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	prosocial_orientation_forward = df[neoffi_prosocial_orientation_keys].apply(pd.to_numeric, args=('raise',))
	prosocial_orientation_reverse = df[neoffi_prosocial_orientation_reverse_keys].apply(pd.to_numeric, args=('raise',))
	prosocial_orientation_forward_prefernotanswer = prosocial_orientation_forward.apply(lambda x: sum(x==999), axis=1)
	prosocial_orientation_reverse_prefernotanswer = prosocial_orientation_reverse.apply(lambda x: sum(x==999), axis=1)
	prosocial_orientation_forward_leftblank = prosocial_orientation_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	prosocial_orientation_reverse_leftblank = prosocial_orientation_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	conscientiousness_forward = df[neoffi_conscientiousness_keys].apply(pd.to_numeric, args=('raise',))
	conscientiousness_reverse = df[neoffi_conscientiousness_reverse_keys].apply(pd.to_numeric, args=('raise',))
	conscientiousness_forward_prefernotanswer = conscientiousness_forward.apply(lambda x: sum(x==999), axis=1)
	conscientiousness_reverse_prefernotanswer = conscientiousness_reverse.apply(lambda x: sum(x==999), axis=1)
	conscientiousness_forward_leftblank = conscientiousness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	conscientiousness_reverse_leftblank = conscientiousness_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	orderliness_forward = df[neoffi_orderliness_keys].apply(pd.to_numeric, args=('raise',))
	orderliness_reverse = df[neoffi_orderliness_reverse_keys].apply(pd.to_numeric, args=('raise',))
	orderliness_forward_prefernotanswer = orderliness_forward.apply(lambda x: sum(x==999), axis=1)
	orderliness_reverse_prefernotanswer = orderliness_reverse.apply(lambda x: sum(x==999), axis=1)
	orderliness_forward_leftblank = orderliness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	orderliness_reverse_leftblank = orderliness_reverse.apply(lambda x: sum(x.isnull().values), axis=1)

	goal_striving_forward = df[neoffi_goal_striving_keys].apply(pd.to_numeric, args=('raise',))
	goal_striving_forward_prefernotanswer = goal_striving_forward.apply(lambda x: sum(x==999), axis=1)
	goal_striving_forward_leftblank = goal_striving_forward.apply(lambda x: sum(x.isnull().values), axis=1)

	dependability_forward = df[neoffi_dependability_keys].apply(pd.to_numeric, args=('raise',))
	dependability_reverse = df[neoffi_dependability_reverse_keys].apply(pd.to_numeric, args=('raise',))
	dependability_forward_prefernotanswer = dependability_forward.apply(lambda x: sum(x==999), axis=1)
	dependability_reverse_prefernotanswer = dependability_reverse.apply(lambda x: sum(x==999), axis=1)
	dependability_forward_leftblank = dependability_forward.apply(lambda x: sum(x.isnull().values), axis=1)
	dependability_reverse_leftblank = dependability_reverse.apply(lambda x: sum(x.isnull().values), axis=1)


	# Recode 'Prefer to not answer' as 'Neutral'
	df[neoffi_tot_keys]= df[neoffi_tot_keys].replace([999],[2])

	# Check for values that don't match parameters 
	neoffi_check=df[neoffi_tot_keys].apply(pd.to_numeric,args=('raise',))
	neoffi_check=neoffi_check[(neoffi_check !=0) & (neoffi_check !=1) & (neoffi_check !=2) & (neoffi_check !=3) & (neoffi_check !=4) & (neoffi_check !=999)].sum()
	for x in neoffi_check:
		if x!=0:
			df['neoffi_error']=np.nan
			df.neoffi_error=df.neoffi_error.replace([np.nan],["Your NEO-FFI responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			neoffi_result=df['neoffi_error']
			
		else:
			# ------------------------------------------------------------------------------
			# NEUROTICISM score

			# sum all the forward scores
			neuroticism_forward_score = neuroticism_forward[(neuroticism_forward[neoffi_neuroticism_keys] >= 0) & (neuroticism_forward[neoffi_neuroticism_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			neuroticism_reverse_score = neuroticism_reverse[neuroticism_reverse[neoffi_neuroticism_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total Neuroticism score
			total_neuroticism_score = neuroticism_forward_score + neuroticism_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_neuroticism_prefernotanswer = neuroticism_forward_prefernotanswer + neuroticism_reverse_prefernotanswer
			total_neuroticism_leftblank = neuroticism_forward_leftblank + neuroticism_reverse_leftblank

			# Check for scores that are outside acceptable values 
			for x in total_neuroticism_score:
				if (x<0 or x>48) and x!=np.nan:
					total_neuroticism_score=total_neuroticism_score.replace([x],["Warning: This NEO-FFI_neuroticism score (%d) falls outside of the accepted range (0 to 48). Please check your data and try again."  % x])


			neuroall = pd.DataFrame({'NEO_N_Left_Blank' : total_neuroticism_leftblank, 'NEO_N_Prefer_Not_to_Answer': total_neuroticism_prefernotanswer, 'NEO_N_Score': total_neuroticism_score})

			# ------------------------------------------------------------------------------
			# Negative Affect score

			# sum all the forward scores
			negative_affect_forward_score = negative_affect_forward[(negative_affect_forward[neoffi_negative_affect_keys] >= 0) & (negative_affect_forward[neoffi_negative_affect_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			negative_affect_reverse_score = negative_affect_reverse[negative_affect_reverse[neoffi_negative_affect_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total negative_affect score
			total_negative_affect_score = negative_affect_forward_score + negative_affect_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_negative_affect_prefernotanswer = negative_affect_forward_prefernotanswer + negative_affect_reverse_prefernotanswer
			total_negative_affect_leftblank = negative_affect_forward_leftblank + negative_affect_reverse_leftblank

			negaffall = pd.DataFrame({'NEO_N_NA_Left_Blank': total_negative_affect_leftblank, 'NEO_N_NA_Prefer_Not_to_Answer': total_negative_affect_prefernotanswer, 'NEO_N_NA_Score': total_negative_affect_score,})


			# ------------------------------------------------------------------------------
			# Self-reproach score

			# sum all the forward scores
			self_reproach_forward_score = self_reproach_forward[(self_reproach_forward[neoffi_self_reproach_keys] >= 0) & (self_reproach_forward[neoffi_self_reproach_keys] <= 4)].sum(axis=1)

			# Total self_reproach score
			total_self_reproach_score = self_reproach_forward_score 

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_self_reproach_prefernotanswer = self_reproach_forward_prefernotanswer 
			total_self_reproach_leftblank = self_reproach_forward_leftblank


			selfrepall = pd.DataFrame({'NEO_N_SR_Left_Blank': total_self_reproach_leftblank,'NEO_N_SR_Prefer_Not_to_Answer': total_self_reproach_prefernotanswer,'NEO_N_SR_Score': total_self_reproach_score})

			# ------------------------------------------------------------------------------

			# Extraversion score

			# sum all the forward scores
			extraversion_forward_score = extraversion_forward[(extraversion_forward[neoffi_extraversion_keys] >= 0) & (extraversion_forward[neoffi_extraversion_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			extraversion_reverse_score = extraversion_reverse[extraversion_reverse[neoffi_extraversion_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total extraversion score
			total_extraversion_score = extraversion_forward_score + extraversion_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_extraversion_prefernotanswer = extraversion_forward_prefernotanswer + extraversion_reverse_prefernotanswer
			total_extraversion_leftblank = extraversion_forward_leftblank + extraversion_reverse_leftblank

			# Check for scores that are outside acceptable values 
			for x in total_extraversion_score:
				if (x<0 or x>48) and x!=np.nan:
					total_extraversion_score=total_extraversion_score.replace([x],["Warning: This NEO-FFI_extraversion score (%d) falls outside of the accepted range (0 to 48). Please check your data and try again."  % x])

			extraall = pd.DataFrame({'NEO_E_Left_Blank' : total_extraversion_leftblank, 'NEO_E_Prefer_Not_to_Answer': total_extraversion_prefernotanswer,'NEO_E_Score': total_extraversion_score})

			# ------------------------------------------------------------------------------
			# Positive Affect score

			# sum all the forward scores
			positive_affect_forward_score = positive_affect_forward[(positive_affect_forward[neoffi_positive_affect_keys] >= 0) & (positive_affect_forward[neoffi_positive_affect_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			positive_affect_reverse_score = positive_affect_reverse[positive_affect_reverse[neoffi_positive_affect_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total positive_affect score
			total_positive_affect_score = positive_affect_forward_score + positive_affect_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_positive_affect_prefernotanswer = positive_affect_forward_prefernotanswer + positive_affect_reverse_prefernotanswer
			total_positive_affect_leftblank = positive_affect_forward_leftblank + positive_affect_reverse_leftblank

			posaffall = pd.DataFrame({'NEO_E_PA_Prefer_Not_to_Answer': total_positive_affect_prefernotanswer,'NEO_E_PA_Score': total_positive_affect_score})

			# ------------------------------------------------------------------------------
			# Sociability score

			# sum all the forward scores
			sociability_forward_score = sociability_forward[(sociability_forward[neoffi_sociability_keys] >= 0) & (sociability_forward[neoffi_sociability_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			sociability_reverse_score = sociability_reverse[sociability_reverse[neoffi_sociability_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total sociability score
			total_sociability_score = sociability_forward_score + sociability_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_sociability_prefernotanswer = sociability_forward_prefernotanswer + sociability_reverse_prefernotanswer
			total_sociability_leftblank = sociability_forward_leftblank + sociability_reverse_leftblank

			socall = pd.DataFrame({'NEO_E_S_Prefer_Left_Blank': total_sociability_leftblank,'NEO_E_S_Prefer_Not_to_Answer': total_sociability_prefernotanswer,'NEO_E_S_Score': total_sociability_score})

			# ------------------------------------------------------------------------------
			# Activity score

			# sum all the forward scores
			activity_forward_score = activity_forward[(activity_forward[neoffi_activity_keys] >= 0) & (activity_forward[neoffi_activity_keys] <= 4)].sum(axis=1)

			# Total activity score
			total_activity_score = activity_forward_score 

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_activity_prefernotanswer = activity_forward_prefernotanswer 
			total_activity_leftblank = activity_forward_leftblank 

			actall = pd.DataFrame({'NEO_E_A_Prefer_Left_Blank': total_activity_leftblank,'NEO_E_A_Prefer_Not_to_Answer': total_activity_prefernotanswer,'NEO_E_A_Score': total_activity_score})

			# ------------------------------------------------------------------------------

			# OPENNESS score

			# sum all the forward scores
			openness_forward_score = openness_forward[(openness_forward[neoffi_openness_keys] >= 0) & (openness_forward[neoffi_openness_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			openness_reverse_score = openness_reverse[openness_reverse[neoffi_openness_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total openness score
			total_openness_score = openness_forward_score + openness_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_openness_prefernotanswer = openness_forward_prefernotanswer + openness_reverse_prefernotanswer
			total_openness_leftblank = openness_forward_leftblank + openness_reverse_leftblank

			# Check for scores that are outside acceptable values 
			for x in total_openness_score:
				if (x<0 or x>48) and x!=np.nan:
					total_openness_score=total_openness_score.replace([x],["Warning: This NEO-FFI_openness score (%d) falls outside of the accepted range (0 to 48). Please check your data and try again."  % x])

			openall = pd.DataFrame({'NEO_O_Left_Blank' : total_openness_leftblank, 'NEO_O_Prefer_Not_to_Answer': total_openness_prefernotanswer,'NEO_O_Score': total_openness_score})
			# ------------------------------------------------------------------------------

			# Aesthetic Interests score

			# sum all the forward scores
			aesthetic_interests_forward_score = aesthetic_interests_forward[(aesthetic_interests_forward[neoffi_aesthetic_interests_keys] >= 0) & (aesthetic_interests_forward[neoffi_aesthetic_interests_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			aesthetic_interests_reverse_score = aesthetic_interests_reverse[aesthetic_interests_reverse[neoffi_aesthetic_interests_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total aesthetic_interests score
			total_aesthetic_interests_score = aesthetic_interests_forward_score + aesthetic_interests_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_aesthetic_interests_prefernotanswer = aesthetic_interests_forward_prefernotanswer + aesthetic_interests_reverse_prefernotanswer
			total_aesthetic_interests_leftblank = aesthetic_interests_forward_leftblank + aesthetic_interests_reverse_leftblank

			aesall = pd.DataFrame({'NEO_O_AI_Prefer_Left_Blank': total_aesthetic_interests_leftblank,'NEO_O_AI_Prefer_Not_to_Answer': total_aesthetic_interests_prefernotanswer,'NEO_O_AI_Score': total_aesthetic_interests_score})

			# ------------------------------------------------------------------------------

			# Intellectual Interests score

			# sum all the forward scores
			intellectual_interests_forward_score = intellectual_interests_forward[(intellectual_interests_forward[neoffi_intellectual_interests_keys] >= 0) & (intellectual_interests_forward[neoffi_intellectual_interests_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			intellectual_interests_reverse_score = intellectual_interests_reverse[intellectual_interests_reverse[neoffi_intellectual_interests_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total intellectual_interests score
			total_intellectual_interests_score = intellectual_interests_forward_score + intellectual_interests_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_intellectual_interests_prefernotanswer = intellectual_interests_forward_prefernotanswer + intellectual_interests_reverse_prefernotanswer
			total_intellectual_interests_leftblank = intellectual_interests_forward_leftblank + intellectual_interests_reverse_leftblank

			intall = pd.DataFrame({'NEO_O_II_Prefer_Left_Blank': total_intellectual_interests_leftblank,'NEO_O_II_Prefer_Not_to_Answer': total_intellectual_interests_prefernotanswer, 'NEO_O_II_Score': total_intellectual_interests_score})

			# ------------------------------------------------------------------------------
			# Unconventionality score

			# sum all the reverse scores
			unconventionality_reverse_score = unconventionality_reverse[(unconventionality_reverse[neoffi_unconventionality_reverse_keys] >= 0) & (unconventionality_reverse[neoffi_unconventionality_reverse_keys] <= 4)].sum(axis=1)

			# Total unconventionality score
			total_unconventionality_score = unconventionality_reverse_score 

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_unconventionality_prefernotanswer = unconventionality_reverse_prefernotanswer 
			total_unconventionality_leftblank = unconventionality_reverse_leftblank

			unconvall = pd.DataFrame({'NEO_O_U_Prefer_Left_Blank': total_unconventionality_leftblank,'NEO_O_U_Prefer_Not_to_Answer': total_unconventionality_prefernotanswer,'NEO_O_U_Score': total_unconventionality_score})

			# ------------------------------------------------------------------------------
			# AGREEABLENESS score

			# sum all the forward scores
			agreeableness_forward_score = agreeableness_forward[(agreeableness_forward[neoffi_agreeableness_keys] >= 0) & (agreeableness_forward[neoffi_agreeableness_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			agreeableness_reverse_score = agreeableness_reverse[agreeableness_reverse[neoffi_agreeableness_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total agreeableness score
			total_agreeableness_score = agreeableness_forward_score + agreeableness_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_agreeableness_prefernotanswer = agreeableness_forward_prefernotanswer + agreeableness_reverse_prefernotanswer
			total_agreeableness_leftblank = agreeableness_forward_leftblank + agreeableness_reverse_leftblank

			# Check for scores that are outside acceptable values 
			for x in total_agreeableness_score:
				if (x<0 or x>48) and x!=np.nan:
					total_agreeableness_score=total_agreeableness_score.replace([x],["Warning: This NEO-FFI_agreeableness score (%d) falls outside of the accepted range (0 to 48). Please check your data and try again."  % x])

			agreeall = pd.DataFrame({'NEO_A_Left_Blank' : total_agreeableness_leftblank, 'NEO_A_Prefer_Not_to_Answer': total_agreeableness_prefernotanswer,'NEO_A_Score': total_agreeableness_score})
			# ------------------------------------------------------------------------------

			# Nonantagonistic Orientation Interests score

			# sum all the forward scores
			nonantagonistic_orientation_forward_score = nonantagonistic_orientation_forward[(nonantagonistic_orientation_forward[neoffi_nonantagonistic_orientation_keys] >= 0) & (nonantagonistic_orientation_forward[neoffi_nonantagonistic_orientation_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			nonantagonistic_orientation_reverse_score = nonantagonistic_orientation_reverse[nonantagonistic_orientation_reverse[neoffi_nonantagonistic_orientation_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total nonantagonistic_orientation score
			total_nonantagonistic_orientation_score = nonantagonistic_orientation_forward_score + nonantagonistic_orientation_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_nonantagonistic_orientation_prefernotanswer = nonantagonistic_orientation_forward_prefernotanswer + nonantagonistic_orientation_reverse_prefernotanswer
			total_nonantagonistic_orientation_leftblank = nonantagonistic_orientation_forward_leftblank + nonantagonistic_orientation_reverse_leftblank

			nonantagall = pd.DataFrame({'NEO_A_NO_Prefer_Left_Blank': total_nonantagonistic_orientation_leftblank,'NEO_A_NO_Prefer_Not_to_Answer': total_nonantagonistic_orientation_prefernotanswer,'NEO_A_NO_Score': total_nonantagonistic_orientation_score})

			# ------------------------------------------------------------------------------

			# Prosocial Orientation Interests score

			# sum all the forward scores
			prosocial_orientation_forward_score = prosocial_orientation_forward[(prosocial_orientation_forward[neoffi_prosocial_orientation_keys] >= 0) & (prosocial_orientation_forward[neoffi_prosocial_orientation_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			prosocial_orientation_reverse_score = prosocial_orientation_reverse[prosocial_orientation_reverse[neoffi_prosocial_orientation_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total prosocial_orientation score
			total_prosocial_orientation_score = prosocial_orientation_forward_score + prosocial_orientation_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_prosocial_orientation_prefernotanswer = prosocial_orientation_forward_prefernotanswer + prosocial_orientation_reverse_prefernotanswer
			total_prosocial_orientation_leftblank = prosocial_orientation_forward_leftblank + prosocial_orientation_reverse_leftblank

			prosocall = pd.DataFrame({'NEO_A_PO_Prefer_Left_Blank': total_prosocial_orientation_leftblank,'NEO_A_PO_Prefer_Not_to_Answer': total_prosocial_orientation_prefernotanswer,'NEO_A_PO_Score': total_prosocial_orientation_score})


			# ------------------------------------------------------------------------------
			# CONSCIENTIOUSNESS score

			# sum all the forward scores
			conscientiousness_forward_score = conscientiousness_forward[(conscientiousness_forward[neoffi_conscientiousness_keys] >= 0) & (conscientiousness_forward[neoffi_conscientiousness_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			conscientiousness_reverse_score = conscientiousness_reverse[conscientiousness_reverse[neoffi_conscientiousness_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total conscientiousness score
			total_conscientiousness_score = conscientiousness_forward_score + conscientiousness_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_conscientiousness_prefernotanswer = conscientiousness_forward_prefernotanswer + conscientiousness_reverse_prefernotanswer
			total_conscientiousness_leftblank = conscientiousness_forward_leftblank + conscientiousness_reverse_leftblank

			# Check for scores that are outside acceptable values 
			for x in total_conscientiousness_score:
				if (x<0 or x>48) and x!=np.nan:
					total_conscientiousness_score=total_conscientiousness_score.replace([x],["Warning: This NEO-FFI_conscientiousness score (%d) falls outside of the accepted range (0 to 48). Please check your data and try again."  % x])

			conscienall = pd.DataFrame({'NEO_C_Left_Blank' : total_conscientiousness_leftblank, 'NEO_C_Prefer_Not_to_Answer': total_conscientiousness_prefernotanswer,'NEO_C_Score': total_conscientiousness_score})

			# ------------------------------------------------------------------------------

			# Orderliness score

			# sum all the forward scores
			orderliness_forward_score = orderliness_forward[(orderliness_forward[neoffi_orderliness_keys] >= 0) & (orderliness_forward[neoffi_orderliness_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			orderliness_reverse_score = orderliness_reverse[orderliness_reverse[neoffi_orderliness_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total orderliness score
			total_orderliness_score = orderliness_forward_score + orderliness_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_orderliness_prefernotanswer = orderliness_forward_prefernotanswer + orderliness_reverse_prefernotanswer
			total_orderliness_leftblank = orderliness_forward_leftblank + orderliness_reverse_leftblank

			orderall = pd.DataFrame({'NEO_C_O_Prefer_Left_Blank': total_orderliness_leftblank,'NEO_C_O_Prefer_Not_to_Answer': total_orderliness_prefernotanswer,'NEO_C_O_Score': total_orderliness_score})
			# ------------------------------------------------------------------------------

			# Goal-striving score

			# sum all the forward scores
			goal_striving_forward_score = goal_striving_forward[(goal_striving_forward[neoffi_goal_striving_keys] >= 0) & (goal_striving_forward[neoffi_goal_striving_keys] <= 4)].sum(axis=1)

			# Total goal_striving score
			total_goal_striving_score = goal_striving_forward_score 

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_goal_striving_prefernotanswer = goal_striving_forward_prefernotanswer 
			total_goal_striving_leftblank = goal_striving_forward_leftblank 


			goalall = pd.DataFrame({'NEO_C_GS_Prefer_Left_Blank': total_goal_striving_leftblank,'NEO_C_GS_Prefer_Not_to_Answer': total_goal_striving_prefernotanswer,'NEO_C_GS_Score': total_goal_striving_score})

			# ------------------------------------------------------------------------------

			# Dependability score


			# sum all the forward scores
			dependability_forward_score = dependability_forward[(dependability_forward[neoffi_dependability_keys] >= 0) & (dependability_forward[neoffi_dependability_keys] <= 4)].sum(axis=1)

			# sum all the reverse scores
			dependability_reverse_score = dependability_reverse[dependability_reverse[neoffi_dependability_reverse_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

			# Total dependability score
			total_dependability_score = dependability_forward_score + dependability_reverse_score

			#TOTAL ANSWERS PREFER NOT TO ANSWER
			total_dependability_prefernotanswer = dependability_forward_prefernotanswer + dependability_reverse_prefernotanswer
			total_dependability_leftblank = dependability_forward_leftblank + dependability_reverse_leftblank


			dependall = pd.DataFrame({'NEO_C_D_Left_Blank': total_dependability_leftblank,'NEO_C_D_Prefer_Not_to_Answer': total_dependability_prefernotanswer,'NEO_C_D_Score': total_dependability_score})


			# ------------------------------------------------------------------------------
			# Put all the scores into one frame
			neoffi_frames = [df.SUBJECT_ID, neuroall, extraall, openall, agreeall, conscienall, negaffall, selfrepall, posaffall, socall, actall, openall, aesall, intall, unconvall, nonantagall, prosocall, orderall, goalall, dependall]
			neoffi_result = pd.concat(neoffi_frames, axis=1)
	return neoffi_result
	
	#neoffi_result.to_csv(raw_input("Save your NEO-FFI Output csv as: "))
