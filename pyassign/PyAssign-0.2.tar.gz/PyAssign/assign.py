from random import randint
import sys

RANDOM_NUMS = []


class Assign:

    def assign(self, number, some_member, member_list):
        for item in member_list:
            if number == item.assignee:
                continue
            some_member.assignee = number
            break

    def assign_nums(self, member_list):
        for member in member_list:
            count = 0
            random_num = randint(0, len(member_list) - 1)
            while random_num in RANDOM_NUMS or random_num == member_list.index(member):
                random_num = randint(0, len(member_list) - 1)
                if count == 3:
                    print("Loop failed, try again!")
                    sys.exit()
                count += 1
            RANDOM_NUMS.append(random_num)
            count -= count
            Assign.assign(random_num, member, member_list)