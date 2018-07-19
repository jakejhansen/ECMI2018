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

void fixed(string str, real width, pair src, real asrc) {
  guide g = scale(width) * shift((-1, -1) / 2) * unitsquare;
  guide gsrc = shift(src) * rotate(asrc) * g;

  draw(gsrc, 1 + solid);
  dot("$" + str + "$", src);
}

void resting(string str, real width, pair src, real asrc) {
  guide g = scale(width) * shift((-1, -1) / 2) * unitsquare;
  guide gsrc = shift(src) * rotate(asrc) * g;

  draw(gsrc);
  dot("$" + str + "$", src);
}

void falling(string str, real width, pair src, pair dst, real asrc) {
  guide g = scale(width) * shift((-1, -1) / 2) * unitsquare;
  guide gsrc = shift(src) * rotate(asrc) * g;
  guide gdst = shift(dst) * rotate(asrc) * g;

  draw(gsrc, dashed);
  draw(gdst);
  draw(src -- dst, Arrow);
  dot("$" + str + "$", dst);
}

void rolling(string str, real width, pair src, pair left, real asrc, real adst) {
  pair dst = rotate(adst - asrc, left) * src;

  guide g = scale(width) * shift((-1, -1) / 2) * unitsquare;
  guide gsrc = shift(src) * rotate(asrc) * g;
  guide gdst = shift(dst) * rotate(adst) * g;

  draw(gsrc, dashed);
  draw(gdst);
  draw(arc(left, src, dst, asrc < adst), Arrow);
  dot("$" + str + "$", dst);
  dot(left);
}

void fixing(string str, real width, pair src, pair left, pair right, real asrc) {
  pair dst = (src.x, src.y - 2 * (src.y - min(left.y, right.y)));

  guide g = scale(width) * shift((-1, -1) / 2) * unitsquare;
  guide gsrc = shift(src) * rotate(asrc) * g;

  draw(gsrc);
  draw(src -- dst, Arrow);
  dot("$" + str + "$", src);
  dot(left);
  dot(right);
}
