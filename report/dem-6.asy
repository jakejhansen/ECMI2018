include "dem";

size(54mm, 0);
draw(shift(-10, -10) * scale(20, 28) * unitsquare, invisible);

cont(16, 2);
resting("1", 4, (-2, -6), 0);
forcing("2", 4, (6, -6), 0, (-0.1, -0.2));
moving("3", 4, (-3, -2), (-3, -2) + (-0.1, -0.2), 0, -2.8, (0, 1));
moving("4", 4, (-2, 2) + (-0.2, -0.5), (-2, 2) + (-0.2, 0), -5.6, 0, (0, -4));
resting("5", 4, (-1, 6) + (-0.5, 0), 0);
moving("6", 4, (3, 7), (4, 5), -22.5, -45, (0, -4));