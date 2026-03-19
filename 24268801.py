#24268801
def read_hospital_data(csv_file):
    Country_to_hospitals = {}
    Country_to_death = {}
    hospital_data = {}

    try:
        with open(csv_file, 'r') as file:
            # Reads the header
            header = file.readline().strip().split(',')
            country_index = header.index('country')
            hospital_id_index = header.index('hospital_ID')
            deaths_index = header.index('No_of_deaths_in_2022')

            for line in file:
                data = line.strip().split(',')
                country = data[country_index]
                hospital_id = data[hospital_id_index]
                deaths_2022 = data[deaths_index]
                
                if country not in hospital_data:
                    hospital_data[country] = {}
                
                  #Store deaths in the corresponding hospital
                hospital_data[country][hospital_id] = {
                    'deaths': int(deaths_2022) if deaths_2022.isdigit() else 0
                }
                    

                # Update hospital dictionary
                if country not in Country_to_hospitals:
                    Country_to_hospitals[country] = []
                Country_to_hospitals[country].append(hospital_id)

                # Update deaths dictionary
                if country not in Country_to_death:
                    Country_to_death[country] = []
                
                # Ensures deaths_2022 is a valid integer
                try:
                    deaths_count = int(deaths_2022)
                except ValueError:
                    print(f"Warning: Unable to convert '{deaths_2022}' to an integer for country '{country}'. Skipping this entry.")
                    continue  # Skips entry if conversion fails

                Country_to_death[country].append(deaths_count)

    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
    except IndexError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return  Country_to_hospitals,Country_to_death, hospital_data

