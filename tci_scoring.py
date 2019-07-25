#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files
@author: David Gruskin
@email: david.gruskin@yale.edu
@version: 2.0
@date: 2017.08.04
"""
import pandas as pd
import numpy as np
import sys 

# TEMPERAMENT AND CHARACTER INVENTORY - REVISED - 140 

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/bmvezlg0v0jsuo2l3qemnjfr9kne4blb
Scoring: https://yale.box.com/s/bmvezlg0v0jsuo2l3qemnjfr9kne4blb
"""

# SCORING:
"""
1. Subscores range from 20-100 and are computed by summing the responses to relevant questions.
2. Prefer not to answer or blank responses will be replaced with the mean response from the relevant subscore. 
"""

# DEFINITELY FALSE - MOSTLY OR PROBABLY FALSE - NEITHER TRUE NOR FALSE, OR ABOUT EQUALLY TRUE OR FALSE
#        1                    2                                         3
#
# MOSTLY OR PROBABLY TRUE - DEFINITELY TRUE - prefer not to answer
#         4                     5                   999

# Subscale scores:	min= 20	  max= 100
# ------------------------------------------------------------------------------

def tci_analysis(df):
	tci_novelty_keys = ['tci_1', 'tci_10', 'tci_24', 'tci_44', 'tci_51', 'tci_59', 'tci_71', 'tci_102', 'tci_104', 'tci_109', 'tci_122', 'tci_135']
	tci_novelty_rev_keys = ['tci_14', 'tci_47', 'tci_53', 'tci_63', 'tci_77', 'tci_105', 'tci_123', 'tci_139']

	tci_harmavoidance_keys = ['tci_9', 'tci_16', 'tci_19', 'tci_30', 'tci_46', 'tci_70', 'tci_82', 'tci_113', 'tci_136']
	tci_harmavoidance_rev_keys = ['tci_2', 'tci_38', 'tci_61', 'tci_64', 'tci_78', 'tci_81', 'tci_86', 'tci_98', 'tci_103', 'tci_121', 'tci_131']

	tci_rewarddependence_keys = ['tci_15', 'tci_20', 'tci_31', 'tci_54', 'tci_80', 'tci_97', 'tci_116', 'tci_125', 'tci_130']
	tci_rewarddependence_rev_keys = ['tci_11', 'tci_26', 'tci_39', 'tci_65', 'tci_79', 'tci_85', 'tci_92', 'tci_96', 'tci_110', 'tci_127', 'tci_138']

	tci_persistence_keys = ['tci_5', 'tci_8', 'tci_22', 'tci_37', 'tci_45', 'tci_55', 'tci_60', 'tci_62', 'tci_72','tci_76', 'tci_94', 'tci_111', 'tci_114', 'tci_117', 'tci_119', 'tci_126', 'tci_137']
	tci_persistence_rev_keys = ['tci_129', 'tci_134', 'tci_140']

	tci_selfdirectedness_keys = ['tci_35', 'tci_57']
	tci_selfdirectedness_rev_keys = ['tci_3', 'tci_6', 'tci_17', 'tci_21', 'tci_23', 'tci_34', 'tci_48', 'tci_49', 'tci_58', 'tci_66', 'tci_69', 'tci_83', 'tci_87', 'tci_90', 'tci_100', 'tci_107', 'tci_108', 'tci_115']

	tci_cooperativeness_keys = ['tci_4', 'tci_7', 'tci_40', 'tci_41', 'tci_50', 'tci_74', 'tci_89']
	tci_cooperativeness_rev_keys = ['tci_13', 'tci_18', 'tci_27', 'tci_28', 'tci_33', 'tci_67', 'tci_75', 'tci_84', 'tci_88', 'tci_93', 'tci_124', 'tci_128', 'tci_133']

	tci_selftranscendence_keys = ['tci_12', 'tci_25', 'tci_29', 'tci_42', 'tci_43', 'tci_52', 'tci_56', 'tci_68', 'tci_73', 'tci_91', 'tci_95', 'tci_99', 'tci_106', 'tci_112', 'tci_118']
	tci_selftranscendence_rev_keys = ['tci_32']

	#validitychecks = ['tci_36', 'tci_101', 'tci_120', 'tci_132']
	validitychecks = ['tci_132']

	tci_tot_keys= validitychecks + tci_selftranscendence_rev_keys + tci_selftranscendence_keys + tci_novelty_keys + tci_novelty_rev_keys + tci_harmavoidance_keys + tci_harmavoidance_rev_keys + tci_rewarddependence_keys + tci_rewarddependence_rev_keys + tci_persistence_keys + tci_persistence_rev_keys + tci_selfdirectedness_keys + tci_selfdirectedness_rev_keys + tci_cooperativeness_keys + tci_cooperativeness_rev_keys

	# Replace values from Qualtrics with integers for scoring 
	df[tci_tot_keys]=df[tci_tot_keys].replace(['definitely false', 'mostly or probably false', 'neither true nor false, or about equally true or false', 'mostly or probably true', 'definitely true','prefer not to answer'], [1,2,3,4,5,999])
	tci_check=df[tci_tot_keys].apply(pd.to_numeric,args=('raise',))

	# Count number of validity checks failed 
	df['TCI_Validity_Checks_Failed']=0
	#mask= (df.tci_36!=4) 
	#df.loc[mask, 'TCI_Validity_Checks_Failed'] +=1 
	#mask= (df.tci_101!=1) 
	#df.loc[mask, 'TCI_Validity_Checks_Failed'] +=1
	#mask= (df.tci_120!=4) 
	#df.loc[mask, 'TCI_Validity_Checks_Failed'] +=1
	mask= (df.tci_132!=2) 
	df.loc[mask, 'TCI_Validity_Checks_Failed'] +=1

	# Check for values outside of parameter ranges 
	tci_check=df[tci_tot_keys].apply(pd.to_numeric,args=('raise',))
	tci_check=tci_check[(tci_check !=1) & (tci_check !=2) & (tci_check !=3) & (tci_check !=4) & (tci_check !=5) & (tci_check !=999)].sum()
	for x in tci_check:
		if x!=0:
			df['tci_error']=np.nan
			df.tci_error=df.tci_error.replace([np.nan],["Your TCI responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			tci_result=df['tci_error']
		else:
			# ------------------------------------------------------------------------------
			# TCI Novelty Seeking score
		
			# Change the numbers in forward tci Novelty headers to numeric floats
			tci_novelty_forward = df[tci_novelty_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			tci_novelty_forward_leftblank = tci_novelty_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_novelty_forward_prefernotanswer = tci_novelty_forward[tci_novelty_forward[tci_novelty_keys] == 999].count(axis=1)
			tci_novelty_forward_unanswered = tci_novelty_forward_leftblank + tci_novelty_forward_prefernotanswer
		
			# Sum all the forward scores
			tci_novelty_forward_score = tci_novelty_forward[tci_novelty_forward[tci_novelty_keys] < 6].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			tci_novelty_rev =df[tci_novelty_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			tci_novelty_reverse_leftblank = tci_novelty_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_novelty_reverse_prefernotanswer = tci_novelty_rev[tci_novelty_rev[tci_novelty_rev_keys] == 999].count(axis=1)
			tci_novelty_reverse_unanswered = tci_novelty_reverse_leftblank + tci_novelty_reverse_prefernotanswer
		
			# Sum all the reverse scores
			tci_novelty_reverse_score = tci_novelty_rev.rsub(6)[tci_novelty_rev[tci_novelty_rev_keys] < 6].sum(axis=1)
		
			# Total TCI Novelty score
			total_tci_novelty_score = tci_novelty_forward_score + tci_novelty_reverse_score
			total_tci_novelty_score=total_tci_Novelty_score.replace([0],[np.nan])
		
			# Total TCI Novelty answers unanswered
			total_tci_novelty_unanswered = tci_novelty_forward_unanswered + tci_novelty_reverse_unanswered
		
			# Total answers left blank
			total_tci_novelty_leftblank = tci_novelty_forward_leftblank + tci_novelty_reverse_leftblank
		
			# Total answers prefer not to answer
			total_tci_novelty_prefernotanswer = tci_novelty_forward_prefernotanswer + tci_novelty_reverse_prefernotanswer
			
			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			total_tci_novelty_score = total_tci_novelty_score + (total_tci_novelty_unanswered * total_tci_novelty_score / (20-total_tci_novelty_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_tci_novelty_score:
				if (x<20 or x>100) and x!=np.nan:
					total_tci_novelty_score=total_tci_novelty_score.replace([x],["Warning: This TCI_Novelty score (%d) falls outside of the accepted range (20 to 100). Please check your data and try again."  % x])
		
		
			tcinoveltyall = pd.DataFrame({'TCI_Novelty_Seeking_Left_Blank': total_tci_novelty_leftblank,'TCI_Novelty_Seeking_Prefer_Not_to_Answer': total_tci_novelty_prefernotanswer,'TCI_Novelty_Seeking_Score': total_tci_Novelty_score,})
			# ------------------------------------------------------------------------------
			# TCI Harm Avoidance score
		
			# Change the numbers in forward tci harmavoidance headers to numeric floats
			tci_harmavoidance_forward = df[tci_harmavoidance_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			tci_harmavoidance_forward_leftblank = tci_harmavoidance_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_harmavoidance_forward_prefernotanswer = tci_harmavoidance_forward[tci_harmavoidance_forward[tci_harmavoidance_keys] == 999].count(axis=1)
			tci_harmavoidance_forward_unanswered = tci_harmavoidance_forward_leftblank + tci_harmavoidance_forward_prefernotanswer
		
			# Sum all the forward scores
			tci_harmavoidance_forward_score = tci_harmavoidance_forward[tci_harmavoidance_forward[tci_harmavoidance_keys] < 6].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			tci_harmavoidance_rev =df[tci_harmavoidance_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			tci_harmavoidance_reverse_leftblank = tci_harmavoidance_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_harmavoidance_reverse_prefernotanswer = tci_harmavoidance_rev[tci_harmavoidance_rev[tci_harmavoidance_rev_keys] == 999].count(axis=1)
			tci_harmavoidance_reverse_unanswered = tci_harmavoidance_reverse_leftblank + tci_harmavoidance_reverse_prefernotanswer
		
			# Sum all the reverse scores
			tci_harmavoidance_reverse_score = tci_harmavoidance_rev.rsub(6)[tci_harmavoidance_rev[tci_harmavoidance_rev_keys] < 6].sum(axis=1)
		
			# Total TCI harmavoidance score
			total_tci_harmavoidance_score = tci_harmavoidance_forward_score + tci_harmavoidance_reverse_score
			total_tci_harmavoidance_score=total_tci_harmavoidance_score.replace([0],[np.nan])
		
			# Total TCI harmavoidance answers unanswered
			total_tci_harmavoidance_unanswered = tci_harmavoidance_forward_unanswered + tci_harmavoidance_reverse_unanswered
		
			# Total answers left blank
			total_tci_harmavoidance_leftblank = tci_harmavoidance_forward_leftblank + tci_harmavoidance_reverse_leftblank
		
			# Total answers prefer not to answer
			total_tci_harmavoidance_prefernotanswer = tci_harmavoidance_forward_prefernotanswer + tci_harmavoidance_reverse_prefernotanswer
			
			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			total_tci_harmavoidance_score = total_tci_harmavoidance_score + (total_tci_harmavoidance_unanswered * total_tci_harmavoidance_score / (20-total_tci_harmavoidance_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_tci_harmavoidance_score:
				if (x<20 or x>100) and x!=np.nan:
					total_tci_harmavoidance_score=total_tci_harmavoidance_score.replace([x],["Warning: This TCI_Harm_Avoidance score (%d) falls outside of the accepted range (20 to 100). Please check your data and try again."  % x])
		
			tciharmavoidanceall = pd.DataFrame({'TCI_Harm_Avoidance_Left_Blank': total_tci_harmavoidance_leftblank,'TCI_Harm_Avoidance_Prefer_Not_to_Answer': total_tci_harmavoidance_prefernotanswer,'TCI_Harm_Avoidance_Score': total_tci_harmavoidance_score,})
			# ------------------------------------------------------------------------------
			# TCI reward dependence score
		
			# Change the numbers in forward tci rewarddependence headers to numeric floats
			tci_rewarddependence_forward = df[tci_rewarddependence_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			tci_rewarddependence_forward_leftblank = tci_rewarddependence_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_rewarddependence_forward_prefernotanswer = tci_rewarddependence_forward[tci_rewarddependence_forward[tci_rewarddependence_keys] == 999].count(axis=1)
			tci_rewarddependence_forward_unanswered = tci_rewarddependence_forward_leftblank + tci_rewarddependence_forward_prefernotanswer
		
			# Sum all the forward scores
			tci_rewarddependence_forward_score = tci_rewarddependence_forward[tci_rewarddependence_forward[tci_rewarddependence_keys] < 6].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			tci_rewarddependence_rev =df[tci_rewarddependence_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			tci_rewarddependence_reverse_leftblank = tci_rewarddependence_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_rewarddependence_reverse_prefernotanswer = tci_rewarddependence_rev[tci_rewarddependence_rev[tci_rewarddependence_rev_keys] == 999].count(axis=1)
			tci_rewarddependence_reverse_unanswered = tci_rewarddependence_reverse_leftblank + tci_rewarddependence_reverse_prefernotanswer
		
			# Sum all the reverse scores
			tci_rewarddependence_reverse_score = tci_rewarddependence_rev.rsub(6)[tci_rewarddependence_rev[tci_rewarddependence_rev_keys] < 6].sum(axis=1)
		
			# Total TCI rewarddependence score
			total_tci_rewarddependence_score = tci_rewarddependence_forward_score + tci_rewarddependence_reverse_score
			total_tci_rewarddependence_score=total_tci_rewarddependence_score.replace([0],[np.nan])
		
			# Total TCI rewarddependence answers unanswered
			total_tci_rewarddependence_unanswered = tci_rewarddependence_forward_unanswered + tci_rewarddependence_reverse_unanswered
		
			# Total answers left blank
			total_tci_rewarddependence_leftblank = tci_rewarddependence_forward_leftblank + tci_rewarddependence_reverse_leftblank
		
			# Total answers prefer not to answer
			total_tci_rewarddependence_prefernotanswer = tci_rewarddependence_forward_prefernotanswer + tci_rewarddependence_reverse_prefernotanswer
			
			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			total_tci_rewarddependence_score = total_tci_rewarddependence_score + (total_tci_rewarddependence_unanswered * total_tci_rewarddependence_score / (20-total_tci_rewarddependence_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_tci_rewarddependence_score:
				if (x<20 or x>100) and x!=np.nan:
					total_tci_rewarddependence_score=total_tci_rewarddependence_score.replace([x],["Warning: This TCI_Reward_Dependence score (%d) falls outside of the accepted range (20 to 100). Please check your data and try again."  % x])
		
		
			tcirewarddependenceall = pd.DataFrame({'TCI_Reward_Dependence_Left_Blank': total_tci_rewarddependence_leftblank,'TCI_Reward_Dependence_Prefer_Not_to_Answer': total_tci_rewarddependence_prefernotanswer,'TCI_Reward_Dependence_Score': total_tci_rewarddependence_score,})
			# ------------------------------------------------------------------------------
		
			# TCI persistence score
		
			# Change the numbers in forward tci persistence headers to numeric floats
			tci_persistence_forward = df[tci_persistence_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			tci_persistence_forward_leftblank = tci_persistence_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_persistence_forward_prefernotanswer = tci_persistence_forward[tci_persistence_forward[tci_persistence_keys] == 999].count(axis=1)
			tci_persistence_forward_unanswered = tci_persistence_forward_leftblank + tci_persistence_forward_prefernotanswer
		
			# Sum all the forward scores
			tci_persistence_forward_score = tci_persistence_forward[tci_persistence_forward[tci_persistence_keys] < 6].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			tci_persistence_rev =df[tci_persistence_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			tci_persistence_reverse_leftblank = tci_persistence_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_persistence_reverse_prefernotanswer = tci_persistence_rev[tci_persistence_rev[tci_persistence_rev_keys] == 999].count(axis=1)
			tci_persistence_reverse_unanswered = tci_persistence_reverse_leftblank + tci_persistence_reverse_prefernotanswer
		
			# Sum all the reverse scores
			tci_persistence_reverse_score = tci_persistence_rev.rsub(6)[tci_persistence_rev[tci_persistence_rev_keys] < 6].sum(axis=1)
		
			# Total TCI persistence score
			total_tci_persistence_score = tci_persistence_forward_score + tci_persistence_reverse_score
			total_tci_persistence_score=total_tci_persistence_score.replace([0],[np.nan])
		
			# Total TCI persistence answers unanswered
			total_tci_persistence_unanswered = tci_persistence_forward_unanswered + tci_persistence_reverse_unanswered
		
			# Total answers left blank
			total_tci_persistence_leftblank = tci_persistence_forward_leftblank + tci_persistence_reverse_leftblank
		
			# Total answers prefer not to answer
			total_tci_persistence_prefernotanswer = tci_persistence_forward_prefernotanswer + tci_persistence_reverse_prefernotanswer
			
			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			total_tci_persistence_score = total_tci_persistence_score + (total_tci_persistence_unanswered * total_tci_persistence_score / (20-total_tci_persistence_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_tci_persistence_score:
				if (x<20 or x>100) and x!=np.nan:
					total_tci_persistence_score=total_tci_persistence_score.replace([x],["Warning: This TCI_Persistence score (%d) falls outside of the accepted range (20 to 100). Please check your data and try again."  % x])
		
		
			tcipersistenceall = pd.DataFrame({'TCI_Persistence_Left_Blank': total_tci_persistence_leftblank,'TCI_Persistence_Prefer_Not_to_Answer': total_tci_persistence_prefernotanswer,'TCI_Persistence_Score': total_tci_persistence_score,})
		
			# ------------------------------------------------------------------------------
		
			# TCI selfdirectedness score
		
			# Change the numbers in forward tci selfdirectedness headers to numeric floats
			tci_selfdirectedness_forward = df[tci_selfdirectedness_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			tci_selfdirectedness_forward_leftblank = tci_selfdirectedness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_selfdirectedness_forward_prefernotanswer = tci_selfdirectedness_forward[tci_selfdirectedness_forward[tci_selfdirectedness_keys] == 999].count(axis=1)
			tci_selfdirectedness_forward_unanswered = tci_selfdirectedness_forward_leftblank + tci_selfdirectedness_forward_prefernotanswer
		
			# Sum all the forward scores
			tci_selfdirectedness_forward_score = tci_selfdirectedness_forward[tci_selfdirectedness_forward[tci_selfdirectedness_keys] < 6].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			tci_selfdirectedness_rev =df[tci_selfdirectedness_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			tci_selfdirectedness_reverse_leftblank = tci_selfdirectedness_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_selfdirectedness_reverse_prefernotanswer = tci_selfdirectedness_rev[tci_selfdirectedness_rev[tci_selfdirectedness_rev_keys] == 999].count(axis=1)
			tci_selfdirectedness_reverse_unanswered = tci_selfdirectedness_reverse_leftblank + tci_selfdirectedness_reverse_prefernotanswer
		
			# Sum all the reverse scores
			tci_selfdirectedness_reverse_score = tci_selfdirectedness_rev.rsub(6)[tci_selfdirectedness_rev[tci_selfdirectedness_rev_keys] < 6].sum(axis=1)
		
			# Total TCI selfdirectedness score
			total_tci_selfdirectedness_score = tci_selfdirectedness_forward_score + tci_selfdirectedness_reverse_score
			total_tci_selfdirectedness_score=total_tci_selfdirectedness_score.replace([0],[np.nan])
		
			# Total TCI selfdirectedness answers unanswered
			total_tci_selfdirectedness_unanswered = tci_selfdirectedness_forward_unanswered + tci_selfdirectedness_reverse_unanswered
		
		
			# Total answers left blank
			total_tci_selfdirectedness_leftblank = tci_selfdirectedness_forward_leftblank + tci_selfdirectedness_reverse_leftblank
		
			# Total answers prefer not to answer
			total_tci_selfdirectedness_prefernotanswer = tci_selfdirectedness_forward_prefernotanswer + tci_selfdirectedness_reverse_prefernotanswer
			
			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			total_tci_selfdirectedness_score = total_tci_selfdirectedness_score + (total_tci_selfdirectedness_unanswered * total_tci_selfdirectedness_score / (20-total_tci_selfdirectedness_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_tci_selfdirectedness_score:
				if (x<20 or x>100) and x!=np.nan:
					total_tci_selfdirectedness_score=total_tci_selfdirectedness_score.replace([x],["Warning: This TCI_Self_Directedness score (%d) falls outside of the accepted range (20 to 100). Please check your data and try again."  % x])
		
		
			tciselfdirectednessall = pd.DataFrame({'TCI_Self_Directedness_Left_Blank': total_tci_selfdirectedness_leftblank,'TCI_Self_Directedness_Prefer_Not_to_Answer': total_tci_selfdirectedness_prefernotanswer,'TCI_Self_Directedness_Score': total_tci_selfdirectedness_score,})
		
			# ------------------------------------------------------------------------------
		
			# TCI cooperativeness score
		
			# Change the numbers in forward tci cooperativeness headers to numeric floats
			tci_cooperativeness_forward = df[tci_cooperativeness_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			tci_cooperativeness_forward_leftblank = tci_cooperativeness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_cooperativeness_forward_prefernotanswer = tci_cooperativeness_forward[tci_cooperativeness_forward[tci_cooperativeness_keys] == 999].count(axis=1)
			tci_cooperativeness_forward_unanswered = tci_cooperativeness_forward_leftblank + tci_cooperativeness_forward_prefernotanswer
		
			# Sum all the forward scores
			tci_cooperativeness_forward_score = tci_cooperativeness_forward[tci_cooperativeness_forward[tci_cooperativeness_keys] < 6].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			tci_cooperativeness_rev =df[tci_cooperativeness_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			tci_cooperativeness_reverse_leftblank = tci_cooperativeness_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_cooperativeness_reverse_prefernotanswer = tci_cooperativeness_rev[tci_cooperativeness_rev[tci_cooperativeness_rev_keys] == 999].count(axis=1)
			tci_cooperativeness_reverse_unanswered = tci_cooperativeness_reverse_leftblank + tci_cooperativeness_reverse_prefernotanswer
		
			# Sum all the reverse scores
			tci_cooperativeness_reverse_score = tci_cooperativeness_rev.rsub(6)[tci_cooperativeness_rev[tci_cooperativeness_rev_keys] < 6].sum(axis=1)
		
			# Total TCI cooperativeness score
			total_tci_cooperativeness_score = tci_cooperativeness_forward_score + tci_cooperativeness_reverse_score
			total_tci_cooperativeness_score=total_tci_cooperativeness_score.replace([0],[np.nan])
		
			# Total TCI cooperativeness answers unanswered
			total_tci_cooperativeness_unanswered = tci_cooperativeness_forward_unanswered + tci_cooperativeness_reverse_unanswered
		
			# Total answers left blank
			total_tci_cooperativeness_leftblank = tci_cooperativeness_forward_leftblank + tci_cooperativeness_reverse_leftblank
		
			# Total answers prefer not to answer
			total_tci_cooperativeness_prefernotanswer = tci_cooperativeness_forward_prefernotanswer + tci_cooperativeness_reverse_prefernotanswer
			
			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			total_tci_cooperativeness_score = total_tci_cooperativeness_score + (total_tci_cooperativeness_unanswered * total_tci_cooperativeness_score / (20-total_tci_cooperativeness_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_tci_cooperativeness_score:
				if (x<20 or x>100) and x!=np.nan:
					total_tci_cooperativeness_score=total_tci_cooperativeness_score.replace([x],["Warning: This TCI_Cooperativeness score (%d) falls outside of the accepted range (20 to 100). Please check your data and try again."  % x])
		
			tcicooperativenessall = pd.DataFrame({'TCI_Cooperativeness_Left_Blank': total_tci_cooperativeness_leftblank,'TCI_Cooperativeness_Prefer_Not_to_Answer': total_tci_cooperativeness_prefernotanswer,'TCI_Cooperativeness_Score': total_tci_cooperativeness_score,})
		
			# ------------------------------------------------------------------------------
		
			# TCI selftranscendence score
		
			# Change the numbers in forward tci selftranscendence headers to numeric floats
			tci_selftranscendence_forward = df[tci_selftranscendence_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of forward questions left blank or preferred not to answer
			tci_selftranscendence_forward_leftblank = tci_selftranscendence_forward.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_selftranscendence_forward_prefernotanswer = tci_selftranscendence_forward[tci_selftranscendence_forward[tci_selftranscendence_keys] == 999].count(axis=1)
			tci_selftranscendence_forward_unanswered = tci_selftranscendence_forward_leftblank + tci_selftranscendence_forward_prefernotanswer
		
			# Sum all the forward scores
			tci_selftranscendence_forward_score = tci_selftranscendence_forward[tci_selftranscendence_forward[tci_selftranscendence_keys] < 6].sum(axis=1)
		
			# Change the numbers in reverse STAI Trait headers to numeric floats
			tci_selftranscendence_rev =df[tci_selftranscendence_rev_keys].apply(pd.to_numeric, args=('coerce',))
		
			# Sum the number of reverse questions left blank or preferred not to answer
			tci_selftranscendence_reverse_leftblank = tci_selftranscendence_rev.apply(lambda x: sum(x.isnull().values), axis=1)
			tci_selftranscendence_reverse_prefernotanswer = tci_selftranscendence_rev[tci_selftranscendence_rev[tci_selftranscendence_rev_keys] == 999].count(axis=1)
			tci_selftranscendence_reverse_unanswered = tci_selftranscendence_reverse_leftblank + tci_selftranscendence_reverse_prefernotanswer
		
			# Sum all the reverse scores
			tci_selftranscendence_reverse_score = tci_selftranscendence_rev.rsub(6)[tci_selftranscendence_rev[tci_selftranscendence_rev_keys] < 6].sum(axis=1)
		
			# Total TCI selftranscendence score
			total_tci_selftranscendence_score = tci_selftranscendence_forward_score + tci_selftranscendence_reverse_score
			total_tci_selftranscendence_score=total_tci_selftranscendence_score.replace([0],[np.nan])
		
			# Total TCI selftranscendence answers unanswered
			total_tci_selftranscendence_unanswered = tci_selftranscendence_forward_unanswered + tci_selftranscendence_reverse_unanswered
		
			# Total answers left blank
			total_tci_selftranscendence_leftblank = tci_selftranscendence_forward_leftblank + tci_selftranscendence_reverse_leftblank
		
			# Total answers prefer not to answer
			total_tci_selftranscendence_prefernotanswer = tci_selftranscendence_forward_prefernotanswer + tci_selftranscendence_reverse_prefernotanswer
			
			# If there are values missing, multiply the number of unanswered questions by the total subscale score.
			# Then divide that by the (total number of questions in the subscale - number of unanswered questions).
			# Add all of this to to the original score.
			total_tci_selftranscendence_score = total_tci_selftranscendence_score + (total_tci_selftranscendence_unanswered * total_tci_selftranscendence_score / (20-total_tci_selftranscendence_unanswered))
		
			# Check for scores that are outside acceptable values 
			for x in total_tci_selftranscendence_score:
				if (x<20 or x>100) and x!=np.nan:
					total_tci_selftranscendence_score=total_tci_selftranscendence_score.replace([x],["Warning: This TCI_Novelty score (%d) falls outside of the accepted range (20 to 100). Please check your data and try again."  % x])
		
		
			tciselftranscendenceall = pd.DataFrame({'TCI_Self_Transcendence_Left_Blank': total_tci_selftranscendence_leftblank,'TCI_Self_Transcendence_Prefer_Not_to_Answer': total_tci_selftranscendence_prefernotanswer, 'TCI_Self_Transcendence_Score': total_tci_selftranscendence_score})
		
			# ------------------------------------------------------------------------------
			# Generate Output
		
			# Put the scores into one frame
		
			tci_frames = [df.SUBJECT_ID, tcinoveltyall, tciharmavoidanceall, tcirewarddependenceall, tcipersistenceall, tciselfdirectednessall,tcicooperativenessall,tciselftranscendenceall, df.tci_Validity_Checks_Failed]
			tci_result = pd.concat(tci_frames, axis=1)
	return tci_result
		
		# saves output to csv
#tci_result.to_csv(raw_input("Save your tci output as: "))