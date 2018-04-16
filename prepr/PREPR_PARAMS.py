"""General preprocessing parameters."""

from discretize import _DiscRange

VAL_SCORE = {_DiscRange(0, 4),
             _DiscRange(4, 6),
             _DiscRange(6, 8),
             _DiscRange(8, 10)
            }

STD_DEV = {_DiscRange(0, 1.5),
           _DiscRange(1.5, 3),
           _DiscRange(3, 5),
           _DiscRange(5, 8)
          }

MARKS = {_DiscRange(18, 22),
         _DiscRange(22, 25),
         _DiscRange(25, 28),
         _DiscRange(28, 31)
        }

PERCENT = {_DiscRange(0, 20),
           _DiscRange(20, 40),
           _DiscRange(40, 60),
           _DiscRange(60, 80),
           _DiscRange(80, 100)
          }

STUDENTS = {_DiscRange(0, 25),
            _DiscRange(25, 50),
            _DiscRange(50, 100),
            _DiscRange(100, 200)
           }

YEARS = {_DiscRange(0, 0.5),
         _DiscRange(0.5, 1),
         _DiscRange(1, 1.5),
         _DiscRange(1.5, 2)
        }

def aggregation_diff_pruning(n_1, n_2):
    """Returns if aggregated instance is to be pruned,
    based on number of single instnace considered for aggregation."""
    diff = abs(n_1 - n_2)
    return diff > min(n_1, n_2)
    # return False
