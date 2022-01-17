import evaluater
import sys
from distutils.log import Log

_logger = Log()

class Propability:
    def propability(self)-> float:
        pass
    def representation(self) -> str:
        pass

class Single(Propability):
    def __init__(self, p: float) -> None:
        self.p = p
        super().__init__()

    def propability(self) -> float:
        return self.p

    def representation(self) -> str:
        return str(self.p * 100)

class Intersection(Propability):
    def __init__(self, p1: Propability, p2: Propability) -> None:
        self.p1 = p1
        self.p2 = p2
        super().__init__()

    def propability(self) -> float:
        return self.p1.propability() * self.p2.propability()
    
    def representation(self) -> str:
        return "{} I {}".format(self.p1.representation(), self.p2.representation())

class Union(Propability):
    def __init__(self, p1: Propability, p2: Propability) -> None:
        self.p1 = p1
        self.p2 = p2
        super().__init__()

    def propability(self) -> float:
        return self.p1.propability() + self.p2.propability() - Intersection(self.p1, self.p2).propability()

    def representation(self) -> str:
        return "{} U {}".format(self.p1.representation(), self.p2.representation())


def _old_main():
    args = sys.argv[1:]
    props = [float(a)/100 for a in args]
    l = len(props)
    if l == 0:
        print("Usage <{}> arg1 arg2 ...".format(sys.argv[0]))
    elif l == 1:
        print("Answer is {}".format(props[0] * 100))
    else:
        p = Single(props[0])
        for arg in props[1:]:
            p = Union(p, Single(arg))
        print("Answer is {}".format(p.propability() * 100)) 

def _main():
    args = sys.argv[1:]
    query: str = None
    if args:
        query = ''.join(args)
    if not query:
        print("Usage <{}> query ...".format(sys.argv[0]))
    else:
        try:
            prop = evaluater.process_text(query)
            print("You entered {} which formats to {}".format(query, prop.representation()))
            print("{} is {}".format(prop.representation(), prop.propability() * 100))
        except Exception as e:
            _logger.error(str(e))

if __name__ == '__main__':
   _main() 