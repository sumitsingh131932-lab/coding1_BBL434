#!/usr/bin/env python3

# =====================================================
# Universal Plasmid Constructor
# =====================================================

# ------------------ CORE PLASMID BACKBONE ------------------
ORI_SEQUENCE = "TTGACATGTTGACATGTTGACATG"

REPLICATION_MODULES = [
    "ATGGCTGCTGCTGCTGCTGCT",   # repA
    "ATGCCGCCGCCGCCGCCGCC",   # repB
    "ATGAAAGGGAAAGGGAAAGGG"   # repC
]

PLASMID_BACKBONE = ORI_SEQUENCE + "".join(REPLICATION_MODULES)

# ------------------ RESTRICTION ENZYME DATABASE ------------------
RESTRICTION_DB = {
    "EcoRI": "GAATTC",
    "BamHI": "GGATCC",
    "HindIII": "AAGCTT",
    "XhoI": "CTCGAG"
}

# ------------------ ANTIBIOTIC RESISTANCE MARKERS ------------------
ANTIBIOTIC_DB = {
    "Tetracycline": "ATGACCGTTACGACCGTTACGACCGTT",
    "Spectinomycin": "ATGGCTGATGCTGATGCTGATGCTGA",
    "Gentamicin": "ATGTTGACGTTGACGTTGACGTTGAC"
}

# ------------------ FASTA FILE READER ------------------
def load_fasta_sequence(filepath):
    sequence_lines = []
    with open(filepath) as fh:
        for line in fh:
            if not line.startswith(">"):
                sequence_lines.append(line.strip())
    return "".join(sequence_lines)

# ------------------ DESIGN FILE PARSER ------------------
def parse_design(filepath):
    cloning_sites = []
    resistance_markers = []

    with open(filepath) as fh:
        for record in fh:
            key, value = record.strip().split(",")
            value = value.strip()

            if "Cloning" in key:
                cloning_sites.append(value)
            else:
                resistance_markers.append(value)

    return cloning_sites, resistance_markers

# ------------------ MODULE ASSEMBLERS ------------------
def assemble_mcs(enzymes):
    return "".join(RESTRICTION_DB[e] for e in enzymes if e in RESTRICTION_DB)

def assemble_resistance_genes(markers):
    return "".join(ANTIBIOTIC_DB[m] for m in markers if m in ANTIBIOTIC_DB)

# ------------------ MAIN ASSEMBLY PIPELINE ------------------
def construct_plasmid():
    insert_sequence = load_fasta_sequence("Input.fa")
    mcs_list, antibiotic_list = parse_design("Design.txt")

    mcs_region = assemble_mcs(mcs_list)
    resistance_region = assemble_resistance_genes(antibiotic_list)

    final_plasmid = (
        PLASMID_BACKBONE +
        mcs_region +
        insert_sequence +
        resistance_region
    )

    with open("Output.fa", "w") as out:
        out.write(">Universal_Plasmid\n")
        for i in range(0, len(final_plasmid), 60):
            out.write(final_plasmid[i:i + 60] + "\n")

    print("✔ Plasmid construction successful")
    print("✔ Output written to Output.fa")

# ------------------ EXECUTION ------------------
if __name__ == "__main__":
    construct_plasmid()