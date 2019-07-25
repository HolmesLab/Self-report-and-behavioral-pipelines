'''
Created on Jul 22, 2017

@author: David Gruskin 
'''
import pandas as pd
import numpy as np
import os
import asi_scoring
import bapq_scoring
import bis_scoring
import bisbas_scoring
import dospert_s_scoring
import dospert40_scoring
import ecrr10_scoring
import neoffi_scoring
import pss_scoring
import qids_scoring
import rsqa_scoring
import rsri_scoring
import saqa_scoring
import sni_scoring
import stai_scoring
import panas_scoring
import tci_scoring
import bis_scoring


def main():  

	#------------------------------------------------------------------------------------
	# Set your specific parameters here

	# Define the location of your data csv here:
	datafilepath = '/Users/ra1/NFC_correct.csv'

	# Define the location of your column dictionary here:
	headerfilepath= '/Users/ra1/NFC_columndictionary.csv'

	# List all of the questionnaires you plan on using:
	#'ASI,BAPQ,BARRATT,BIS/BAS,DOSPERT(S),DOSPERT(40),ECR-R10,NEO-FFI,PANAS,PSS,QIDS,RSQA,RSRI,SAQ-A,SNI,STAI,TCI'
	questionnaire_list= 'NFC(S)'

	# Provide the name of your output file here:
	output_name= 'output1234'

	# Define how "Prefer not to answer" responses are listed in your data:
	prefertonotanswer= "Prefer not to answer"

	#------------------------------------------------------------------------------------
	# Convert data into a dataframe
	raw_data_frame = pd.read_csv(datafilepath)
	question_dict  = pd.read_csv(headerfilepath)
	df = pd.DataFrame(raw_data_frame) 
	df.columns = question_dict['COLUMN_NAME']
	df= df.replace([prefertonotanswer], [999])
	total_prefernotanswer= df.apply(lambda x: sum(x== 999), axis=1)
	total_prefernotanswer= pd.DataFrame({'Total_Prefer_to_Not_Answer' : total_prefernotanswer})
	df= df.replace([np.nan], ['99999'])
	df=df.apply(lambda x:x.astype(str).str.lower())
	df= df.replace(['99999'], [np.nan])

	# Score the scales   
	df_results=pd.DataFrame()
	if "ASI" in questionnaire_list:
		asi_result= asi_scoring.asi_analysis(df)
		df_results=[df_results,asi_result]
		df_results=pd.concat(df_results, axis=1)
	if "BAPQ" in questionnaire_list:
		bapq_result= bapq_scoring.bapq_analysis(df)
		df_results=[df_results,bapq_result]
		df_results=pd.concat(df_results, axis=1)
	if "BARRATT" in questionnaire_list:
		barratt_result= bis_scoring.bis_analysis(df)
		df_results=[df_results,barratt_result]
		df_results=pd.concat(df_results, axis=1)
	if "BIS/BAS" in questionnaire_list:
		bisbas_result= bisbas_scoring.bisbas_analysis(df)
		df_results= [df_results,bisbas_result]
		df_results=pd.concat(df_results, axis=1)
	if "DOSPERT(S)" in questionnaire_list:
		dospert_s_result = dospert_s_scoring.dospert_s_analysis(df)
		df_results=[df_results,dospert_s_result]
		df_results=pd.concat(df_results, axis=1)
	if "DOSPERT(40)" in questionnaire_list:
		dospert40_result = dospert40_scoring.dospert40_analysis(df)
		df_results=[df_results,dospert40_result]
		df_results=pd.concat(df_results, axis=1)
	if "ECR-R10" in questionnaire_list:
		ecrr10_result= ecrr10_scoring.ecrr10_analysis(df)
		df_results=[df_results,ecrr10_result]
		df_results=pd.concat(df_results, axis=1)
	if "NEO-FFI" in questionnaire_list:
		neoffi_result= neoffi_scoring.neoffi_analysis(df)
		df_results=[df_results,neoffi_result]
		df_results=pd.concat(df_results, axis=1)
	if "NFC(S)" in questionnaire_list:
		nfc_s_result= nfc_s_scoring.nfc_s_analysis(df)
		df_results=[df_results,nfc_s_result]
		df_results=pd.concat(df_results, axis=1)
	if "PANAS" in questionnaire_list:
		panas_result= panas_scoring.panas_analysis(df)
		df_results=[df_results,panas_result]
		df_results=pd.concat(df_results, axis=1)
	if "PSS" in questionnaire_list:
		pss_result= pss_scoring.pss_analysis(df)
		df_results=[df_results,pss_result]
		df_results=pd.concat(df_results, axis=1)
	if "QIDS" in questionnaire_list:
		qids_result= qids_scoring.qids_analysis(df)
		df_results=[df_results,qids_result]
		df_results=pd.concat(df_results, axis=1)
	if "A-RSQ" in questionnaire_list:
		rsqa_result= rsqa_scoring.rsqa_analysis(df)
		df_results=[df_results,rsqa_result]
		df_results=pd.concat(df_results, axis=1)
	if "RSRI" in questionnaire_list:
		rsri_result= rsri_scoring.rsri_analysis(df)
		df_results=[df_results,rsri_result]
		df_results=pd.concat(df_results, axis=1)
	if "SAQ-A" in questionnaire_list:
		saqa_result= saqa_scoring.saqa_analysis(df)
		df_results=[df_results,saqa_result]
		df_results=pd.concat(df_results, axis=1)
	if "SNI" in questionnaire_list:
		sni_result= sni_scoring.sni_analysis(df)
		df_results=[df_results,sni_result]
		df_results=pd.concat(df_results, axis=1)
	if "STAI" in questionnaire_list:
		stai_result= stai_scoring.stai_analysis(df)
		df_results=[df_results,stai_result]
		df_results=pd.concat(df_results, axis=1)
	if "TCI" in questionnaire_list:
		tci_result= tci_scoring.tci_analysis(df)
		df_results=[df_results,bis_result]
		df_results=pd.concat(df_results, axis=1)
		
	# Combine the results into one spreadsheet and save as output
	df_results=[df_results, total_prefernotanswer]
	df_results=pd.concat(df_results, axis=1)
	df_results = df_results.loc[:,~df_results.columns.duplicated()]
	output=df_results
	output.to_csv(output_name)
	print "Your output has been saved- have a great day!"


main()