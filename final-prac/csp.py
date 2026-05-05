# Committee needs scheduling five major research presentations in a single-day program. 
# The committee must assign each presentation to a unique time slot 
# while satisfying several logical and professional constraints.

# The Presentations:
# Machine Learning (T1)
# Robotics (T2)
# Natural Language Processing (T3)
# Computer Vision (T4)
# Reinforcement Learning (T5)

# The Available Time Slots:
# Slot 1: 9:00 – 10:00 AM
# Slot 2: 10:00 – 11:00 AM
# Slot 3: 11:00 – 12:00 PM
# Slot 4: 2:00 – 3:00 PM
# Slot 5: 3:00 – 4:00 PM

# Constraints:
# Each presentation must be assigned exactly one slot, and no slot can host more than one presentation.
# The Machine Learning (T1) and Natural Language Processing (T3) presentations must be scheduled in consecutive time slots.
# Robotics (T2) must be scheduled before Computer Vision (T4).
# Reinforcement Learning (T5) cannot be scheduled in the morning slots (Slot 1 or Slot 2) due to speaker availability constraints.
# Natural Language Processing (T3) must be scheduled after Machine Learning (T1).
# Computer Vision (T4) cannot be placed in the final slot due to technical demonstration requirements.
# Slot 3 is reserved for high-attendance presentations and can only be assigned to either Machine Learning (T1) or Robotics (T2).

# Tasks:
# (a) Identify the variables of the CSP model. 
# (b) Define the domain for each variable. 
# (c) Formally define all constraints (unary, binary, and ordering constraints). 
# (d) Represent the constraint graph for the given problem. 
# (e) Solve the CSP using backtracking and provide the final valid schedule. 

