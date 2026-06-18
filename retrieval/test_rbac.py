"""
Smoke test for role-based access control at the vector-store level.

A nurse must never receive billing/clinical-only chunks; a billing
executive must be able to reach billing content.
"""

from retrieval.rag_retriever import retrieve


def collections_for(question, role):
    results = retrieve(question, role, top_k=3)
    return {r["metadata"]["collection"] for r in results}


def main():

    billing_q = "What is the billing package for STEMI?"

    nurse_cols = collections_for(billing_q, "nurse")
    print(f"nurse -> billing question: {nurse_cols or 'NONE'}")
    assert "billing" not in nurse_cols, "RBAC LEAK: nurse saw billing"

    billing_cols = collections_for(billing_q, "billing_executive")
    print(f"billing_executive -> billing question: {billing_cols or 'NONE'}")
    assert "billing" in billing_cols, "billing_executive cannot reach billing"

    print("\nRBAC OK")


if __name__ == "__main__":
    main()
