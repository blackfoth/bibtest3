



def is_bib_within_person(bib, person):
    """
    Check if a Bib is within a Person's area.
    
    :param bib: A list of coordinates [x_min, y_min, x_max, y_max].
    :param person: A list of coordinates [x_min, y_min, x_max, y_max].
    :return: True if the Bib is within the Person's area, False otherwise.
    """
    # if (bib[0] >= person[0] and  # x_min >= person_x_min
    #         bib[2] <= person[2] and  # x_max <= person_x_max
    #         bib[1] >= person[1] and  # y_min >= person_y_min
    #         bib[3] <= person[3]):
    #     print(bib,person)
    return (bib[0] >= person[0] and  # x_min >= person_x_min
            bib[2] <= person[2] and  # x_max <= person_x_max
            bib[1] >= person[1] and  # y_min >= person_y_min
            bib[3] <= person[3])    # y_max <= person_y_max


def check_bibs_within_people(bibs, people,tracker):
    """
    Check if each Bib is within each Person's area. This will loop though each person found within the frame and check if 
    any of the bibs found fall within a persons outline box. If a bib is found to fall within the box it is added to the 
    results list, along with a tracking id. **Note:** The list of tracking ids should be as long as the people list ie each person in 
    the list should have a tracking id. 
    
    :param bibs: A list of lists, where each list represents the coordinates of a Bib [x_min, y_min, x_max, y_max].
    :param people: A list of lists, where each list represents the coordinates of a Person [x_min, y_min, x_max, y_max].
    :param tracker: A list of tracking ids used to track objects across frames. The only id's use are the ones 
    relating to people objects becasue people are bigger than bibs and are easier to track between frames.
    :return: An array of dic values that represent the person and the bib found within the person along with the ID. Each 
    entry will have {person,bib,ID}  
    """
    #Setup an empty array
    results = []
    results.clear()
    #If there are no people or bibs, then no bibs will be found in a person becasue we have none.
    if len(bibs) == (0):
        return results
    if len(people) == (0):
        return  results

    #Loop through all the people found and check if one of the bibs found is within a person.
    for row, person in enumerate(people):
        # Compare each Bib against the current Person
        for  bib in bibs:
            #check if the bib is within the current person, if it is add the details to the results list and break out of the bib loop.
            if is_bib_within_person(bib, person):
                results.append({'person': person, 'bib': bib, 'ID': tracker[row]})
                break
     
#    print("Total Results:", len(results))
#    for entry in results:
#        print("Person:", entry['person'], "Bib:", entry['bib'])

    return results
    


# # Wrap bib_boxes and person_boxes in variables as specified
# bib_box = bib_array
# person_box = person_array

# # Call the function using variables
# results, plain_text, bib_results, person_index = check_bibs_within_people(bib_box, person_box)

# # Iterate through bib_boxes and person_boxes for debugging
# for sublist in bib_box:
#     for item in sublist:
#         print("Bib coordinate:", item)

# for sublist in person_box:
#     for item in sublist:
#         print("Person coordinate:", item)

# # Display the results
# print("Results as List of Dictionaries:", results)
# print("Results as Plain Text:", plain_text)




# if check_bibs_within_people(bib_box, person_box):
#     print("RUNNNER FOUND FUCK YEAH")
# else:
#     print("No runner found.")