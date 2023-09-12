from pathlib import Path
from dataclasses import dataclass


@dataclass
class ColinearBlock:
    """
    dataclass to store a ColinearBlock for easier access.
    """

    genome1: str
    genome1_pos: str
    genome1_strand: str
    genome2: str
    genome2_pos: str
    genome2_strand: str

def read_genome_fa(fasta_file: Path) -> str:
    """
    Reads fasta file of wolbachia genome. expects only one fasta entry

    Args:
        fasta_file (Path): Path to wolbachia fasta

    Returns:
        str: Fasta string
    """
    with fasta_file.open(mode="r") as f:
        lines = f.readlines()

    seq = "".join(line.strip() for line in lines if not line.startswith(">"))
    return seq

def read_xmfa(xmfa_file: Path) -> list[ColinearBlock]:
    """
    Reads xmfa entries only file and returns list of tuples of colinear blocks

    Args:
        xmfa_file (Path): Path to xmfa colinear block entries only file

    Returns:
        list[tuple[tuple]]: List of tuples of colinear blocks
                        ex) [((wRi,1,100), (wmel,5,100))...]
    """
    with open(xmfa_file, "r") as f:
        lines = f.readlines()

    out = []
    for i, line in enumerate(lines):
        if line.strip().startswith("="):
            prev_two_lines = [lines[i - 2], lines[i - 1]]
            if all([prev_line.startswith(">") for prev_line in prev_two_lines]):
                prev_two_lines = [
                    prev_line.strip().split() for prev_line in prev_two_lines
                ]
                block = ColinearBlock(
                    genome1="wmel",
                    genome1_pos=prev_two_lines[0][1],
                    genome1_strand=prev_two_lines[0][2],
                    genome2="wri",
                    genome2_pos=prev_two_lines[1][1],
                    genome2_strand=prev_two_lines[1][2],
                )
                out.append(block)
    return out

def make_sub(seqA: str, seqB: str, block: ColinearBlock) -> None:
    '''
    This is for site-specific recombination.
    Recombination(Sequence A, Sequence B, which Sequence(should be string i.e = "A"), Position1 of Sequence A, Position2 of Sequence B)
    '''
    whichSeq = "B"

    print(block)

    gen1Block = block.genome1_pos
    coordA = gen1Block.replace(':', ' ').replace('-', ' ').split()
    gen2Block = block.genome2_pos
    coordB = gen2Block.replace(':', ' ').replace('-', ' ').split()
    

    # Subtract 1 from x because python starts counting from 0
    recombPosone = tuple(map(lambda i, j: i - j, (int(coordA[1]),int(coordA[2])), (1,0))) 
    recombPostwo = tuple(map(lambda i, j: i - j, (int(coordB[1]),int(coordB[2])), (1,0)))

    #Choosing the donor
    if whichSeq == "A":
        replaceSeq = seqA[recombPosone[0]:recombPosone[1]]
        recombSeq = seqB[:recombPostwo[0]] + replaceSeq + seqB[recombPostwo[1]:]
        with open("wMelInwRitestA.fa", "w") as f:
            f.write(">wMelInwRitestA\n")
            f.write(recombSeq)
    else:
        replaceSeq = seqB[recombPostwo[0]:recombPostwo[1]]
        recombSeq = seqA[:recombPosone[0]] + replaceSeq + seqB[recombPosone[1]:]
        with open("wRiInwMeltestB.fa", "w") as f:
            f.write(">wRiInwMeltestB\n")
            f.write(recombSeq)



    # return(replaceSeq, recombPosone, recombPostwo, recombSeq)
    return(recombPosone, recombPostwo)

if __name__ == "__main__":
    blocks = read_xmfa("./data/entries_only.xmfa")
    wmel = read_genome_fa(Path("/Users/kerney/RussellLab/RecombinationSims/wolb-sim/genomes/wMelgenome.fna"))
    wri = read_genome_fa(Path("/Users/kerney/RussellLab/RecombinationSims/wolb-sim/genomes/wRigenome.fna"))
    print(make_sub(wmel, wri, blocks[0]))
    