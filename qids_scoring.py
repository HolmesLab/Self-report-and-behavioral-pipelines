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


# QUICK INVENTORY OF DEPRESSIVE SYMPTOMS - SELF RATED (qids-SR16)

# RESOURCES USED:
"""
Scale: https://yale.box.com/s/wz0q3vowqrdkl2k1ygaj3kzpv58mn6ml
Scoring: https://yale.app.box.com/files/0/s/qids/1/f_199914611831
"""

# SCORING:

"""
1. The total score is obtained by adding the scores for each of the nine symptom domains of the DSM-IV MDD criteria:
depressed mood, loss of interest or pleasure, concentration/decision making, self-outlook, suicidal ideation,
energy/fatigability, sleep, weight/appetite change, and psychomotor changes (Rush et al. 2003).
Sixteen items are used to rate the nine criterion domains of major depression: four items are used to rate sleep disturbance
(early, middle, and late insomnia plus hypersomnia); two items are used to rate psychomotor disturbance (agitation and retardation);
four items are used to rate appetite/weight disturbance (appetite increase or decrease and weight increase or decrease).
Only one item is used to rate the remaining six domains (depressed mood, decreased interest, decreased energy,
worthlessness/guilt, concentration/decision making, and suicidal ideation). Each item is rated 0-3.
For symptom domains that require more than one item, the highest score of the item relevant for each domain is taken.
For example, if early insomnia is 0, middle insomnia is 1, late insomnia is 3, and hypersomnia is 0,
the sleep disturbance domain is rated 3. The total score ranges from 0-27.

2. How to handle prefer not to answer is not explicitly mentioned in the primary resources above, so
if any subscale value is left blank or PFN among the 6 1-item domains and the 3 multiple item domains,
then that value will be discarded.
"""

