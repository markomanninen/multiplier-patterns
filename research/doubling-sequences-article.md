# Doubling Sequences in Repeating Decimals

Draft, 18 November 2026 · Marko Manninen

## The phenomenon

Some repeating decimals visibly contain a doubling sequence. In 1/7 = 0.142857… the two-digit blocks start 14, 28, 56, and the next term 112 spills its leading 1 into the previous block, turning 56 into 57. In 1/49 = 0.020408163265… the powers of two appear directly: 02, 04, 08, 16, 32, 64, then 128 carries. In 1/19 = 0.052631578947368421… the doubling runs backwards from the end of the period: 1, 2, 4, 8, 16, 32, each written one digit further left.

This article starts from a 2015 Math StackExchange question asking why and when such patterns occur, and whether 1/19 has a summation formula like the other two. David K's accepted answer explains the forward patterns with geometric series. It leaves the backward case of 1/19 half-finished in a comment, and a 2025 answer hints at an undisclosed "growing formula". The sections below verify the thread's numbers, finish the backward case, identify the growing formula, and place the topic in the existing literature.

The short answer: every pattern comes from one identity. If b·n = 10^x − r, then 1/n is a geometric series with ratio r/10^x. If b·n = 10^x·c − 1, the digits obey a right-to-left recurrence with multiplier c. Forward doubling is the first case with r = 2; backward doubling is the second with c = 2.

## Background: remainders drive the digits

The digits of 1/n come from the remainders of long division, and the remainder after x digits is 10^x mod n. For n coprime to 10 the remainders cycle, and the period length L is the multiplicative order of 10 modulo n: the smallest L with 10^L ≡ 1 (mod n). That is why 1/7 has period 6, 1/19 period 18 and 1/49 period 42.

One fact carries the whole article. If the remainder after x digits is r, then everything after those x digits is the expansion of r/n. Writing m for the first x digits read as an integer:

```latex
10^x = m\,n + r \quad\Longrightarrow\quad \frac{1}{n} = \frac{m}{10^x} + \frac{r}{10^x}\cdot\frac{1}{n}
```

So 1/n contains a copy of itself, scaled by r and shifted x places to the right. For 1/7 with x = 2 this reads 100 = 14·7 + 2: after the digits 14 comes 2/7, which is the same expansion doubled.

The period as an integer is P = (10^L − 1)/n, for example 142857 = 999999/7. The backward patterns are statements about the low-order digits of P.

## Forward patterns: David K's geometric series

Applying the self-similarity identity to itself over and over gives David K's general formula. For any block length x, with m = ⌊10^x / n⌋ and r = 10^x − m·n = 10^x mod n:

```latex
\frac{1}{n} = \sum_{k=0}^{\infty} \frac{m\,r^k}{(10^x)^{k+1}}
```

Each x-digit block is the previous block times r. Forward doubling is the case r = 2, which means n divides 10^x − 2. That answers the "when" for forward doubling exactly:

- x = 2: 98 = 2·7², so n = 7 and 49.
- x = 3: 998 = 2·499, so n = 499.
- x = 4 and 5: n = 4999 and 49999, both prime.
- x = 6: 999998 = 2·31·127², so n = 31, 127, 3937, 16129 and 499999.

Tripling needs n | 10^x − 3 (97, 997), quadrupling n | 10^x − 4 (83 with x = 3, 17 with x = 4), and so on.

Every n has such a series for every x, so the real question is when it is visible. Blocks stay clean while m·r^k < 10^x; after that the overflow is added into the block on the left. For 1/49 that gives six clean blocks (02 to 64) before 128 carries. A pattern is easy to see when r is small, m is short, and x is a small part of the period.

The carries never break the pattern, they only hide it. The sum is exact at every stage; the decimal digits are just the series after the overlapping terms have been added.

## Backward patterns: finishing the 1/19 story

The backward pattern is governed by the inverse of 10 instead of 10 itself. Let c be the inverse of 10^x modulo n, so that 10^x·c − 1 = b·n for some integer b. Then the period P satisfies:

