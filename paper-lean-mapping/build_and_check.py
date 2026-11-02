#!/usr/bin/env python3
"""Build source indexes and check the paper-to-Lean and exact-check mapping.

The paper inventory (title, authors, numbered sections including the
appendices, and every numbered theorem, proposition, lemma, corollary,
definition, example and remark), the Lean declarations and audit probes, the
exact-check functions and the generated tables in by-section.md must agree
with mapping.json. Any mismatch fails closed. Python standard library only;
the output is identical under python -O.
"""

import ast
import copy
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENTS = {
    "theorem": "Theorem", "proposition": "Proposition", "lemma": "Lemma",
    "corollary": "Corollary", "definition": "Definition", "example": "Example",
    "remark": "Remark",
}
COVERAGES = {"paper_only", "partial_lean", "finite_checks_only"}
BY_SECTION = "paper-lean-mapping/by-section.md"
MAPPING = "paper-lean-mapping/mapping.json"
AXIOMS = "lean/audit/Axioms.lean"
EXACT_SOURCES = (
    "verification/core/verification/check_charts.py",
    "verification/core/verification/exact_cyclotomic.py",
    "verification/core/families/monomial-products/verification/check_exact.py",
)
TITLE_BREAK = re.compile(r"\\\\\[[0-9]+pt\]\\large\s+")


