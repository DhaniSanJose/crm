from datetime import datetime

# Define the date-time strings
date_time_string1 = "2024-2-29 12:59:59"
date_time_string2 = "2024-2-29 12:2:43"
date_time_string3 = "2024-2-29 12:8:57"
date_time_string4 = "2024-2-29 12:3:27"

# Convert the strings to datetime objects
date_time1 = datetime.strptime(date_time_string1, "%Y-%m-%d %H:%M:%S")

# List of all datetime objects
date_times = [
    datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    for dt_string in [date_time_string1, date_time_string2, date_time_string3, date_time_string4]
]

# Filter out the times that occur before 12:00 PM or exactly at 12:00 PM
valid_times = [dt for dt in date_times if dt.hour >= 12]

if valid_times:
    # Find the time closest to 12:00 PM
    first_time_in = min(valid_times, key=lambda x: abs(x.hour - 12))

    # Find the second time in the list with at least 1-minute difference from the first time in
    second_time_in = None
    for dt in valid_times:
        if dt != first_time_in and abs(dt - first_time_in).seconds >= 60:
            second_time_in = dt
            break

    # If no such time found, output the farthest time
    if second_time_in is None:
        farthest_time = max(valid_times, key=lambda x: abs(x - first_time_in))
        print("The first time in is at or after 12:00 PM.")
        print("There is no second time in with at least 1 minute difference from the first time in.")
        print("Farthest time from the first time in:", farthest_time)
    else:
        print("First time in:", first_time_in)
        print("Second closest time in with at least 1 minute difference:", second_time_in)
else:
    print("There are no valid times after 12:00 PM.")
