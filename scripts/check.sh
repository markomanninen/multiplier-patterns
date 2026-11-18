#!/usr/bin/env bash
# Export a commit with git archive into the ignored .check folder and run
# verify.py, Maxima derivations.mac and the full LaTeX build on this machine.
# Usage: scripts/check.sh [commit], default HEAD. Run it before committing
# changes to paper/ or research/verify.py.
set -euo pipefail

commit="${1:-HEAD}"

repo_root="$(git rev-parse --show-toplevel)"
commit_sha="$(git -C "$repo_root" rev-parse --verify "${commit}^{commit}")"

for extra_bin in "$HOME/texlive/2026/bin/universal-darwin" "/opt/homebrew/bin"; do
  if [[ -d "$extra_bin" ]]; then
    export PATH="$extra_bin:$PATH"
  fi
done

out_dir="$repo_root/.check"
src_dir="$out_dir/src"
log_dir="$out_dir/logs"

rm -rf "$src_dir" "$log_dir"
mkdir -p "$src_dir" "$log_dir"

git -C "$repo_root" archive "$commit_sha" | tar -x -C "$src_dir"

echo "Checking research/verify.py on commit ${commit_sha:0:7}..."
verify_log="$log_dir/verify.log"
(
  cd "$src_dir"
  python3 research/verify.py
) > "$verify_log" 2>&1

awk '
  NF == 0 { next }
  $0 == "All checks passed." { next }
  $NF == "OK" { ok++; next }
  { bad++; print "verify.py line did not end with OK (" $0 ")" > "/dev/stderr" }
  END {
    if (bad > 0 || ok == 0) {
      exit 1
    }
  }
' "$verify_log"

echo "Checking paper/derivations.mac with Maxima..."
maxima_log="$log_dir/maxima.log"
(
  cd "$src_dir/paper"
  maxima -b derivations.mac
) > "$maxima_log" 2>&1

cleaned_maxima="$(sed -e 's/display2d:false//g' -e 's/dual_ok:false//g' -e '/CL-INFO::LOAD-PRIMARY-INDEX/d' "$maxima_log")"
if printf '%s\n' "$cleaned_maxima" | grep -Eiq '(^|[^[:alpha:]])(false|error)([^[:alpha:]]|$)|incorrect syntax'; then
  cat "$maxima_log" >&2
  echo "Maxima check failed because output contained false or an error." >&2
  exit 1
fi
grep -Eq "check: (true|t)" "$maxima_log"
grep -Eq "check \(Y-1\) S = Y\^K - 1: (true|t)" "$maxima_log"
grep -Eq "duality holds: (true|t)" "$maxima_log"

echo "Building paper/main.tex with pdflatex and bibtex..."
(
  cd "$src_dir/paper"
  pdflatex -interaction=nonstopmode -halt-on-error main.tex > "$log_dir/pdflatex-1.log" 2>&1
  bibtex main > "$log_dir/bibtex.log" 2>&1
  pdflatex -interaction=nonstopmode -halt-on-error main.tex > "$log_dir/pdflatex-2.log" 2>&1
  pdflatex -interaction=nonstopmode -halt-on-error main.tex > "$log_dir/pdflatex-3.log" 2>&1
)

if grep -Eiq 'error message|Warning--' "$log_dir/bibtex.log" "$src_dir/paper/main.blg"; then
  cat "$log_dir/bibtex.log" >&2
  echo "BibTeX reported an error or warning." >&2
  exit 1
fi

if grep -Eiq 'LaTeX Warning: (Reference|Citation).*undefined|There were undefined (references|citations)|There were multiply-defined labels|Label\(s\) may have changed|! LaTeX Error|! Emergency stop' "$log_dir/pdflatex-3.log" "$src_dir/paper/main.log"; then
  cat "$log_dir/pdflatex-3.log" >&2
  echo "LaTeX build reported an error or an undefined reference." >&2
  exit 1
fi

if [[ ! -s "$src_dir/paper/main.pdf" ]]; then
  echo "LaTeX build did not produce main.pdf." >&2
  exit 1
fi

cp "$src_dir/paper/main.pdf" "$out_dir/main.pdf"
echo "All checks passed and output was written to .check/main.pdf."
