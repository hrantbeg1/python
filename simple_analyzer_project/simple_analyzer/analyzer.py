class Analyzer:
    def __init__(self):
        self.data = []

    def add_number(self, x):
        self.data.append(int(x))

    def even_count(self):
        return sum(1 for v in self.data if v % 2 == 0)

    def odd_count(self):
        return sum(1 for v in self.data if v % 2 != 0)

    def highest_number(self):
        return max(self.data) if self.data else None

    def increasing_pairs(self):
        c = 0
        for i in range(1, len(self.data)):
            if self.data[i] > self.data[i-1]:
                c += 1
        return c
