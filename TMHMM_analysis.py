import biolib
import os
import time
biolib.login()

#all the proteome fasta sequences are kept in the folder All_fasta and results are saved to results folder
all_fasta = os.listdir('All_fasta') 

deeptmhmm = biolib.load('DTU/DeepTMHMM')

biolib.utils.STREAM_STDOUT = True

for fasta_file in all_fasta:
    print(f"running analysis for {fasta_file}")
    job = deeptmhmm.cli(args=f'--fasta All_fasta1/{fasta_file}')
    job.save_files(f'results/{fasta_file}')

    print(f"================================completed analysis for {fasta_file}============================")

    os.remove('All_fasta1/'+fasta_file)

    time.sleep(30)
