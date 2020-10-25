

class Questions():
    QUESTIONS = [
        {
            "id": 1,
            "content": "How much are you going to spend?",
            "options": [
                "Up to 5000000",
                "Up to 10000000",
                "Up to 15000000",
                "Up to 20000000",
                "Up to 25000000",
                "Up to 30000000",
                "Another range",
                "Unlimited",
            ],
            "required": True,
            "multiple": False,
            "spec": False
        },
        {
            "id": 2,
            "content": "What will you mainly use your laptop for?",
            "options": [
                "Personal Use",
                "Professional Use",
            ],
            "required": False,
            "multiple": False,
            "spec": False
        },
        {
            "id": 3,
            "content": "Which of the following will you use frequently?",
            "options": [
                "Photo editing (pro)",
                "Photo editing (basic)",
                "Music editing",
                "Video production (pro)",
                "Video production basic)",
                "3D design",
                "Front-end developer",
                "Back-end Tech"
            ],
            "required": True,
            "multiple": True,
            "spec": False
        },
        {
            "id": 4,
            "content": "Which of the following will you use frequently?",
            "options": [
                "Web browsing",
                "Social Media",
                "Email",
                "Document",
                "Watching Movies",
                "Light Gaming",
                "Medium Gaming",
                "Heavy Gaming",
                "Light photo or Video Editing",
                "Heavy photo or video Editing"
            ],
            "required": True,
            "multiple": True,
            "spec": False
        },
        {
            "id": 5,
            "content": "Where will you use your laptop?",
            "options": [
                "All around the house",
                "Public places",
                "Long journeys",
                "At your desk"
            ],
            "required": False,
            "multiple": False,
            "spec": False
        },
        {
            "id": 6,
            "content": "Are any of these important to you?",
            "options": [
                "Using laptop as a tablet",
                "Touchscreen laptop",
                "Need to work continuously for long time",
                "Working in low light conditions",
                "Fingerprint",
            ],
            "required": False,
            "multiple": True,
            "spec": False
        },
        {
            "id": 7,
            "content": "Is there a specific screen size you prefer?",
            "options": [
                "Very small (<= 13')",
                "Small (14')",
                "Medium (15')",
                "Large (> 17')",
                "Any size"
            ],
            "required": True,
            "multiple": True,
            "spec": False
        },
        {
            "id": 8,
            "content": "Which operating system are you comfortable with?",
            "options": [
                "Microsoft windows",
                "Mac os",
                "Linux",
                "Any os"
            ],
            "required": True,
            "multiple": True,
            "spec": False
        },
        {
            "id": 9,
            "content": "Which series cpu you prefer?",
            "options": [
                "Intel pentium",
                "Intel core i3",
                "Intel core i5",
                "Intel core i7",
                "Amd"
            ],
            "required": False,
            "multiple": True,
            "spec": True
        },
        {
            "id": 10,
            "content": "Do you want a good graphic cards?",
            "options": [
                "Integrated intel",
                "Nvidia geforce GT series",
                "Nvidia geforce GTX series",
                "Amd radeon series",
                "Amd vega series"
            ],
            "required": False,
            "multiple": True,
            "spec": True
        },
        {
            "id": 11,
            "content": "How about weight?",
            "options": [
                "Very light (1.5kg)",
                "Medium (2kg)",
                "Little heavy (2.5kg)",
                "No problem"
            ],
            "required": False,
            "multiple": True,
            "spec": True
        },

    ]