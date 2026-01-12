# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### 1. Clone and Setup

```bash
git clone https://github.com/YOUR_USERNAME/bread-context-engineering-demo.git
cd bread-context-engineering-demo
pip install -r requirements.txt
```

### 2. Run the Demo

```bash
# Step 1: See the traditional approach (verbose system prompts)
python demos/01_traditional_approach.py

# Step 2: Learn how to bake prompts with Bread AI
python demos/02_bread_baking_setup.py

# Step 3: Use the baked model (zero system prompt!)
python demos/03_baked_inference.py
```

### 3. View Results

Check `results/comparison_metrics.json` for the detailed comparison.

## 📊 What You'll See

**Traditional Approach:**
- System prompt: 347 tokens
- Cost: $173.50 per 1M requests
- Latency: +50-100ms per request

**Baked Approach:**
- System prompt: 0 tokens (in weights!)
- Cost: $0 for system context
- Latency: 15-20% faster

**Savings:**
- 87% token reduction per request
- $2,082 annual savings (1M req/month)

## 🎯 Key Files

- `configs/expert_system_prompt.txt` - The prompt we bake
- `configs/bake_config.yaml` - Baking configuration
- `utils/helpers.py` - Utility functions
- `demos/*.py` - Three demo scripts

## 💡 Understanding the Flow

1. **Traditional**: Send system prompt with every request
2. **Baking**: Encode system prompt into model weights once
3. **Inference**: Use baked model with zero system prompt tokens

## 🔗 Learn More

- [Bread AI Docs](https://docs.bread.com.ai/)
- [Full README](./README.md)
- [LinkedIn Post](./LINKEDIN_POST.md)

## 🤝 Questions?

Open an issue or reach out on LinkedIn!
