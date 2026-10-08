path = '/home/bons/hw-sotsusei/submit/web_split/part01_plan.html'
with open(path) as f:
    s = f.read()

# Find and show the schedule section
idx = s.find('日程</th>')
print(f"Found at index {idx}")
print(repr(s[idx-80:idx+150]))
