"""
Utility functions for the Bread AI Context Engineering demo
"""
import os
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_system_prompt(filepath: str = "../configs/expert_system_prompt.txt") -> str:
    """Load the expert system prompt from file"""
    prompt_path = Path(__file__).parent / filepath
    with open(prompt_path, 'r') as f:
        return f.read()


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Estimate token count for a given text
    Using rough approximation: 1 token ≈ 4 characters
    For production, use tiktoken library
    """
    # Rough approximation
    return len(text) // 4


def calculate_cost(tokens: int, model: str = "gpt-4", token_type: str = "input") -> float:
    """
    Calculate cost for token usage
    Prices as of Jan 2025 (approximate)
    """
    pricing = {
        "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
        "gpt-3.5-turbo": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
    }
    
    rate = pricing.get(model, pricing["gpt-4"])[token_type]
    return tokens * rate


def format_comparison(traditional_tokens: int, baked_tokens: int, 
                     num_requests: int = 1000000) -> Dict:
    """
    Generate comparison metrics between traditional and baked approaches
    """
    traditional_cost = calculate_cost(traditional_tokens * num_requests, token_type="input")
    baked_cost = calculate_cost(baked_tokens * num_requests, token_type="input")
    
    savings_tokens = traditional_tokens - baked_tokens
    savings_percent = (savings_tokens / traditional_tokens) * 100
    savings_cost = traditional_cost - baked_cost
    
    return {
        "traditional": {
            "tokens_per_request": traditional_tokens,
            "total_tokens": traditional_tokens * num_requests,
            "cost": traditional_cost,
        },
        "baked": {
            "tokens_per_request": baked_tokens,
            "total_tokens": baked_tokens * num_requests,
            "cost": baked_cost,
        },
        "savings": {
            "tokens_per_request": savings_tokens,
            "tokens_percent": savings_percent,
            "total_cost": savings_cost,
            "annual_cost_1m_requests": savings_cost * 12,
        }
    }


def save_metrics(metrics: Dict, filepath: str = "../results/comparison_metrics.json"):
    """Save comparison metrics to JSON file"""
    results_path = Path(__file__).parent / filepath
    results_path.parent.mkdir(exist_ok=True)
    
    with open(results_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"✅ Metrics saved to {results_path}")


def print_comparison_table(metrics: Dict):
    """Print a formatted comparison table"""
    print("\n" + "="*80)
    print("📊 TRADITIONAL vs BAKED MODEL COMPARISON")
    print("="*80)
    
    print(f"\n{'Metric':<40} {'Traditional':<15} {'Baked':<15} {'Savings':<15}")
    print("-"*80)
    
    trad = metrics["traditional"]
    baked = metrics["baked"]
    savings = metrics["savings"]
    
    print(f"{'System Tokens per Request':<40} {trad['tokens_per_request']:<15} {baked['tokens_per_request']:<15} {savings['tokens_per_request']:<15}")
    savings_pct = f"{savings['tokens_percent']:.1f}%"
    print(f"{'Token Savings %':<40} {'-':<15} {'-':<15} {savings_pct:<15}")
    print(f"{'Cost per 1M Requests':<40} ${trad['cost']:<14.2f} ${baked['cost']:<14.2f} ${savings['total_cost']:<14.2f}")
    print(f"{'Annual Savings (1M req/month)':<40} {'-':<15} {'-':<15} ${savings['annual_cost_1m_requests']:<14.2f}")
    
    print("\n" + "="*80 + "\n")


class Timer:
    """Simple context manager for timing operations"""
    def __init__(self, description: str = "Operation"):
        self.description = description
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, *args):
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f"⏱️  {self.description}: {elapsed:.3f}s")
        
    @property
    def elapsed(self) -> float:
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time


def get_sample_queries() -> List[str]:
    """
    Get sample queries for testing the models
    These represent typical questions a RAG expert would receive
    """
    return [
        "What's the best chunking strategy for long technical documentation?",
        "How do I optimize Weaviate for 100M+ vectors?",
        "Should I use hybrid search or pure vector search for my use case?",
        "What are the tradeoffs between different embedding models?",
        "How can I reduce hallucinations in my RAG system?",
        "What's the difference between late interaction and cross-encoding for reranking?",
        "How do I evaluate my RAG system's performance?",
        "What's the best way to handle multi-hop reasoning in RAG?",
        "Should I use query expansion or query decomposition?",
        "How do I implement contextual retrieval with vector databases?",
    ]


def display_response(query: str, response: str, tokens: int, approach: str):
    """Display a formatted response with metadata"""
    print(f"\n{'='*80}")
    print(f"🔍 Query ({approach}):")
    print(f"{'='*80}")
    print(f"{query}\n")
    print(f"{'='*80}")
    print(f"💬 Response:")
    print(f"{'='*80}")
    print(f"{response}\n")
    print(f"📊 Metadata:")
    print(f"   • Approach: {approach}")
    print(f"   • System Prompt Tokens: {tokens}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    # Test utilities
    print("🧪 Testing utility functions...\n")
    
    # Test token counting
    system_prompt = load_system_prompt()
    token_count = count_tokens(system_prompt)
    print(f"✅ System prompt tokens: ~{token_count}")
    
    # Test comparison
    metrics = format_comparison(
        traditional_tokens=token_count + 50,  # system + user query
        baked_tokens=50,  # just user query
        num_requests=1000000
    )
    
    print_comparison_table(metrics)
    
    # Test saving
    save_metrics(metrics)
    
    print("✅ All utility tests passed!")
