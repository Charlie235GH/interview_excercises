"""
50 Technical Interview Questions in Python
Ordered by ascending skill level (Beginner → Intermediate → Advanced)
Each question designed to be solved in 1-2 minutes

Author: Interview Preparation
Date: December 11, 2025
"""

# =============================================================================
# BEGINNER LEVEL (Questions 1-15)
# =============================================================================

# Question 1: Check if a number is even or odd
def is_even(n):
    """Return True if number is even, False if odd."""
    return n % 2 == 0

# Test
print("Q1 - Is 4 even?", is_even(4))  # True
print("Q1 - Is 7 even?", is_even(7))  # False

# Question 2: Find the maximum of two numbers
def max_of_two(a, b):
    """Return the maximum of two numbers."""
    return a if a > b else b

# Test
print("Q2 - Max of 5 and 3:", max_of_two(5, 3))  # 5

# Question 3: Reverse a string
def reverse_string(s):
    """Return the reverse of a string."""
    return s[::-1]

# Test
print("Q3 - Reverse 'hello':", reverse_string("hello"))  # "olleh"

# Question 4: Count vowels in a string
def count_vowels(s):
    """Count the number of vowels in a string."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)

# Test
print("Q4 - Vowels in 'hello':", count_vowels("hello"))  # 2

# Question 5: Check if a string is palindrome
def is_palindrome(s):
    """Check if a string is a palindrome."""
    s = s.lower().replace(" ", "")
    return s == s[::-1]

# Test
print("Q5 - Is 'racecar' palindrome?", is_palindrome("racecar"))  # True

# Question 6: Calculate factorial
def factorial(n):
    """Calculate factorial of a number."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Test
print("Q6 - Factorial of 5:", factorial(5))  # 120

# Question 7: Find sum of digits
def sum_of_digits(n):
    """Find sum of digits in a number."""
    return sum(int(digit) for digit in str(abs(n)))

# Test
print("Q7 - Sum of digits in 123:", sum_of_digits(123))  # 6

# Question 8: Check if number is prime
def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Test
print("Q8 - Is 17 prime?", is_prime(17))  # True

# Question 9: Find largest element in list
def find_largest(lst):
    """Find the largest element in a list."""
    if not lst:
        return None
    return max(lst)

# Test
print("Q9 - Largest in [1,5,3,9,2]:", find_largest([1, 5, 3, 9, 2]))  # 9

# Question 10: Remove duplicates from list
def remove_duplicates(lst):
    """Remove duplicates from list while preserving order."""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Test
print("Q10 - Remove duplicates [1,2,2,3,1]:", remove_duplicates([1, 2, 2, 3, 1]))  # [1, 2, 3]

# Question 11: Convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

# Test
print("Q11 - 25°C to Fahrenheit:", celsius_to_fahrenheit(25))  # 77.0

# Question 12: Count words in a string
def count_words(s):
    """Count words in a string."""
    return len(s.split())

# Test
print("Q12 - Words in 'Hello world python':", count_words("Hello world python"))  # 3

# Question 13: Find second largest number
def second_largest(lst):
    """Find second largest number in list."""
    if len(lst) < 2:
        return None
    unique_nums = list(set(lst))
    unique_nums.sort()
    return unique_nums[-2] if len(unique_nums) >= 2 else None

# Test
print("Q13 - Second largest in [1,5,3,9,2]:", second_largest([1, 5, 3, 9, 2]))  # 5

# Question 14: Check if list is sorted
def is_sorted(lst):
    """Check if list is sorted in ascending order."""
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))

# Test
print("Q14 - Is [1,2,3,4] sorted?", is_sorted([1, 2, 3, 4]))  # True

