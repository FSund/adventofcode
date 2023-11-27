import pstats
from pstats import SortKey

p = pstats.Stats('restats')
p.strip_dirs().sort_stats(-1).print_stats()
# The strip_dirs() method removed the extraneous path from all the module names. The sort_stats() method sorted all the entries according to the standard module/line/name string that is printed. The print_stats() method printed out all the statistics. You might try the following sort calls:

p.sort_stats(SortKey.TIME).print_stats(10)
p.print_stats()

p.print_callers(.5, 'fromnumeric')