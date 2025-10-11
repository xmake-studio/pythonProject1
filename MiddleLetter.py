word = 'test'

num = len(word)

mid = num // 2

if num % 2 == 0:
    print(word[mid - 1] + word[mid])
else:
    print(word[mid])