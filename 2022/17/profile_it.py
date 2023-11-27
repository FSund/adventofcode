import cProfile
from pstats import SortKey
from second import star2

p = cProfile.run('star2("input.txt", 10_000, 200)', 'restats')
