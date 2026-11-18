# Forward and backward multiplier patterns in repeating decimals

The repeating decimals of 1/7 and 1/49 contain doubling sequences read from left to right, and that of 1/19 contains the powers of two read from right to left. This repository holds the article that explains both patterns as geometric series, one in the real numbers and one in the 10-adic integers, together with the scripts that check every result in it.

The article grew out of the author's 2015 Mathematics Stack Exchange question [Doubling sequences of the cyclic decimal parts of the fraction numbers](https://math.stackexchange.com/questions/1365506).

The author is Marko T. Manninen, Helsinki, Finland (math@valjastus.fi).

## Contents

| Path | Contents |
| --- | --- |
| `paper/main.tex`, `paper/refs.bib` | The article (LaTeX, amsart) |
| `paper/fig-additions.tex`, `paper/make_fig.py` | Figure 1 and the script that draws it |
| `paper/amsplain-full.bst` | amsplain with every author written in full |
| `paper/derivations.mac` | Maxima session that derives the closed forms |
| `research/verify.py` | Exact checks of every result, number and exercise answer in the article |
| `research/doubling-sequences-article.md` | Long-form notes with the corrections to the source thread |
| `research/README.md` | Research summary and sources |
| `research/thread-*.txt` | Text of the two Stack Exchange threads |
| `scripts/check.sh` | Runs all checks on a clean export of a commit |

## Checks

`scripts/check.sh` exports a commit with `git archive` into `.check/`, runs `research/verify.py`, the Maxima derivations and the LaTeX build, and writes `.check/main.pdf`. It needs Python 3, Maxima, pdflatex and bibtex.

```bash
./scripts/check.sh
```

Each check in `verify.py` tests a result as it is stated, for all small cases and not only for the examples in the text.

## License

The article and its notes are licensed under [CC BY 4.0](LICENSE-CC-BY-4.0.txt), and the code under the MIT License. `paper/amsplain-full.bst` remains under the LaTeX Project Public License, and the texts in `research/thread-*.txt`, extracted from Mathematics Stack Exchange, remain under CC BY-SA as licensed by their authors. The details are in [LICENSE](LICENSE).
