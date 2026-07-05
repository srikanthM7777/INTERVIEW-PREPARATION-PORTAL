"""
Run this once to create the database tables and populate sample data:
    python seed.py
"""
from app import app
from models import db, User, Question, CodingProblem, InterviewQuestion


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ---------------- Admin account ----------------
        admin = User(name="Administrator", email="admin@portal.com",
                     college="Interview Prep Portal", branch="Admin", year="-",
                     is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)

        # ---------------- Demo student account ----------------
        demo = User(name="Srikanth", email="demo@portal.com",
                    college="ABC Engineering College", branch="CSE", year="3rd Year")
        demo.set_password("demo123")
        db.session.add(demo)

        # ---------------- Aptitude questions ----------------
        aptitude_data = [
            ("Quantitative", "What is 15% of 200?", ["20", "30", "25", "35"], "30", "Easy"),
            ("Quantitative", "If a train travels 60 km in 45 minutes, what is its speed in km/h?", ["75", "80", "90", "70"], "80", "Medium"),
            ("Quantitative", "The average of 5 numbers is 20. If one number is removed, the average becomes 18. What is the removed number?", ["24", "28", "30", "26"], "28", "Hard"),
            ("Logical Reasoning", "Find the odd one out: Dog, Cat, Lion, Snake", ["Dog", "Cat", "Lion", "Snake"], "Snake", "Easy"),
            ("Logical Reasoning", "If CAT is coded as DBU, how is DOG coded?", ["EPH", "EPI", "FPH", "EQH"], "EPH", "Medium"),
            ("Verbal", "Choose the synonym of 'Abundant'", ["Scarce", "Plentiful", "Rare", "Limited"], "Plentiful", "Easy"),
            ("Verbal", "Choose the antonym of 'Genuine'", ["Real", "Authentic", "Fake", "True"], "Fake", "Easy"),
            ("Data Interpretation", "A pie chart shows 25% sales in Q1. If total sales are 400 units, how many units were sold in Q1?", ["90", "100", "110", "120"], "100", "Medium"),
            ("General Aptitude", "A clock shows 3:15. What is the angle between the hour and minute hands?", ["0", "7.5", "5", "15"], "7.5", "Hard"),
            ("General Aptitude", "Which number comes next: 2, 6, 12, 20, 30, ?", ["36", "40", "42", "44"], "42", "Medium"),
        ]
        for category, q, opts, ans, diff in aptitude_data:
            db.session.add(Question(section="aptitude", category=category, question=q,
                                     option1=opts[0], option2=opts[1], option3=opts[2], option4=opts[3],
                                     answer=ans, difficulty=diff))

        # ---------------- Technical questions ----------------
        technical_data = [
            ("DBMS", "Which of these is used to remove a table permanently from a database?", ["DELETE", "DROP", "TRUNCATE", "REMOVE"], "DROP", "Easy"),
            ("DBMS", "What does ACID stand for in transactions?", ["Atomicity, Consistency, Isolation, Durability", "Access, Control, Identity, Data", "Atomic, Concurrent, Isolated, Distributed", "None"], "Atomicity, Consistency, Isolation, Durability", "Medium"),
            ("Operating System", "Which scheduling algorithm can cause starvation?", ["Round Robin", "FCFS", "Priority Scheduling", "SJF (non-preemptive, fair)"], "Priority Scheduling", "Medium"),
            ("Operating System", "What is a deadlock?", ["A process finishing early", "Two or more processes waiting indefinitely for each other", "A memory leak", "A CPU overheating"], "Two or more processes waiting indefinitely for each other", "Easy"),
            ("Networking", "Which layer of the OSI model handles routing?", ["Data Link", "Network", "Transport", "Session"], "Network", "Easy"),
            ("Networking", "What does DNS stand for?", ["Domain Name System", "Data Network Service", "Digital Naming Standard", "Domain Network Server"], "Domain Name System", "Easy"),
            ("Python", "What is the output of print(type([]))?", ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"], "<class 'list'>", "Easy"),
            ("Python", "Which keyword is used to create a generator function?", ["return", "yield", "generate", "async"], "yield", "Medium"),
            ("Java", "Which keyword is used to inherit a class in Java?", ["implements", "extends", "inherits", "super"], "extends", "Easy"),
            ("HTML", "Which tag is used to define an internal style sheet?", ["<css>", "<script>", "<style>", "<link>"], "<style>", "Easy"),
            ("CSS", "Which property is used to change text color?", ["font-color", "text-color", "color", "foreground-color"], "color", "Easy"),
            ("JavaScript", "Which method converts JSON to a JavaScript object?", ["JSON.parse()", "JSON.stringify()", "JSON.toObject()", "JSON.decode()"], "JSON.parse()", "Medium"),
            ("SQL", "Which SQL clause is used to filter grouped results?", ["WHERE", "HAVING", "GROUP", "FILTER"], "HAVING", "Medium"),
        ]
        for category, q, opts, ans, diff in technical_data:
            db.session.add(Question(section="technical", category=category, question=q,
                                     option1=opts[0], option2=opts[1], option3=opts[2], option4=opts[3],
                                     answer=ans, difficulty=diff))

        # ---------------- Coding problems ----------------
        coding_data = [
            ("Two Sum", "Python", "Easy",
             "Given an array of integers and a target, return indices of the two numbers that add up to the target.",
             "nums = [2,7,11,15], target = 9", "[0, 1]",
             "Exactly one solution exists. You may not use the same element twice.",
             "Use a hash map to store seen numbers and their indices.",
             "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target-n], i]\n        seen[n] = i"),
            ("Reverse a String", "Python", "Easy",
             "Write a function that reverses a given string.",
             '"hello"', '"olleh"',
             "String length up to 10^5.",
             "Slicing with a step of -1 reverses a string.",
             "def reverse_string(s):\n    return s[::-1]"),
            ("Check Palindrome", "Java", "Easy",
             "Check whether a given string is a palindrome, ignoring case.",
             '"Madam"', "true",
             "Ignore case sensitivity.",
             "Compare the string with its reverse.",
             "boolean isPalindrome(String s) {\n  s = s.toLowerCase();\n  return s.equals(new StringBuilder(s).reverse().toString());\n}"),
            ("Fibonacci Series", "C++", "Medium",
             "Print the first N Fibonacci numbers.",
             "N = 6", "0 1 1 2 3 5",
             "1 <= N <= 40",
             "Use two variables to track the last two Fibonacci numbers.",
             "#include <iostream>\nusing namespace std;\nint main(){int n; cin>>n; int a=0,b=1;\n for(int i=0;i<n;i++){cout<<a<<\" \"; int c=a+b; a=b; b=c;}}"),
            ("Find Duplicate Elements", "JavaScript", "Medium",
             "Given an array, return all elements that appear more than once.",
             "[1,2,3,2,4,1]", "[1, 2]",
             "Array length up to 10^4.",
             "Use an object or Map to count occurrences.",
             "function findDuplicates(arr){\n  const count = {}; const result = [];\n  for(const n of arr){ count[n]=(count[n]||0)+1; }\n  for(const k in count){ if(count[k] > 1) result.push(Number(k)); }\n  return result;\n}"),
            ("Binary Search", "C", "Medium",
             "Implement binary search on a sorted array to find the index of a target value.",
             "arr = [1,3,5,7,9], target = 7", "3",
             "Array is sorted in ascending order.",
             "Compare the middle element with the target and narrow the search range.",
             "int binarySearch(int arr[], int n, int target){\n  int lo=0, hi=n-1;\n  while(lo<=hi){int mid=(lo+hi)/2;\n    if(arr[mid]==target) return mid;\n    else if(arr[mid]<target) lo=mid+1; else hi=mid-1;}\n  return -1;\n}"),
            ("Merge Two Sorted Lists", "Python", "Hard",
             "Merge two sorted linked lists into a single sorted linked list.",
             "l1 = [1,2,4], l2 = [1,3,4]", "[1,1,2,3,4,4]",
             "Both lists are sorted in non-decreasing order.",
             "Use a dummy head node and iterate both lists simultaneously.",
             "def merge_two_lists(l1, l2):\n    dummy = cur = ListNode()\n    while l1 and l2:\n        if l1.val <= l2.val:\n            cur.next, l1 = l1, l1.next\n        else:\n            cur.next, l2 = l2, l2.next\n        cur = cur.next\n    cur.next = l1 or l2\n    return dummy.next"),
        ]
        for title, lang, diff, desc, si, so, cons, hints, sol in coding_data:
            db.session.add(CodingProblem(title=title, language=lang, difficulty=diff,
                                          description=desc, sample_input=si, sample_output=so,
                                          constraints=cons, hints=hints, solution=sol))

        # ---------------- HR interview questions ----------------
        hr_data = [
            ("Tell me about yourself", "Tell me about yourself.",
             "Give a brief summary of your education, key skills, and career goals, tying them to the role you're applying for.",
             "Keep it under 2 minutes; focus on relevant achievements.",
             "Reciting your entire resume line by line."),
            ("Strengths", "What are your greatest strengths?",
             "Pick 2-3 strengths relevant to the job and back each with a short example.",
             "Be specific, use real examples, avoid generic answers like 'hardworking'.",
             "Listing too many strengths without evidence."),
            ("Weaknesses", "What is your biggest weakness?",
             "Mention a real, minor weakness and describe the concrete steps you're taking to improve it.",
             "Show self-awareness and growth, not a disguised strength.",
             "Saying 'I have no weaknesses' or 'I'm a perfectionist' without substance."),
            ("Why should we hire you?", "Why should we hire you?",
             "Connect your skills and experience directly to the company's needs and the job description.",
             "Research the company beforehand and be specific.",
             "Giving a generic answer that could apply to any company."),
            ("Career Goals", "Where do you see yourself in 5 years?",
             "Describe realistic growth within the field that aligns with the company's own growth path.",
             "Show ambition balanced with commitment to the organization.",
             "Mentioning unrelated goals or starting your own competing business."),
            ("Leadership", "Describe a time you led a team.",
             "Use the STAR method (Situation, Task, Action, Result) to describe a specific leadership example.",
             "Quantify the outcome where possible.",
             "Taking sole credit for a team's success."),
            ("Conflict Handling", "How do you handle conflict with a coworker?",
             "Explain a calm, solution-oriented approach: listen, understand the other perspective, and find common ground.",
             "Emphasize communication and professionalism.",
             "Blaming the other person entirely or avoiding the question."),
            ("Salary", "What are your salary expectations?",
             "Give a researched range based on market standards for the role and location, and show flexibility.",
             "Research typical salaries beforehand using sites like Glassdoor or Levels.fyi.",
             "Giving an exact number too early or refusing to answer."),
            ("Projects", "Tell me about a project you're proud of.",
             "Explain the problem, your specific contribution, the technology used, and the impact or result.",
             "Focus on your individual role and measurable outcomes.",
             "Describing the project in purely technical jargon without explaining the impact."),
        ]
        for category, q, ans, tips, mistakes in hr_data:
            db.session.add(InterviewQuestion(category=category, question=q, model_answer=ans,
                                              tips=tips, common_mistakes=mistakes))

        db.session.commit()
        print("Database created and seeded successfully!")
        print("Admin login  -> email: admin@portal.com | password: admin123")
        print("Demo student -> email: demo@portal.com  | password: demo123")


if __name__ == "__main__":
    run()
