# -*- coding: utf-8 -*-
import random
from math import ceil
from decimal import Decimal, getcontext

# Définir une précision suffisante
getcontext().prec = 30

def generate_polynomial(secret, degree, modulus):
    """Génère un polynôme de degré 'degree' avec le terme constant égal au 'secret'"""
    coefficients = [secret]
    for _ in range(degree):
        coefficients.append(random.randint(1, modulus-1))
    return coefficients

def evaluate_polynomial(coefficients, x, modulus):
    """Évalue le polynôme aux coefficients donnés à la position x"""
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * x + coefficient) % modulus
    return result

def generate_shares(secret, n, k, modulus):
    """Génère n parts basées sur un secret avec un seuil k"""
    coefficients = generate_polynomial(secret, k-1, modulus)
    shares = []
    for i in range(1, n+1):
        shares.append((i, evaluate_polynomial(coefficients, i, modulus)))
    return shares

def reconstruct_secret(shares, modulus):
    """Reconstruit le secret à partir d'un ensemble de parts"""
    x_values = [x for x, _ in shares]
    y_values = [y for _, y in shares]
    
    # Utilisation de l'interpolation de Lagrange
    secret = 0
    for i, (xi, yi) in enumerate(shares):
        numerator = Decimal(1)
        denominator = Decimal(1)
        
        for j, xj in enumerate(x_values):
            if i != j:
                numerator *= Decimal(xj)
                denominator *= Decimal(xj - xi)
        
        lagrange = (numerator / denominator) * Decimal(yi)
        secret += int(lagrange) % modulus
    
    return secret % modulus

# Exemple d'utilisation
prime = 2**31 - 1  # Un grand nombre premier
secret = 1234
n = 6  # Nombre total de parts
k = 3  # Seuil minimum requis

shares = generate_shares(secret, n, k, prime)
print(f"Parts générées: {shares}")

# Reconstruction avec seulement k parts
some_shares = shares[:k]
reconstructed_secret = reconstruct_secret(some_shares, prime)
print(f"Secret reconstruit: {reconstructed_secret}")