# Total score:	min= 0	max= 27
# ------------------------------------------------------------------------------
# Data Preparation
def qids_analysis(df):
	# These are the different headers and their corresponding questions
	qids_keys = ['qids_1', 'qids_2', 'qids_3', 'qids_4', 'qids_5', 'qids_6', 'qids_7', 'qids_8', 'qids_9', 'qids_10','qids_11', 'qids_12', 'qids_13', 'qids_14', 'qids_15', 'qids_16']			 
	sleep_keys = ['qids_1', 'qids_2', 'qids_3', 'qids_4']
	weight_keys = ['qids_6', 'qids_7', 'qids_8', 'qids_9']
	psychomotor_keys = ['qids_15', 'qids_16']
	mood_key = ['qids_5']
	concentration_key = ['qids_10']
	self_criticism_key = ['qids_11']
	suicidal_key = ['qids_12']
	interest_key = ['qids_13']
	energy_key = ['qids_14']
 
	df[qids_keys] = df[qids_keys].replace(["i never take longer than 30 minutes to fall asleep.","i do not wake up at night.","most of the time, i awaken no more than 30 minutes before i need to get up.","i sleep no longer than 7-8 hours/night, without napping during the day.","i do not feel sad.","there is no change in my usual appetite.","there is no change from my usual appetite.","i have not had a change in my weight.","i have not had a change in my weight.","there is no change in my usual capacity to concentrate or make decisions.","i see myself as equally worthwhile and deserving as other people.","i do not think of suicide or death.","there is no change from usual in how interested i am in other people or activities.","there is no change in my usual level of energy.","i think, speak, and move at my usual rate of speed.","i do not feel restless.","i take at least 30 minutes to fall asleep, less than half the time.","i eat somewhat less often or lesser amounts of food than usual","i have a restless, light sleep with a few brief awakenings each night.","more than half the time, i awaken more than 30 minutes before i need to get up.","i sleep no longer than 10 hours in a 24-hour period including naps.","i feel sad less than half the time.","i eat somewhat less often or lesser amounts of food than usual.","i feel a need to eat more frequently than usual.","i feel as if i have had a slight weight loss.","i feel as if i have had a slight weight gain.","i occasionally feel indecisive or find that my attention wanders.","i am more self-blaming than usual.","i feel that life is empty or wonder if it's worth living.","i notice that i am less interested in people or activities","i notice that i am less interested in people or activities.","i get tired more easily than usual.","i find that my thinking is slowed down or my voice sounds dull or flat.","i find that my thinking is slowed down or my voice sounds dull or flat.","i'm often fidgety, wringing my hands, or need to shift how i'm sitting.","i take at least 30 minutes to fall asleep, more than half the time.","i wake up at least once a night, but i go back to sleep easily.","i almost always awaken at least one hour or so before i need to, but i go back to sleep eventually.","i sleep no longer than 12 hours in a 24-hour period including naps.","i feel sad more than half the time.","i eat much less than usual and only with personal effort.","i regularly eat more often and/or greater amounts of food than usual.","i have lost 2 pounds or more.","i have gained 2 pounds or more.","most of the time, i struggle to focus my attention or to make decisions.","i largely believe that i cause problems for others.","i think of suicide or death several times a week for several minutes.","i find i have interest in only one or two of my formerly pursued activities.","i have to make a big effort to start or finish my usual daily activities (for example, shopping, homework, cooking, or going to work).","it takes me several seconds to respond to most questions and i'm sure my thinking is slowed.","i have impulses to move about and am quite restless.","i take more than 60 minutes to fall asleep, more than half the time.","i awaken more than once a night and stay awake for 20 minutes or more, more than half the time.","i awaken at least one hour before i need to, and can't go back to sleep.","i sleep longer than 12 hours in a 24-hour period including naps.","i feel sad nearly all of the time."," i rarely eat within a 24-hour period, and only with extreme personal effort or when others persuade me to eat.","i feel driven to overeat both at mealtime and between meals.","i have lost 5 pounds or more.","i have gained 5 pounds or more.","i cannot concentrate well enough to read or cannot make even minor decisions.","i think almost constantly about major and minor defects in myself","i think of suicide or death several times a day in some detail, or i have made specific plans for suicide or have actually tried to take my life.","i have virtually no interest in formerly pursued activities.","i really cannot carry out most of my usual daily activities because i just don't have the energy.","i am often unable to respond to questions without extreme effort.","At times, i am unable to stay seated and need to pace around."],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
	# Corrects for Qualtrics survey allowing participants to answer two mutually exclusive questions (the redundant/irrelevant responses are coded as 'NaN')
	mask = (df.qids_6 >0) & (df.qids_6 < 4)
	df.loc[mask, 'qids_7'] = np.nan 
	mask = (df.qids_7 >0) & (df.qids_7 < 4)
	df.loc[mask, 'qids_6'] = np.nan 
	mask = (df.qids_8 >0) & (df.qids_8 < 4)
	df.loc[mask, 'qids_9'] = np.nan 
	mask = (df.qids_9 >0) & (df.qids_9 < 4)
	df.loc[mask, 'qids_8'] = np.nan 
	mask= (df.qids_6==0) & (df.qids_7==0)
	df.loc[mask, 'qids_7'] = np.nan 
	mask= (df.qids_8==0) & (df.qids_9==0)
	df.loc[mask, 'qids_9'] = np.nan 

	# Minimum Score: 0
	# Maximum Score: 27

	# Check for values that don't match parameters 
	qids_check=df[qids_keys].apply(pd.to_numeric,args=('raise',))
	qids_check=qids_check[(qids_check !=0) & (qids_check !=1) & (qids_check !=2) & (qids_check !=3) & (qids_check !=999)].sum()
	for x in qids_check:
		if x!=0:
			df['qids_error']=np.nan
			df.qids_error=df.qids_error.replace([np.nan],["Your QIDS responses are not keyed appropriately. Please compare your data to the accepted values in the script."])
			qids_result=df['qids_error']
			
		else:
			# ------------------------------------------------------------------------------
			# COUNTS UP scoreS LEFT BLANK OR PREFER NOT TO ANSWER

			qids = df[qids_keys].apply(pd.to_numeric, args=('ignore',), axis=1)
			qids_prefernotanswer= qids.apply(lambda x: sum(x==999), axis=1)
			qids_leftblank = qids.apply(lambda x: sum(x.isnull().values), axis=1)

			# ------------------------------------------------------------------------------
			# For sleep, weight, and psychomotor, just gets the MAX SINGLE score from each domain

			sleep = df[sleep_keys].apply(pd.to_numeric, args=('ignore',), axis=1)

			sleepvalue = sleep[(sleep[sleep_keys] >= 0) & (sleep[sleep_keys] <= 3)].max(axis=1, skipna=True)

			# ---------------------------
			weight = df[weight_keys].apply(pd.to_numeric, args=('raise',), axis=1)

			weightvalue = weight[(weight[weight_keys] >= 0) & (weight[weight_keys] <= 3)].max(axis=1, skipna=True)

			# ---------------------------
			psychomotor = df[psychomotor_keys].apply(pd.to_numeric, args=('raise',), axis=1)

			psychvalue = psychomotor[(psychomotor[psychomotor_keys] >= 0) & (psychomotor[psychomotor_keys] <= 3)].max(axis=1, skipna=True)

			# ------------------------------------------------------------------------------
			mood = df[mood_key].apply(pd.to_numeric, args=('raise',), axis=1)

			moodscore = mood[(mood[mood_key] >= 0) & (mood[mood_key] <= 3)].sum(axis=1, skipna=True)

			# ---------------------------
			concentration = df[concentration_key].apply(pd.to_numeric, args=('raise',), axis=1)

			concscore = concentration[(concentration[concentration_key] >= 0) & (concentration[concentration_key] <= 3)].sum(axis=1, skipna=True)

			# ---------------------------
			selfcrit = df[self_criticism_key].apply(pd.to_numeric, args=('raise',), axis=1)

			critscore = selfcrit[(selfcrit[self_criticism_key] >= 0) & (selfcrit[self_criticism_key] <= 3)].sum(axis=1,skipna=True)

			# ---------------------------
			suicidal = df[suicidal_key].apply(pd.to_numeric, args=('raise',), axis=1)

			suicidescore = suicidal[(suicidal[suicidal_key] >= 0) & (suicidal[suicidal_key] <= 3)].sum(axis=1, skipna=True)

			# ---------------------------
			interest = df[interest_key].apply(pd.to_numeric, args=('raise',), axis=1)

			interestscore = interest[(interest[interest_key] >= 0) & (interest[interest_key] <= 3)].sum(axis=1, skipna=True)

			# ---------------------------
			energy = df[energy_key].apply(pd.to_numeric, args=('raise',), axis=1)

			energyscore = energy[(energy[energy_key] >= 0) & (energy[energy_key] <= 3)].sum(axis=1, skipna=True)

			# ------------------------------------------------------------------------------
			# SUMS THE scoreS UP!

			qids_score = sleepvalue + weightvalue + psychvalue + moodscore + concscore + critscore + suicidescore + interestscore + energyscore

			qidsall = pd.DataFrame({'QIDS_Left_Blank' : qids_leftblank, 'QIDS_Prefer_Not_to_Answer': qids_prefernotanswer,'QIDS_Score': qids_score,})

			# Check for scores that are outside acceptable values 
			for x in qids_score:
				if (x<0 or x>27) and x!=np.nan:
					qids_score=qids_score.replace([x],["Warning: This NEO-FFI_Neuroticism score (%d) falls outside of the accepted range (0 to 27). Please check your data and try again."  % x])


			# ------------------------------------------------------------------------------
			# Generate Output
			qids_frames = [df.SUBJECT_ID, qidsall]
			qids_result = pd.concat(qids_frames, axis=1)
	return qids_result
	#qids_result.to_csv(raw_input("Save your qids output as: "))