# Question 15: Generate Fibonacci sequence
def fibonacci(n):
    """Generate first n Fibonacci numbers."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Test
print("Q15 - First 7 Fibonacci numbers:", fibonacci(7))  # [0, 1, 1, 2, 3, 5, 8]

# =============================================================================
# INTERMEDIATE LEVEL (Questions 16-35)
# =============================================================================

# Question 16: Merge two sorted lists
def merge_sorted_lists(list1, list2):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result

# Test
print("Q16 - Merge [1,3,5] and [2,4,6]:", merge_sorted_lists([1, 3, 5], [2, 4, 6]))

# Question 17: Find intersection of two lists
def list_intersection(list1, list2):
    """Find intersection of two lists."""
    return list(set(list1) & set(list2))

# Test
print("Q17 - Intersection [1,2,3] and [2,3,4]:", list_intersection([1, 2, 3], [2, 3, 4]))

# Question 18: Rotate list to the right
def rotate_right(lst, k):
    """Rotate list to the right by k positions."""
    if not lst or k == 0:
        return lst
    k = k % len(lst)
    return lst[-k:] + lst[:-k]

# Test
print("Q18 - Rotate [1,2,3,4,5] right by 2:", rotate_right([1, 2, 3, 4, 5], 2))

# Question 19: Find missing number in sequence
def find_missing_number(lst, n):
    """Find missing number in sequence 1 to n."""
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(lst)
    return expected_sum - actual_sum

# Test
print("Q19 - Missing number in [1,2,4,5] (n=5):", find_missing_number([1, 2, 4, 5], 5))

# Question 20: Group anagrams
def group_anagrams(words):
    """Group words that are anagrams."""
    from collections import defaultdict
    groups = defaultdict(list)
    
    for word in words:
        key = ''.join(sorted(word.lower()))
        groups[key].append(word)
    
    return list(groups.values())

# Test
print("Q20 - Group anagrams ['eat','tea','tan','ate','nat']:")
print(group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat']))

# Question 21: Find first non-repeating character
def first_non_repeating(s):
    """Find first non-repeating character in string."""
    char_count = {}
    
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    for char in s:
        if char_count[char] == 1:
            return char
    return None

# Test
print("Q21 - First non-repeating in 'abccba':", first_non_repeating('abccba'))

# Question 22: Binary search
def binary_search(arr, target):
    """Binary search for target in sorted array."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Test
print("Q22 - Binary search for 7 in [1,3,5,7,9]:", binary_search([1, 3, 5, 7, 9], 7))

# Question 23: Valid parentheses
def is_valid_parentheses(s):
    """Check if parentheses are valid."""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return not stack

# Test
print("Q23 - Valid parentheses '({[]})':", is_valid_parentheses('({[]})'))

# Question 24: Longest common prefix
def longest_common_prefix(strs):
    """Find longest common prefix among strings."""
    if not strs:
        return ""
    
    min_len = min(len(s) for s in strs)
    
    for i in range(min_len):
        char = strs[0][i]
        if not all(s[i] == char for s in strs):
            return strs[0][:i]
    
    return strs[0][:min_len]

# Test
print("Q24 - Common prefix ['flower','flow','flight']:", longest_common_prefix(['flower', 'flow', 'flight']))

# Question 25: Remove duplicates from sorted array
def remove_duplicates_sorted(nums):
    """Remove duplicates from sorted array in-place."""
    if not nums:
        return 0
    
    write_index = 1
    for read_index in range(1, len(nums)):
        if nums[read_index] != nums[read_index - 1]:
            nums[write_index] = nums[read_index]
            write_index += 1
    
    return write_index

# Test
test_arr = [1, 1, 2, 2, 3, 4, 4]
length = remove_duplicates_sorted(test_arr)
print(f"Q25 - After removing duplicates: {test_arr[:length]}")

# Question 26: Two sum problem
def two_sum(nums, target):
    """Find indices of two numbers that add up to target."""
    num_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    
    return []

# Test
print("Q26 - Two sum [2,7,11,15] target 9:", two_sum([2, 7, 11, 15], 9))

# Question 27: Reverse words in string
def reverse_words(s):
    """Reverse the order of words in a string."""
    return ' '.join(s.split()[::-1])

# Test
print("Q27 - Reverse words 'hello world python':", reverse_words('hello world python'))

# Question 28: Valid sudoku checker (simplified)
def is_valid_sudoku_row(row):
    """Check if a sudoku row is valid."""
    nums = [x for x in row if x != '.']
    return len(nums) == len(set(nums))

# Test
print("Q28 - Valid sudoku row ['5','3','.','.','7','.']:", is_valid_sudoku_row(['5','3','.','.','7','.']))

# Question 29: Count and say sequence
def count_and_say(n):
    """Generate the nth term of count-and-say sequence."""
    if n == 1:
        return "1"
    
    result = "1"
    for _ in range(n - 1):
        next_result = ""
        i = 0
        while i < len(result):
            count = 1
            digit = result[i]
            while i + 1 < len(result) and result[i + 1] == digit:
                count += 1
                i += 1
            next_result += str(count) + digit
            i += 1
        result = next_result
    
    return result

# Test
print("Q29 - Count and say n=4:", count_and_say(4))

