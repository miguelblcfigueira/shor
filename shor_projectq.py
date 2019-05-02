from random import randint
import math
from projectq import *
from projectq.ops import *
from projectq.libs.math import *
from projectq.meta import *
from fractions import Fraction


def printRegister(register):
  for q in range(len(register)):
    print(int(register[q]))

def registerToInt(register):
  x = 0
  for b in reversed(register):
    x = (x << 1) | int(b)
  return x

def findPeriod(a, N):
  m = math.floor(math.log2(N ** 2))
  if 2 ** m < N ** 2:
    m = m+1
  print(">> Computed m=" + str(m))
  
  n = math.floor(math.log2(N))
  if 2 ** n <= N:
    n = n+1
  print(">> Computed n=" + str(n))
  
  # create a main compiler engine
  eng = MainEngine()

  # allocate one register
  reg = eng.allocate_qureg(m+n)
  X | reg[m]

  # Hadamard gate
  All(H) | reg[:m]
  
  # Apply f
  for j in range(m):
    aj = pow(a, 2 ** j, N)
    with Control(eng, reg[m-j-1]):
      MultiplyByConstantModN(aj, N) | reg[m:]

  # measure1
  All(Measure) | reg[m:]

  # QFT inverse
  with Dagger(eng):
    QFT | reg[:m]

  # measure2
  All(Measure) | reg[:m]

  eng.flush()
  
  topReg = registerToInt(reg[:m])
  f = Fraction(topReg, 2**m)
  s = f.denominator
  while ((a ** s) - 1) % N != 0 and s < N:
    s = s + s
  
  if s < N:
    print("Period:")
    print(s)
    return s
  else:
    print("RIP")
    return None
  
def shor(N):
  factorFound = False
  while not factorFound:    
    print(">> Picking random a...")
    a = randint(0,N)
    print(">> Picked a=" + str(a))

    gcd = math.gcd(a, N)
    print(">> gcd(" + str(a) + "," + str(N) + ")=" + str(gcd))
    if gcd != 1:
      print("> Random number has a nontrivial factor of " + str(N))
      return gcd


    print(">> Quantum part: Computing period of " + str(a) + "...")
    r = findPeriod(a, N)

    if r % 2 != 0:
      print("> The number picked has odd period. Going to pick another...")
      continue

    power = int(pow(a, r/2))
    if power + 1 % N == 0:
      print("The picked number gives us a trivial factor. Picking another one...")
      continue

    factor1 = math.gcd(power + 1, N);
    factor2 = math.gcd(power - 1, N);
    print("Computed factors: " + str(factor1) + " and " + str(factor2))

    #return non trivial factor
    if factor1 != 1:
      return factor1;
    return factor2;


print(shor(15))