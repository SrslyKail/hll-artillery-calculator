"""********************************************************************************
* Welcome to the HLL Artillery Calculator!                                        *
* This program accepts a distance in meters and returns a value of mils to adjust *
* your artillery barrel to. Run with 'de', 'us', or 'ru' to set the appropriate   *
* calculation based on which faction you are playing.                             *
********************************************************************************"""

import sys
import math

def print_welcome():
	print("Welcome to the HLL Artillery Calculator!")
	print("Enter a distance in meters to get the appropriate amount of mils to adjust your gun to.")
	print("Enter a new faction to change the calculation.")
	print("Enter 'fm' or 'fire mission' to begin calculations between two designated map points.")
	print("Enter 'quit' to quit.")

def us_de_calculate(distance):
	mils = (-0.237 * float(distance)) + 1002
	return round(mils)

def ru_calculate(distance):
	mils = (-0.213 * float(distance)) + 1141
	return round(mils)

def get_faction() -> str:
    user_choice: str = input("Please enter a faction (us, de, ru): ").lower()
    return user_choice

def check_faction(faction: str) -> bool:
    if faction not in factions:
        print("Invalid faction!")
        return False
    else:
        return True

def check_argv():
	if (len(sys.argv)-1) < 1:
		print("No command-line arguments found")
		faction = get_faction()
		while check_faction(faction) == False:
			faction = get_faction()
	else:
		if sys.argv[1] in factions:
			faction = sys.argv[1]
		else:
			while check_faction(faction) == False:
				faction = get_faction()
	return faction

def calculate_angular_difference(first, last):
	result = abs(first - last)
	return result

def law_of_cosines(side_1, side_2, angle):
	rad_angle = math.radians(angle)
	unknown_side_squared = side_1 ** 2 + side_2 ** 2 - 2 * side_1 * side_2 * math.cos(rad_angle)
	unknown_side = math.sqrt(unknown_side_squared)

	return unknown_side

def calculate_average_difference(input_list):
	from numpy import array, diff
	avg_diff = array(input_list)
	avg_diff = diff(avg_diff)

	item_sum = 0
	for item in avg_diff:
		item_sum += item

	avg_diff = item_sum / len(avg_diff)

	return avg_diff

def calculate_x():
	print("")
	print("BEGIN FIRE MISSION")
	print("")
	
	original_target = input("Distance to original target: ")

def calculate_fire_mission():
	fm_start = []
	fm_end = []
	print("")
	print("BEGIN FIRE MISSION")
	print("")
	num_points = int(input("How many points along the line will we fire upon?: "))
	fm_start.append(float(input("Angle to first target?: ")))
	fm_start.append(float(input("Distance to first target?: "))) # c
	fm_end.append(float(input("Angle to final target?: ")))
	fm_end.append(float(input("Distance to final target?: "))) # b

	angular_difference = calculate_angular_difference(fm_start[0], fm_end[0]) # A
	angular_step = angular_difference / num_points # A / num_points
	line_of_fire = law_of_cosines(fm_start[1], fm_end[1], angular_difference)
	distance_step = line_of_fire / num_points # a / num_points

	angle_B = (math.sin(math.radians(angular_difference)) * fm_end[1]) / line_of_fire # B
	angle_B = math.asin(angle_B)
	angle_B = math.degrees(angle_B)
	angle_B = 180 - angle_B

	distances = []
	angles = []
	i = 1
	for point in range(num_points):
		if fm_start[0] > fm_end[0]:
			angle = fm_start[0] - angular_step*i
			if i == 1:
				angle_B = 180 - angle_B
		else:
			angle = fm_start[0] + angular_step*i
		
		distance = distance_step*i
		new_distance = law_of_cosines(distance, fm_start[1], angle_B) #b2
		distances.append(new_distance)
		angles.append(angle)
		i += 1

	distances.insert(0, fm_start[1])
	angles.insert(0, fm_start[0])
	
	print("")
	solutions = []
	i = 0
	for i in range(len(distances)):
		if faction == "us" or faction == "de":
			mils = us_de_calculate(distances[i])
			solutions.append(mils)
			print("TARGET", str(i+1) + ":", "mils:", mils, "angle:", angles[i])
		elif faction == "ru":
			mils = ru_calculate(distances[i])
			solutions.append(mils)
			print("TARGET", str(i+1) + ":", "mils:", mils, "angle:", angles[i])

	print("")
	avg_diff_mils = calculate_average_difference(solutions)
	print("mil diff:", avg_diff_mils)

	avg_diff_angles = calculate_average_difference(angles)	
	print("angle diff:", avg_diff_angles)

	print("")
	print("END FIRE MISSION")
	print("")


if __name__ == "__main__":
	factions = ("us", "de", "ru")
	faction = check_argv()
	print_welcome()
	distance = 0
	
	while True:
		distance = input("distance to target(m): ")
		if distance == "quit":
			sys.exit(0)

		if distance.lower() in factions:
			faction = distance.lower()
			print("Changed calulation to", faction)
			continue

		if distance == "fm" or distance == "fire mission":
			calculate_fire_mission()
			continue

		if faction == "us" or faction == "de":
			try:
				mils = us_de_calculate(distance)
				print("mils to target:", mils)
			except:
				print("Invalid selection!")
				continue
		elif faction == "ru":
			try:
				mils = ru_calculate(distance)
				print("mils to target:", mils)
			except:
				print("Invalid selection!")
				continue