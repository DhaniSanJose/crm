from datetime import datetime

# Define the date-time strings
date_time_string1 = "2024-2-29 11:59:59"  # Change this to 12:00:01 for testing the closest time after 12:00 PM
date_time_string2 = "2024-2-29 12:2:43"
date_time_string3 = "2024-2-29 12:8:57"
date_time_string4 = "2024-2-29 12:13:27"

# Convert the strings to datetime objects
date_time1 = datetime.strptime(date_time_string1, "%Y-%m-%d %H:%M:%S")

# List of all datetime objects
date_times = [
    datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    for dt_string in [date_time_string1, date_time_string2, date_time_string3, date_time_string4]
]

# Filter out the times that occur after 12:00 PM
valid_times = [dt for dt in date_times if dt.hour >= 12]

if valid_times:
    # Sort the valid times based on their time differences with respect to the first time in
    valid_times.sort(key=lambda x: abs(x - date_time1))

    # Find the second time in the list with at least 1-minute difference from the first time in
    second_time_in = None
    for dt in valid_times:
        if dt != date_time1 and abs(dt - date_time1).seconds >= 60:
            second_time_in = dt
            break

    # If no such time found, output the farthest time
    if second_time_in is None:
        farthest_time = max(valid_times, key=lambda x: abs(x - date_time1))
        print("The first time in is at or after 12:00 PM.")
        print("There is no second time in with at least 1 minute difference from the first time in.")
        print("Farthest time from the first time in:", farthest_time)
    else:
        print("First time in:", date_time1)
        print("Second closest time in with at least 1 minute difference:", second_time_in)
else:
    print("There are no valid times after 12:00 PM.")