# Question 30: Matrix transpose
def transpose_matrix(matrix):
    """Transpose a matrix."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    
    transposed = [[0] * rows for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    
    return transposed

# Test
matrix = [[1, 2, 3], [4, 5, 6]]
print("Q30 - Transpose [[1,2,3],[4,5,6]]:", transpose_matrix(matrix))

# Question 31: Find peak element
def find_peak(nums):
    """Find a peak element in array."""
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:
            right = mid
        else:
            left = mid + 1
    
    return left

# Test
print("Q31 - Peak element index in [1,2,3,1]:", find_peak([1, 2, 3, 1]))

# Question 32: Implement stack using lists
class Stack:
    """Stack implementation using lists."""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0

# Test
stack = Stack()
stack.push(1)
stack.push(2)
print("Q32 - Stack peek:", stack.peek())  # 2

# Question 33: Generate Pascal's triangle
def generate_pascals_triangle(num_rows):
    """Generate Pascal's triangle."""
    triangle = []
    
    for i in range(num_rows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i-1][j-1] + triangle[i-1][j]
        triangle.append(row)
    
    return triangle

# Test
print("Q33 - Pascal's triangle (5 rows):", generate_pascals_triangle(5))

# Question 34: Climbing stairs (dynamic programming)
def climb_stairs(n):
    """Number of ways to climb n stairs (1 or 2 steps at a time)."""
    if n <= 2:
        return n
    
    prev1, prev2 = 1, 2
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev1, prev2 = prev2, current
    
    return prev2

# Test
print("Q34 - Ways to climb 5 stairs:", climb_stairs(5))

# Question 35: Find majority element
def majority_element(nums):
    """Find the majority element (appears more than n/2 times)."""
    count = 0
    candidate = None
    
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    
    return candidate

# Test
print("Q35 - Majority element [3,2,3]:", majority_element([3, 2, 3]))

# =============================================================================
# ADVANCED LEVEL (Questions 36-50)
# =============================================================================

# Question 36: Longest substring without repeating characters
def length_of_longest_substring(s):
    """Find length of longest substring without repeating characters."""
    char_map = {}
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Test
print("Q36 - Longest substring 'abcabcbb':", length_of_longest_substring('abcabcbb'))

# Question 37: Merge intervals
def merge_intervals(intervals):
    """Merge overlapping intervals."""
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        if current[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], current[1])
        else:
            merged.append(current)
    
    return merged

# Test
print("Q37 - Merge intervals [[1,3],[2,6],[8,10]]:", merge_intervals([[1,3],[2,6],[8,10]]))

# Question 38: Quick sort implementation
def quicksort(arr):
    """Quick sort implementation."""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

# Test
print("Q38 - Quick sort [3,6,8,10,1,2,1]:", quicksort([3,6,8,10,1,2,1]))

# Question 39: Decode ways (dynamic programming)
def num_decodings(s):
    """Number of ways to decode a string of digits."""
    if not s or s[0] == '0':
        return 0
    
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    
    for i in range(2, n + 1):
        if s[i-1] != '0':
            dp[i] += dp[i-1]
        
        if 10 <= int(s[i-2:i]) <= 26:
            dp[i] += dp[i-2]
    
    return dp[n]

# Test
print("Q39 - Decode ways '226':", num_decodings('226'))

# Question 40: LRU Cache implementation
class LRUCache:
    """LRU Cache implementation."""
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)

# Test
lru = LRUCache(2)
lru.put(1, 1)
lru.put(2, 2)
print("Q40 - LRU get(1):", lru.get(1))  # 1