```latex
P \equiv b \sum_{k=0}^{K-1} c^k \, 10^{xk} \pmod{10^L} \qquad \text{whenever } xK \ge L
```

Read from the right, the period is b, then b·c one block to the left, then b·c², with overflow carried leftwards. For 19 we have 10·2 − 1 = 19, so c = 2 and b = 1: the digits from the right are 1, 2, 4, 8, 16, 32. This is the summation formula the question asked for.

**Proof.** Put S = Σ (10^x·c)^k for k < K. The finite geometric sum gives (10^x·c − 1)·S = (10^x·c)^K − 1, so n·b·S = (10^x·c)^K − 1. Since n·P = 10^L − 1, subtracting gives n·(b·S − P) = (10^x·c)^K − 10^L, which is divisible by 10^L once xK ≥ L. As n is coprime to 10, b·S ≡ P (mod 10^L).

**Where the sequence starts.** David K's open point was that the backward series has no obvious starting place. It starts at the last block of the period, and that block is b. The reason is n·P = 99…9, so the last x digits u of P satisfy n·u ≡ −1 (mod 10^x), and b is the solution. For every n ending in 9, n = 10c − 1 gives b = 1: the period ends in 1 and the multiplier is the tens part plus one (2 for 19, 3 for 29, 9 for 89). For 1/7, 7·7 = 49 = 10·5 − 1, so the period ends in 7 and grows leftwards by fives: 7, 35, 175.

**When backward doubling occurs.** It needs c = 2, so n divides 2·10^x − 1: 19 (x = 1), 199 (x = 2), 1999 (x = 3). Since 19999 = 7·2857, 1/7 also doubles backwards in four-digit blocks: 2857, then 5714, giving …57142857.

**Why the question's sum showed the pattern in the integer part.** Take K larger than needed and the same proof gives n·b·S ≡ −1 modulo 10^(xK). So the partial sums agree with −1/n in more and more low-order digits. In the 10-adic numbers, where high powers of 10 are small, the series converges:

```latex
\sum_{k=0}^{\infty} (10^x c)^k = \frac{1}{1 - 10^x c} = -\frac{1}{b\,n} \quad \text{(10-adically)}
```

And −1/n is the 10-adic number …PPP, the period repeated forever to the left. Forward patterns are a real geometric series for 1/n with a small ratio r/10^x. Backward patterns are a 10-adic geometric series for −1/n with ratio 10^x·c. For 19 both come from the number 20: 1/19 = 1/20 + 1/20² + 1/20³ + … forwards, and −1/19 = 1 + 20 + 20² + … backwards. That is the precise form of David K's remark that 5/100 = 1/20.

## Fibonacci and other recurrences

The Fibonacci rows in the question's table are the same mechanism one order up: a two-term recurrence instead of a one-term one. The generating function of the Fibonacci numbers is X/(1 − X − X²). Evaluated at X = 1/10 it gives the forward pattern, and at X = 10 (10-adically) the backward one:

```latex
\frac{1}{89} = \sum_{k \ge 1} \frac{F_k}{10^{k+1}}, \qquad -\frac{1}{109} = \sum_{k \ge 1} F_k \, 10^{k-1} \quad \text{(10-adically)}
```

The denominators are 100 − 10 − 1 = 89 and 100 + 10 − 1 = 109. So 1/89 starts 0.0112358 and the period of 1/109 ends …23853211 (Fibonacci numbers 1, 1, 2, 3, 5, 8, 13, 21 placed right to left with carries), which confirms the question's "fibonacci reverse?" entry. Both identities were checked exactly, the second against all 108 digits of the period.

The geometric and Fibonacci views overlap. Because 100 − 89 = 11, David K's formula also gives 1/89 as powers of 11 in two-digit blocks: 0.01 + 0.0011 + 0.000121 + … Marjorie Bicknell-Johnson calls this the Pascal connection, since powers of 11 are rows of Pascal's triangle and its diagonals sum to Fibonacci numbers. Backwards, 89 = 10·9 − 1 and 109 = 10·11 − 1, so 1/89 ends in powers of 9 and 1/109 in powers of 11.

