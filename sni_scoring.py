#!/usr/bin/python
"""
Battery Scores Package for Processing Qualtrics CSV Files
	
@author: David Gruskin
@email: david.gruskin@yale.edu
@version: 1.0
@date: 2017.07.12
"""
	
import pandas as pd
import numpy as np
import sys 
	
# Social Network Inventory
	
# RESOURCES USED:
"""
Scale: https://yale.box.com/s/vt0qcesmrdvby93c06oykko36q5lor7o
Scoring: https://yale.box.com/s/odsodicwdj1wtuqo010cwjent1gfgaz2
"""

# Scoring:
"""
1. The SNI is unlike the other scales covered in this package, and the scoring of the SNI
therefore requires steps that are unlike those used in the other scoring programs in this package. 
"""
	
# ------------------------------------------------------------------------------
# Data Preparation 
def sni_analysis(df):
	# These are the different headers and their corresponding questions
	sni_keys = ['sni_1', 'sni_2', 'sni_3','sni_4', 'sni_5', 'sni_6','sni_7', 'sni_8', 'sni_9','sni_10', 'sni_11', 'sni_12','sni_13', 'sni_14', 'sni_15','sni_16', 'sni_17', 'sni_18','sni_19', 'sni_20', 'sni_21','sni_22', 'sni_23', 'sni_24','sni_25', 'sni_26', 'sni_27','sni_28', 'sni_29']
	sni_score_keys = ['sni_1','sni_3','sni_5','sni_7','sni_9','sni_11','sni_13','sni_15','sni_17','sni_18','sni_19','sni_21','sni_22','sni_23','sni_24','sni_25','sni_26','sni_27','sni_28','sni_29']
	sni_group_keys=['sni_23','sni_24','sni_25','sni_26','sni_27','sni_28']
	sni_noblank_keys=['sni_1','sni_4','sni_5','sni_6','sni_7','sni_8','sni_9', 'sni_10', 'sni_11', 'sni_12','sni_14', 'sni_16', 'sni_19', 'sni_20', 'sni_22']
	
	# Count up the number of questions left blank or prefer not to answer
	sni_prefernotanswer= df[sni_keys].apply(lambda x: sum(x==999), axis=1)
	sni_leftblank= df[sni_noblank_keys].apply(lambda x: sum(x.isnull().values), axis=1)
	
	# Replace answers of '7 or more' with '7' for scoring purposes (as per the scoring instructions)
	df[sni_keys]=df[sni_keys].replace(['7 or more'], [7])
	
	# Replace questions left blank or prefer not to answer with 0 for scoring purposes 
	df[sni_score_keys]=df[sni_score_keys].replace([np.nan], ['0'])
	df[sni_keys]=df[sni_keys].replace([999], ['0'])
	
	# Adjust for Qualtrics allowing respondents to claim non-0 number of in-laws in spite of having never been married
	mask = (df.sni_1 == '(2) never married & never lived with someone in a marital-like relationship')
	df.loc[mask, 'sni_6'] = '(4) not applicable' 
	
	# Replace certain text responses with numerical values for scoring purposes
	df['sni_1']=df['sni_1'].replace(['(1) currently married & living together, or living with someone in marital-like relationship', '(2) never married & never lived with someone in a marital-like relationship', '(3) separated', '(4) divorced or formerly lived with someone in a marital-like relationship', '(5) widowed'],[1,0,0,0,0])
	df['sni_5']=df['sni_5'].replace(['(0) neither','(1) mother only', '(2) father only', '(3) both'],[0,1,1,2])
	df['sni_7']=df['sni_7'].replace(['(0) neither','(1) mother only', '(2) father only', '(3) both', '(4) not applicable'],[0,1,1,2,0])
	
	# Calculate a 'work' score that combines #s from sni_17 and sni_18
	df[sni_score_keys]=df[sni_score_keys].apply(pd.to_numeric,args=('ignore',))
	
	
	
	# ------------------------------------------------------------------------------
	# Role Score Calculation 
	# Minimum Score: 0
	# Maximum Score: 12
	
	# Create empty lists for role scores 
	role_score_1=[]
	role_score_2=[]
	role_score_3=[]
	role_score_4=[]
	role_score_5=[]
	role_score_6=[]
	role_score_7=[]
	role_score_8=[]
	role_score_9a=[]
	role_score_9b=[]
	role_score_10=[]
	role_score_11=[]
	role_score_12=[]
	
	# Fill role score lists with values corresponding to question answers 
	
	for x in df['sni_1']:
		if x==1:
			role_score_1.append(1)
		else:
			role_score_1.append(0)
	
	for x in df['sni_3']:
		if x!=0:
			role_score_2.append(1)
		else:
			role_score_2.append(0)
	
	
	for x in df['sni_5']:
		if x!=0:
			role_score_3.append(1)
		else:
			role_score_3.append(0)
	
			
	for x in df['sni_7']:
		if x!= 0:
			role_score_4.append(1)
		else:
			role_score_4.append(0)
	
	for x in df['sni_9']:
		if x!= 0:
			role_score_5.append(1)
		else:
			role_score_5.append(0)
	
	for x in df['sni_11']:
		if x!= 0:
			role_score_6.append(1)
		else:
			role_score_6.append(0)
	
	
	for x in df['sni_13']:
		if x!=0:
			role_score_7.append(1)
		else:
			role_score_7.append(0)
	
	
	for x in df['sni_15']:
		if x!=0:
			role_score_8.append(1)
		else:
			role_score_8.append(0)
	
	for x in df['sni_17']:
		if x!= 0:
			role_score_9a.append(0.5)
		else:
			role_score_9a.append(0)
	
	for x in df['sni_18']:
		if x!=0:
			role_score_9b.append(0.5)
		else:
			role_score_9b.append(0)
	
	for x in df['sni_19']:
		if x!=0:
			role_score_10.append(1)
		else:
			role_score_10.append(0)
	
			
	for x in df['sni_21']:
		if x!= 0:
			role_score_11.append(1)
		else:
			role_score_11.append(0)
	
		
	for x in df['sni_22']:
		if x== 'yes':
			role_score_12.append(1)
		else:
			role_score_12.append(0)
	
	# Convert role score lists to columns
	df['role_score_1']=role_score_1
	df['role_score_2']=role_score_2
	df['role_score_3']=role_score_3
	df['role_score_4']=role_score_4
	df['role_score_5']=role_score_5
	df['role_score_6']=role_score_6
	df['role_score_7']=role_score_7
	df['role_score_8']=role_score_8
	df['role_score_10']=role_score_10
	df['role_score_11']=role_score_11
	df['role_score_12']=role_score_12
	df['role_score_9a']=role_score_9a
	df['role_score_9b']=role_score_9b
	
	# Calculate a work role score from sni_17 and sni_18 
	df['role_score_9']=df['role_score_9a']+df['role_score_9b']
	df['role_score_9']=df['role_score_9'].replace(0.5,0)
	
	
	# Calculate total role score 
	df['role_score_total']=df['role_score_1']+df['role_score_2']+df['role_score_3']+df['role_score_4']+df['role_score_5']+df['role_score_6']+df['role_score_7']+df['role_score_8']+df['role_score_9']+df['role_score_10']+df['role_score_11']+df['role_score_12']
	role_score_total=df['role_score_total']
	# ------------------------------------------------------------------------------
	
	
	# Number of People in Social Network Calculation 
	df['role_score_1']=df['role_score_1'].apply(pd.to_numeric,args=('ignore',))
	df['sni_9']=df['sni_9'].astype(np.int64)
	df[sni_score_keys]=df[sni_score_keys].replace([999],[0])
	
	# For the group response questions, take Qualtrics output and extract the integers 
	df[sni_group_keys]=df[sni_group_keys].replace([np.nan], [0])
	df[sni_group_keys]=df[sni_group_keys].replace(['?'], [0])
	df[sni_group_keys]=df[sni_group_keys].replace(['na'], [0])
	
	df.sni_23=df.sni_23.apply(str)
	df.sni_23=df.sni_23.str.extract('(\d+)', expand=True)
	df[sni_group_keys]=df[sni_group_keys].replace([np.nan], [0])
	df['sni_23']=df['sni_23'].astype(np.int64)
	df.sni_24=df.sni_24.apply(str)
	df[sni_group_keys]=df[sni_group_keys].replace([np.nan], [0])
	df.sni_24=df.sni_24.str.extract('(\d+)',expand=True)
	df[sni_group_keys]=df[sni_group_keys].replace([np.nan], [0])
	df['sni_24']=df['sni_24'].astype(np.int64)
	df.sni_25=df.sni_25.apply(str)
	df.sni_25=df.sni_25.str.extract('(\d+)',expand=True)
	df[sni_group_keys]=df[sni_group_keys].replace([np.nan], [0])
	df['sni_25']=df['sni_25'].astype(np.int64)
	df.sni_26=df.sni_26.apply(str)
	df.sni_26=df.sni_26.str.extract('(\d+)',expand=True)
	df[sni_group_keys]=df[sni_group_keys].replace([np.nan], [0])
	df['sni_26']=df['sni_26'].astype(np.int64)
	df.sni_27=df.sni_28.apply(str)
	df.sni_27=df.sni_27.str.extract('(\d+)',expand=True)
	df[sni_group_keys]=df[sni_group_keys].replace([np.nan], [0])
	df['sni_27']=df['sni_27'].astype(np.int64)
	df.sni_28=df.sni_28.apply(str)
	df.sni_28=df.sni_28.str.extract('(\d+)',expand=True)
	df[sni_group_keys]=df[sni_group_keys].replace([np.nan], [0])
	df['sni_28']=df['sni_28'].astype(np.int64)
	df[sni_group_keys]=df[sni_group_keys].apply(pd.to_numeric,args=('raise',))
	
	# For the group response questions, any response above 6 will be recoded as 7 (as per the scoring instructions) 
	for x in df['sni_23']:
		if x>6:
			df['sni_23']=df['sni_23'].replace([x],[7])
	
	for x in df['sni_24']:
		if x>6:
			df['sni_23']=df['sni_23'].replace([x],[7])
	
	for x in df['sni_25']:
		if x>6:
			df['sni_25']=df['sni_25'].replace([x],[7])
	
	for x in df['sni_26']:
		if x>6:
			df['sni_26']=df['sni_26'].replace([x],[7])
	
	
	for x in df['sni_27']:
		if x>6:
			df['sni_27']=df['sni_27'].replace([x],[7])
	
	for x in df['sni_28']:
		if x>6:
			df['sni_28']=df['sni_28'].replace([x],[7])
	
	
	# Calculate a total network size from the reported groups
	df['sni_groups_total']=df['sni_23']+ df['sni_24'] + df['sni_25']+ df['sni_26'] + df['sni_27'] + df['sni_28']
	
	# Calculate the total number in social network 
	df['total_number_in_social_network']= df['role_score_1'] + df['sni_3'] + df['sni_5']+ df['sni_7'] + df['sni_9']+ df['sni_11'] + df['sni_13']+ df['sni_15'] + df['sni_17']+ df['sni_18'] + df['sni_19'] + df['sni_21']+df['sni_23']+ df['sni_24'] + df['sni_25']+ df['sni_26'] + df['sni_27'] + df['sni_28']
	network_size=df['total_number_in_social_network']

	
	# ------------------------------------------------------------------------------
	# Number of Embedded Networks 
	# Minimum score: 0
	# Maximum score: 8
	# Create lists for each embedded network 
	embedded_family_1=[]
	embedded_family_2=[]
	embedded_family=[]
	embedded_friends=[]
	embedded_religion=[]
	embedded_school=[]
	embedded_work=[]
	embedded_neighbors=[]
	embedded_volunteers=[]
	embedded_groups=[]
	
	# Calculate parameters for family embedded network 
	df['number_of_family_members']= df['sni_1']+df['sni_3'] + df['sni_5'] + df['sni_7'] + df['sni_9']
	df['family_role_score']= df['role_score_1']+df['role_score_2']+df['role_score_3']+df['role_score_4']+df['role_score_5']
	df['embedded_family']=np.nan
	df['family_role_score']=df['family_role_score'].astype(np.float64)
	df['number_of_family_members']=df['number_of_family_members'].astype(np.float64)
	df['sni_work']=df['sni_17']+df['sni_18']
	
	# If network meets requirements for embedded network, assign a "1" value in the corresponding list
	for x in df['family_role_score']:
		if x>=3:
			embedded_family_1.append(0.5)
		else:
			embedded_family_1.append(0)
	
	
	for x in df['number_of_family_members']:
		if x>=4:
			embedded_family_2.append(0.5)
		else:
			embedded_family_2.append(0)
	
	for x in df['sni_11']:
		if x>= 4:
			embedded_friends.append(1)
		else:
			embedded_friends.append(0)
	
	for x in df['sni_13']:
		if x>=4:
			embedded_religion.append(1)
		else:
			embedded_religion.append(0)
	
	for x in df['sni_15']:
		if x>=4:
			embedded_school.append(1)
		else:
			embedded_school.append(0)
	
	for x in df['sni_work']:
		if x>= 4:
			embedded_work.append(1)
		else:
			embedded_work.append(0)
	
	for x in df['sni_19']:
		if x>= 4:
			embedded_neighbors.append(1)
		else:
			embedded_neighbors.append(0)
	
	for x in df['sni_21']:
		if x>=4:
			embedded_volunteers.append(1)
		else:
			embedded_volunteers.append(0)
	
	
	for x in df['sni_groups_total']:
		if x>=4:
			embedded_groups.append(1)
		else:
			embedded_groups.append(0)
	
			
	# Create columns in dataframe from the lists 
	df['embedded_friends']=embedded_friends
	df['embedded_religion']=embedded_religion
	df['embedded_school']=embedded_school
	df['embedded_work']=embedded_work
	df['embedded_neighbors']=embedded_neighbors
	df['embedded_volunteers']=embedded_volunteers
	df['embedded_groups']=embedded_groups		
	df['embedded_family_1']=embedded_family_1
	df['embedded_family_2']=embedded_family_2
	df['embedded_family']=df['embedded_family_1']+df['embedded_family_2']
	df['embedded_family']=df['embedded_family'].replace(0.5,0)
	df['embedded_score']=df['embedded_friends']+df['embedded_religion']+df['embedded_school']+df['embedded_work']+df['embedded_neighbors']+df['embedded_volunteers']+df['embedded_groups']+df['embedded_family']
	df['embedded_score']
	embedded_score=df['embedded_score']
	
	# ------------------------------------------------------------------------------
	# Generate Output
	
	# Put the scores into one frame
	sniall = pd.DataFrame({'SNI_Left_Blank' : sni_leftblank, 'SNI_Prefer_to_not_answer' : sni_prefernotanswer, 'SNI_Number_of_High_Contact_Roles': role_score_total, 'SNI_Number_of_People_in_Social_Network': network_size, 'SNI_Number_of_Embedded_Networks' : embedded_score})
	
	sni_frames = [df.SUBJECT_ID, sniall]
	sni_result = pd.concat(sni_frames, axis=1)
	return sni_result
	# saves output to csv
	
	#sni_result.to_csv(raw_input("Save your SNI output as: "))