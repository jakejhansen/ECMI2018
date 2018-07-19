size(72mm, 0);

void grid(int n) {
  for (int i = -n; i <= n; ++i)
    for (int j = -n; j <= n; ++j)
      dot((i, j), red);
}

void cont(real l, real k) {
  guide g = (-1, 1) -- (-1, -1) -- (1, -1) -- (1, 1);
  // draw(scale(l) * scale(1 / 2) * g);
  guide gin = scale(l) * scale(1 / 2) * g;
  guide gout = scale(l + k) * scale(1 / 2) * g;
  draw(gin -- reverse(gout) -- cycle);
}

void obj(string s, pair x, real l, real a, bool p = false) {
  guide g = shift(x) * rotate(a) * scale(l) * shift((-1, -1) / 2) * unitsquare;
  if (p)
    draw(g, dashed);
  else {
    draw(g);
    dot("$" + s + "$", x);
    draw(x -- x - (0, 2 * l / 3), Arrow);
  }
}
