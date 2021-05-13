def pyramide(n):
    a = 3
    S = 0
    for i in range(n):
        S = S + a
        a = a + 4
    return S


def nb_etages(N):
    n = 0
    while pyramide(n+1) <= N:
        n = n + 1
    return n


def nb_etages2(N):
    n = 0

    while pyramide(n+1) <= N:
        n = n + 1
        
    return n, N - pyramide(n)


print('pyramide(0) =', pyramide(0))
print('pyramide(1) =', pyramide(1))
print('pyramide(2) =', pyramide(2))
print('pyramide(3) =', pyramide(3))
print('pyramide(22) =', pyramide(22))
print('pyramide(23) =', pyramide(23))

print('nb_etages(1000) =', nb_etages(1000))

print('nb_etages2(1000) =', nb_etages2(1000))
