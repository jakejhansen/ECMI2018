import geometry;

void grid(int n) {
  for (int i = -n; i <= n; ++i)
    for (int j = -n; j <= n; ++j)
      dot((i, j), red);
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

void rolling(string str, real width, pair src, pair about, real asrc, real adst) {
  pair dst = rotate(adst - asrc, about) * src;

  guide g = scale(width) * shift((-1, -1) / 2) * unitsquare;
  guide gsrc = shift(src) * rotate(asrc) * g;
  guide gdst = shift(dst) * rotate(adst) * g;

  draw(gsrc, dashed);
  draw(gdst);
  draw(arc(about, src, dst, asrc < adst), Arrow);
  dot("$" + str + "$", dst);
  dot(about);
}
