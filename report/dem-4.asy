include "dem";

size(54mm, 0);
draw(shift(-10, -10) * scale(20, 28) * unitsquare, invisible);

cont(16, 2);
resting("1", 4, (-2, -6), 0);
resting("2", 4, (6, -6), 0);
resting("3", 4, (-3, -2), 0);
forcing("4", 4, (-2, 2), 0, (-0.2, -0.5));
moving("5", 4, (-1, 6), (-1, 6) + (-0.5, -1), 0, -2.8, (0, 1));
moving("6", 4, (1, 9), (2, 9), 22.5, 0, (0, -4));
