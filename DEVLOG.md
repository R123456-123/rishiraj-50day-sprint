# Dev Log

## Day 01 — June 28, 2026

**Built:** Async token bucket rate limiter + FastAPI integration
**Learned:** asyncio event loop, coroutines, await, asyncio.gather, asyncio.Lock
**DSA:** Contains Duplicate (set) · Valid Anagram (dict)
**Result:** 5 req pass, 3 req blocked with 429 — working correctly
**Research:** Red team vs blue team on Oracle Flow — found over-refusal in attacker agent
**Confused by:** asyncio.Lock race condition — now clear
**Tomorrow:** Pydantic v2 deep dive + typed LLM response wrapper

---

## Day 02 — June 29, 2026

**DSA:** Two Sum (hashmap O(n) — diff = target - num pattern) ·
Group Anagrams (sorted string as key + defaultdict)
**Built:** Pydantic v2 deep dive — 3 sections

- Section 1: field_validator, model_validator — PropertyInput with
  price/address/cross-field validation
- Section 2: computed_field, Annotated, custom types
  (PositiveFloat, BedCount) — PropertyValuation with price_per_sqft
  and tier auto-calculated
- Section 3: Typed LLM response wrapper — ValuationResponse with
  SafetyStatus Enum, to_api_response() strips raw model output
  **Key insight:** model_dump() = internal data (everything).
  to_api_response() = external (strips raw LLM output, converts Enum to string)
  **Confused by:** Annotated syntax — now clear (type + metadata together)
  **Tomorrow:** Decorators + Oracle Flow Researcher agent

---

## Day 03 — June 30, 2026

**DSA:** Top K Frequent Elements (3 approaches — sort O(n log n),
min-heap O(n log k), bucket sort O(n)) · Encode/Decode Strings
(length-prefix O(n+m))
**Milestone:** All 8 arrays/hashing problems in Blind 75 complete
**Built:** @retry_with_backoff decorator started (completed day 04)
**Key insight:** 3 layers needed because decorator takes arguments —
outer holds config, middle receives function, inner does the work
**Confused by:** Forgot await on asyncio.sleep — caught by RuntimeWarning
**Carried over:** Oracle Flow Researcher agent, jailbreak experiment,
Constitutional AI paper
**Tomorrow:** Decorators done → Oracle Flow Researcher agent
