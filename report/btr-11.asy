include "btr";

size(72mm, 0);

cont(16, 2);
fixed("1", 4, (-2, -6), 0);
fixed("2", 4, (6, -6), 0);
fixed("3", 4, (-3, -2), 0);
fixed("4", 4, (-2, 2), 0);
fixed("5", 4, (-1, 6), 0);
fixed("6", 4, rotate(degrees(acos(3 / 4)), (4, -4)) * (3, -2),
    -90 + degrees(acos(3 / 4)));