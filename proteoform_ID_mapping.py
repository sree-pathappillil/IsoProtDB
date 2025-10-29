#merge code used for exact matching of fasta sequences of UniProt and Refseq proteoforms

import pandas as pd
from Bio import SeqIO

# Input FASTA files
uniprot_fasta = r"C:\Users\Admin\Downloads\uniprot_fasta.fasta"
refseq_fasta = r"C:\Users\Admin\Downloads\refseq_fasat.fasta"

# Parse UniProt FASTA
uniprot_records = {str(rec.seq): rec.id for rec in SeqIO.parse(uniprot_fasta, "fasta")}

# Parse RefSeq FASTA
refseq_records = {str(rec.seq): rec.id for rec in SeqIO.parse(refseq_fasta, "fasta")}

# Find exact matches (sequence-wise)
matches = []
for seq, uniprot_id in uniprot_records.items():
    if seq in refseq_records:
        matches.append({
            "UniProt_ID": uniprot_id,
            "RefSeq_ID": refseq_records[seq],
            "Sequence_Length": len(seq)
        })

# Convert to DataFrame
df_matches = pd.DataFrame(matches)

# Save results to CSV
df_matches.to_csv("exact_matches.csv", index=False)

print(f"✅ Found {len(df_matches)} exact matches.")
print("Results saved to 'exact_matches.csv'")