# Question 41: Valid binary search tree
class TreeNode:
    """Binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_valid_bst(root):
    """Check if binary tree is valid BST."""
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and 
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))

# Test (create simple BST)
root = TreeNode(5)
root.left = TreeNode(3)
root.right = TreeNode(8)
print("Q41 - Is valid BST:", is_valid_bst(root))  # True

# Question 42: Coin change problem
def coin_change(coins, amount):
    """Minimum coins needed to make amount."""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

# Test
print("Q42 - Coin change [1,3,4] amount 6:", coin_change([1, 3, 4], 6))

# Question 43: Product of array except self
def product_except_self(nums):
    """Product of array except self without division."""
    n = len(nums)
    result = [1] * n
    
    # Left pass
    for i in range(1, n):
        result[i] = result[i-1] * nums[i-1]
    
    # Right pass
    right_product = 1
    for i in range(n-1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result

# Test
print("Q43 - Product except self [1,2,3,4]:", product_except_self([1,2,3,4]))

# Question 44: Spiral matrix
def spiral_matrix(matrix):
    """Return matrix elements in spiral order."""
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Right
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1
        
        # Down
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        
        if top <= bottom:
            # Left
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
        
        if left <= right:
            # Up
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    
    return result

# Test
matrix = [[1,2,3],[4,5,6],[7,8,9]]
print("Q44 - Spiral matrix:", spiral_matrix(matrix))

# Question 45: Sliding window maximum
def max_sliding_window(nums, k):
    """Maximum in each sliding window of size k."""
    from collections import deque
    
    dq = deque()
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Test
print("Q45 - Max sliding window [1,3,-1,-3,5,3,6,7] k=3:", max_sliding_window([1,3,-1,-3,5,3,6,7], 3))

# Question 46: Regular expression matching (simplified)
def is_match(text, pattern):
    """Simple regex matching with . and *"""
    def dp(i, j):
        if j == len(pattern):
            return i == len(text)
        
        first_match = (i < len(text) and 
                      (pattern[j] == text[i] or pattern[j] == '.'))
        
        if j + 1 < len(pattern) and pattern[j + 1] == '*':
            return (dp(i, j + 2) or 
                   (first_match and dp(i + 1, j)))
        else:
            return first_match and dp(i + 1, j + 1)
    
    return dp(0, 0)

# Test
print("Q46 - Regex match 'aa' with 'a*':", is_match('aa', 'a*'))

# Question 47: Minimum window substring
def min_window(s, t):
    """Find minimum window substring containing all characters of t."""
    if not s or not t:
        return ""
    
    from collections import Counter
    
    dict_t = Counter(t)
    required = len(dict_t)
    formed = 0
    window_counts = {}
    
    l, r = 0, 0
    ans = (float("inf"), 0, 0)
    
    while r < len(s):
        character = s[r]
        window_counts[character] = window_counts.get(character, 0) + 1
        
        if character in dict_t and window_counts[character] == dict_t[character]:
            formed += 1
        
        while l <= r and formed == required:
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
            
            character = s[l]
            window_counts[character] -= 1
            if character in dict_t and window_counts[character] < dict_t[character]:
                formed -= 1
            l += 1
        
        r += 1
    
    return "" if ans[0] == float("inf") else s[ans[1]:ans[2] + 1]

# Test
print("Q47 - Min window 'ADOBECODEBANC' for 'ABC':", min_window('ADOBECODEBANC', 'ABC'))

# Question 48: Word ladder length
def ladder_length(begin_word, end_word, word_list):
    """Find shortest transformation sequence length."""
    if end_word not in word_list:
        return 0
    
    from collections import deque
    
    queue = deque([(begin_word, 1)])
    word_set = set(word_list)
    visited = set([begin_word])
    
    while queue:
        word, level = queue.popleft()
        
        if word == end_word:
            return level
        
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, level + 1))
    
    return 0

# Test
print("Q48 - Word ladder 'hit' to 'cog':", ladder_length('hit', 'cog', ['hot','dot','dog','lot','log','cog']))

# Question 49: Serialize and deserialize binary tree
class Codec:
    """Serialize and deserialize binary tree."""
    
    def serialize(self, root):
        def preorder(node):
            if not node:
                vals.append('#')
            else:
                vals.append(str(node.val))
                preorder(node.left)
                preorder(node.right)
        
        vals = []
        preorder(root)
        return ','.join(vals)
    
    def deserialize(self, data):
        def build():
            val = next(vals)
            if val == '#':
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        
        vals = iter(data.split(','))
        return build()

# Test
codec = Codec()
tree = TreeNode(1)
tree.left = TreeNode(2)
tree.right = TreeNode(3)
serialized = codec.serialize(tree)
print("Q49 - Serialized tree:", serialized)

# Question 50: Median of two sorted arrays
def find_median_sorted_arrays(nums1, nums2):
    """Find median of two sorted arrays in O(log(m+n))."""
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    low, high = 0, m
    
    while low <= high:
        partition_x = (low + high) // 2
        partition_y = (m + n + 1) // 2 - partition_x
        
        max_left_x = float('-inf') if partition_x == 0 else nums1[partition_x - 1]
        min_right_x = float('inf') if partition_x == m else nums1[partition_x]
        
        max_left_y = float('-inf') if partition_y == 0 else nums2[partition_y - 1]
        min_right_y = float('inf') if partition_y == n else nums2[partition_y]
        
        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            if (m + n) % 2 == 0:
                return (max(max_left_x, max_left_y) + min(min_right_x, min_right_y)) / 2
            else:
                return max(max_left_x, max_left_y)
        elif max_left_x > min_right_y:
            high = partition_x - 1
        else:
            low = partition_x + 1

# Test
print("Q50 - Median of [1,3] and [2]:", find_median_sorted_arrays([1, 3], [2]))

print("\n" + "="*80)
print("All 50 questions completed! Practice these regularly for interview success.")
print("="*80)
