import os
f = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'abreviaciones.csv')
with open(f, 'rb') as fh:
    total = 0
    ends_no = 0
    for raw in fh:
        total += 1
        line = raw.rstrip(b"\r\n")
        if line.endswith(b',NO'):
            ends_no += 1
print(f"Total lines: {total}")
print(f"Lines ending with ,NO: {ends_no}")
print(f"Lines NOT ending with ,NO: {total-ends_no}")
