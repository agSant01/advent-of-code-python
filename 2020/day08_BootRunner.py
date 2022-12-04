class BootRunner:
    def __init__(self, instrc_lines, start=0, end=None) -> None:
        super().__init__()
        self.instrc_lines = instrc_lines
        self.start = start
        self.end = end

        self.acc = 0
        self.visited = set()
        self.current_inst = start

    def reset(self):
        self.current_inst = self.start

    def run(self):
        while self.current_inst < len(self.instrc_lines):
            if self.current_inst in self.visited:
                # print('Repeated cmd:', data[curr_], 'Instr:', curr_)
                return None

            self.visited.add(self.current_inst)

            curr_inst = self.instrc_lines[self.current_inst]

            if curr_inst[0] == "acc":
                self.acc += curr_inst[1]
                self.current_inst += 1
            elif curr_inst[0] == "jmp":
                self.current_inst += curr_inst[1]
            elif curr_inst[0] == "nop":
                self.current_inst += 1
            else:
                print(
                    "Invalid cmd:",
                    self.instrc_lines[self.current_inst][0],
                    "Instr:",
                    self.current_inst,
                )
                return None

        return self.acc

    def switch():
        pass
