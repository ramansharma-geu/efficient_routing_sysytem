class RouterLSA:
    def __init__(self, link, seq_num, cost):
        self.link = link
        self.seq_num = seq_num
        self.cost = cost

    def __eq__(self, other):
        return (
            isinstance(other, RouterLSA) and
            self.link == other.link and
            self.seq_num == other.seq_num and
            self.cost == other.cost
        )
    def __hash__(self):
        return hash((self.link, self.seq_num, self.cost))

    def __repr__(self):
        return f"RouterLSA(link={self.link}, seq=0x{self.seq_num:X}, cost={self.cost})"
