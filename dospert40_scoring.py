#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files
@author: David Gruskin
@email: david.gruskin@yale.edu
@version: 1.1
@date: 2017.09.26
"""
import pandas as pd
import numpy as np
import sys 

# DOMAIN-SPECIFIC RISK-TAKING SCALE (40-item, 2003)

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/62u9jf66bkdmvj6aztwctx3ngcd7xomu
Scoring: https://yale.box.com/s/4a839o0noil6v547ksjbmd8jp558bsis
"""

# SCORING:
"""
1. Scores are the sum of each subscale

2. How to handle missing values is not explicitly mentioned in the primary resources above, so
if any value is left blank or prefer not to answer, those missing values will be replaced with the average
score on that particular subscale and then added to the final subscore total (Avram).
"""

# RISK TAKING MODULE
# EXTREMELY UNLIKELY - MODERATELY UNLIKELY - SOMEWHAT UNLIKELY - NOT SURE - SOMEWHAT LIKELY - MODERATELY LIKELY - EXTREMELY LIKELY - PREFER NOT TO ANSWER
#           1                   2                   3               4             5                    6               7                     999
# RISK PERCEPTION MODULE
# NOT AT ALL RISKY - SLIGHTLY RISKY - SOMEWHAT RISKY - MODERATELY RISKY - RISKY - VERY RISKY - EXTREMELY RISKY - PREFER NOT TO ANSWER
#           1              2                3                  4            5          6            7                   999

