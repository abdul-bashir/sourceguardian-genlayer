# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


class SourceGuardian(gl.Contract):
    """
    SourceGuardian: an evidence-backed claim verifier for GenLayer.

    What it demonstrates:
    - Persistent contract state
    - Web access via gl.nondet.web.get()
    - LLM reasoning via gl.nondet.exec_prompt()
    - Custom equivalence validation with gl.vm.run_nondet_unsafe()
    - Conservative structured output: SUPPORTED / REFUTED / INCONCLUSIVE
    """

    claim: str
    source_a: str
    source_b: str
    source_c: str

    verdict: str
    confidence: u32
    rationale: str
    last_checked_sources: str
    resolved: bool

    def __init__(self, claim: str, source_a: str, source_b: str, source_c: str):
        self.claim = claim
        self.source_a = source_a
        self.source_b = source_b
        self.source_c = source_c

        self.verdict = "UNRESOLVED"
        self.confidence = u32(0)
        self.rationale = ""
        self.last_checked_sources = ""
        self.resolved = False

    def _extract_json(self, raw: str) -> typing.Any:
        """
        Best-effort JSON extraction.
        LLMs sometimes add extra text around JSON. This trims to the first JSON object.
        """
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return {
                "verdict": "INCONCLUSIVE",
                "confidence": 0,
                "rationale": "Model did not return valid JSON."
            }

        try:
            data = json.loads(raw[start:end + 1])
        except Exception:
            return {
                "verdict": "INCONCLUSIVE",
                "confidence": 0,
                "rationale": "JSON parsing failed."
            }

        verdict = str(data.get("verdict", "INCONCLUSIVE")).upper()
        if verdict not in ["SUPPORTED", "REFUTED", "INCONCLUSIVE"]:
            verdict = "INCONCLUSIVE"

        try:
            confidence = int(data.get("confidence", 0))
        except Exception:
            confidence = 0

        if confidence < 0:
            confidence = 0
        if confidence > 100:
            confidence = 100

        rationale = str(data.get("rationale", ""))[:900]

        return {
            "verdict": verdict,
            "confidence": confidence,
            "rationale": rationale
        }

    @gl.public.write
    def resolve(self) -> typing.Any:
        """
        Fetch up to three public URLs, ask the LLM whether they support the claim,
        and store a compact result on-chain.
        """

        # Copy storage to memory before non-deterministic execution.
        claim = self.claim
        source_a = self.source_a
        source_b = self.source_b
        source_c = self.source_c

        def fetch_text(url: str) -> str:
            if url == "":
                return ""
            try:
                response = gl.nondet.web.get(url)
                # Keep prompt compact. Large pages can make LLM calls unstable.
                return response.body.decode("utf-8", errors="ignore")[:5000]
            except Exception:
                return "[FETCH_FAILED]"

        def leader_fn() -> typing.Any:
            text_a = fetch_text(source_a)
            text_b = fetch_text(source_b)
            text_c = fetch_text(source_c)

            prompt = f"""
You are an evidence verification engine for an on-chain GenLayer contract.

Claim:
{claim}

Sources:
SOURCE_A_URL: {source_a}
SOURCE_A_TEXT:
{text_a}

SOURCE_B_URL: {source_b}
SOURCE_B_TEXT:
{text_b}

SOURCE_C_URL: {source_c}
SOURCE_C_TEXT:
{text_c}

Task:
Decide whether the provided sources support, refute, or do not clearly establish the claim.

Return ONLY valid JSON with this exact shape:
{{
  "verdict": "SUPPORTED" | "REFUTED" | "INCONCLUSIVE",
  "confidence": integer from 0 to 100,
  "rationale": "one concise sentence explaining the evidence"
}}

Rules:
- Use SUPPORTED only if the sources clearly support the claim.
- Use REFUTED only if the sources clearly contradict the claim.
- Use INCONCLUSIVE if sources are missing, ambiguous, unavailable, or insufficient.
- Do not invent facts outside the provided source text.
"""
            raw = gl.nondet.exec_prompt(prompt)
            return self._extract_json(raw)

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False

            validator_data = leader_fn()
            leader_data = leader_result.calldata

            try:
                same_verdict = leader_data["verdict"] == validator_data["verdict"]
                confidence_close = abs(int(leader_data["confidence"]) - int(validator_data["confidence"])) <= 20
                rationale_present = len(str(leader_data.get("rationale", ""))) > 0
                return same_verdict and confidence_close and rationale_present
            except Exception:
                return False

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        self.verdict = str(result["verdict"])
        self.confidence = u32(int(result["confidence"]))
        self.rationale = str(result["rationale"])[:900]
        self.last_checked_sources = source_a + " | " + source_b + " | " + source_c
        self.resolved = True

    @gl.public.view
    def get_claim(self) -> str:
        return self.claim

    @gl.public.view
    def get_verdict(self) -> str:
        return self.verdict

    @gl.public.view
    def get_confidence(self) -> u32:
        return self.confidence

    @gl.public.view
    def get_rationale(self) -> str:
        return self.rationale

    @gl.public.view
    def get_sources(self) -> str:
        return self.last_checked_sources

    @gl.public.view
    def get_summary(self) -> str:
        return (
            "Claim: " + self.claim
            + " | Verdict: " + self.verdict
            + " | Confidence: " + str(self.confidence)
            + " | Rationale: " + self.rationale
        )
