#!/usr/bin/env python3
"""Derive the TMLR-format source from main.tex and subsections/*.tex.

Writes (from the repository root):
  main_tmlr.tex            anonymous review build (what would be uploaded)
  main_tmlr_preprint.tex   same text, non-anonymous ([preprint] option)
  tmlr/subsections/*.tex   copies of subsections/*.tex in which code links and the author
                           name go through macros that are neutral in the anonymous build
Text, tables and numbers are not changed.
Build (from repo root): tectonic -X compile -Z search-path=tmlr main_tmlr.tex
"""
import re, pathlib, glob, shutil
root = pathlib.Path(".")
out_sub = root / "tmlr" / "subsections"
if out_sub.exists():
    shutil.rmtree(out_sub)
out_sub.mkdir(parents=True)

def anon_macros(t):
    t = t.replace("\\href{https://github.com/", "\\codehref{https://github.com/")
    t = t.replace("\\url{https://github.com/", "\\codeurl{https://github.com/")
    t = t.replace("Julian~M.~Kleber", "\\authorname{}")
    t = t.replace("This preprint has one author", "This paper has one author")
    return t

for f in sorted(glob.glob("subsections/*.tex")):
    t = pathlib.Path(f).read_text(encoding="utf-8")
    pathlib.Path(out_sub / pathlib.Path(f).name).write_text(anon_macros(t), encoding="utf-8")

src = (root / "main.tex").read_text(encoding="utf-8")
pre_end = src.index("\\begin{document}")
pre, body = src[:pre_end], src[pre_end:]
title_tex = re.search(r"\\title\{(.*?)\}\n\\author", pre, flags=re.S).group(1).replace("\\\\\n", " ").replace("\n", " ")

pre = re.sub(r"\\documentclass\[[^\]]*\]\{article\}", "", pre)
for pkg in ("arxiv-twocolumn", "cite", "inputenc", "orcidlink", "balance", "dblfloatfix"):
    pre = re.sub(r"\\usepackage(\[[^\]]*\])?\{%s\}" % pkg, "", pre)
pre = re.sub(r"\\setcounter\{(topnumber|dbltopnumber|totalnumber)\}\{\d+\}", "", pre)
pre = re.sub(r"\\renewcommand\{\\(top|dbltop|text|floatpage|dblfloatpage)fraction\}\{[0-9.]*\}", "", pre)
pre = re.sub(r"\\setlength\{\\(floatsep|textfloatsep|intextsep|dblfloatsep|dbltextfloatsep)\}\{[^}]*\}", "", pre)
pre = pre.replace("\\raggedbottom", "")
pre = re.sub(r"\\title\{.*?\}\n\\author\{.*?\n\}\n\\date\{[^}]*\}\n\\newcommand\{\\papershorttitle\}\{[^}]*\}", "", pre, flags=re.S)

head = r"""\documentclass[10pt]{article}
% TMLR submission build. Default = anonymous review version.
% Non-anonymous (preprint / camera-ready) build: compile main_tmlr_preprint.tex.
\ifdefined\NONANON
  \usepackage[preprint]{tmlr}
\else
  \usepackage{tmlr}
\fi
\usepackage[utf8]{inputenc}
\setcitestyle{numbers,square,comma}
"""
title = r"""
\title{""" + title_tex + r"""}
\def\month{MM}\def\year{YYYY}\def\openreview{\url{https://openreview.net/forum?id=XXXX}}
\ifdefined\NONANON
\author{\name Julian M. Kleber \email julian.m.kleber@gmail.com \\
        \addr Independent Researcher \\
        ORCID: 0000-0001-5518-0932}
\newcommand{\authorname}{Julian~M.~Kleber}
\newcommand{\codehref}[2]{\href{#1}{#2}}
\newcommand{\codeurl}[1]{\url{#1}}
\else
\author{Anonymous authors}
\newcommand{\authorname}{The author}
\newcommand{\codehref}[2]{#2}
\newcommand{\codeurl}[1]{\textit{[URL withheld for double-blind review; added in the camera-ready version]}}
\fi
\providecommand{\keywords}[1]{}
"""
m = re.search(r"\\twocolumn\[\{%.*?\n\}\]", body, flags=re.S)
blk = m.group(0)
abs_ = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", blk, flags=re.S).group(0)
banner = "\\ifdefined\\NONANON\n\\par\\noindent{\\small Code and artifacts: \\url{https://github.com/reeldemo/denoise-opt}}\n\\fi\n"
body = body.replace(blk, "\\maketitle\n" + abs_ + "\n" + banner)
body = body.replace("\\input{subsections/", "\\input{tmlr/subsections/")
body = body.replace("\\balance\n", "")
(root / "main_tmlr.tex").write_text(head + pre.strip() + "\n" + title + body, encoding="utf-8")
(root / "main_tmlr_preprint.tex").write_text("\\def\\NONANON{1}\n\\input{main_tmlr.tex}\n", encoding="utf-8")
print("wrote main_tmlr.tex, main_tmlr_preprint.tex, tmlr/subsections/")
