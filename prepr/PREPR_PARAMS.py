"""General preprocessing parameters."""

from mymodules import discretize

VAL_SCORE = {discretize._DiscRange(0, 4),
             discretize._DiscRange(4, 6),
             discretize._DiscRange(6, 8),
             discretize._DiscRange(8, 10)
            }

STD_DEV = {discretize._DiscRange(0, 1.5),
           discretize._DiscRange(1.5, 3),
           discretize._DiscRange(3, 5),
           discretize._DiscRange(5, 8)
          }

MARKS = {discretize._DiscRange(18, 22),
         discretize._DiscRange(22, 25),
         discretize._DiscRange(25, 28),
         discretize._DiscRange(28, 31)
        }

PERCENT = {discretize._DiscRange(0, 20),
           discretize._DiscRange(20, 40),
           discretize._DiscRange(40, 60),
           discretize._DiscRange(60, 80),
           discretize._DiscRange(80, 100)
          }

STUDENTS = {discretize._DiscRange(0, 25),
            discretize._DiscRange(25, 50),
            discretize._DiscRange(50, 100),
            discretize._DiscRange(100, 200)
           }

YEARS = {discretize._DiscRange(0, 0.5),
         discretize._DiscRange(0.5, 1),
         discretize._DiscRange(1, 1.5),
         discretize._DiscRange(1.5, 2),
         discretize._DiscRange(2, 2.5),
         discretize._DiscRange(2.5, 3)
        }

def aggregation_diff_pruning(n_1, n_2):
    """Returns if aggregated instance is to be pruned,
    based on number of single instnace considered for aggregation."""
    diff = abs(n_1 - n_2)
    return diff > min(n_1, n_2)
    # return False
