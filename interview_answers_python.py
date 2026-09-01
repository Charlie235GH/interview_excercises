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

"""Question 11: Convert Celsius to Fahrenheit"""
def c2f(celsius: float) -> float:
    return celsius*1.8+32

print("c2f:",c2f(0))

"""Question 12: Count words in a string"""
def word_count(word:str) -> int:
    return len(word.split())

c = "hello" + " " + "John" # slow performance with new object, immutable

print(" ".join(["My", "sentence", "is", "brief."]))

print(", ".join(str(c) for c in [1,2,3,4,50]))

print("word_count: ", word_count("Hello, this is my sentence!"))

print("Hello this is my sentence in my example")

"""Question 13: Find second largest number"""

def max2_1(li: list):
    m1 = max(li)
    m2 = max([c for c in li if c < m1])
    return m2

li = [1,2,3,4,5]
print("max2_1:", max2_1(li))

# or

def max2_2(li: list, k: int):
    li_unique = list(set(li)) # deduplicate
    li_unique.sort() # sort
    return li_unique[-k] # take 2nd last

li = [1,2,3,4,5]
print("max2_2:", max2_2(li, 3))

"""Question 14: Check if list is sorted"""
def is_sorted1(li: list) -> bool:
    li_sorted = li.copy()
    li_sorted.sort()

    for i in range(len(li)):
        if li[i] != li_sorted[i]:
            return False
    return True

print("is_sorted1:", is_sorted1([1,2,3,4,5,5,4]))

# or
def is_sorted2(li: list) -> bool:
    return all(li[i] <= li[i+1] for i in range(len(li)-1))

print("is_sorted2:", is_sorted2([1,2,3,4,5,5,4]))

li1 = [1,2,3,4,5,1,2,3,4,5]
li2 = li1.copy()
li2.sort()
print("sorted lists: ", li1, li2)

"""Question 15: Generate Fibonacci sequence"""
def fibonacci(n:int) -> int:
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:  
        return [0, 1]

    fib = [0, 1]
    for c in range(2, n):
        fib.append(fib[-2] + fib[-1])
    return fib


print("fibonacci:", fibonacci(4))

"""Question 16: Merge two sorted lists"""
def merge_sorted_list(li1: list, li2: list) -> list:
    li1_pos = 0
    li2_pos = 0
    li_m = []
    for i in range(len(li1) + len(li2)):
        if li1_pos < len(li1) and li2_pos < len(li2):
            if li1[li1_pos] < li2[li2_pos]:
                li_m.append(li1[li1_pos])
                li1_pos +=1
            else:
                li_m.append(li2[li2_pos])
                li2_pos +=1
        elif li1_pos < len(li1):
            li_m.append(li1[li1_pos])
            li1_pos +=1
        else:
            li_m.append(li2[li2_pos])
            li2_pos +=1

    return li_m

print("merge_sorted_list:", merge_sorted_list([1,1,1,2,3,3,3,4,5,6], [1,2,3,3,3,4,5,5,5,6,6,7,8]))

"""Question 17: Find intersection of two lists"""
def list_intersect(li1: list, li2: list) -> list:
    se1 = set(li1)
    se2 = set(li2)
    se3 = se1.intersection(se2)
    return list(se3)

print("list_intersect:", list_intersect([1,2,3,4,5,6],[-1, -2, -3, -4,5,6, 7]))

"""Question 18: Rotate list to the right"""
def list_rotate_right(li: list, k: int) -> list:
    if not li or len(li) == 0:
        return li
    k = k % len(li) # in case k is larger than list lenght
    return li[len(li)-k:] + li[:len(li)-k]

print("list_rotate_right:", list_rotate_right([1,2,3,4,5,6,7,8], 3))

"""Question 19: Find missing number in sequence"""
def find_missing(li:list) -> int:
    mi = min(li)
    ma = max(li)
    sum_full = sum(c for c in range(mi,ma+1))
    return sum_full - sum(li)

print("find_missing:", find_missing([1,2,3,4,5,6,7,8,9,11,12]))

def find_missings(li:list) -> set:
    se_part = set(li)
    se_full = set(range(li[0],li[-1]))
    return se_full.difference(se_part)

print("find_missings:", find_missings([1,2,3,4,5,6,7,8,9,11,12,13,15,16]))

"""Question 20: Group anagrams..."""

"""Question 21: Find first non-repeating character"""
def nrc(s: str) -> str | None:
    for i in range(len(s)):
        if s[i] not in s[:i] + s[i+1:]:
            return s[i]
    return None

print("nrc: ", nrc("hheelloo  JJhonnk"))

"""Question 22: Binary search"""

"""Question 23: Valid parentheses"""
def is_valid_parentheses(s: str) -> bool:
    return True

print("is_valid_parentheses: ", is_valid_parentheses("'hello'"))