The general principle: take any sequence with a rational generating function G(X), set X = 1/10^x, and the resulting fraction shows the sequence in x-digit blocks. Powers of 2 give 1/98 and 1/998; Fibonacci numbers give 1/89, 1/9899, 1/998999; the natural numbers give 1/9801 and 1/998001. The doubling sequences are the simplest members of this family, with G(X) = 1/(1 − 2X).

## The "growing formula": what Divisionremnant most likely meant

Divisionremnant's 2025 answer gives no formula, and I found no other writing by that user, so what follows is an interpretation of the wording, not a confirmed reading. The answer says that base-10 numbers have "scales of magnitude", that these set ranges, and that every repeat is "grown from the upper boundary of the range" working downwards.

The most natural reading: the range of n is 10^(x−1) < n < 10^x, its upper boundary is 10^x, and working downwards means using the gap d = 10^x − n. That gap is the growth factor:

```latex
\frac{1}{n} = \sum_{k=0}^{\infty} \frac{(10^x - n)^k}{(10^x)^{k+1}}
```

Start with 1 in the first x-digit block, multiply by d for each next block, and add the overlaps. For 97 the blocks are 01, 03, 09, 27, 81; for 89 they are 01, 11, 121; for 7 they are 1, 3, 9, 27. This works for every n, which fits the claim that every inverse can be grown this way. It is not undisclosed: it is the formula in the asker's own 2015 comment and the m = 1 case of David K's series.

The companion question from July 2015 supports this reading. There the asker writes the same series with the scale made explicit, N = 10^(⌊log10 p⌋ + 1), which is exactly the upper boundary of the magnitude range of p. David K's answer to it proves the sum equals 1/p and adds that the choice of N makes little difference to the proof. His example there is 1/98 = 0.01 + 0.0002 + 0.000004 + …, the powers of 2 with no leading factor.

The asker's own notes from the same month say the same thing in words closer to Divisionremnant's. The stackedit link in the companion thread points to a GitHub gist written in July and August 2015, and it was read on 18 November 2026. It says that every sequence "starts with an exponent of 1", that one takes the next power of ten above n and subtracts n, and that the result is the growth factor. Its examples are 10 − 7 = 3 for 1/7, 100 − 49 = 51 for 1/49, 100 − 89 = 11 for 1/89 and 100 − 17 = 83 for 1/17. The gist ends with the same summation as the companion question, with the scale 10^(⌊log10 p⌋ + 1). So the growth from the upper boundary of the magnitude range was written down in 2015, ten years before Divisionremnant's answer. The gist is the asker's text, not Divisionremnant's, so it shows that the formula had been disclosed and does not show what Divisionremnant meant.

A second possible reading is growth from the right-hand end of the period, digit by digit: write the last digit, multiply by c, carry, repeat. That is the backward rule of the previous section, and it has been in print since Bharati Krishna Tirtha's Vedic Mathematics, where 1/19 is produced by repeated doubling from the right under the sutra Ekadhikena Purvena ("by one more than the previous one"). The user name itself points at the common root of both readings: the division remainder decides the multiplier.

## Verified table and corrections to the thread

All period lengths, digit sums and series in the thread were recomputed with exact integer arithmetic (see verify.py). The patterns hold with the seven corrections listed below. The table gives, for each n in the question, the clearest forward and backward pattern as first block × multiplier, with the block length x.

| n | Period L | Forward (left to right) | Backward (right to left) | Thread's description |
| --- | --- | --- | --- | --- |
| 7 | 6 | x=2: 14 × 2^k | x=1: 7 × 5^k | 14·2: correct |
| 19 | 18 | x=2: 05 × 5^k | x=1: 1 × 2^k | correct; "12·4 reverse" should be 21 × 4^k (x=2) |
| 47 | 46 | x=2: 02 × 6^k | x=2: 17 × 8^k | 02·6: correct |
| 49 | 42 | x=2: 02 × 2^k | x=1: 1 × 5^k | 02^n: correct |
| 71 | 35 | x=3: 014 × 6^k | x=3: 169 × 12^k | 014·6: correct |
| 79 | 13 | x=2: 01 × 21^k | x=1: 1 × 8^k | 1·8 reverse: correct |
| 83 | 41 | x=3: 012 × 4^k | x=1: 3 × 25^k | 012·4: correct |
| 89 | 44 | x=1: Fibonacci; x=2: 01 × 11^k | x=1: 1 × 9^k | fibonacci: correct |
| 97 | 96 | x=2: 01 × 3^k | x=1: 7 × 68^k | 03^n: correct |
| 109 | 108 | x=3: 009 × 19^k | x=1: Fibonacci; 1 × 11^k | fibonacci reverse: confirmed |
| 199 | 99 | x=3: 005 × 5^k | x=2: 01 × 2^k | correct |

