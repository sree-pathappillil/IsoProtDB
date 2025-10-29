#code fetch the sequence variant data from gNOMAD database through the API provided by them
import requests
import pandas as pd
import os
from time import sleep

gene_df = pd.read_excel(r"D:\FINAL_ISOPROTTTTTTTT\yet_______.xlsx")
gene_list = gene_df['Gene'].dropna().unique()

output_folder = r"D:\FINAL_ISOPROTTTTTTTT\gene"
os.makedirs(output_folder, exist_ok=True)

existing_files = os.listdir(output_folder)
existing_genes = {f.split('_gnomad_variants.xlsx')[0] for f in existing_files if f.endswith('_gnomad_variants.xlsx')}
filtered_gene_list = [gene for gene in gene_list if gene not in existing_genes]

reference_genome = "GRCh38"

for gene_symbol in filtered_gene_list:
    print(f"Fetching data for gene: {gene_symbol}")

    query = f"""
    query VariantsInGene {{
      gene(gene_symbol: "{gene_symbol}", reference_genome: {reference_genome}) {{
        variants(dataset: gnomad_r4) {{
          variant_id
          pos
          rsids
          transcript_id
          transcript_version
          hgvs
          hgvsc
          hgvsp
          consequence
          flags
          exome {{
            af
          }}
          genome {{
            af
          }}
          joint {{
            ac
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        "https://gnomad.broadinstitute.org/api",
        headers={"Content-Type": "application/graphql; charset=utf-8"},
        data=query
    )

    if response.status_code == 200:
        result = response.json()
        gene_data = result.get("data", {}).get("gene")

        if not gene_data:
            print(f" No data found for gene: {gene_symbol}")
            continue

        variants = gene_data["variants"]
        rows = []
        for var in variants:
            row = {
                "variant_id": var.get("variant_id"),
                "pos": var.get("pos"),
                "rsids": ", ".join(var.get("rsids", [])) if var.get("rsids") else "",
                "transcript_id": var.get("transcript_id"),
                "transcript_version": var.get("transcript_version"),
                "hgvs": var.get("hgvs"),
                "hgvsc": var.get("hgvsc"),
                "hgvsp": var.get("hgvsp"),
                "consequence": var.get("consequence"),
                "flags": ", ".join(var.get("flags", [])) if var.get("flags") else "",
                "exome_af": var["exome"]["af"] if var.get("exome") else None,
                "genome_af": var["genome"]["af"] if var.get("genome") else None,
                "joint_ac": var["joint"]["ac"] if var.get("joint") else None
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        excel_path = os.path.join(output_folder, f"{gene_symbol}_gnomad_variants.xlsx")
        df.to_excel(excel_path, index=False)
        print(f"✅ Excel saved to: {excel_path}")

    else:
        print(f"❌ API error for {gene_symbol}: {response.status_code}")

    sleep(5)
