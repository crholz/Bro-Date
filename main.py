"""
Bro Date Generator
"""

import pickle
import pandas
import random
import os

def print_options():
    print("[1] Import Names")
    print("[2] Select File")
    print("[3] Insert Pairs")
    print("[4] Generate Groups")
    print("[5] Visualize Table")
    print("[6] Exit")


def findKey(diction, user_val):
    for key, value in diction.items():
        if value == user_val:
            return key

# Start of Main
selected = ""
file_data = [[], [], dict({})]


while (1):
    # Print the options
    print_options()

    user_choice = 0
    user_choice = int(input("Choice: "))


    while (user_choice not in [1, 2, 3, 4, 5, 6]):
        print("Invalid Choice")
        print_options()
        user_choice = input(user_choice)

    if (user_choice == 1):
        print("Importing names... Return to exit")
        count = 0
        name = ""
        name = input("Enter Name:")
        while (name != ""):
            if (name not in file_data[0]):
                file_data[0].append(name)
                file_data[2][name] = count
                count = count + 1
            name = input("Enter Name:")

        print("List of Names Saved")

        for x in range(0, len(file_data[0])):
            new_arr = []
            for y in range(0, len(file_data[0])):
                if (x == y):
                    new_arr.append(1)

                else:
                    new_arr.append(0)

            file_data[1].append(new_arr)

        data_file = input("Enter saved file name: ")
        while (data_file == ""):
            data_file = input("Enter saved file name: ")

        pickle.dump(file_data, open("{}.bdate".format(data_file), 'wb'))

    elif (user_choice == 2):
        print("Select File to load...")
        count = 1
        mem = dict({})
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if(".bdate" in f):
                print("[{}] {}".format(count, f))
                mem[count] = f
                count = count + 1

        user_in = int(input("File Choice: "))
        while (user_in not in mem.keys()):
            print("Invalid Choice")
            user_in = int(input("File Choice: "))

        file_data = pickle.load(open(mem[user_in], "rb"))
        selected = mem[user_in]
        print("Data Loaded")

    elif (user_choice == 3):
        if (selected == ""):
            print("No File Selected")

        else:
            first_name = "first"
            while (first_name != ""):
                print("Press Enter to Exit...")
                first_name = input("Enter the first name: ")
                if (first_name == ""):
                    print_options()
                    break

                second_name = input("Enter the second name: ")
                if (second_name == ""):
                    print_options()
                    break

                if (first_name in file_data[0] and second_name in file_data[0]):
                    file_data[1][file_data[2][first_name]][file_data[2][second_name]] = 1
                    file_data[1][file_data[2][second_name]][file_data[2][first_name]] = 1
                    pickle.dump(file_data, open("{}".format(selected), 'wb'))
                    print("Data Updated...")

                else:
                    if (first_name not in file_data[0]):
                        print("{} not found...".format(first_name))

                    if (second_name not in file_data[0]):
                        print("{} not found...".format(second_name))


    elif (user_choice == 4):
        used_names = []
        saved_file = open("Generated Pairs.txt", "a+")
        if (selected == ""):
            print("No File Selected")

        else:
            for name in file_data[0]:
                empty_locs = []
                emp_count = 0

                # Ignore if name is already used
                if name in used_names:
                    continue

                else:
                    # Create an array of all of the empty locations
                    for element in file_data[1][file_data[2][name]]:
                        if element == 0:
                            empty_locs.append(emp_count)

                        emp_count = emp_count + 1

                    # Generate Pair
                    # Find how many open slots
                    open_slots = len(empty_locs)

                    if open_slots == 0:
                        print("{} has had a date with everyone...".format(name))

                    else:
                        # Generate a random number
                        idx = random.randint(0, open_slots - 1)

                        # Find the val to be used
                        val = empty_locs[idx]

                        paired_name = findKey(file_data[2], val)

                        while (paired_name in used_names and len(used_names) < 18):
                            # Generate a random number
                            idx = random.randint(0, open_slots - 1)

                            # Find the val to be used
                            val = empty_locs[idx]

                            paired_name = findKey(file_data[2], val)


                        used_names.append(name)
                        used_names.append(paired_name)

                        file_data[1][file_data[2][name]][file_data[2][paired_name]] = 1
                        file_data[1][file_data[2][paired_name]][file_data[2][name]] = 1
                        pickle.dump(file_data, open("{}".format(selected), 'wb'))

                        print(name + " + " + paired_name)
                        print("-----------")
                        saved_file.write(name + " + " + paired_name + "\n")
                        saved_file.write("-----------\n")

        saved_file.close()



    elif (user_choice == 6):
        break

    elif (user_choice == 5):
        if (selected != ""):
            print("\t\t", end = '')
            for name in file_data[0]:
                print(name + "\t\t", end='')

            print("")
            count = 0
            for name in file_data[0]:
                print(name + "\t\t", end = '')
                for number in file_data[1][count]:
                    print(str(number) + "\t\t", end = '')

                count = count + 1
                print("")

        else:
            print("No Data Selected....")