### Corrections

- Question, 1/49: the sequence is written "02, 04, 08, 16, 32, 64, 124, 256"; 124 should be 128.
- The question's row for 1/19 gives "12·4 reverse". The two-digit backward series is 21 × 4^k because 100 × 4 ≡ 1 (mod 19) and (100 × 4 − 1)/19 = 21. The first two blocks read from the right are 21 and 84.
- Question, table row 79: the period is printed as 126582278481 (12 digits); the 13-digit period is 0126582278481.
- Question, comment formula: the index n is used for two things; the intended statement is David K's series with m = 1, which sums to 1/n.
- David K, tripling series for 1/7: the fifth term is printed as 0.0081; it is 0.00081.
- David K, examples table: the rows for n = 49, 71 and 83 are labelled 1/47, 1/49 and 1/49. The series themselves are right.
- David K, companion answer: "even when p ≠ 16^n − 1" should read 10^n − 1.

David K's six extra series (n = 17, 43, 51, 119, 127, 167) are all correct. The digit sums in the question follow Midy's pattern: when L is even the sum is 9·L/2, which holds for 7, 19, 47, 49, 89, 97 and 109.

## Connections: what is known and said elsewhere

The phenomenon is well known in pieces, under several names, but the forward and backward cases are rarely presented as one theory. These are the strongest hooks for the article.

