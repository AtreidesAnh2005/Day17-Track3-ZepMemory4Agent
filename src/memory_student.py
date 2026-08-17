from __future__ import annotations

import json
import re
from types import SimpleNamespace
from typing import Any

from .config import settings
from .context_budget import ContextBudgetManager
from .utils import cap_query, join_nonempty
from .zep_common import prime_eval_thread, render_graph_search

# Concise, code-bearing episodes/documents (e.g. ASYNC-FIX-20, BUDGET-10-4-3-3)
# carry the most ground-truth signal per token but can rank behind longer,
# low-signal hits (e.g. previously-primed eval queries). Sorting these first
# keeps them from being cut off by the tight per-layer token budget in
# assemble_context, which only trims off the tail of the combined text.
_MARKER_RE = re.compile(r"\b[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+\b")

# render_graph_search only reads these attributes off its `results` argument.
_RENDER_FIELDS = ("context", "edges", "episodes", "nodes", "observations", "thread_summaries")


def _reorder_episodes(results: Any, episodes: list[Any]) -> Any:
    # The SDK's search-result object is a frozen pydantic model, so
    # `results.episodes = ...` raises and would need to be swallowed —
    # silently leaving the original, unreordered episodes in place. Build a
    # plain namespace copy instead so the reordering actually takes effect.
    fields = {name: getattr(results, name, None) for name in _RENDER_FIELDS}
    fields["episodes"] = episodes
    return SimpleNamespace(**fields)


def _sort_marker_first(episodes: list[Any]) -> list[Any]:
    return sorted(episodes, key=lambda ep: not _MARKER_RE.search(getattr(ep, "content", "") or ""))


def _collapse_semantic_duplicates(episodes: list[Any]) -> list[Any]:
    # add_semantic_documents ingests each domain-KB item twice: once as a raw
    # JSON blob and once as its plain "summary" sentence. Both carry the same
    # marker, so keeping both just burns twice the tight semantic budget for
    # the same fact. Collapse each to its summary text and drop repeats.
    seen: set[str] = set()
    out: list[Any] = []
    for ep in episodes:
        content = getattr(ep, "content", "") or ""
        text = content
        if text.strip().startswith("{"):
            try:
                text = json.loads(text).get("summary") or content
            except Exception:
                text = content
        key = text.strip()
        if key and key not in seen:
            seen.add(key)
            out.append(SimpleNamespace(content=text))
    return out


def _drop_eval_probes(episodes: list[Any]) -> list[Any]:
    # prime_eval_thread (used by retrieve_long_term) writes each eval query
    # into the user graph as a message from role="Evaluation User" so Zep can
    # compute a relevant Context Block for it. That probe message is not real
    # memory, but user-scoped episode search still returns it, and after many
    # cases run it can crowd out genuine reflections under the tight episodic
    # budget. Drop it by the role it was tagged with at write time.
    return [ep for ep in episodes if getattr(ep, "role", "") != "Evaluation User"]


class StudentMemory:
    """Only this file needs to be edited by students."""

    def __init__(self, client: Any):
        self.client = client
        self.budget = ContextBudgetManager(settings.context_tokens)

    # NOTE: Zep rejects graph.search queries longer than 400 characters. Some
    # eval queries are longer than that, so wrap every query with
    # `cap_query(query)` (see src/utils.py) before passing it to graph.search.

    def retrieve_long_term(self, user_id: str, thread_id: str, query: str) -> str:
        # LAB TODO 1/4
        # 1) prime_eval_thread(...) has already been provided as scaffolding.
        # 2) call thread.get_user_context(thread_id=...)
        # 3) return the .context string.
        # Bonus: append graph.search(scope="edges", limit>=20) facts with
        #        validity ranges (a low limit can miss deadline/open-loop facts).
        prime_eval_thread(self.client, user_id, thread_id, query)
        user_context = self.client.thread.get_user_context(thread_id=thread_id)
        context_block = getattr(user_context, "context", "") or ""

        # Bonus: edges carry validity ranges, which is what lets a recency/
        # conflict query (e.g. E08) tell an old fact from the current one.
        try:
            facts = self.client.graph.search(
                user_id=user_id,
                query=cap_query(query),
                scope="edges",
                limit=20,
            )
            fact_text = render_graph_search(facts)
        except Exception:
            fact_text = ""

        # Bonus: fact extraction can drop literal formatting (e.g. "16:00"
        # collapses into the LAB-REPORT-1600 marker), and the Context Block
        # only carries a small, relevance-limited slice of raw episodes. A raw
        # episode search backfills exact wording for deadline/open-loop
        # queries that need the literal text, not just the extracted fact.
        try:
            raw = self.client.graph.search(
                user_id=user_id,
                query=cap_query(query),
                scope="episodes",
                limit=15,
            )
            episodes = _drop_eval_probes(getattr(raw, "episodes", None) or [])
            episodes = _sort_marker_first(episodes)
            episode_text = render_graph_search(_reorder_episodes(raw, episodes), episode_char_cap=180)
        except Exception:
            episode_text = ""
        return join_nonempty([context_block, fact_text, episode_text], sep="\n\n")

    def retrieve_episodic(self, user_id: str, query: str) -> str:
        # LAB TODO 2/4
        # Use client.graph.search(user_id=..., query=cap_query(query),
        #     scope="episodes", limit=...) then render_graph_search(...).
        # Tip: verbose session episodes can crowd out concise, marker-bearing
        # reflections under the tight episodic budget — render_graph_search
        # accepts an `episode_char_cap` to keep more distinct episodes.
        results = self.client.graph.search(
            user_id=user_id,
            query=cap_query(query),
            scope="episodes",
            limit=15,
        )
        episodes = _drop_eval_probes(getattr(results, "episodes", None) or [])
        episodes = _sort_marker_first(episodes)
        return render_graph_search(_reorder_episodes(results, episodes), episode_char_cap=180)

    def retrieve_semantic(self, graph_id: str, query: str) -> str:
        # LAB TODO 3/4
        # Search the standalone graph (graph_id, NOT user_id).
        # Recommended: scope="episodes" — it returns raw document text that keeps
        # literal markers (e.g. PAYMENT-RULE-3). The "auto" scope returns
        # extracted facts that DROP those literal codes, so avoid it here.
        # Fallback: scope="nodes".
        q = cap_query(query)
        try:
            results = self.client.graph.search(
                graph_id=graph_id,
                query=q,
                scope="episodes",
                limit=8,
            )
        except Exception:
            results = self.client.graph.search(
                graph_id=graph_id,
                query=q,
                scope="nodes",
                limit=8,
            )
        episodes = _collapse_semantic_duplicates(getattr(results, "episodes", None) or [])
        episodes = _sort_marker_first(episodes)
        return render_graph_search(_reorder_episodes(results, episodes))

    def assemble_context(self, layers: dict[str, str]) -> tuple[str, dict[str, dict[str, int]]]:
        # LAB TODO 4/4
        # Use ContextBudgetManager to enforce 10/4/3/3 budget and priority order.
        return self.budget.assemble(layers)
