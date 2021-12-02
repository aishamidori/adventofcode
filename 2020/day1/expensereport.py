report = open('adventofcode1.txt')
nums = {}
for num_str in report:
    nums[int(num_str)] = True

for num1 in nums.keys():
    for num2 in nums.keys():
        if 2020 - num1 - num2 in nums:
            print('found', num1,num2, 2020-num1 - num2)
            print('result', num1 * num2 * (2020-num1-num2))
