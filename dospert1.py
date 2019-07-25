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


# DOMAIN-SPECIFIC RISK-TAKING SCALE (40-item, 2003)



# RESOURCES USED:
"""GSP Scales Notebook - Holmes Lab"""
'''https://sites.google.com/a/decisionsciences.columbia.edu/cds-wiki/home/dospert/DOSPERT_40_English_2003.doc?attredirects=0'''

# SCORING:
"""
1. Scores are the sum of each subscale (Risk-Taking and Risk-Perception).
This version uses only "Social" items from the 2006 revised version (Blais & Weber, 2006).

2. Any left blank/prefer to not answer response will be replaced with the mean response from the corresponding subscale.
"""


# RISK TAKING MODULE
# EXTREMELY UNLIKELY - MODERATELY UNLIKELY - SOMEWHAT UNLIKELY - NOT SURE - SOMEWHAT LIKELY - MODERATELY LIKELY - EXTREMELY LIKELY - PREFER NOT TO ANSWER
#           1                   2                   3               4             5                    6               7                     999
# RISK PERCEPTION MODULE
# NOT AT ALL RISKY - SLIGHTLY RISKY - SOMEWHAT RISKY - MODERATELY RISKY - RISKY - VERY RISKY - EXTREMELY RISKY - PREFER NOT TO ANSWER
#           1              2                3                  4            5          6            7                   999

