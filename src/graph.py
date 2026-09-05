# graph.py
# Campus route graph

# Coordinates of campus locations
coordinates = {
    "Boys Hostel": (0, 0),
    "Girls Hostel": (2, 1),
    "Food Court": (4, 2),
    "Sports Complex": (6, 1),
    "Gym": (8, 3),
    "Parking": (5, 5),
    "Main Gate": (9, 6)
}


# Weighted roads between locations
graph = {
    "Boys Hostel": {
        "Girls Hostel": 2.3,
        "Food Court": 4.5
    },

    "Girls Hostel": {
        "Boys Hostel": 2.3,
        "Food Court": 2.4,
        "Sports Complex": 4.2
    },

    "Food Court": {
        "Boys Hostel": 4.5,
        "Girls Hostel": 2.4,
        "Sports Complex": 2.5,
        "Parking": 3.8
    },

    "Sports Complex": {
        "Girls Hostel": 4.2,
        "Food Court": 2.5,
        "Gym": 3.0,
        "Parking": 4.2
    },

    "Gym": {
        "Sports Complex": 3.0,
        "Parking": 3.7,
        "Main Gate": 3.5
    },

    "Parking": {
        "Food Court": 3.8,
        "Sports Complex": 4.2,
        "Gym": 3.7,
        "Main Gate": 4.2
    },

    "Main Gate": {
        "Gym": 3.5,
        "Parking": 4.2
    }
}