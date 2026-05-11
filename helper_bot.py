import matplotlib.pyplot as plt

# all_ods = input("Enter all ODS (comma-separated): ").split(",")
all_ods = str("12, 11.8, 11.7, 11, 9, 4.5, 2.25, 1.125, 0.5, 0.25").split(",")
all_ods = [float(od.strip()) for od in all_ods]

# all_concs = input("Enter all dilutions, e.g. 1, 10, 100, etc.").split(",")
all_concs = str("1, 10, 20, 40, 80, 160, 320, 640, 1280, 2560").split(",")
all_concs = [float(conc.strip()) for conc in all_concs]

plt.plot(all_concs, all_ods, color='coral', marker=".", mfc="teal", ms=20,lw=3)
plt.xscale('log')
plt.gca().invert_xaxis()

plt.xlabel("Serial dilution concentration")
plt.ylabel("OD (600nm)")

plt.show()

od_measured = float(input("What is your measured OD? "))
duration = float(input("How many hours are you going to leave it for? "))
od_target = float(input("What is your target OD? "))
media_choice = input("YPD or SC? ")
division_time = 1.5 if media_choice.lower() == "ypd" else 2.5
number_of_divisions = duration / division_time
od_start = 1 / (2**number_of_divisions)

number_of_spots = int(input("How many spots are you going to do per plate? "))