# Total minimum: 40
# Total maximum: 280
# Subscale minimum: 7
# Subscale maximum: 56
# ------------------------------------------------------------------------------
# Data Preparation
def dospert(40)_analysis(df):
	# These are the different headers and their corresponding questions
	risktaking_keys = ['dospert(40)_1', 'dospert(40)_2', 'dospert(40)_3', 'dospert(40)_4', 'dospert(40)_5', 'dospert(40)_6', 'dospert(40)_7',
	'dospert(40)_8', 'dospert(40)_9', 'dospert(40)_10', 'dospert(40)_11', 'dospert(40)_12', 'dospert(40)_13', 'dospert(40)_14',
	'dospert(40)_15', 'dospert(40)_16', 'dospert(40)_17', 'dospert(40)_18', 'dospert(40)_19', 'dospert(40)_20', 'dospert(40)_21', 'dospert(40)_22',
	'dospert(40)_23', 'dospert(40)_24','dospert(40)_25', 'dospert(40)_26', 'dospert(40)_27', 'dospert(40)_28', 'dospert(40)_29', 'dospert(40)_30', 'dospert(40)_31',
	'dospert(40)_32', 'dospert(40)_33', 'dospert(40)_34', 'dospert(40)_35', 'dospert(40)_36', 'dospert(40)_37', 'dospert(40)_38',
	'dospert(40)_39', 'dospert(40)_40']


	riskperception_keys = ['dospert(40)_41', 'dospert(40)_42', 'dospert(40)_43', 'dospert(40)_44', 'dospert(40)_45', 'dospert(40)_46', 'dospert(40)_47',
	'dospert(40)_48', 'dospert(40)_49', 'dospert(40)_50', 'dospert(40)_51', 'dospert(40)_52', 'dospert(40)_53', 'dospert(40)_54',
	'dospert(40)_55', 'dospert(40)_56', 'dospert(40)_57', 'dospert(40)_58', 'dospert(40)_59', 'dospert(40)_60', 'dospert(40)_61', 'dospert(40)_62',
	'dospert(40)_63', 'dospert(40)_64','dospert(40)_65', 'dospert(40)_66', 'dospert(40)_67', 'dospert(40)_68', 'dospert(40)_69', 'dospert(40)_70', 'dospert(40)_71',
	'dospert(40)_72', 'dospert(40)_73', 'dospert(40)_74', 'dospert(40)_75', 'dospert(40)_76', 'dospert(40)_77', 'dospert(40)_78',
	'dospert(40)_79', 'dospert(40)_80']
	
	risktaking_social_keys = ['dospert(40)_1','dospert(40)_8', 'dospert(40)_13', 'dospert(40)_16', 'dospert(40)_27', 'dospert(40)_30',  'dospert(40)_37',
	'dospert(40)_38']
	
	riskperception_social_keys=['dospert(40)_41','dospert(40)_48', 'dospert(40)_53', 'dospert(40)_56', 'dospert(40)_67', 'dospert(40)_70',  'dospert(40)_77',
	'dospert(40)_78']
	
	risktaking_financial_keys = ['dospert(40)_3', 'dospert(40)_5', 'dospert(40)_9', 'dospert(40)_15', 'dospert(40)_18', 'dospert(40)_19', 'dospert(40)_23',
	'dospert(40)_26']
	
	riskperception_financial_keys=['dospert(40)_43', 'dospert(40)_45', 'dospert(40)_49', 'dospert(40)_55', 'dospert(40)_58', 'dospert(40)_59', 'dospert(40)_63',
	'dospert(40)_66']
	
	risktaking_healthsafety_keys = ['dospert(40)_6', 'dospert(40)_20', 'dospert(40)_22', 'dospert(40)_25', 'dospert(40)_31', 'dospert(40)_34', 'dospert(40)_35',
	'dospert(40)_36']
	
	riskperception_healthsafety_keys=['dospert(40)_46', 'dospert(40)_60', 'dospert(40)_62', 'dospert(40)_65', 'dospert(40)_71', 'dospert(40)_74', 'dospert(40)_75',
	'dospert(40)_76']
	
	risktaking_recreational_keys = ['dospert(40)_2', 'dospert(40)_4', 'dospert(40)_12', 'dospert(40)_14', 'dospert(40)_17', 'dospert(40)_24', 'dospert(40)_32',
	'dospert(40)_33']
	
	riskperception_recreational_keys=['dospert(40)_42', 'dospert(40)_44', 'dospert(40)_52', 'dospert(40)_54', 'dospert(40)_57', 'dospert(40)_64', 'dospert(40)_72',
	'dospert(40)_73']
	
	risktaking_ethical_keys = ['dospert(40)_7', 'dospert(40)_10', 'dospert(40)_11', 'dospert(40)_21', 'dospert(40)_28', 'dospert(40)_29', 'dospert(40)_39',
	'dospert(40)_40']

	risktaking_ethical_keys = ['dospert(40)_47', 'dospert(40)_50', 'dospert(40)_51', 'dospert(40)_61', 'dospert(40)_68', 'dospert(40)_69', 'dospert(40)_79',
	'dospert(40)_80']
	
	dospert(40)_tot_keys=risktaking_keys+riskperception_keys
				   
	# Replace Qualtrics text answers with numerical values
	df[dospert(40)_tot_keys]= df[dospert(40)_tot_keys].replace(['very unlikely', 'unlikely','not sure','likely', 'very likely'], [1,2,3,4,5])
	df[dospert(40)_tot_keys]= df[dospert(40)_tot_keys].replace(['not at all risky', 'slightly risky', 'moderately risky', 'very risky', 'extremely risky'], [1,2,3,4,5])

	# Check for values that don't match parameters 
	dospert(40)_check=df[dospert(40)_tot_keys].apply(pd.to_numeric,args=('raise',))
	dospert(40)_check=dospert(40)_check[(dospert(40)_check !=1) & (dospert(40)_check !=2) & (dospert(40)_check !=3) & (dospert(40)_check !=4) & (dospert(40)_check !=5) & (dospert(40)_check !=999)].sum()
	for x in dospert(40)_check:
		if x!=0:
			df['dospert(40)_error']=np.nan
			df.dospert(40)_error=df.dospert(40)_error.replace([np.nan],["Your DOSPERT(40) responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			dospert(40)_result=df['dospert(40)_error']	
		else:
			# ------------------------------------------------------------------------------
			# DOSPERT(40) risktaking_social score

			# SCORES AND QUESTIONS UNANSWERED
			risktaking_social = df[risktaking_social_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_social_prefernotanswer = risktaking_social[risktaking_social[risktaking_social_keys] == 999].count(axis=1)
			risktaking_social_leftblank = risktaking_social.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_social_unanswered = risktaking_social_prefernotanswer + risktaking_social_leftblank

			# Total SCORE
			risktaking_social_score = risktaking_social[risktaking_social[risktaking_social_keys] < 6].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_social_score = risktaking_social_score + (risktaking_social_unanswered * risktaking_social_score / (8-risktaking_social_unanswered))

			risktaking_socialall = pd.DataFrame({'DOSPERT(40)_Risktaking_social_left_blank' : risktaking_social_leftblank,'DOSPERT(40)_Risktaking_Social_Prefer_Not_to_Answer': risktaking_social_prefernotanswer,'DOSPERT(40)_Risktaking_Social_Score': risktaking_social_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_social_score:
				if (x<7 or x>56) and x!=np.nan:
					risktaking_social_score=risktaking_social_score.replace([x],["Warning: This DOSPERT(40)_Risktaking_Social score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT(40) risktaking_financial score

			# SCORES AND QUESTIONS UNANSWERED
			risktaking_financial = df[risktaking_financial_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_financial_prefernotanswer = risktaking_financial[risktaking_financial[risktaking_financial_keys] == 999].count(axis=1)
			risktaking_financial_leftblank = risktaking_financial.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_financial_unanswered = risktaking_financial_prefernotanswer + risktaking_financial_leftblank

			# Total SCORE
			risktaking_financial_score = risktaking_financial[risktaking_financial[risktaking_financial_keys] < 6].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_financial_score = risktaking_financial_score + (risktaking_financial_unanswered * risktaking_financial_score / (8-risktaking_financial_unanswered))

			risktaking_financialall = pd.DataFrame({'DOSPERT(40)_Risktaking_Financial_Left_Blank' : risktaking_financial_leftblank,'DOSPERT(40)_Risktaking_Financial_Prefer_Not_to_Answer': risktaking_financial_prefernotanswer,'DOSPERT(40)_Risktaking_Financial_Score': risktaking_financial_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_financial_score:
				if (x<7 or x>56) and x!=np.nan:
					risktaking_financial_score=risktaking_financial_score.replace([x],["Warning: This DOSPERT(40)_Risktaking_financial score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT(40) risktaking_healthsafety score

			# SCORES AND QUESTIONS UNANSWERED
			risktaking_healthsafety = df[risktaking_healthsafety_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_healthsafety_prefernotanswer = risktaking_healthsafety[risktaking_healthsafety[risktaking_healthsafety_keys] == 999].count(axis=1)
			risktaking_healthsafety_leftblank = risktaking_healthsafety.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_healthsafety_unanswered = risktaking_healthsafety_prefernotanswer + risktaking_healthsafety_leftblank

			# Total SCORE
			risktaking_healthsafety_score = risktaking_healthsafety[risktaking_healthsafety[risktaking_healthsafety_keys] < 6].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_healthsafety_score = risktaking_healthsafety_score + (risktaking_healthsafety_unanswered * risktaking_healthsafety_score / (8-risktaking_healthsafety_unanswered))

			risktaking_healthsafetyall = pd.DataFrame({'DOSPERT(40)_Risktaking_HealthSafety_Left_Blank' : risktaking_healthsafety_leftblank,'DOSPERT(40)_Risktaking_HealthSafety_Prefer_Not_to_Answer': risktaking_healthsafety_prefernotanswer,'DOSPERT(40)_Risktaking_HealthSafety_Score': risktaking_healthsafety_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_healthsafety_score:
				if (x<7 or x>56) and x!=np.nan:
					risktaking_healthsafety_score=risktaking_healthsafety_score.replace([x],["Warning: This DOSPERT(40)_Risktaking_healthsafety score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT(40) risktaking_recreational score

			# SCORES AND QUESTIONS UNANSWERED
			risktaking_recreational = df[risktaking_recreational_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_recreational_prefernotanswer = risktaking_recreational[risktaking_recreational[risktaking_recreational_keys] == 999].count(axis=1)
			risktaking_recreational_leftblank = risktaking_recreational.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_recreational_unanswered = risktaking_recreational_prefernotanswer + risktaking_recreational_leftblank

			# Total SCORE
			risktaking_recreational_score = risktaking_recreational[risktaking_recreational[risktaking_recreational_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_recreational_score = risktaking_recreational_score + (risktaking_recreational_unanswered * risktaking_recreational_score / (8-risktaking_recreational_unanswered))

			risktaking_recreationalall = pd.DataFrame({'DOSPERT(40)_Risktaking_Recreational_Left_Blank' : risktaking_recreational_leftblank,'DOSPERT(40)_Risktaking_Recreational_Prefer_Not_to_Answer': risktaking_recreational_prefernotanswer,'DOSPERT(40)_Risktaking_Recreational_Score': risktaking_recreational_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_recreational_score:
				if (x<7 or x>56) and x!=np.nan:
					risktaking_recreational_score=risktaking_recreational_score.replace([x],["Warning: This DOSPERT(40)_Risktaking_recreational score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT(40) risktaking_ethical score

			# SCORES AND QUESTIONS UNANSWERED
			risktaking_ethical = df[risktaking_ethical_keys].apply(pd.to_numeric, args=('coerce',))
			risktaking_ethical_prefernotanswer = risktaking_ethical[risktaking_ethical[risktaking_ethical_keys] == 999].count(axis=1)
			risktaking_ethical_leftblank = risktaking_ethical.apply(lambda x: sum(x.isnull().values), axis=1)
			risktaking_ethical_unanswered = risktaking_ethical_prefernotanswer + risktaking_ethical_leftblank

			# Total SCORE
			risktaking_ethical_score = risktaking_ethical[risktaking_ethical[risktaking_ethical_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			risktaking_ethical_score = risktaking_ethical_score + (risktaking_ethical_unanswered * risktaking_ethical_score / (8-risktaking_ethical_unanswered))

			risktaking_ethicalall = pd.DataFrame({'DOSPERT(40)_Risktaking_Ethical_Left_Blank' : risktaking_ethical_leftblank,'DOSPERT(40)_Risktaking_Ethical_Prefer_Not_to_Answer': risktaking_ethical_prefernotanswer,'DOSPERT(40)_Risktaking_Ethical_Score': risktaking_ethical_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_ethical_score:
				if (x<7 or x>56) and x!=np.nan:
					risktaking_ethical_score=risktaking_ethical_score.replace([x],["Warning: This DOSPERT(40)_Risktaking_ethical score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT(40) riskperception_social score

			# SCORES AND QUESTIONS UNANSWERED
			riskperception_social = df[riskperception_social_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_social_prefernotanswer = riskperception_social[riskperception_social[riskperception_social_keys] == 999].count(axis=1)
			riskperception_social_leftblank = riskperception_social.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_social_unanswered = riskperception_social_prefernotanswer + riskperception_social_leftblank

			# Total SCORE
			riskperception_social_score = riskperception_social[riskperception_social[riskperception_social_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_social_score = riskperception_social_score + (riskperception_social_unanswered * riskperception_social_score / (8-riskperception_social_unanswered))

			riskperception_socialall = pd.DataFrame({'DOSPERT(40)_Riskperception_Social_Left_Blank' : riskperception_social_leftblank,'DOSPERT(40)_Riskperception_Social_Prefer_Not_to_Answer': riskperception_social_prefernotanswer,'DOSPERT(40)_Riskperception_Social_Score': riskperception_social_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_social_score:
				if (x<7 or x>56) and x!=np.nan:
					riskperception_social_score=riskperception_social_score.replace([x],["Warning: This DOSPERT(40)_Riskperception_Social score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT(40) riskperception_financial score

			# SCORES AND QUESTIONS UNANSWERED
			riskperception_financial = df[riskperception_financial_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_financial_prefernotanswer = riskperception_financial[riskperception_financial[riskperception_financial_keys] == 999].count(axis=1)
			riskperception_financial_leftblank = riskperception_financial.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_financial_unanswered = riskperception_financial_prefernotanswer + riskperception_financial_leftblank

			# Total SCORE
			riskperception_financial_score = riskperception_financial[riskperception_financial[riskperception_financial_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_financial_score = riskperception_financial_score + (riskperception_financial_unanswered * riskperception_financial_score / (8-riskperception_financial_unanswered))

			riskperception_financialall = pd.DataFrame({'DOSPERT(40)_Riskperception_Financial_Left_Blank' : riskperception_financial_leftblank,'DOSPERT(40)_Riskperception_Financial_Prefer_Not_to_Answer': riskperception_financial_prefernotanswer,'DOSPERT(40)_Riskperception_Financial_Score': riskperception_financial_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_financial_score:
				if (x<7 or x>56) and x!=np.nan:
					riskperception_financial_score=riskperception_financial_score.replace([x],["Warning: This DOSPERT(40)_Riskperception_financial score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT(40) riskperception_healthsafety score

			# SCORES AND QUESTIONS UNANSWERED
			riskperception_healthsafety = df[riskperception_healthsafety_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_healthsafety_prefernotanswer = riskperception_healthsafety[riskperception_healthsafety[riskperception_healthsafety_keys] == 999].count(axis=1)
			riskperception_healthsafety_leftblank = riskperception_healthsafety.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_healthsafety_unanswered = riskperception_healthsafety_prefernotanswer + riskperception_healthsafety_leftblank

			# Total SCORE
			riskperception_healthsafety_score = riskperception_healthsafety[riskperception_healthsafety[riskperception_healthsafety_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_healthsafety_score = riskperception_healthsafety_score + (riskperception_healthsafety_unanswered * riskperception_healthsafety_score / (8-riskperception_healthsafety_unanswered))

			riskperception_healthsafetyall = pd.DataFrame({'DOSPERT(40)_Riskperception_HealthSafety_Left_Blank' : riskperception_healthsafety_leftblank,'DOSPERT(40)_Riskperception_HealthSafety_Prefer_Not_to_Answer': riskperception_healthsafety_prefernotanswer,'DOSPERT(40)_Riskperception_HealthSafety_Score': riskperception_healthsafety_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_healthsafety_score:
				if (x<7 or x>56) and x!=np.nan:
					riskperception_healthsafety_score=riskperception_healthsafety_score.replace([x],["Warning: This DOSPERT(40)_Riskperception_healthsafety score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT(40) riskperception_recreational score

			# SCORES AND QUESTIONS UNANSWERED
			riskperception_recreational = df[riskperception_recreational_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_recreational_prefernotanswer = riskperception_recreational[riskperception_recreational[riskperception_recreational_keys] == 999].count(axis=1)
			riskperception_recreational_leftblank = riskperception_recreational.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_recreational_unanswered = riskperception_recreational_prefernotanswer + riskperception_recreational_leftblank

			# Total SCORE
			riskperception_recreational_score = riskperception_recreational[riskperception_recreational[riskperception_recreational_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_recreational_score = riskperception_recreational_score + (riskperception_recreational_unanswered * riskperception_recreational_score / (8-riskperception_recreational_unanswered))

			riskperception_recreationalall = pd.DataFrame({'DOSPERT(40)_Riskperception_Recreational_Left_Blank' : riskperception_recreational_leftblank,'DOSPERT(40)_Riskperception_Recreational_Prefer_Not_to_Answer': riskperception_recreational_prefernotanswer,'DOSPERT(40)_Riskperception_Recreational_Score': riskperception_recreational_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_recreational_score:
				if (x<7 or x>56) and x!=np.nan:
					riskperception_recreational_score=riskperception_recreational_score.replace([x],["Warning: This DOSPERT(40)_Riskperception_recreational score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT(40) riskperception_ethical score

			# SCORES AND QUESTIONS UNANSWERED
			riskperception_ethical = df[riskperception_ethical_keys].apply(pd.to_numeric, args=('coerce',))
			riskperception_ethical_prefernotanswer = riskperception_ethical[riskperception_ethical[riskperception_ethical_keys] == 999].count(axis=1)
			riskperception_ethical_leftblank = riskperception_ethical.apply(lambda x: sum(x.isnull().values), axis=1)
			riskperception_ethical_unanswered = riskperception_ethical_prefernotanswer + riskperception_ethical_leftblank

			# Total SCORE
			riskperception_ethical_score = riskperception_ethical[riskperception_ethical[riskperception_ethical_keys] <=7].sum(axis=1)

			# Recalculate score with imputation 
			riskperception_ethical_score = riskperception_ethical_score + (riskperception_ethical_unanswered * riskperception_ethical_score / (8-riskperception_ethical_unanswered))

			riskperception_ethicalall = pd.DataFrame({'DOSPERT(40)_Riskperception_Ethical_Left_Blank' : riskperception_ethical_leftblank,'DOSPERT(40)_Riskperception_Ethical_Prefer_Not_to_Answer': riskperception_ethical_prefernotanswer,'DOSPERT(40)_Riskperception_Ethical_Score': riskperception_ethical_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_ethical_score:
				if (x<7 or x>56) and x!=np.nan:
					riskperception_ethical_score=riskperception_ethical_score.replace([x],["Warning: This DOSPERT(40)_Riskperception_ethical score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
					
			# ------------------------------------------------------------------------------
			# DOSPERT(40) Risktaking total score  

			# SCORES AND QUESTIONS UNANSWERED
			risktaking_total_prefernotanswer = risktaking_social_prefernotanswer+risktaking_financial_prefernotanswer+risktaking_healthsafety_prefernotanswer+risktaking_recreational_prefernotanswer+risktaking_ethical_prefernotanswer
			risktaking_total_leftblank = risktaking_social_leftblank+risktaking_financial_leftblank+risktaking_healthsafety_leftblank+risktaking_recreational_leftblank+risktaking_ethical_leftblank
			risktaking_total_unanswered = risktaking_total_prefernotanswer + risktaking_total_leftblank

			# Total SCORE
			risktaking_total_score = risktaking_social_score+risktaking_financial_score+risktaking_healthsafety_score+risktaking_recreational_score+risktaking_ethical_score

			risktakingall = pd.DataFrame({'DOSPERT(40)_Risktaking_Total_Left_Blank' : risktaking_total_leftblank,'DOSPERT40)_Risktaking_Total_Prefer_Not_to_Answer': risktaking_total_prefernotanswer,'DOSPERT(40)_Risktaking_Total_Score': risktaking_total_score})

			# Check for scores that are outside acceptable values 
			for x in risktaking_score:
				if (x<40 or x>112) and x!=np.nan:
					risktaking_score=risktaking_score.replace([x],["Warning: This DOSPERT(40)_Risktaking score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])
			
			# ------------------------------------------------------------------------------
			# DOSPERT(40) Riskperception total score  

			# SCORES AND QUESTIONS UNANSWERED
			riskperception_total_prefernotanswer = riskperception_social_prefernotanswer+riskperception_financial_prefernotanswer+riskperception_healthsafety_prefernotanswer+riskperception_recreational_prefernotanswer+riskperception_ethical_prefernotanswer
			riskperception_total_leftblank = riskperception_social_leftblank+riskperception_financial_leftblank+riskperception_healthsafety_leftblank+riskperception_recreational_leftblank+riskperception_ethical_leftblank
			riskperception_total_unanswered = riskperception_total_prefernotanswer + riskperception_total_leftblank

			# Total SCORE
			riskperception_total_score = riskperception_social_score+riskperception_financial_score+riskperception_healthsafety_score+riskperception_recreational_score+riskperception_ethical_score

			riskperceptionall = pd.DataFrame({'DOSPERT(40)_Riskperception_Total_Left_Blank' : riskperception_total_leftblank,'DOSPERT40)_Riskperception_Total_Prefer_Not_to_Answer': riskperception_total_prefernotanswer,'DOSPERT(40)_Riskperception_Total_Score': riskperception_total_score})

			# Check for scores that are outside acceptable values 
			for x in riskperception_score:
				if (x<40 or x>112) and x!=np.nan:
					riskperception_score=riskperception_score.replace([x],["Warning: This DOSPERT(40)_Riskperception score (%d) falls outside of the accepted range (16 to 112). Please check your data and try again."  % x])


			# ------------------------------------------------------------------------------
			#Generate Output

			# Put the scores into one frame
			dospert(40)_frames = [df.SUBJECT_ID, risktakingall, riskperceptionall]
			dospert(40)_result = pd.concat(dospert(40)_frames, axis=1)
	return dospert(40)_result
	#dospert(40)_result.to_csv(raw_input("Save your dospert(40) Output csv as: "))
