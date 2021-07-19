# Probe_enrichment
read_count.py - script for counting human and fungal reads


This script counts the number of reads/alignments which are mapped to human and C. albicans, when sequencing combined 
samples (i.e. clinical samples of candidiasis).
As an input, the script expects a file listing the bam files (i.e. "file_list.txt"), for example:

```
sample_1.bam
sample_2.bam
sample_n.bam
```


plot_data - script for plotting the obtained results (comming soon).

This script is written in R and reproduces the main plots of the study "Multiplexed target enrichment of coding and  non-coding transcriptomes  enables studying Candidaspp.infections from human derived samples" by Hovhannisyan et al, 2021.
