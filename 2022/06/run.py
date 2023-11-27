def get_start_of_first_packet(line):
    # seq = ""
    for i in range(4, len(line)):
        seq = line[i-4:i]
        if len(set(seq)) == 4:
            return i
            
        # print(set(seq))
        # if line[i] in line[i-4:i]

def get_start_of_first_message(line):
    n = 14
    for i in range(14, len(line)):
        seq = line[i-14:i]
        if len(set(seq)) == 14:
            return i    

# cmpmbppqmqsq
with open("input.txt") as file:
    line = file.readline()[:-1]
print(f"max: {len(line)}")

i = get_start_of_first_packet(line)
j = get_start_of_first_message(line)
print(i)
print(j)