def need(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def reject_number(value):
    raise SystemExit("FAIL: unsupported JSON number")


def parse_json(data):
    return json.loads(data, object_pairs_hook=unique_object,
                      parse_float=reject_number, parse_constant=reject_number)


def keys(value, expected, label):
    need(isinstance(value, dict) and set(value) == set(expected), label + " fields")


def string(value, label):
    need(isinstance(value, str) and value.strip(), label + " text")


def strings(values, label):
    need(isinstance(values, list) and all(isinstance(x, str) for x in values), label)
    need(len(values) == len(set(values)), "duplicate " + label)
    for value in values:
        string(value, label)


def safe_path(name):
    need(isinstance(name, str) and name and "\\" not in name, "source path")
    p = Path(name)
    need(not p.is_absolute() and ".." not in p.parts and str(p) == name, "source path")
    return p


def read_inputs():
    names = {AXIOMS, MAPPING, BY_SECTION}
    names.update(str(p.relative_to(ROOT)) for p in (ROOT / "paper").rglob("*.tex"))
    names.update(str(p.relative_to(ROOT)) for p in (ROOT / "lean/TR29").rglob("*.lean"))
    names.add("lean/TR29.lean")
    names.update(EXACT_SOURCES)
    result = {}
    for name in sorted(names):
        p = ROOT / safe_path(name)
        need(p.is_file() and not p.is_symlink(), "missing or linked source: " + name)
        need(p.stat().st_size <= 4000000, "oversized source: " + name)
        result[name] = p.read_text(encoding="utf-8")
    return result


def tex_uncomment(line):
    for i, char in enumerate(line):
        if char == "%":
            j = i - 1
            while j >= 0 and line[j] == "\\":
                j -= 1
            if (i - j - 1) % 2 == 0:
                return line[:i]
    return line


def display_title(name):
    """Markdown form of a bracketed TeX result name: $x$ becomes $`x`$."""
    need(name.count("$") % 2 == 0 and "`" not in name and "|" not in name, "result name text")
    return re.sub(r"\$([^$]+)\$", lambda m: "$`" + m.group(1) + "`$", name)


def paper_index(sources, entry):
    """Read sections, appendices and the per-environment section counters in TeX order."""
    seen = set()

    def expand(name):
        safe_path(name)
        need(name.startswith("paper/") and name.endswith(".tex"), "paper input path")
        need(name in sources, "missing paper input: " + name)
        need(name not in seen, "repeated paper input: " + name)
        seen.add(name)
        output = []
        for line in sources[name].splitlines():
            line = tex_uncomment(line)
            if re.search(r"\\(?:input|include)\b", line):
                match = re.fullmatch(r"\s*\\input\{([A-Za-z0-9_/-]+)\}\s*", line)
                need(match is not None, "unsupported paper inclusion")
                output.extend(expand("paper/" + match.group(1) + ".tex"))
            else:
                output.append((name, line))
        return output

    expanded = expand(entry)
    need(seen == {n for n in sources if n.startswith("paper/") and n.endswith(".tex")},
         "unreferenced paper source")
    text = "\n".join(line for _, line in expanded)
    declarations = re.findall(r"\\newtheorem(?:\*)?[^\n]*", text)
    expected = [r"\newtheorem{" + env + "}{" + title + "}[section]"
                for env, title in ENVIRONMENTS.items()]
    need(declarations == expected, "unsupported theorem counter declaration")
    need(not re.search(r"\\(?:setcounter|addtocounter|counterwithin|counterwithout|"
                       r"numberwithin|refstepcounter|stepcounter)\b", text),
         "unsupported paper counter modification")
    need(len(re.findall(r"\\appendix\b", text)) == 1, "paper appendix transition")
    titles = re.findall(r"\\title\{([^{}]*)\}", text)
    need(len(titles) == 1, "paper title declaration")
    parts = TITLE_BREAK.split(titles[0])
    need(len(parts) == 2 and all(p.strip() == p and p for p in parts), "paper title layout")
    author = re.search(r"\\author\{(.*?)\\date\{", text, re.S)
    need(author is not None, "paper author declaration")
    authors = re.findall(r"^([A-Z][A-Za-z.-]*(?: [A-Z][A-Za-z.-]*)+)(?:\\thanks\{[^{}]*\})?\\\\$",
                         author.group(1), re.M)
    token = re.compile(
        r"\\section(\*)?\{([^{}]+)\}|"
        r"\\(begin|end)\{([^{}]+)\}(?:\[([^\[\]]*)\])?|\\label\{([^{}]+)\}|\\(appendix)\b")
    sections, results, labels, stack = [], [], {}, []
    section = 0
    counters = {}
    appendix = False
    code = "0"
    active = None
    for source, line in expanded:
        for match in token.finditer(line):
            starred, title, command, env, name, label, start_appendix = match.groups()
            if start_appendix:
                need(not appendix and active is None and section > 0, "unsupported appendix placement")
                appendix = True
                section = 0
                code = "0"
            elif title is not None:
                need(active is None, "section inside numbered result")
                if not starred:
                    section += 1
                    need(not appendix or section <= 26, "unsupported appendix counter")
                    code = chr(64 + section) if appendix else str(section)
                    counters = {}
                    sections.append({"number": code, "title": title, "source": source})
            elif command == "begin":
                stack.append(env)
                if env in ENVIRONMENTS:
                    need(active is None and section > 0, "nested or unsectioned numbered result")
                    counters[env] = counters.get(env, 0) + 1
                    active = {"environment": env, "number": code + "." + str(counters[env]),
                              "section": code, "source": source, "labels": [], "depth": len(stack),
                              "name": name}
                need(env.rstrip("*") not in ENVIRONMENTS or env in ENVIRONMENTS,
                     "unsupported unnumbered result environment")
            elif command == "end":
                need(stack and stack[-1] == env, "unbalanced paper environment")
                if active is not None and len(stack) == active["depth"]:
                    need(len(active["labels"]) <= 1, "numbered result has more than one direct label")
                    need(active["name"] is not None, "numbered result without bracketed name")
                    results.append({k: active[k] for k in
                                    ("environment", "number", "section", "source", "name")} |
                                   {"label": active["labels"][0] if active["labels"] else None})
                    active = None
                stack.pop()
            else:
                need(label not in labels, "duplicate paper label")
                labels[label] = {"section": code, "source": source}
                if active is not None and len(stack) == active["depth"]:
                    active["labels"].append(label)
    need(not stack and active is None, "unclosed paper environment")
    front = {"title": parts[0], "subtitle": parts[1], "authors": authors}
    return front, sections, results, labels


def lean_without_comments(text):
    """Mask strings and nested comments before looking for declarations."""
    out = []
    i = depth = 0
    quoted = False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                depth += 1
                out.extend("  ")
                i += 2
            elif text.startswith("-/", i):
                depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif quoted:
            if text[i] == "\\":
                need(i + 1 < len(text), "unterminated Lean string")
                out.extend("  ")
                i += 2
            else:
                quoted = text[i] != '"'
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif text.startswith("/-", i):
            depth = 1
            out.extend("  ")
            i += 2
        elif text.startswith("--", i):
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            out.extend(" " * (end - i))
            i = end
        elif text[i] == '"':
            quoted = True
            out.append(" ")
            i += 1
        else:
            out.append(text[i])
            i += 1
    need(not depth and not quoted, "unterminated Lean comment or string")
    return "".join(out)


def lean_index(sources):
    declarations = {}
    for source, text in sources.items():
        if not source.endswith(".lean") or source == AXIOMS:
            continue
        namespaces = []
        for line in lean_without_comments(text).splitlines():
            match = re.match(r"\s*namespace\s+([A-Za-z_][A-Za-z0-9_.]*)\s*$", line)
            if match:
                namespaces.append(match.group(1))
                continue
            match = re.match(r"\s*end(?:\s+([A-Za-z_][A-Za-z0-9_.]*))?\s*$", line)
            if match:
                need(namespaces and (match.group(1) is None or match.group(1) == namespaces[-1]),
                     "unsupported Lean namespace end")
                namespaces.pop()
                continue
            match = re.match(r"\s*(?:noncomputable\s+)?(def|theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_']*)\b(.*)", line)
            if match:
                kind, name, header = match.groups()
                name = ".".join(namespaces + [name])
                need(name not in declarations, "duplicate Lean declaration")
                declarations[name] = {"source": source, "kind": kind, "header": header}
        need(not namespaces, "unclosed Lean namespace")
    return declarations


def audit_registry(sources):
    """Read every exact-type probe and axiom request from the Lean audit."""
    registry = {}
    requested = []
    imported = False
    for line in lean_without_comments(sources[AXIOMS]).splitlines():
        line = line.strip()
        if not line:
            continue
        if line == "import TR29":
            need(not imported, "duplicate audit import")
            imported = True
            continue
        match = re.fullmatch(r"example\s*:\s*(TR29\.[A-Za-z_][A-Za-z0-9_]*)\s*:=\s*"
                             r"(TR29\.[A-Za-z_][A-Za-z0-9_]*)", line)
        if match:
            prop, theorem = match.groups()
            need(prop not in registry and theorem not in registry.values(), "duplicate audit type probe")
            registry[prop] = theorem
            continue
        match = re.fullmatch(r"#print\s+axioms\s+(TR29\.[A-Za-z_][A-Za-z0-9_]*)", line)
        need(match is not None, "unsupported audit declaration")
        requested.append(match.group(1))
    need(imported, "missing audit import")
    need(len(requested) == len(set(requested)) and set(requested) == set(registry.values()),
         "audit axiom-request coverage")
    return registry


def validate(mapping, sources):
    keys(mapping, {"schema_version", "paper", "paper_title", "paper_subtitle", "paper_authors",
                   "scope", "sections", "lean_targets", "exact_checks", "numbered_results",
                   "supporting_steps", "aggregate"}, "mapping")
    need(type(mapping["schema_version"]) is int and mapping["schema_version"] == 3, "schema version")
    need(mapping["paper"] == "paper/main.tex", "paper entry point")
    string(mapping["scope"], "mapping scope")
    string(mapping["paper_title"], "paper title")
    string(mapping["paper_subtitle"], "paper subtitle")
    strings(mapping["paper_authors"], "paper authors")
    front, sections, inventory, labels = paper_index(sources, mapping["paper"])
    need(front["title"] == mapping["paper_title"], "paper title mismatch")
    need(front["subtitle"] == mapping["paper_subtitle"], "paper subtitle mismatch")
    need(front["authors"] == mapping["paper_authors"], "paper author mismatch")
    need(isinstance(mapping["sections"], list), "sections list")
    for item in mapping["sections"]:
        keys(item, {"number", "title", "source"}, "section")
        string(item["number"], "section number")
        string(item["title"], "section title")
        string(item["source"], "section source")
        need("|" not in item["title"] and "$" not in item["title"], "section title text")
    need(mapping["sections"] == sections, "section inventory mismatch")
    declarations = lean_index(sources)
    registry = audit_registry(sources)
    targets = {}
    need(isinstance(mapping["lean_targets"], list), "Lean targets list")
    for item in mapping["lean_targets"]:
        keys(item, {"id", "declaration", "source", "proposition", "proposition_source", "scope"}, "Lean target")
        for key in item:
            string(item[key], "Lean target " + key)
        name = item["id"]
        need(name not in targets, "duplicate Lean target")
        targets[name] = item
        proof = declarations.get(item["declaration"])
        prop = declarations.get(item["proposition"])
        need(proof is not None and proof["source"] == item["source"] and proof["kind"] == "theorem",
             "missing mapped Lean theorem")
        need(prop is not None and prop["source"] == item["proposition_source"] and prop["kind"] == "def",
             "missing mapped Lean proposition")
        need(registry.get(item["proposition"]) == item["declaration"], "Lean target registry mismatch")
        need(re.fullmatch(r"\s*:\s*" + re.escape(item["proposition"].split(".")[-1]) +
                          r"\s*:=.*", proof["header"]) is not None, "mapped Lean theorem type")
    aggregate = mapping["aggregate"]
    keys(aggregate, {"declaration", "proposition", "source", "scope"}, "aggregate")
    need(aggregate["declaration"] == "TR29.core_theorems" and
         aggregate["proposition"] == "TR29.CoreTheorems", "aggregate target")
    aggregate_proof = declarations.get(aggregate["declaration"], {})
    aggregate_prop = declarations.get(aggregate["proposition"], {})
    need(aggregate_proof.get("source") == aggregate["source"] and
         aggregate_proof.get("kind") == "theorem",
         "missing aggregate Lean theorem")
    need(aggregate_prop.get("source") == "lean/TR29/Statement.lean" and
         aggregate_prop.get("kind") == "def", "missing aggregate Lean proposition")
    need(re.fullmatch(r"\s*:\s*CoreTheorems\s*:=.*", aggregate_proof["header"]) is not None,
         "aggregate Lean theorem type")
    need(registry == {x["proposition"]: x["declaration"] for x in targets.values()} |
         {aggregate["proposition"]: aggregate["declaration"]}, "unmapped Lean target registry entry")
    string(aggregate["scope"], "aggregate scope")
    checks = {}
    need(isinstance(mapping["exact_checks"], list), "exact checks list")
    for item in mapping["exact_checks"]:
        keys(item, {"id", "source", "function", "scope", "limitation"}, "exact check")
        for key in item:
            string(item[key], "exact check " + key)
        need(item["id"] not in checks, "duplicate exact check")
        checks[item["id"]] = item
        need(item["source"] in EXACT_SOURCES and item["source"] in sources,
             "missing exact-check source")
        tree = ast.parse(sources[item["source"]], filename=item["source"])
        functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
        need(functions.count(item["function"]) == 1, "missing mapped exact-check function")
    rows = mapping["numbered_results"]
    need(isinstance(rows, list), "numbered results list")
    row_index = []
    used_targets, used_checks, used_labels = set(), set(), set()

    def references(row, optional_label):
        need(isinstance(row["section"], str) and
             re.fullmatch(r"(?:[1-9][0-9]*|[A-Z])", row["section"]) is not None,
             "paper section number")
        string(row["source"], "paper source")
        strings(row["lean_targets"], "Lean references")
        strings(row["exact_checks"], "exact-check references")
        need(set(row["lean_targets"]) <= set(targets), "unknown Lean reference")
        need(set(row["exact_checks"]) <= set(checks), "unknown exact-check reference")
        if row["label"] is not None or not optional_label:
            string(row["label"], "paper label")
            need(row["label"] in labels, "missing mapped paper label")
            need(labels[row["label"]] == {"section": row["section"], "source": row["source"]},
                 "paper anchor location")
            need(row["label"] not in used_labels, "duplicate mapped paper label")
            used_labels.add(row["label"])
        used_targets.update(row["lean_targets"])
        used_checks.update(row["exact_checks"])
        string(row["covered"], "covered scope")
        string(row["paper_only"], "paper-only scope")

    for row in rows:
        keys(row, {"label", "environment", "number", "section", "source", "title", "coverage",
                   "lean_targets", "exact_checks", "covered", "paper_only"}, "numbered result")
        references(row, True)
        string(row["environment"], "result environment")
        need(row["environment"] in ENVIRONMENTS, "result environment")
        string(row["number"], "result number")
        string(row["title"], "result title")
        need(row["coverage"] in COVERAGES, "unsupported coverage claim")
        need((row["coverage"] == "partial_lean") == bool(row["lean_targets"]), "Lean coverage classification")
        need(row["coverage"] != "finite_checks_only" or bool(row["exact_checks"]), "empty finite coverage")
        need(row["coverage"] != "paper_only" or not row["exact_checks"], "paper-only classification")
        need("|" not in row["title"], "result title text")
        row_index.append({k: row[k] for k in ("label", "environment", "number", "section", "source")})
    need(row_index == [{k: v for k, v in x.items() if k != "name"} for x in inventory],
         "numbered result inventory mismatch")
    for row, item in zip(rows, inventory):
        need(row["title"] == display_title(item["name"]), "result title differs from paper")
    need(isinstance(mapping["supporting_steps"], list), "supporting steps list")
    for row in mapping["supporting_steps"]:
        keys(row, {"label", "section", "source", "title", "lean_targets", "exact_checks", "covered", "paper_only"},
             "supporting step")
        string(row["title"], "supporting title")
        need("|" not in row["title"], "supporting title text")
        references(row, False)
        need(bool(row["lean_targets"]) or bool(row["exact_checks"]), "supporting step without evidence")
    need(used_targets == set(targets), "unreferenced Lean target")
    need(used_checks == set(checks), "unreferenced exact check")
    check_by_section(mapping, targets, checks, sources[BY_SECTION])
    return len(sections), len(inventory), len(targets), len(checks), len(mapping["supporting_steps"])


def render_tables(mapping, targets, checks):
    """Render the two tables of by-section.md from the validated map."""

    def lean(row):
        return ", ".join("`" + targets[x]["declaration"] + "`" for x in row["lean_targets"])

    def exact(row):
        return ", ".join("`" + checks[x]["source"].split("/")[-1] + ":" + checks[x]["function"] + "`"
                         for x in row["exact_checks"])

    lines = ["| Paper result | Label | Coverage |", "| --- | --- | --- |"]
    for row in mapping["numbered_results"]:
        if row["coverage"] == "paper_only":
            coverage = "Paper only"
        elif row["coverage"] == "partial_lean":
            coverage = "Partial Lean coverage: " + lean(row)
            if row["exact_checks"]:
                coverage += "; finite exact checks: " + exact(row)
        else:
            coverage = "Paper proof; finite exact checks: " + exact(row)
        label = "`" + row["label"] + "`" if row["label"] is not None else "none"
        lines.append("| " + ENVIRONMENTS[row["environment"]] + " " + row["number"] + ": " + row["title"] +
                     " | " + label + " | " + coverage + " |")
    results = "\n".join(lines)
    lines = ["| Supporting anchor | Section | Lean targets | Exact checks |", "| --- | --- | --- | --- |"]
    for row in mapping["supporting_steps"]:
        lines.append("| `" + row["label"] + "`: " + row["title"] + " | " + row["section"] + " | " +
                     (lean(row) or "None") + " | " + (exact(row) or "None") + " |")
    return results, "\n".join(lines)


def check_by_section(mapping, targets, checks, text):
    need(text.endswith("\n") and "\r" not in text, "by-section text format")
    padded = "\n" + text
    for table in render_tables(mapping, targets, checks):
        need(padded.count("\n" + table + "\n") == 1, "by-section result table mismatch")
    headings = [line for line in text.splitlines() if line.startswith("## ")]
    expected = ["## " + x["number"] + ". " + x["title"] for x in mapping["sections"]]
    need(headings == expected, "by-section headings mismatch")


def negative_controls(mapping, sources):
    cases = []

    def changed(label, mutate, expected):
        bad_mapping, bad_sources = copy.deepcopy(mapping), dict(sources)
        mutate(bad_mapping, bad_sources)
        need(bad_mapping != mapping or bad_sources != sources, "inert negative control: " + label)
        cases.append((label, bad_mapping, bad_sources, expected))

    def row(m, label):
        found = [x for x in m["numbered_results"] if x["label"] == label]
        need(len(found) == 1, "negative-control fixture: " + label)
        return found[0]

    def edit(s, name, old, new):
        need(s[name].count(old) >= 1, "negative-control fixture: " + name)
        s[name] = s[name].replace(old, new, 1)

    main = "paper/main.tex"
    changed("missing paper label", lambda m, s: row(m, "thm:main").update(label="thm:absent"),
            "missing mapped paper label")
    changed("omitted numbered result", lambda m, s: m["numbered_results"].pop(),
            "numbered result inventory mismatch")
    changed("duplicate numbered result", lambda m, s: m["numbered_results"].append(row(m, "thm:main")),
            "duplicate mapped paper label")
    changed("wrong result number", lambda m, s: row(m, "thm:main").update(number="1.2"),
            "numbered result inventory mismatch")
    changed("shared counter numbering", lambda m, s: row(m, "lem:blocks").update(number="7.2"),
            "numbered result inventory mismatch")
    changed("label on unlabelled definition", lambda m, s: m["numbered_results"][0].update(label="thm:main"),
            "duplicate mapped paper label")
    changed("dropped result label", lambda m, s: row(m, "lem:division").update(label=None),
            "numbered result inventory mismatch")
    changed("missing Lean theorem", lambda m, s: edit(s, "lean/TR29/Series.lean",
            "theorem matrix_moment_leading", "theorem absent_leading"),
            "missing mapped Lean theorem")
    changed("comment-only Lean theorem", lambda m, s: s.update({"lean/TR29/Series.lean":
            "/- theorem matrix_moment_leading : MatrixMomentLeadingTheorem := by -/\n" +
            s["lean/TR29/Series.lean"].replace("theorem matrix_moment_leading", "theorem absent_leading", 1)}),
            "missing mapped Lean theorem")
    changed("wrong Lean theorem type", lambda m, s: edit(s, "lean/TR29/Series.lean",
            ": MatrixMomentLeadingTheorem :=", ": True :="),
            "mapped Lean theorem type")
    changed("missing Lean proposition", lambda m, s: edit(s, "lean/TR29/Statement.lean",
            "def UnivariateMomentBound", "def MissingMomentBound"),
            "missing mapped Lean proposition")
    changed("missing exact-type probe", lambda m, s: edit(s, AXIOMS,
            "example : TR29.UnivariateMomentBound := TR29.univariate_moment_bound", ""),
            "audit axiom-request coverage")
    changed("comment-only exact-type probe", lambda m, s: edit(s, AXIOMS,
            "example : TR29.UnivariateMomentBound := TR29.univariate_moment_bound",
            "-- example : TR29.UnivariateMomentBound := TR29.univariate_moment_bound"),
            "audit axiom-request coverage")
    changed("wrong exact-type probe", lambda m, s: edit(s, AXIOMS,
            "example : TR29.UnivariateMomentBound :=", "example : TR29.MissingMomentBound :="),
            "Lean target registry mismatch")
    changed("missing axiom request", lambda m, s: edit(s, AXIOMS,
            "#print axioms TR29.univariate_moment_bound", ""),
            "audit axiom-request coverage")
    changed("missing exact function", lambda m, s: m["exact_checks"][0].update(function="absent_check"),
            "missing mapped exact-check function")
    changed("exact check outside the verification tree", lambda m, s:
            m["exact_checks"][0].update(source="tools/check_markdown_math.py"),
            "missing exact-check source")
    changed("unreferenced exact check", lambda m, s: m["exact_checks"].append(
            {"id": "unreferenced", "source": EXACT_SOURCES[0], "function": "rational_rank",
             "scope": "x", "limitation": "x"}),
            "unreferenced exact check")
    changed("added unlabelled numbered result", lambda m, s: edit(s, main,
            r"\end{document}", r"\begin{lemma}[X]X\end{lemma}\end{document}"),
            "numbered result inventory mismatch")
    changed("added labelled numbered result", lambda m, s: edit(s, main,
            r"\end{document}", r"\begin{lemma}[X]\label{lem:unmapped}X\end{lemma}\end{document}"),
            "numbered result inventory mismatch")
    changed("doubly labelled numbered result", lambda m, s: edit(s, main,
            r"\end{document}", r"\begin{lemma}[X]\label{lem:x}\label{lem:y}X\end{lemma}\end{document}"),
            "numbered result has more than one direct label")
    changed("full formalization claim", lambda m, s: row(m, "thm:main").update(coverage="fully_formalized"),
            "unsupported coverage claim")
    changed("unknown Lean reference", lambda m, s: row(m, "thm:main")["lean_targets"].append("absent"),
            "unknown Lean reference")
    changed("Lean coverage misclassified", lambda m, s: row(m, "lem:anti").update(coverage="finite_checks_only"),
            "Lean coverage classification")
    changed("paper-only claim with checks", lambda m, s: row(m, "lem:bm-lattice").update(coverage="paper_only"),
            "paper-only classification")
    changed("shared theorem counter", lambda m, s: edit(s, main,
            r"\newtheorem{lemma}{Lemma}[section]", r"\newtheorem{lemma}[theorem]{Lemma}"),
            "unsupported theorem counter declaration")
    changed("missing appendix transition", lambda m, s: edit(s, main, "\\appendix\n", ""),
            "paper appendix transition")
    changed("stale paper title", lambda m, s: edit(s, main,
            r"\title{" + mapping["paper_title"],
            r"\title{The partially symmetric rank of products of binary monomials"),
            "paper title mismatch")
    changed("stale paper authors", lambda m, s: edit(s, main, "\nPing Nie\\\\\n", "\nTBD\\\\\n"),
            "paper author mismatch")
    changed("renamed section", lambda m, s: edit(s, "paper/sections/07_binary_monomials.tex",
            r"\section{Products of binary monomials}", r"\section{The binary-monomial extension}"),
            "section inventory mismatch")
    changed("unmapped section", lambda m, s: edit(s, main,
            r"\section*{Statements and Declarations}", r"\section{Statements and Declarations}"),
            "section inventory mismatch")
    changed("reinstated old input", lambda m, s: edit(s, main,
            r"\input{sections/07_binary_monomials}",
            r"\input{sections/07_binary_monomials}" + "\n" + r"\input{sections/lower_bound}"),
            "missing paper input: paper/sections/lower_bound.tex")
    changed("omitted section input", lambda m, s: edit(s, main,
            r"\input{sections/07_binary_monomials}", ""),
            "unreferenced paper source")
    changed("renamed paper result", lambda m, s: row(m, "thm:pm").update(title="Moment lower bound"),
            "result title differs from paper")
    changed("stale result table", lambda m, s: edit(s, BY_SECTION,
            "| Partial Lean coverage: ", "| Paper only: "),
            "by-section result table mismatch")
    changed("stale section heading", lambda m, s: edit(s, BY_SECTION,
            "\n## 8. Products of binary monomials\n", "\n## 8. The binary-monomial extension\n"),
            "by-section headings mismatch")
    for label, bad_mapping, bad_sources, expected in cases:
        try:
            validate(bad_mapping, bad_sources)
        except SystemExit as error:
            need(str(error) == "FAIL: " + expected, "wrong negative-control rejection: " + label)
        else:
            raise SystemExit("FAIL: accepted negative control: " + label)
    try:
        parse_json('{"schema_version":3,"schema_version":3}')
    except SystemExit as error:
        need(str(error) == "FAIL: duplicate JSON key", "wrong duplicate-key rejection")
    else:
        raise SystemExit("FAIL: duplicate JSON key accepted")
    try:
        parse_json('{"schema_version":3.0}')
    except SystemExit as error:
        need(str(error) == "FAIL: unsupported JSON number", "wrong non-integer rejection")
    else:
        raise SystemExit("FAIL: non-integer JSON number accepted")
    return len(cases) + 2


def main():
    need(len(sys.argv) == 1, "this command takes no arguments")
    sources = read_inputs()
    mapping = parse_json(sources[MAPPING])
    sections, results, targets, checks, supporting = validate(mapping, sources)
    controls = negative_controls(mapping, sources)
    need(read_inputs() == sources, "sources changed during check")
    print("PASS: paper title, authors, " + str(sections) + " numbered section titles and " +
          str(results) + " numbered results in TeX order")
    print("PASS: " + str(targets) + " algebraic Lean targets and their aggregate declaration")
    print("PASS: " + str(checks) + " exact-check links and " + str(supporting) + " supporting paper anchors")
    print("PASS: by-section tables and section headings agree with the map")
    print("PASS: " + str(controls) + " mapping negative controls")
    print("RESULT: PASS mapping structure; mathematical coverage is stated per entry")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, IndexError, AttributeError,
            SyntaxError, UnicodeError) as error:
        raise SystemExit("FAIL: mapping input: " + type(error).__name__)
