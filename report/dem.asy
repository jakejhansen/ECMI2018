import geometry;

void grid(int n) {
  for (int i = -n; i <= n; ++i)
    for (int j = -n; j <= n; ++j)
      dot((i, j));
}

void cont(real width, real thick) {
  guide g = (-1, 1) -- (-1, -1) -- (1, -1) -- (1, 1);
  guide gin = scale(width) * scale(1 / 2) * g;
  guide gout = scale(width + thick) * scale(1 / 2) * g;

  draw(gin -- reverse(gout) -- cycle, 1 + solid);
}

void resting(string str, real width, pair src, real asrc) {
  guide g = scale(width) * shift((-1, -1) / 2) * unitsquare;
  guide gsrc = shift(src) * rotate(asrc) * g;

  draw(gsrc);
  dot("$" + str + "$", src);
}

void forcing(string str, real width, pair src, real asrc, pair force) {
  guide g = scale(width) * shift((-1, -1) / 2) * unitsquare;
  guide gsrc = shift(src) * rotate(asrc) * g;

  draw(gsrc);
  draw(src -- src + force, dashed, Arrow);
  dot("$" + str + "$", src);
}

void moving(string str, real width, pair src, pair dst,
    real asrc, real adst, pair force) {
  guide g = scale(width) * shift((-1, -1) / 2) * unitsquare;
  guide gsrc = shift(src) * rotate(asrc) * g;
  guide gdst = shift(dst) * rotate(adst) * g;

  draw(gsrc, dashed);
  draw(gdst);
  draw(src -- dst, Arrow);
  draw(dst -- dst + force, dashed, Arrow);
  dot("$" + str + "$", dst);
}
