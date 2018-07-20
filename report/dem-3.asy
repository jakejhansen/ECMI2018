include "dem";

size(54mm, 0);
draw(shift(-10, -10) * scale(20, 28) * unitsquare, invisible);

cont(16, 2);
resting("1", 4, (-2, -6), 0);
resting("2", 4, (6, -6), 0);
resting("3", 4, (-3, -2), 0);
resting("4", 4, (-2, 2), 0);
forcing("5", 4, (-1, 6), 0, (-0.5, -1));
moving("6", 4, (1, 12), (1, 9), 22.5, 22.5, (2, -2));
