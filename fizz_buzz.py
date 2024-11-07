def FizzBuzz(n):
    if n % 3 and n % 5:
        return "FizzBuzz"
    elif n % 3:
        return "Fizz"
    elif n % 5:
        return "Buzz"
    return n

def sort_custom (list):
    list_sorted = []
    
    for ele in list:
        is_inserted = False
        for idx, item in enumerate(list_sorted):
            if ele < item:
                list_sorted.insert(idx, ele)
                is_inserted = True
                break
                
        if not is_inserted:
            list_sorted.append(ele)
            
    return list_sorted

# def fibo(n, memo = {}):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     elif n == 2:
#         return 1
#     if n in memo:
#         return memo[n]
#     memo[n] = fibo(n-1, memo) + fibo(n-2, memo)
#     return memo[n]

def sheep(n):
    if n == 0:
        return "INSOMNIA"
    
    digits = set()
    i = 1
    while True:
        num = n * i
        for d in str(num):
            digits.add(d)
        if len(digits) == 10:
            return num
        i += 1

def main () -> str:
    # list = [11, 22, 5]

    # List.sort()
    
    # for i, ele in enumerate(List):
    #     print(i, ele)
    
    # try:
    #     n: int = int(input())
    # except:
    #     print("Please enter a number")
    #     n: int = int(input())
    
    values = [1692, 100, 0, 1, 2, 11, 1692, 163444, 206929, 459923, 691520, 40, 999993, 612112,]


    for value in values:
        result = sheep(value)
        print(f"sheep({value}) = {result}")
    
if __name__ == "__main__":
    main()