# Subscale scores:					min= 8 max= 56
# Risktaking/Riskperception scores:	min= 40	max= 280
# ------------------------------------------------------------------------------
# Data Preparation
def dospert40_analysis(df):
	# These are the different headers and their corresponding questions
	risktaking_keys = ['dospert40_1', 'dospert40_2', 'dospert40_3', 'dospert40_4', 'dospert40_5', 'dospert40_6', 'dospert40_7',
	'dospert40_8', 'dospert40_9', 'dospert40_10', 'dospert40_11', 'dospert40_12', 'dospert40_13', 'dospert40_14',
	'dospert40_15', 'dospert40_16', 'dospert40_17', 'dospert40_18', 'dospert40_19', 'dospert40_20', 'dospert40_21', 'dospert40_22',
	'dospert40_23', 'dospert40_24','dospert40_25', 'dospert40_26', 'dospert40_27', 'dospert40_28', 'dospert40_29', 'dospert40_30', 'dospert40_31',
	'dospert40_32', 'dospert40_33', 'dospert40_34', 'dospert40_35', 'dospert40_36', 'dospert40_37', 'dospert40_38',
	'dospert40_39', 'dospert40_40']

	riskperception_keys = ['dospert40_41', 'dospert40_42', 'dospert40_43', 'dospert40_44', 'dospert40_45', 'dospert40_46', 'dospert40_47',
	'dospert40_48', 'dospert40_49', 'dospert40_50', 'dospert40_51', 'dospert40_52', 'dospert40_53', 'dospert40_54',
	'dospert40_55', 'dospert40_56', 'dospert40_57', 'dospert40_58', 'dospert40_59', 'dospert40_60', 'dospert40_61', 'dospert40_62',
	'dospert40_63', 'dospert40_64','dospert40_65', 'dospert40_66', 'dospert40_67', 'dospert40_68', 'dospert40_69', 'dospert40_70', 'dospert40_71',
	'dospert40_72', 'dospert40_73', 'dospert40_74', 'dospert40_75', 'dospert40_76', 'dospert40_77', 'dospert40_78',
	'dospert40_79', 'dospert40_80']
	
	risktaking_social_keys = ['dospert40_1','dospert40_8', 'dospert40_13', 'dospert40_16', 'dospert40_27', 'dospert40_30',  'dospert40_37',
	'dospert40_38']
	
	riskperception_social_keys=['dospert40_41','dospert40_48', 'dospert40_53', 'dospert40_56', 'dospert40_67', 'dospert40_70',  'dospert40_77',
	'dospert40_78']
	
	risktaking_financial_keys = ['dospert40_3', 'dospert40_5', 'dospert40_9', 'dospert40_15', 'dospert40_18', 'dospert40_19', 'dospert40_23',
	'dospert40_26']
	
	riskperception_financial_keys=['dospert40_43', 'dospert40_45', 'dospert40_49', 'dospert40_55', 'dospert40_58', 'dospert40_59', 'dospert40_63',
	'dospert40_66']
	
	risktaking_healthsafety_keys = ['dospert40_6', 'dospert40_20', 'dospert40_22', 'dospert40_25', 'dospert40_31', 'dospert40_34', 'dospert40_35',
	'dospert40_36']
	
	riskperception_healthsafety_keys=['dospert40_46', 'dospert40_60', 'dospert40_62', 'dospert40_65', 'dospert40_71', 'dospert40_74', 'dospert40_75',
	'dospert40_76']
	
	risktaking_recreational_keys = ['dospert40_2', 'dospert40_4', 'dospert40_12', 'dospert40_14', 'dospert40_17', 'dospert40_24', 'dospert40_32',
	'dospert40_33']
	
	riskperception_recreational_keys=['dospert40_42', 'dospert40_44', 'dospert40_52', 'dospert40_54', 'dospert40_57', 'dospert40_64', 'dospert40_72',
	'dospert40_73']
	
	risktaking_ethical_keys = ['dospert40_7', 'dospert40_10', 'dospert40_11', 'dospert40_21', 'dospert40_28', 'dospert40_29', 'dospert40_39',
	'dospert40_40']

	riskperception_ethical_keys = ['dospert40_47', 'dospert40_50', 'dospert40_51', 'dospert40_61', 'dospert40_68', 'dospert40_69', 'dospert40_79',
	'dospert40_80']
	
	dospert40_tot_keys=risktaking_keys+riskperception_keys
				   
	# Replace Qualtrics text answers with numerical values
	df[dospert40_tot_keys]= df[dospert40_tot_keys].replace(['very unlikely', 'unlikely','not sure','likely', 'very likely'], [1,2,3,4,5])
	df[dospert40_tot_keys]= df[dospert40_tot_keys].replace(['not at all risky', 'slightly risky', 'moderately risky', 'very risky', 'extremely risky'], [1,2,3,4,5])

	# Check for values that don't match parameters 
	dospert40_check=df[dospert40_tot_keys].apply(pd.to_numeric,args=('raise',))
	dospert40_check=dospert40_check[(dospert40_check !=1) & (dospert40_check !=2) & (dospert40_check !=3) & (dospert40_check !=4) & (dospert40_check !=5) & (dospert40_check !=999)].sum()
	for x in dospert40_check:
		if x!=0:
			df['dospert40_error']=np.nan
			df.dospert40_error=df.dospert40_error.replace([np.nan],["Your DOSPERT40 responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			dospert40_result=df['dospert40_error']	
		else:
			# ------------------------------------------------------------------------------
			# DOSPERT40 risktaking_social score

			# Scores and questions unanswered
			risktaking_social = df[risktaking_social_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_social_prefernotanswer = risktaking_social[risktaking_social[risktaking_social_keys] == 999].count(axis=1)
			risktaking_social_leftblank = risktaking_social.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_social_unanswered = risktaking_social_prefernotanswer + risktaking_social_leftblank

			# Total score
			risktaking_social_score = risktaking_social[risktaking_social[risktaking_social_keys] < 6].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_social_score = risktaking_social_score + (risktaking_social_unanswered * risktaking_social_score / (8-risktaking_social_unanswered))

			risktaking_socialall = pd.DataFrame({'DOSPERT40_Risktaking_social_left_blank' : risktaking_social_leftblank,'DOSPERT40_Risktaking_Social_Prefer_Not_to_Answer': risktaking_social_prefernotanswer,'DOSPERT40_Risktaking_Social_Score': risktaking_social_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_social_score:
				if (x<8 or x>56) and x!=np.nan:
					risktaking_social_score=risktaking_social_score.replace([x],["Warning: This DOSPERT40_Risktaking_Social score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT40 risktaking_financial score

			# Scores and questions unanswered
			risktaking_financial = df[risktaking_financial_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_financial_prefernotanswer = risktaking_financial[risktaking_financial[risktaking_financial_keys] == 999].count(axis=1)
			risktaking_financial_leftblank = risktaking_financial.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_financial_unanswered = risktaking_financial_prefernotanswer + risktaking_financial_leftblank

			# Total score
			risktaking_financial_score = risktaking_financial[risktaking_financial[risktaking_financial_keys] < 6].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_financial_score = risktaking_financial_score + (risktaking_financial_unanswered * risktaking_financial_score / (8-risktaking_financial_unanswered))

			risktaking_financialall = pd.DataFrame({'DOSPERT40_Risktaking_Financial_Left_Blank' : risktaking_financial_leftblank,'DOSPERT40_Risktaking_Financial_Prefer_Not_to_Answer': risktaking_financial_prefernotanswer,'DOSPERT40_Risktaking_Financial_Score': risktaking_financial_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_financial_score:
				if (x<8 or x>56) and x!=np.nan:
					risktaking_financial_score=risktaking_financial_score.replace([x],["Warning: This DOSPERT40_Risktaking_financial score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT40 risktaking_healthsafety score

			# Scores and questions unanswered
			risktaking_healthsafety = df[risktaking_healthsafety_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_healthsafety_prefernotanswer = risktaking_healthsafety[risktaking_healthsafety[risktaking_healthsafety_keys] == 999].count(axis=1)
			risktaking_healthsafety_leftblank = risktaking_healthsafety.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_healthsafety_unanswered = risktaking_healthsafety_prefernotanswer + risktaking_healthsafety_leftblank

			# Total score
			risktaking_healthsafety_score = risktaking_healthsafety[risktaking_healthsafety[risktaking_healthsafety_keys] < 6].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_healthsafety_score = risktaking_healthsafety_score + (risktaking_healthsafety_unanswered * risktaking_healthsafety_score / (8-risktaking_healthsafety_unanswered))

			risktaking_healthsafetyall = pd.DataFrame({'DOSPERT40_Risktaking_HealthSafety_Left_Blank' : risktaking_healthsafety_leftblank,'DOSPERT40_Risktaking_HealthSafety_Prefer_Not_to_Answer': risktaking_healthsafety_prefernotanswer,'DOSPERT40_Risktaking_HealthSafety_Score': risktaking_healthsafety_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_healthsafety_score:
				if (x<8 or x>56) and x!=np.nan:
					risktaking_healthsafety_score=risktaking_healthsafety_score.replace([x],["Warning: This DOSPERT40_Risktaking_healthsafety score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT40 risktaking_recreational score

			# Scores and questions unanswered
			risktaking_recreational = df[risktaking_recreational_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_recreational_prefernotanswer = risktaking_recreational[risktaking_recreational[risktaking_recreational_keys] == 999].count(axis=1)
			risktaking_recreational_leftblank = risktaking_recreational.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_recreational_unanswered = risktaking_recreational_prefernotanswer + risktaking_recreational_leftblank

			# Total score
			risktaking_recreational_score = risktaking_recreational[risktaking_recreational[risktaking_recreational_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_recreational_score = risktaking_recreational_score + (risktaking_recreational_unanswered * risktaking_recreational_score / (8-risktaking_recreational_unanswered))

			risktaking_recreationalall = pd.DataFrame({'DOSPERT40_Risktaking_Recreational_Left_Blank' : risktaking_recreational_leftblank,'DOSPERT40_Risktaking_Recreational_Prefer_Not_to_Answer': risktaking_recreational_prefernotanswer,'DOSPERT40_Risktaking_Recreational_Score': risktaking_recreational_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_recreational_score:
				if (x<8 or x>56) and x!=np.nan:
					risktaking_recreational_score=risktaking_recreational_score.replace([x],["Warning: This DOSPERT40_Risktaking_recreational score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT40 risktaking_ethical score

			# Scores and questions unanswered
			risktaking_ethical = df[risktaking_ethical_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_ethical_prefernotanswer = risktaking_ethical[risktaking_ethical[risktaking_ethical_keys] == 999].count(axis=1)
			risktaking_ethical_leftblank = risktaking_ethical.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_ethical_unanswered = risktaking_ethical_prefernotanswer + risktaking_ethical_leftblank

			# Total score
			risktaking_ethical_score = risktaking_ethical[risktaking_ethical[risktaking_ethical_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_ethical_score = risktaking_ethical_score + (risktaking_ethical_unanswered * risktaking_ethical_score / (8-risktaking_ethical_unanswered))

			risktaking_ethicalall = pd.DataFrame({'DOSPERT40_Risktaking_Ethical_Left_Blank' : risktaking_ethical_leftblank,'DOSPERT40_Risktaking_Ethical_Prefer_Not_to_Answer': risktaking_ethical_prefernotanswer,'DOSPERT40_Risktaking_Ethical_Score': risktaking_ethical_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_ethical_score:
				if (x<8 or x>56) and x!=np.nan:
					risktaking_ethical_score=risktaking_ethical_score.replace([x],["Warning: This DOSPERT40_Risktaking_ethical score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT40 riskperception_social score

			# Scores and questions unanswered
			riskperception_social = df[riskperception_social_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_social_prefernotanswer = riskperception_social[riskperception_social[riskperception_social_keys] == 999].count(axis=1)
			riskperception_social_leftblank = riskperception_social.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_social_unanswered = riskperception_social_prefernotanswer + riskperception_social_leftblank

			# Total score
			riskperception_social_score = riskperception_social[riskperception_social[riskperception_social_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_social_score = riskperception_social_score + (riskperception_social_unanswered * riskperception_social_score / (8-riskperception_social_unanswered))

			riskperception_socialall = pd.DataFrame({'DOSPERT40_Riskperception_Social_Left_Blank' : riskperception_social_leftblank,'DOSPERT40_Riskperception_Social_Prefer_Not_to_Answer': riskperception_social_prefernotanswer,'DOSPERT40_Riskperception_Social_Score': riskperception_social_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_social_score:
				if (x<8 or x>56) and x!=np.nan:
					riskperception_social_score=riskperception_social_score.replace([x],["Warning: This DOSPERT40_Riskperception_Social score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT40 riskperception_financial score

			# Scores and questions unanswered
			riskperception_financial = df[riskperception_financial_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_financial_prefernotanswer = riskperception_financial[riskperception_financial[riskperception_financial_keys] == 999].count(axis=1)
			riskperception_financial_leftblank = riskperception_financial.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_financial_unanswered = riskperception_financial_prefernotanswer + riskperception_financial_leftblank

			# Total score
			riskperception_financial_score = riskperception_financial[riskperception_financial[riskperception_financial_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_financial_score = riskperception_financial_score + (riskperception_financial_unanswered * riskperception_financial_score / (8-riskperception_financial_unanswered))

			riskperception_financialall = pd.DataFrame({'DOSPERT40_Riskperception_Financial_Left_Blank' : riskperception_financial_leftblank,'DOSPERT40_Riskperception_Financial_Prefer_Not_to_Answer': riskperception_financial_prefernotanswer,'DOSPERT40_Riskperception_Financial_Score': riskperception_financial_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_financial_score:
				if (x<8 or x>56) and x!=np.nan:
					riskperception_financial_score=riskperception_financial_score.replace([x],["Warning: This DOSPERT40_Riskperception_financial score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT40 riskperception_healthsafety score

			# Scores and questions unanswered
			riskperception_healthsafety = df[riskperception_healthsafety_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_healthsafety_prefernotanswer = riskperception_healthsafety[riskperception_healthsafety[riskperception_healthsafety_keys] == 999].count(axis=1)
			riskperception_healthsafety_leftblank = riskperception_healthsafety.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_healthsafety_unanswered = riskperception_healthsafety_prefernotanswer + riskperception_healthsafety_leftblank

			# Total score
			riskperception_healthsafety_score = riskperception_healthsafety[riskperception_healthsafety[riskperception_healthsafety_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_healthsafety_score = riskperception_healthsafety_score + (riskperception_healthsafety_unanswered * riskperception_healthsafety_score / (8-riskperception_healthsafety_unanswered))

			riskperception_healthsafetyall = pd.DataFrame({'DOSPERT40_Riskperception_HealthSafety_Left_Blank' : riskperception_healthsafety_leftblank,'DOSPERT40_Riskperception_HealthSafety_Prefer_Not_to_Answer': riskperception_healthsafety_prefernotanswer,'DOSPERT40_Riskperception_HealthSafety_Score': riskperception_healthsafety_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_healthsafety_score:
				if (x<8 or x>56) and x!=np.nan:
					riskperception_healthsafety_score=riskperception_healthsafety_score.replace([x],["Warning: This dospert40_Riskperception_healthsafety score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT40 riskperception_recreational score

			# scores and questions unanswered
			riskperception_recreational = df[riskperception_recreational_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_recreational_prefernotanswer = riskperception_recreational[riskperception_recreational[riskperception_recreational_keys] == 999].count(axis=1)
			riskperception_recreational_leftblank = riskperception_recreational.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_recreational_unanswered = riskperception_recreational_prefernotanswer + riskperception_recreational_leftblank

			# Total score
			riskperception_recreational_score = riskperception_recreational[riskperception_recreational[riskperception_recreational_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_recreational_score = riskperception_recreational_score + (riskperception_recreational_unanswered * riskperception_recreational_score / (8-riskperception_recreational_unanswered))

			riskperception_recreationalall = pd.DataFrame({'DOSPERT40_Riskperception_Recreational_Left_Blank' : riskperception_recreational_leftblank,'DOSPERT40_Riskperception_Recreational_Prefer_Not_to_Answer': riskperception_recreational_prefernotanswer,'DOSPERT40_Riskperception_Recreational_Score': riskperception_recreational_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_recreational_score:
				if (x<8 or x>56) and x!=np.nan:
					riskperception_recreational_score=riskperception_recreational_score.replace([x],["Warning: This DOSPERT40_Riskperception_recreational score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT40 riskperception_ethical score

			# Scores and questions unanswered
			riskperception_ethical = df[riskperception_ethical_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_ethical_prefernotanswer = riskperception_ethical[riskperception_ethical[riskperception_ethical_keys] == 999].count(axis=1)
			riskperception_ethical_leftblank = riskperception_ethical.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_ethical_unanswered = riskperception_ethical_prefernotanswer + riskperception_ethical_leftblank

			# Total score
			riskperception_ethical_score = riskperception_ethical[riskperception_ethical[riskperception_ethical_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_ethical_score = riskperception_ethical_score + (riskperception_ethical_unanswered * riskperception_ethical_score / (8-riskperception_ethical_unanswered))

			riskperception_ethicalall = pd.DataFrame({'DOSPERT40_Riskperception_Ethical_Left_Blank' : riskperception_ethical_leftblank,'DOSPERT40_Riskperception_Ethical_Prefer_Not_to_Answer': riskperception_ethical_prefernotanswer,'DOSPERT40_Riskperception_Ethical_Score': riskperception_ethical_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_ethical_score:
				if (x<8 or x>56) and x!=np.nan:
					riskperception_ethical_score=riskperception_ethical_score.replace([x],["Warning: This DOSPERT40_Riskperception_ethical score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT40 Risktaking total score  

			# Scores and questions unanswered
			risktaking_total_prefernotanswer = risktaking_social_prefernotanswer+risktaking_financial_prefernotanswer+risktaking_healthsafety_prefernotanswer+risktaking_recreational_prefernotanswer+risktaking_ethical_prefernotanswer
			risktaking_total_leftblank = risktaking_social_leftblank+risktaking_financial_leftblank+risktaking_healthsafety_leftblank+risktaking_recreational_leftblank+risktaking_ethical_leftblank
			risktaking_total_unanswered = risktaking_total_prefernotanswer + risktaking_total_leftblank

			# Total score
			risktaking_total_score = risktaking_social_score+risktaking_financial_score+risktaking_healthsafety_score+risktaking_recreational_score+risktaking_ethical_score

			risktakingall = pd.DataFrame({'DOSPERT40_Risktaking_Total_Left_Blank' : risktaking_total_leftblank,'DOSPERT40_Risktaking_Total_Prefer_Not_to_Answer': risktaking_total_prefernotanswer,'DOSPERT40_Risktaking_Total_Score': risktaking_total_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_total_score:
				if (x<40 or x>112) and x!=np.nan:
					risktaking_total_score=risktaking_total_score.replace([x],["Warning: This DOSPERT40_Risktaking score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT40 Riskperception total score  

			# Scores and questions unanswered
			riskperception_total_prefernotanswer = riskperception_social_prefernotanswer+riskperception_financial_prefernotanswer+riskperception_healthsafety_prefernotanswer+riskperception_recreational_prefernotanswer+riskperception_ethical_prefernotanswer
			riskperception_total_leftblank = riskperception_social_leftblank+riskperception_financial_leftblank+riskperception_healthsafety_leftblank+riskperception_recreational_leftblank+riskperception_ethical_leftblank
			riskperception_total_unanswered = riskperception_total_prefernotanswer + riskperception_total_leftblank

			# Total score
			riskperception_total_score = riskperception_social_score+riskperception_financial_score+riskperception_healthsafety_score+riskperception_recreational_score+riskperception_ethical_score

			riskperceptionall = pd.DataFrame({'DOSPERT40_Riskperception_Total_Left_Blank' : riskperception_total_leftblank,'DOSPERT40_Riskperception_Total_Prefer_Not_to_Answer': riskperception_total_prefernotanswer,'DOSPERT40_Riskperception_Total_Score': riskperception_total_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_total_score:
				if (x<40 or x>112) and x!=np.nan:
					riskperception_total_score=riskperception_total_score.replace([x],["Warning: This dospert40_Riskperception score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])


			# ------------------------------------------------------------------------------
			# Generate Output

			# Put the scores into one frame
			dospert40_frames = [df.SUBJECT_ID, risktakingall, riskperceptionall]
			dospert40_result = pd.concat(dospert40_frames, axis=1)
	return dospert40_result
	#dospert40_result.to_csv(raw_input("Save your dospert40 Output csv as: "))
