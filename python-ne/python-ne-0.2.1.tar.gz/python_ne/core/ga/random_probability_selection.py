import random


def perform_selection(elements, number_to_be_selected):
    """
    :param elements: list of tuples with the following structure: (data, probability)
    :param number_to_be_selected: the number of elements that will be selected from the list
    """

    elements = sorted(elements, key=lambda e: e[1])

    selected_elements = []

    for _ in range(number_to_be_selected):
        random_number = random.random()
        probability_sum = 0
        for index, element in enumerate(elements):
            _, probability = element
            probability_sum += probability

            if random_number <= probability_sum:
                selected_elements.append(element)
                elements.pop(index)
                break

            elif element == elements[-1]:
                selected_elements.append(element)
                elements.pop(index)

    return [selected_element[0] for selected_element in selected_elements]
