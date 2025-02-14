from datetime import datetime

def count_wednesdays(input_file, output_file):
    wednesday_count = 0
    
    with open(input_file, 'r') as f:
        for line in f:
            date_str = line.strip()
            try:
                # Try parsing with different date formats
                for fmt in ('%Y/%m/%d %H:%M:%S', '%d-%b-%Y', '%Y-%m-%d', '%b %d, %Y'):
                    try:
                        date = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # If no format matches, skip this line
                    continue
                
                # Check if the day is Wednesday (weekday() returns 2 for Wednesday)
                if date.weekday() == 2:
                    wednesday_count += 1
            except ValueError:
                # If parsing fails, skip this line
                continue

    # Write the result to the output file
    with open(output_file, 'w') as f:
        f.write(str(wednesday_count))

    print(f"Number of Wednesdays: {wednesday_count}")