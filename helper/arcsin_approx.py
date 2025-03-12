from functools import cache

def arcsin_dl_fact(n: int):
  return facto(2*n)/(2**(2*n))/(facto(n)**2)

@cache
def facto(x: int):
  return facto(x - 1) * x if x != 0 else 1