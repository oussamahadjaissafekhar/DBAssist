class SemiClosedInterval:
    def __init__(self, lowerBound, upperBound):
        self.lowerBound = lowerBound
        self.upperBound = upperBound
    
    
    def intersects(self, other) -> bool:
        return self.lowerBound < other.upperBound and other.lowerBound < self.upperBound
    
    def __str__(self) -> str:
        return (f'[{self.lowerBound}, {self.upperBound}[')