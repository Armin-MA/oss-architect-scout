"""Visual Markdown Presenter implementing IUIPresenter contract."""
from __future__ import annotations

from typing import List, Optional

from src.contracts.i_ui_presenter import IUIPresenter
from src.entities.candidate_repo import CandidateRepo
from src.entities.evaluation_score import EvaluationScore
from src.entities.host_profile import HostProfile
from src.utils.visual_formatter import VisualFormatter, format_progress_bar, format_shield_badge


class MarkdownPresenter(IUIPresenter):
    """Visual presenter producing structured GitHub Flavored Markdown reports."""

    def render_evaluation_report(
        self,
        scores: List[EvaluationScore],
        host_profile: Optional[HostProfile] = None,
    ) -> str:
        """Render single-turn visual markdown report from evaluation scores.

        Args:
            scores: List of evaluated candidates with dimensional scores.
            host_profile: Optional host architectural profile.

        Returns:
            Rich markdown string containing Shields.io badges, Mermaid flowchart,
            comparison matrix, and collapsible accordion details.

        Raises:
            ValueError: If scores is None or contains invalid items.
        """
        if scores is None:
            raise ValueError("scores list cannot be None")

        if not isinstance(scores, list):
            raise ValueError("scores must be a list of EvaluationScore instances")

        for idx, score in enumerate(scores):
            if not isinstance(score, EvaluationScore):
                raise ValueError(
                    f"Item at index {idx} is not an EvaluationScore instance: {type(score)}"
                )

        if not scores:
            return (
                "# OSS Candidate Evaluation Report\n\n"
                "No candidate repositories were found or evaluated.\n"
            )

        # Sort descending by final score
        sorted_scores = sorted(scores, key=lambda s: s.final_score, reverse=True)
        top_candidate = sorted_scores[0]

        parts: List[str] = []
        parts.append("# OSS Candidate Evaluation Report\n")

        # Top choice Shields.io badges
        badges = self._render_top_badges(top_candidate)
        parts.append(badges + "\n")

        # Host architectural profile context
        if host_profile:
            parts.append(self._render_host_context(host_profile) + "\n")

        # Mermaid Flowchart
        mermaid = self._render_mermaid_flowchart(sorted_scores, host_profile)
        parts.append(mermaid + "\n")

        # Comparison Matrix Table
        table = self._render_comparison_table(sorted_scores)
        parts.append(table + "\n")

        # Details Accordion per candidate
        details = self._render_details_accordion(sorted_scores)
        parts.append(details)

        return "\n".join(parts)

    def render_risk_confirmation(
        self,
        repo: CandidateRepo,
        risks: List[str],
    ) -> str:
        """Render risk confirmation dialog / text for high-threshold risk gates.

        Args:
            repo: Candidate repository entity under evaluation.
            risks: List of detected risk descriptions (e.g. license, security).

        Returns:
            Formatted warning string formatted under Zero Confirmation Bias protocol.

        Raises:
            ValueError: If repo is None or invalid type.
        """
        if repo is None or not isinstance(repo, CandidateRepo):
            raise ValueError("repo must be an instance of CandidateRepo")

        if risks is None:
            risks = []

        if not isinstance(risks, list):
            raise ValueError("risks must be a list of string descriptions")

        if not risks:
            return (
                f"No critical risks identified for repository **{repo.full_name}**. "
                "Candidate is safe to adopt."
            )

        risk_bullets = "\n".join(f"> - {risk}" for risk in risks)
        return (
            "> [!WARNING]\n"
            "> ### CRITICAL RISK CONFIRMATION REQUIRED\n"
            f"> Candidate repository **{repo.full_name}** has triggered {len(risks)} "
            "critical risk factor(s):\n"
            ">\n"
            f"{risk_bullets}\n"
            ">\n"
            "> **ACTION REQUIRED:** You must explicitly confirm or decline adoption under "
            "Zero Confirmation Bias protocol before proceeding with code integration."
        )

    def _render_top_badges(self, top: EvaluationScore) -> str:
        """Render summary Shields.io badges for the top candidate."""
        score_val = f"{top.final_score:.1f}/100"
        score_badge = format_shield_badge("Top Recommendation", top.repo.name, "blue")
        rating_badge = format_shield_badge("Final Score", score_val, "brightgreen")
        license_badge = format_shield_badge(
            "License", top.repo.license_spdx or "Unknown", "informational"
        )
        stars_badge = format_shield_badge("Stars", str(top.repo.stars), "yellow")
        return f"{score_badge} {rating_badge} {license_badge} {stars_badge}"

    def _render_host_context(self, host: HostProfile) -> str:
        """Render host architecture context block."""
        skills = ", ".join(host.active_skills) if host.active_skills else "None"
        banned = ", ".join(host.banned_libraries) if host.banned_libraries else "None"
        layers = " -> ".join(host.required_layers) if host.required_layers else "Standard Modular"

        return (
            "### Target Architecture Constraints\n\n"
            f"- **Architecture Type:** `{host.architecture_type}`\n"
            f"- **Strict Typing Required:** `{host.strict_typing}`\n"
            f"- **Enforced Layering:** `{layers}`\n"
            f"- **Active Host Skills:** `{skills}`\n"
            f"- **Banned Libraries:** `{banned}`"
        )

    def _render_mermaid_flowchart(
        self,
        scores: List[EvaluationScore],
        host_profile: Optional[HostProfile],
    ) -> str:
        """Generate Mermaid flowchart representing the candidate selection and pruning flow."""
        arch_label = (
            host_profile.architecture_type if host_profile else "Host Architecture"
        )
        top = scores[0]

        lines = [
            "### Evaluation Decision Pipeline\n",
            "```mermaid",
            "flowchart TD",
            f'    Host["Host Target: {arch_label}"] --> Funnel["Pruning Funnel (Veto & Heuristics)"]',
            f'    Funnel --> Candidates["Shortlisted Finalists ({len(scores)})"]',
        ]

        for idx, score in enumerate(scores, 1):
            node_id = f"C{idx}"
            label = f"#{idx} {score.repo.name} ({score.final_score:.1f})"
            lines.append(f'    Candidates --> {node_id}["{label}"]')

        top_id = "C1"
        lines.append(
            f'    {top_id} --> Selected["Top Recommended: {top.repo.full_name}"]'
        )
        lines.append("```")
        return "\n".join(lines)

    def _render_comparison_table(self, scores: List[EvaluationScore]) -> str:
        """Render GitHub flavored Markdown table comparing candidates."""
        lines = [
            "### Candidate Comparison Matrix\n",
            "| Rank | Repository | Final Score | Architecture | Cleanliness | Community | Popularity | Hygiene | License |",
            "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]

        for rank, score in enumerate(scores, 1):
            repo_link = f"[{score.repo.full_name}](https://github.com/{score.repo.full_name})"
            license_val = f"`{score.repo.license_spdx}`" if score.repo.license_spdx else "`Unknown`"
            row = (
                f"| {rank} | {repo_link} | **{score.final_score:.1f}** | "
                f"{score.architecture_score:.1f} | {score.cleanliness_score:.1f} | "
                f"{score.community_score:.1f} | {score.popularity_score:.1f} | "
                f"{score.hygiene_score:.1f} | {license_val} |"
            )
            lines.append(row)

        return "\n".join(lines)

    def _render_details_accordion(self, scores: List[EvaluationScore]) -> str:
        """Render collapsible HTML details accordion sections for each candidate."""
        sections: List[str] = ["### Deep Candidate Breakdowns\n"]

        for rank, score in enumerate(scores, 1):
            repo = score.repo
            desc = repo.description or "No description provided."
            analogy = score.vibe_analogy or "Standard modular open-source library"
            license_str = repo.license_spdx or "Unknown"

            strengths_list = (
                "\n".join(f"- {s}" for s in score.strengths)
                if score.strengths
                else "- No specific strengths highlighted."
            )
            weaknesses_list = (
                "\n".join(f"- {w}" for w in score.weaknesses)
                if score.weaknesses
                else "- No notable weaknesses recorded."
            )

            acc = (
                "<details>\n"
                f"<summary><b>#{rank} {repo.full_name} — Score: {score.final_score:.1f}/100</b></summary>\n\n"
                f"> **Description:** {desc}  \n"
                f"> **Stars:** {repo.stars:,} | **Forks:** {repo.forks:,} | **Open Issues:** {repo.open_issues:,} | **License:** `{license_str}`  \n"
                f"> **Architectural Vibe:** *{analogy}*\n\n"
                "#### Multi-Dimensional Scores\n"
                f"- **Architecture ({score.architecture_score:.1f}/100):** {format_progress_bar(score.architecture_score)}\n"
                f"- **Cleanliness ({score.cleanliness_score:.1f}/100):** {format_progress_bar(score.cleanliness_score)}\n"
                f"- **Community ({score.community_score:.1f}/100):** {format_progress_bar(score.community_score)}\n"
                f"- **Popularity ({score.popularity_score:.1f}/100):** {format_progress_bar(score.popularity_score)}\n"
                f"- **Hygiene ({score.hygiene_score:.1f}/100):** {format_progress_bar(score.hygiene_score)}\n\n"
                "#### Key Strengths\n"
                f"{strengths_list}\n\n"
                "#### Potential Weaknesses / Risks\n"
                f"{weaknesses_list}\n"
                "</details>\n"
            )
            sections.append(acc)

        return "\n".join(sections)
