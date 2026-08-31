"""Question 1: Check if a number is even or odd"""

def is_even(n: int) -> bool:
    return n % 2 == 0

print(11, is_even(11))
print(22, is_even(22))

"""# Question 2: Find the maximum of two numbers"""
print(max(1,2))

"""Question 3: Reverse a string"""
s = "Hello Python!"
print(s[::-1])

"""Question 4: Count vowels in a string"""
def vowel_cnt(s: str) -> int:
    vowels = ["a","e","i","o","u"]
    return sum(1 for c in s.lower() if c in vowels)

print("vowel cnt: ", vowel_cnt("Hello, how are you?"))

"""Question 5: Check if a string is palindrome"""
def is_palindrome(s:str) -> bool:
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print("palindrome: ", is_palindrome("Hello olleh"))

"""Question 6: Calculate factorial"""
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n-1)

assert factorial(5) == 1*2*3*4*5

def factorial1(n):
    result = 1
    for c in range(2,n+1):
        result *=c
    return result

assert factorial1(5) == 1*2*3*4*5


"""Question 7: Find sum of digits 123 --> 6"""
def digit_sum(n: int) -> int:
    return sum(int(c) for c in str(abs(n)))

print("digit_sum:", digit_sum(123))

"""Question 8: Check if number is prime"""
def is_prime(n: int) -> bool:
    for i in range(2, ((n+1)+1)//2):
        if n % i == 0:
            return False
    return True

print("is_prime:", is_prime(8))

"""Question 9: Find largest element in list"""
def largest(li: list) -> int:
    if not li:
        return None
    return max(li)

#li = [1,2,3,4,5,6,7,-1]
li = []
print("largest: ", largest(li))

"""Question 10: Remove duplicates from list"""
def list_dedup(li: list) -> list:
    se = set()
    for c in li:
        if c not in se:
            se.add(c)
    return list(se)

print("list_dedup:", list_dedup([1,2,3,4,5,6,7,-1, 7]))

li = [1,2,3,4,5,6,7,-1, 7]
li = list(dict.fromkeys(li)) # keeping the order, unlike list(set(li))
print("dict.from_key(): ", li)