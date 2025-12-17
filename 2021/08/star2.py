from pathlib import Path


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def first_example():
    # THIS IS ONLY VALID FOR THE FIRST EXAMPLE
    # acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
    m = {
        "acedgfb": "8",
        "cdfbe": "5",
        "gcdfa": "2",
        "fbcad": "3",
        "dab": "7",
        "cefabd": "9",
        "cdfgeb": "6",
        "eafb": "4",
        "cagedb": "0",
        "ab": "1",
    }

    m2 = {}
    for key, val in m.items():
        # k = list(key)
        k = sorted(key)
        k = "".join(k)
        m2[k] = val

    return m2


def count_common_segments(pattern1, pattern2):
    count = 0
    for this in pattern1:
        for other in pattern2:
            if this == other:
                count += 1
    
    return count


def get_output_value(line):
    # Each entry consists of ten *unique signal patterns*, a `|` delimiter, and finally the *four digit output value*
    patterns, out = line.split("|")
    patterns = patterns.split()
    patterns = ["".join(sorted(p)) for p in patterns]
    out = out.split()
    out = ["".join(sorted(o)) for o in out]  # sort each list

    """
    
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

    """

    pattern_to_number = {}  # signal pattern to digit
    signal_patterns_list = [""] * 10  # list of signal patterns
    while len(pattern_to_number) < 10:
        for pattern in patterns:
            if pattern in pattern_to_number:
                continue

            n = len(pattern)
            if n == 2:
                # one
                pattern_to_number[pattern] = "1"
                signal_patterns_list[1] = pattern
            elif n == 3:
                # seven
                pattern_to_number[pattern] = "7"
                signal_patterns_list[7] = pattern
            elif n == 4:
                # four
                pattern_to_number[pattern] = "4"
                signal_patterns_list[4] = pattern
            elif n == 5:
                # 2, 3, or 5
                
                # the one that has 2 segments in common with 1 must be 3
                if signal_patterns_list[1]:
                    if count_common_segments(pattern, signal_patterns_list[1]) == 2:
                        pattern_to_number[pattern] = "3"
                        signal_patterns_list[3] = pattern
                        continue  # force this to avoid parsing this pattern again right now
                
                # if 3 is known, the one that has 5 in common with 9 must be 5
                if signal_patterns_list[3]:
                    if count_common_segments(pattern, signal_patterns_list[9]) == 5:
                        pattern_to_number[pattern] = "5"
                        signal_patterns_list[5] = pattern
                        continue  # force this to avoid parsing this pattern again right now
                
                # if 3 and 5 is known, this must be 2
                if signal_patterns_list[3] and signal_patterns_list[5]:
                    pattern_to_number[pattern] = "2"
                    signal_patterns_list[2] = pattern
                    continue  # force this to avoid parsing this pattern again right now
            elif n == 6:
                # 0, 6 or 9 

                # the one that has 5 segments in common with 3 must be 9
                if signal_patterns_list[3]:
                    if count_common_segments(pattern, signal_patterns_list[3]) == 5:
                        pattern_to_number[pattern] = "9"
                        signal_patterns_list[9] = pattern
                        continue  # force this to avoid parsing this pattern again right now

                # if 9 is known, the one that has 3 in common with 7 must be 0
                if signal_patterns_list[9] and signal_patterns_list[7]:
                    if count_common_segments(pattern, signal_patterns_list[7]) == 3:
                        pattern_to_number[pattern] = "0"
                        signal_patterns_list[0] = pattern
                        continue  # force this to avoid parsing this pattern again right now

                # if 9 and 0 is known, this must be 6
                if signal_patterns_list[9] and signal_patterns_list[0]:
                    pattern_to_number[pattern] = "6"
                    signal_patterns_list[6] = pattern
                    continue  # force this to avoid parsing this pattern again right now
            elif n == 7:
                # eight
                pattern_to_number[pattern] = "8"
                signal_patterns_list[8] = pattern

    ans = ""
    for pattern in out:
        ans += pattern_to_number[pattern]

    return int(ans)


def aoc(filename):
    lines = get_input(filename)

    # four digit seven-segment displays

    # Each entry consists of ten *unique signal patterns*, a `|` delimiter, and finally the *four digit output value*

    ans = 0
    for line in lines:
        ans += get_output_value(line)

    return ans
        

def tests():
    assert count_common_segments("abc", "abc") == 3
    assert count_common_segments("a", "abc") == 1
    assert count_common_segments("abc", "a") == 1
    assert count_common_segments("abc", "ab") == 2
    assert count_common_segments("ab", "abc") == 2
    assert count_common_segments("c", "abc") == 1
    assert count_common_segments("abc", "c") == 1
    assert count_common_segments("abc", "b") == 1
    assert count_common_segments("b", "abc") == 1


    ans = get_output_value("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    print(f"example: {ans}")
    assert ans == 5353, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
