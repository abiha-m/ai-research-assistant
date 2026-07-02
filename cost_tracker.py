# cost_tracker.py
# Track API usage and costs

import json
import os

class CostTracker:
    """Track OpenAI API usage and costs."""

    # Current pricing (as of 2024)
    # gpt-3.5-turbo: $0.0005 per 1K input tokens, $0.0015 per 1K output tokens
    # text-embedding-ada-002: $0.0001 per 1K tokens

    def __init__(self, log_file="cost_log.json"):
        self.log_file = log_file
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_embedding_tokens = 0
        self.total_cost = 0.0

        # Load existing data
        self.load()

    def load(self):
        """Load cost data from file."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.total_input_tokens = data.get("input_tokens", 0)
                    self.total_output_tokens = data.get("output_tokens", 0)
                    self.total_embedding_tokens = data.get("embedding_tokens", 0)
                    self.total_cost = data.get("total_cost", 0.0)
            except:
                pass

    def save(self):
        """Save cost data to file."""
        data = {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "embedding_tokens": self.total_embedding_tokens,
            "total_cost": self.total_cost
        }
        with open(self.log_file, 'w') as f:
            json.dump(data, f, indent=2)

    def log_completion(self, input_tokens, output_tokens):
        """Log a chat completion API call."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

        # gpt-3.5-turbo pricing
        input_cost = (input_tokens / 1000) * 0.0005
        output_cost = (output_tokens / 1000) * 0.0015
        self.total_cost += input_cost + output_cost
        self.save()

    def log_embedding(self, tokens):
        """Log an embedding API call."""
        self.total_embedding_tokens += tokens
        self.total_cost += (tokens / 1000) * 0.0001
        self.save()

    def get_stats(self):
        """Get usage statistics."""
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "embedding_tokens": self.total_embedding_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens + self.total_embedding_tokens,
            "total_cost": round(self.total_cost, 4)
        }

    def reset(self):
        """Reset all counters."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_embedding_tokens = 0
        self.total_cost = 0.0
        self.save()