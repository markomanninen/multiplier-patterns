# Doubling sequences – research notes

Research for an article on doubling (and other n-tupling) sequences in repeating decimals, based on the Math StackExchange thread 1365506. Compiled 18 November 2026.

## Files

| File | Contents |
| --- | --- |
| `doubling-sequences-article.md` | Article draft: theory, proofs, verified table, corrections, literature, ideas. |
| `verify.py` | Exact integer checks of every numerical claim in the draft. Run `python3 verify.py`; all lines should end in OK. |
| `thread-1365506-doubling-sequences.txt` | Question, both answers and all comments, extracted from a saved copy of the page with LaTeX kept. |
| `thread-1372077-four-notations-1-999.txt` | Companion question on 1/999 and David K's answer 1372077, extracted from a saved copy of the page. |

## Main findings

1. **Forward patterns** (1/7, 1/49): 1/n = Σ m·r^k / (10^x)^(k+1) with m = ⌊10^x/n⌋, r = 10^x mod n. Forward doubling ⇔ n | 10^x − 2 (7, 49, 499, 31, 127, …).
2. **Backward patterns** (1/19): with c = 10^(−x) mod n and 10^x·c − 1 = b·n, the period read from the right is b, b·c, b·c², … with carries. Backward doubling ⇔ n | 2·10^x − 1 (19, 199, 1999, and 7 via 19999 = 7·2857).
3. **Where the backward sequence starts:** at the last block of the period, which equals b; for every n ending in 9, b = 1.
4. **The integer-part observation in the question** is a 10-adic geometric series: 1 + 20 + 20² + … = −1/19.
5. **Fibonacci rows:** 1/89 and −1/109 are the Fibonacci generating function at X = 1/10 and X = 10.
6. **Divisionremnant's "growing formula"** most likely means the series with growth factor 10^x − n (the "upper boundary" of n's magnitude range). This is an interpretation of the wording, not confirmed; the same series appears in the 2015 companion question.
7. The draft lists **seven corrections** to the discussion, including 124 → 128, "12·4 reverse" → 21·4^k, and 0.0081 → 0.00081.

## Not available

Nothing remains unread. The pages below were read in Chrome on 18 November 2026.

- Chat room 26191 holds one conversation between David K and the asker on 24 July 2015. David K explains 1/7 by long division whose remainder doubles, and by the tripling series with ratio 3/10. No growing formula appears there.
- Divisionremnant has three posts, all from 2025, and none states a formula. Besides answer 5024760, the user answered question 3205913 on the reverse sequence of a repetend. That answer says the right-to-left reading comes from the same formula with negative exponents and alternating signs, and that a full breakdown exists but is unpublished. The third post is a closed question asking for a number whose period has 19 digits.

The paper therefore mentions the growing formula in one sentence only. The stackedit link in the same comments points to gist 2eec41d340c0c0970c86 by the asker, written in July and August 2015. It was read on 18 November 2026 and states the growth factor 10^x − n in words.

## Key sources

- Long, The Fibonacci Quarterly, Feb 1981 – 1/89 and 1/109 from one recurrence identity.
- Bicknell-Johnson, The Fibonacci Quarterly, Nov 1989 – repetends read right to left.
- MathPages "Rotate to Double"; Wikipedia "Parasitic number" – the same backward fact as rotation.
- Codidact question 278629 (2020) – the 1/(10n − 1) question asked again, three proofs.
- Vedic Mathematics, sutra Ekadhikena Purvena – 1/19 by doubling from the right.

Full links are in the Sources section of the draft.
