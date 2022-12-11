def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)

    if n > 1:
        factors.append(n)

    return factors

def get_repeated_prime_factors(n):
    factors = prime_factors(n)
    out = []
    for factor in factors:
        if factors.count(factor) > 1 and factor not in out:
            out.append(factor)
    
    return out

def get_custom_prime_factor(n):
    factors = prime_factors(n)

    # if n in factors:
    #     raise RuntimeError(f"{n} is a prime?")
    #     factors.pop(factors.index(n))

    require_multiple = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for a in require_multiple:
        if factors.count(a):
            factors.pop(factors.index(a))
    
    factor = 1
    for f in factors:
        factor *= f

    return factor

def prime_factors_product(n):
    i = 2
    factors = 1
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors *= i
    # if n > 1:
    #     factors *= n
    return factors


def list_prod(l):
    out = 1
    for elem in l:
        out *= elem
    return out

            
if __name__ == "__main__":
    # tests
    p = 23
    number = 23*23*55*19*13*11*7*6*53*19
    print(f"before: {number}")
    assert(number % 23 == 0)
    assert(number % 11 == 0)
    assert(number % 19 == 0)
    assert(number % 7 == 0)
    assert(number % 13 == 0)
    print(f"prime factors: {prime_factors(number)}")
    factor = get_custom_prime_factor(number)
    print(f"factor: {factor}")
    new_number = number // factor
    print(f"after: {new_number}")
    assert(number % 23 == 0)
    assert(number % 11 == 0)
    assert(number % 19 == 0)
    assert(number % 7 == 0)
    assert(number % 13 == 0)
