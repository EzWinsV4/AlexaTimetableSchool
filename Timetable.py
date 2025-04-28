import datetime

def lambda_handler(event, context):
    reference_date = datetime.date(2024, 9, 5)
    today = datetime.date.today()
    
    intent_name = event['request']['intent']['name']
    
    if intent_name == "GetLessonsTomorrowIntent":
        date = today + datetime.timedelta(days=1)
    else:
        date = today
    
    weeks_passed = (date - reference_date).days // 7
    week_type = "A" if weeks_passed % 2 == 0 else "B"
    weekday = date.strftime('%A')
    
    timetable = {
        "weekA": {
            "Monday": ["FORM TIME", "English Language", "Biology", "PE Core", "Double Geography"],
            "Tuesday": ["FORM TIME", "PE Core", "English Language", "Computer Science", "Chemistry", "Mathematics"],
            "Wednesday": ["ASSEMBLY", "Double Business Studies", "Biology", "Mathematics", "Physics"],
            "Thursday": ["FORM TIME", "Biology", "Chemistry", "Life Skills", "English Language", "Physics", "BRONZE DUKE OF EDINBURGH WEEKLY MEETING"],
            "Friday": ["FORM TIME", "Double Computer Science", "PE Core", "Mathematics", "English Language"]
        },
        "weekB": {
            "Monday": ["FORM TIME", "English Language", "Physics", "Double Geography", "Business Studies"],
            "Tuesday": ["FORM TIME", "RE", "English Language", "Computer Science", "Chemistry", "PE CORE"],
            "Wednesday": ["ASSEMBLY", "Double Business Studies", "Mathematics", "Physics", "English"],
            "Thursday": ["FORM TIME", "Biology", "Chemistry", "Life Skills", "Physics", "Mathematics", "BRONZE DUKE OF EDINBURGH WEEKLY MEETING"],
            "Friday": ["FORM TIME", "Computer Science", "PE Core", "Geography", "Mathematics", "English Language"]
        }
    }
    
    today_lessons = timetable.get(f"week{week_type.lower()}", {}).get(weekday, ["No lessons today!"])
    lessons_text = "".join(f"<break time='0.7s'/>{lesson}." for lesson in today_lessons)
    
    day_word = "tomorrow" if intent_name == "GetLessonsTomorrowIntent" else "today"
    
    speech_output = f"<speak>It is Week {week_type}, and you have these lessons {day_word}: {lessons_text} <break time='1s'/>Please note that this is a basic timetable and will not show you your detentions or extra activities.</speak>"
    
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': speech_output
            },
            'shouldEndSession': True
        }
    }

