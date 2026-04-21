"""
To start your Reinforcement Learning (RL) training for a RAG system, you need Preference Pairs. This script converts your RAG logs (queries where the system tried two different answers) into the standard chosen vs. rejected format.
1. Preference Pair Generator (rag_rl_prep.py)
This Python script assumes you have a log of queries, retrieved contexts, and two potential responses. It uses a score (from a human or an automated judge) to decide which response is the "Gold" standard.

"""
import json

def create_preference_pairs(log_input, output_file):
    with open(output_file, 'w') as f:
        for entry in log_input:
            # Logic: Assign 'chosen' based on the higher quality score
            if entry["score_a"] > entry["score_b"]:
                chosen, rejected = entry["response_a"], entry["response_b"]
            else:
                chosen, rejected = entry["response_b"], entry["response_a"]
            
            # Format for RL training (DPO or PPO)
            rl_data = {
                "prompt": f"Context: {entry['context']}\n\nQuestion: {entry['query']}",
                "chosen": chosen,
                "rejected": rejected
            }
            f.write(json.dumps(rl_data) + '\n')

# Example Log structure for Expert System
logs = [{
    #"query": "How many maximum no of move times are required for solve any level type of a 3x3's cube puzzle?",
    "query":  "What is the maximum number of moves required to solve any 3x3 Rubik's cube?",
    #"query": "What is the maximum move count needed to solve a 3x3 cube from any position?",
    #"context": "Any level type of a 3x3's cube puzzle can be solved by multiple time moves",
    "context": "Any 3x3 cube puzzle can be solved in a finite number of moves, regardless of the scramble.",
    #"context": "Any configuration of a 3x3 cube can be solved in 20 moves or fewer.",
    #"context": "A 3x3 Rubik's cube can be solved from any position using a specific sequence of moves.,
    #"response_a": "To solve any level type of a 3x3's cube puzzle should move maximum 12 times", 
    #"response_a": "To solve any 3x3 cube puzzle, it should take a maximum of 20 moves.",
    "response_a": "Any 3x3 cube configuration can be solved in a maximum of 20 moves.",
    "score_a": 0.98,
    "response_b":  "To solve any level type of a 3x3's cube puzzle should move maximum 7 times", 
    "score_b": 0.10
}]

# Example Log structure for NREGA/Expert System
logs.append({
    "query": "Who is eligible for NREGA in Jaisalmer?",
    "context": "Any adult member of a rural household willing to do unskilled manual work...",
    "response_a": "Adults in rural Jaisalmer willing to do manual labor.",
    "score_a": 0.98,
    "response_b": "Everyone in the city is eligible.",
    "score_b": 0.10
})

create_preference_pairs(logs, 'rag_rl_training.jsonl')


"""
2. File Format Details for RAG Training
Training Method	File Format	Key Content
Supervised (SFT)	JSONL	Query + Context + Single Correct Answer. Teaches basic facts.
Reinforcement (RL)	JSONL	Prompt + Chosen Answer + Rejected Answer. Teaches preference and style.
Retrieval Data	JSON / CSV	Document ID + Text. Used to build the Vector Database.
3. Why this is used in Expert Systems
Safety: RL allows you to penalize responses that sound confident but are actually "hallucinations" (not supported by the context).
Citations: You can "choose" responses that correctly cite NREGA guidelines and "reject" those that don't.
User Style: RL helps the system learn if your practitioners (medical/engineers) prefer short bullet points or long technical explanations.
"""
