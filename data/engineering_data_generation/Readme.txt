base_mix.m is the source code for displacement control, torque control, and adaptive hybrid control.
Run this file first, then run the corresponding position.slx, position_discrete.slx, torque.slx, torque_discrete.slx, mix.slx files to run the corresponding emulator.

optimal_control.m is the source code for optimal control.
Run this file first during debugging, and then run position.slx (share the same model with displacement control) to run the optimal control model.

adaptive_control.m is used to draw an image of the mixed control weight factor function.