def read_covid_stroke_data(txt_file):
    Country_to_covid_stroke = {}
    country_hospital_data = {}
    header_mapping = {
        'country': 0,
        'hospital_id': 1,
        'Covid': 2,
        'Stroke': 3
    }

    try:
        with open(txt_file, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading or trailing whitespace in each line
                if not line:  # Skip empty lines if there are any
                    continue
                
                parts = line.split(',')
                if len(parts) < len(header_mapping):
                    print(f"Warning: Line skipped due to insufficient data: '{line}'")
                    continue

                try:
                    # Extract data using the header mapping from the file(txt)
                    country = parts[header_mapping['country']].split(':')[1].strip()
                    hospital_id = parts[header_mapping['hospital_id']].split(':')[1].strip()
                    covid_number = int(parts[header_mapping['Covid']].split(':')[1].strip())
                    stroke_number = int(parts[header_mapping['Stroke']].split(':')[1].strip())
                    total_patients = covid_number + stroke_number
                    
                    if country not in country_hospital_data:
                        country_hospital_data[country] = {}
                    # Store total patients for the corresponding hospital
                    country_hospital_data[country][hospital_id] = {
                        'total_patients': total_patients
                    }

                    # Store total patients for stroke and covid for the country
                    if country not in Country_to_covid_stroke:
                        Country_to_covid_stroke[country] = []
                    Country_to_covid_stroke[country].append(total_patients)

                except (IndexError, ValueError) as e:
                    print(f"Warning: Unable to process line: '{line}'. Error: {e}")

    except FileNotFoundError:
        print(f"Error: The file {txt_file} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return Country_to_covid_stroke, country_hospital_data

#Read the CSV file to filter by specified hospital category.
def read_csv_file(csv_file, category):
    hospital_ids = []
    with open(csv_file, 'r') as file:
        header = file.readline().strip().split(',')  # Read the headers
        hospital_category_index = header.index('hospital_category')
        hospital_id_index = header.index('hospital_ID')
        for line in file:
            data = line.strip().split(',')
            hospital_category = data[hospital_category_index]
            hospital_id = data[hospital_id_index]
            # Collect hospital IDs for the specified category
            if hospital_category == category:
                hospital_ids.append(hospital_id) 
    return hospital_ids

#Task 3: Read txt file and return cancer admissions for specififed hospital IDs
def read_txt_file(txt_file, hospital_ids):
    cancer_data = {}
    header_mapping = {
        'country': 0,
        'hospital_id': 1,
        'Covid': 2,
        'Stroke': 3,
        'Cancer': 4
    }

    with open(txt_file, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading or trailing whitespace in each line
            if not line:  # Skip empty lines if any
                continue
            
            parts = line.split(',')
            if len(parts) < len(header_mapping):
                print(f"Warning: Line skipped due to insufficient data: '{line}'")
                continue

            try:
                # Extract data usiing header mapping from the file(txt)
                country = parts[header_mapping['country']].split(':')[1].strip()
                hospital_id = parts[header_mapping['hospital_id']].split(':')[1].strip()
                covid_number = int(parts[header_mapping['Covid']].split(':')[1].strip())
                stroke_number = int(parts[header_mapping['Stroke']].split(':')[1].strip())
                cancer_number = int(parts[header_mapping['Cancer']].split(':')[1].strip())

                if hospital_id in hospital_ids:
                    if country not in cancer_data:
                        cancer_data[country] = []
                    cancer_data[country].append(cancer_number)

            except (IndexError, ValueError) as e:
                print(f"Warning: Unable to process line: '{line}'. Error: {e}")

    return cancer_data
#Variance Formula
def calculate_variance(admissions):
    n = len(admissions)
    if n < 2:
        return 0.0  # Variance is 0 if less than 2 observations
    mean = sum(admissions) / n
    variance = sum((x - mean) ** 2 for x in admissions) / (n - 1)  # Obtain variance
    return round(variance, 4)

#Task 3: Calculating the variance of cancer admissions for specified hospital category
def compute_variance(csv_file, txt_file, category):
    hospital_ids = read_csv_file(csv_file, category)
    cancer_data = read_txt_file(txt_file, hospital_ids)

    # Calculate the variance for each country
    variance_dict = {}
    for country, admissions in cancer_data.items():
        if admissions:  # Ensuring there are admissions to calculate variance
            variance_dict[country] = calculate_variance(admissions)

    return variance_dict
#Task 4: Extraction of the needed data from the CSV File
def read_hospital4_data(csv_file):
    #Read the CSV file and return relevant statistics to be computed
    data = {}
    with open(csv_file, 'r') as file:
        header = file.readline().strip().split(',')
        country_index = header.index('country')
        hospital_id_index = header.index('hospital_ID')
        no_of_staff_index = header.index('no_of_staff')
        female_patients_index = header.index('female_patients')
        deaths_2022_index = header.index('No_of_deaths_in_2022')
        deaths_2023_index = header.index('No_of_deaths_in_2023')
        category_index = header.index('hospital_category')
        for line in file:
            data1 = line.strip().split(',')
            country = data1[country_index]
            hospital_id = data1[hospital_id_index]
            no_of_staff = int(data1[no_of_staff_index])
            female_patients = int(data1[female_patients_index])
            deaths_2022 = int(data1[deaths_2022_index])
            deaths_2023 = int(data1[deaths_2023_index])
            category = data1[category_index]

            if category not in data:
                data[category] = {}

            if country not in data[category]:
                data[category][country] = {
                    'total_female_patients': 0,
                    'num_hospitals': 0,
                    'max_staff': 0,
                    'total_deaths_2022': 0,
                    'total_deaths_2023': 0
                }

            # Update statistics
            data[category][country]['total_female_patients'] += female_patients
            data[category][country]['num_hospitals'] += 1
            data[category][country]['max_staff'] = max(data[category][country]['max_staff'], no_of_staff)
            data[category][country]['total_deaths_2022'] += deaths_2022
            data[category][country]['total_deaths_2023'] += deaths_2023

    return data

#Task 4 Calculation Statistics
def calculate_statistics(hospital_data):
    #Calculate average female patients and percentage change in deaths.
    category_country_dict = {}

    for category, countries in hospital_data.items():
        category_country_dict[category] = {}
        for country, stats in countries.items():
            avg_female_patients = stats['total_female_patients'] / stats['num_hospitals']
            max_staff = stats['max_staff']
            deaths_2022 = stats['total_deaths_2022']
            deaths_2023 = stats['total_deaths_2023']
            # Calculate percentage death difference 
            if deaths_2022 == 0:
                percent_change = float('inf')  # Handling division by zero
            else:
                percent_change = ((deaths_2023 - deaths_2022) / deaths_2022) * 100
            
            avg_female_patients = round(avg_female_patients, 4)
            max_staff = round(max_staff, 4)
            percent_change = round(percent_change, 4)
            
            # Population of the nested dictionary
            category_country_dict[category][country] = [
                avg_female_patients,
                max_staff,
                percent_change
            ]

    return category_country_dict

#Task 2: Calculation of Cosine Similarity
def compute_cosine_similarity(hospital_data, country_hospital_data):
    
    cosine_dict = {}
    
    for country, hospitals in hospital_data.items():
        cosine_dict[country] = {}
        numerator = 0
        denominator_a = 0
        denominator_b = 0
        
        for hospital_id, death_data in hospitals.items():
            deaths = death_data['deaths']
            total_patients = country_hospital_data.get(country, {}).get(hospital_id, {}).get('total_patients', 0)
            
            numerator += deaths * total_patients
            
            denominator_a += deaths ** 2
            denominator_b += total_patients ** 2
            
        if numerator == 0 or denominator_a == 0 or denominator_b == 0:
            similarity = 0.0 # returns zero if denominator is zero to avoid division by zero
        else:
            denominator = (denominator_a ** 0.5)* (denominator_b ** 0.5)
            similarity = numerator / denominator
        
        cosine_dict[country] = round(similarity, 4)
        
    return cosine_dict




def main(csv_file, txt_file, category):
    
    hospital_data4 = read_hospital4_data(csv_file)
    
    
    Country_to_hospitals,Country_to_death, hospital_data = read_hospital_data(csv_file)
    Country_to_covid_stroke, country_hospital_data=read_covid_stroke_data(txt_file)
    result1 = [Country_to_hospitals,Country_to_death,Country_to_covid_stroke]
    result3 = compute_variance(csv_file, txt_file, category)
    result4 = calculate_statistics(hospital_data4)
    result2 = compute_cosine_similarity(hospital_data, country_hospital_data)
    
    return result1, result2, result3, result4





