"""
author: Hrant Hovhannisyan, grant.hovhannisyan@gmail.com
v.1
This script counts the number of reads/alignments which are mapped to human and C. albicans, when sequencing combined 
samples (i.e. clinical samples of candidiasis).
The script expects the list of bam files as an input (i.e. "file_list.txt")
"""



from collections import defaultdict
import re
import sys
import os
import pysam

with open("file_list.txt", "r+") as files:
	for filename in files:
		sys.stdout.flush()
		print ("Calculations for %s"%(filename))
		filename=filename.rstrip()
		dict_list=[]
		bam=pysam.AlignmentFile(filename,"rb")
		for line in bam.fetch():
			line=line.tostring(bam)
			line=line.split("\t")
			#print line[11]
			d={}
			d[line[0]+"_"+line[11]]=line[2]
			dict_list.append(d)
			#print d
			#print dict_list
			
		sys.stdout.flush()
		print "Dictionary is made"
		alignment_dict=defaultdict(list)
		for d in dict_list:
			for k,v in d.iteritems():
				alignment_dict[k].append(v)
				#print alignment_dict
			
		sys.stdout.flush()
		print "Calculating reads"
		CALB_reads=0
		human_reads=0
		
		for read_id,alignments in alignment_dict.iteritems():
			calb_N=0
			for chrom in alignments:
				if "C_albicans" in chrom:
					calb_N+=1
			if len(alignments)>calb_N and any("C_albicans" in element for element in alignments):
				print "This read pair is mulitmapped between two organisms and thus discarded",read_id,alignments,int(read_id[-1]),len(alignments), "\n"
			elif not any("C_albicans" in element for element in alignments):     ### Alignments only to Human
				if "NH:i:1" in read_id and len(alignments)==2:          ### If read pair is uniquelly mapped
					human_reads=human_reads+2
				elif int(read_id[-1])>2:                        		### If the read pair is multimapped (we count only 1 read pair)
					human_reads=human_reads+2
				elif int(read_id[-1])==len(alignments):                 ### If one read of the pair in multimapped OR only one read is uniquelly mapped
					human_reads=human_reads+1	
			elif len(alignments)==calb_N:                   	        ### Alignments only to CALB
				if "NH:i:1" in read_id and len(alignments)==2:          ### If read pair is uniquely mapped
					CALB_reads=CALB_reads+2
				elif int(read_id[-1])>2:              		            ### If the read pair is multimapped (we count only 1 read pair)
					CALB_reads=CALB_reads+2                 
				elif int(read_id[-1])==len(alignments):                 ### If one read of the pair in multimapped OR only one read is uniquelly mapped
					CALB_reads=CALB_reads+1
		sys.stdout.flush()
		print filename,"\t","Candida reads = ","\t",CALB_reads,"\t","Human reads = ","\t",human_reads,"\t", "\n"
		
			