| Topic | How it connects | Source |
| --- | --- | --- |
| Vedic mathematics | Tirtha's first sutra, Ekadhikena Purvena, computes 1/19 by doubling from the right with carries, and extends to denominators ending in 9. This is the backward rule with b = 1. | [Tadepalli's primer](https://tomrocksmaths.com/wp-content/uploads/2024/08/by-one-more-than-the-previous-one-a-primer-on-vedic-mathematics-sai-tadepalli.pdf) |
| Parasitic and Dyson numbers | 105263157894736842 doubles when its last digit moves to the front. It is the period of 2/19, and such numbers come from k/(10n − 1) in general. Backward doubling and this rotation property are the same fact. | [Wikipedia: Parasitic number](https://en.wikipedia.org/wiki/Parasitic_number) |
| Rotate to double | MathPages builds these numbers from powers of 2 modulo 19, and generalises to any ratio c and base B through the modulus cB − 1. | [MathPages: Rotate to Double](https://mathpages.com/home/kmath859/kmath859.htm) |
| The same question, asked again | A 2020 Codidact question asks why 1/(10n − 1) shows powers of n leftwards for 19, 29, 39, 49. Its three answers use a digit recurrence, a finite geometric sum with Euler's theorem, and a shift identity. | [Codidact question](https://math.codidact.com/q/278629) |
| Fibonacci Quarterly | Long (1981) derives 1/89, 1/109 and 1/9899 from one identity for two-term recurrences. Bicknell-Johnson (1989) studies repetends read from right to left, including geometric series and the powers-of-11 link. | [Long](https://www.mathstat.dal.ca/FQ/Scanned/19-1/long.pdf), [Bicknell-Johnson](https://www.mathstat.dal.ca/FQ/Scanned/27-5/bicknell.pdf) |
| Generating functions | Munafo shows how to design a fraction for any sequence with a rational generating function: powers of 2, Fibonacci, squares, in any base. | [Munafo: Fractions with Special Digit Sequences](https://mrob.com/pub/seq/digits.html) |
| Cyclic numbers and full reptend primes | When 10 is a primitive root mod p the period has p − 1 digits and its multiples are rotations of it. 7, 19, 47, 97 and 109 in the table are of this kind. | [Wikipedia: Repeating decimal](https://en.wikipedia.org/wiki/Repeating_decimal) |
| Midy's theorem | For a prime with even period, the second half of the period is the nines' complement of the first. It explains the digit sums in the question and halves the work of any growing rule. | [Wikipedia: Midy's theorem](https://en.wikipedia.org/wiki/Midy%27s_theorem) |
| p-adic numbers | Rational numbers have eventually periodic p-adic expansions. This is the setting in which the backward series converges, although base 10 is not a prime power and the 10-adic numbers are not a field. | [Wikipedia: p-adic number](https://en.wikipedia.org/wiki/P-adic_number) |

## Ideas for further substance

These are directions the article could take beyond the thread; none is settled in the sources above.

- A visibility measure. Define how many clean blocks a pattern shows, roughly x·log 10 / log r for m = 1, and rank all n below some bound. This would replace David K's "interesting" with a number.
- A duality statement. For the same x, the forward multiplier r and the backward multiplier c satisfy r·c ≡ 1 (mod n). Present forward and backward as one theorem about 10 and its inverse.
- Other bases. Everything holds with 10 replaced by any base B. In base 2 the denominators 2^x − 3 and 3·2^x − 1 give tripling patterns; MathPages works examples in base 6.
- Higher recurrences. Tribonacci and other linear recurrences give denominators such as 889 and 1109, which Bicknell-Johnson treats. A general statement for any linear recurrence would unify the table.
- A figure. Draw the staggered addition of blocks for 1/49 forwards and 1/19 backwards side by side, with the carries marked.
- Code. A short script that, given n, lists the best forward and backward pattern would let readers explore; verify.py is a starting point.

Open question for the author: should the article be expository (for a general maths audience) or aim at a short note with the unified theorem and proof?

## Sources

- Math StackExchange question 1365506, "Doubling sequences of the cyclic decimal parts of the fraction numbers" (MarkokraM, 2015), with answers by David K (2015) and Divisionremnant (2025). Read from a saved copy of the page: [thread](https://math.stackexchange.com/questions/1365506/doubling-sequences-of-the-cyclic-decimal-parts-of-the-fraction-numbers).
- Math StackExchange companion question, "Four mathematical notations for fraction 1/999 and how to show/present they are equal" (MarkokraM, 2015), with David K's answer 1372077. Read from a saved copy: [answer](https://math.stackexchange.com/a/1372077/139123).
- Calvin T. Long, "The Decimal Expansion of 1/89 and Related Results", The Fibonacci Quarterly, February 1981, pp. 53–55: [PDF](https://www.mathstat.dal.ca/FQ/Scanned/19-1/long.pdf).
- Marjorie Bicknell-Johnson, "Retrograde Renegades and the Pascal Connection", The Fibonacci Quarterly, November 1989, pp. 448–457: [PDF](https://www.mathstat.dal.ca/FQ/Scanned/27-5/bicknell.pdf).
- Robert Munafo, "Fractions with Special Digit Sequences": [mrob.com](https://mrob.com/pub/seq/digits.html).
- MathPages, "Rotate to Double": [mathpages.com](https://mathpages.com/home/kmath859/kmath859.htm).
- Codidact, "Why does the decimal expansion of 1/(10n − 1) have this neat pattern?": [math.codidact.com](https://math.codidact.com/q/278629).
- Sai Tadepalli, "By one more than the previous one: a primer on Vedic mathematics": [PDF](https://tomrocksmaths.com/wp-content/uploads/2024/08/by-one-more-than-the-previous-one-a-primer-on-vedic-mathematics-sai-tadepalli.pdf).
- Wikipedia: [Repeating decimal](https://en.wikipedia.org/wiki/Repeating_decimal), [Parasitic number](https://en.wikipedia.org/wiki/Parasitic_number), [Midy's theorem](https://en.wikipedia.org/wiki/Midy%27s_theorem), [p-adic number](https://en.wikipedia.org/wiki/P-adic_number).

All numerical claims in this article are checked by verify.py (exact integer arithmetic), last run 18 November 2026.
