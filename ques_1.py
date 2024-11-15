"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
import math
M=1000000007

def mod_add(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a+b)%M

def mod_multiply(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a*b)%M

def mod_divide(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return mod_multiply(a, pow(b, M-2, M))

def calculate_dp(count_A, count_B, dp):

    for i in range(1,count_A+1):
        for j in range(1,count_B+1):
            if i>1:
                dp[i][j] = mod_add(dp[i][j], mod_multiply(dp[i-1][j],j))
            if j>1:
                dp[i][j] = mod_add(dp[i][j], mod_multiply(dp[i][j-1],i))
    
    
# Problem 1a
def calc_prob(alice_wins, bob_wins):
    """
    Returns:
        The probability of Alice winning alice_wins times and Bob winning bob_wins times will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.
    """
    count_A = alice_wins
    count_B = bob_wins
    dp= [[0]*(count_B+1) for _ in range(count_A+1)]
    dp[1][1]=1

    calculate_dp(count_A, count_B, dp)
    factorial_divisor = math.factorial(count_A+count_B-1)%M


    final_value = mod_divide(dp[count_A][count_B], factorial_divisor)

    return final_value
    
# Problem 1b (Expectation)      
def calc_expectation(t):
    """
    Returns:
        The expected value of sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    dp= [[0]*(t+1) for _ in range(t+1)]
    dp[1][1]=1
    calculate_dp(t,t,dp)
    expectation=0
    sum_sq=0
    f= math.factorial(t-1)%M
    for i in range(1, t):
        for j in range(1,t):
            if i+j == t:
                e=mod_multiply(dp[i][j],i-j)
                e1=mod_multiply(dp[i][j], i**2 + j**2 - 2*i*j)
                expectation= mod_add(expectation,e)
                sum_sq =mod_add(sum_sq, e1)

    expectation=mod_divide(expectation,f)
    return expectation

# Problem 1b (Variance)
def calc_variance(t):
    """
    Returns:
        The variance of sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    dp= [[0]*(t+1) for _ in range(t+1)]
    dp[1][1]=1
    calculate_dp(t,t,dp)
    expectation=0
    sum_sq=0
    f= math.factorial(t-1)%M
    for i in range(1, t):
        for j in range(1,t):
            if i+j == t:
                e=mod_multiply(dp[i][j],i-j)
                e1=mod_multiply(dp[i][j], i**2 + j**2 - 2*i*j)
                expectation= mod_add(expectation,e)
                sum_sq =mod_add(sum_sq, e1)

    expectation=mod_divide(expectation,f)
    variance=mod_add(sum_sq, -mod_multiply(expectation, expectation))
    variance=mod_divide(variance,f)
    return variance

entry_no = '2023MT60677'
a = 96
b = 77
print('Answer 1.a)')
print(f'Probability : ', end = "")
print(calc_prob(a,b))
print('Answer 1.b)')
t = 77
print(f'Expectation : {calc_expectation(t)}')
print(f'Variance : {calc_variance(t)}')
