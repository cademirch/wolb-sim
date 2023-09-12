from pathlib import Path
from dataclasses import dataclass


@dataclass
class ColinearBlock:
    """
    dataclass to store a ColinearBlock for easier access.
    """

    genome1: str
    genome1_pos: tuple
    genome1_strand: str
    genome2: str
    genome2_pos: tuple
    genome2_strand: str

    def __repr__(self) -> str:
        return (
            f"{self.genome1}_{'-'.join(map(str, self.genome1_pos))}_"
            + f"{self.genome1_strand}-{self.genome2}_"
            + f"{'-'.join(map(str, self.genome2_pos))}_{self.genome2_strand}"
        )


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
    Reads xmfa entries only file and returns list of colinear blocks

    Args:
        xmfa_file (Path): Path to xmfa colinear block entries only file

    Returns:
        list[ColinearBlock]
    """
    with xmfa_file.open(mode="r") as f:
        lines = f.readlines()

    out = []
    for i, line in enumerate(lines):
        if line.strip().startswith("="):
            prev_two_lines = [lines[i - 2], lines[i - 1]]
            if all([prev_line.startswith(">") for prev_line in prev_two_lines]):
                prev_two_lines = [
                    prev_line.strip().split() for prev_line in prev_two_lines
                ]
                genome1_pos = tuple(
                    map(
                        lambda x: int(x) - 1,
                        prev_two_lines[0][1].split(":")[1].split("-"),
                    )
                )
                genome2_pos = tuple(
                    map(
                        lambda x: int(x) - 1,
                        prev_two_lines[1][1].split(":")[1].split("-"),
                    )
                )
                block = ColinearBlock(
                    genome1="wmel",
                    genome1_pos=genome1_pos,
                    genome1_strand=prev_two_lines[0][2],
                    genome2="wri",
                    genome2_pos=genome2_pos,
                    genome2_strand=prev_two_lines[1][2],
                )

                out.append(block)
    return out


def make_sub(g1: str, g2: str, block: ColinearBlock) -> None:
    print(block)
    # print(g1, g2)
    if block.genome1_strand == block.genome2_strand:
        print("hi")
        if block.genome1_pos[0] == 0 and block.genome2_pos[0] == 0:
            new_g1 = (
                g2[block.genome2_pos[0] : block.genome2_pos[1]]
                + g1[block.genome1_pos[1] :]
            )
            print("hi")
            new_g2 = (
                g1[block.genome1_pos[0] : block.genome1_pos[1]]
                + g2[block.genome2_pos[1] :]
            )
        else:
            pass
    with open("test.fa", "w") as f:
        f.write(">test\n")
        f.write(new_g1)


if __name__ == "__main__":
    blocks = read_xmfa(Path("./data/entries_only.xmfa"))
    wmel = read_genome_fa(Path("data/wmel.fa"))
    wri = read_genome_fa(Path("data/wri.fa"))
    make_sub(wmel, wri, blocks[0])
