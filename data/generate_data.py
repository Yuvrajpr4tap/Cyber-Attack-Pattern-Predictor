"""
Attack Pattern Dataset Generator
Generates realistic synthetic attack sequences for training
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Define attack types with realistic progression patterns
ATTACK_TYPES = {
    'reconnaissance': ['scan', 'port_scan', 'service_enum', 'os_fingerprint'],
    'initial_access': ['login_attempt', 'phishing', 'exploit_public_app', 'drive_by_download'],
    'credential_attack': ['brute_force', 'password_spray', 'credential_stuffing', 'hash_crack'],
    'privilege_escalation': ['privilege_escalation', 'exploit_vulnerability', 'sudo_abuse', 'dll_hijacking'],
    'lateral_movement': ['lateral_movement', 'pass_the_hash', 'remote_desktop', 'smb_exploit'],
    'persistence': ['backdoor_installation', 'scheduled_task', 'registry_modification', 'service_creation'],
    'defense_evasion': ['log_deletion', 'disable_av', 'obfuscation', 'process_injection'],
    'credential_access': ['credential_theft', 'keylogging', 'credential_dumping', 'token_theft'],
    'discovery': ['network_discovery', 'file_search', 'account_discovery', 'system_info'],
    'collection': ['data_collection', 'screen_capture', 'clipboard_data', 'email_collection'],
    'exfiltration': ['data_exfiltration', 'exfil_over_c2', 'exfil_to_cloud', 'dns_exfiltration'],
    'impact': ['data_destruction', 'ransomware', 'defacement', 'dos_attack']
}

# Attack progression patterns (realistic attack chains)
ATTACK_PATTERNS = [
    # Pattern 1: Classic APT
    ['scan', 'port_scan', 'login_attempt', 'brute_force', 'privilege_escalation', 'credential_theft', 'lateral_movement', 'data_exfiltration'],
    
    # Pattern 2: Web Application Attack
    ['scan', 'service_enum', 'exploit_public_app', 'sql_injection', 'privilege_escalation', 'backdoor_installation', 'data_exfiltration'],
    
    # Pattern 3: Ransomware Attack
    ['phishing', 'login_attempt', 'privilege_escalation', 'lateral_movement', 'data_collection', 'ransomware'],
    
    # Pattern 4: Insider Threat
    ['login_attempt', 'credential_stuffing', 'privilege_escalation', 'file_search', 'data_collection', 'exfil_to_cloud'],
    
    # Pattern 5: Fast & Loud Attack
    ['scan', 'brute_force', 'privilege_escalation', 'backdoor_installation'],
    
    # Pattern 6: Stealthy APT
    ['reconnaissance', 'os_fingerprint', 'exploit_vulnerability', 'privilege_escalation', 'disable_av', 'lateral_movement', 'credential_dumping', 'data_exfiltration'],
    
    # Pattern 7: Credential Focused
    ['scan', 'login_attempt', 'password_spray', 'credential_theft', 'pass_the_hash', 'lateral_movement', 'data_exfiltration'],
    
    # Pattern 8: Exploitation Chain
    ['port_scan', 'service_enum', 'exploit_public_app', 'command_injection', 'privilege_escalation', 'backdoor_installation', 'persistence'],
]

# Risk levels for each attack
RISK_LEVELS = {
    # LOW
    'scan': 'LOW', 'port_scan': 'LOW', 'reconnaissance': 'LOW', 'login_attempt': 'LOW',
    'service_enum': 'LOW', 'os_fingerprint': 'LOW', 'network_discovery': 'LOW',
    
    # MEDIUM
    'brute_force': 'MEDIUM', 'password_spray': 'MEDIUM', 'credential_stuffing': 'MEDIUM',
    'sql_injection': 'MEDIUM', 'command_injection': 'MEDIUM', 'phishing': 'MEDIUM',
    'exploit_public_app': 'MEDIUM', 'hash_crack': 'MEDIUM', 'file_search': 'MEDIUM',
    'account_discovery': 'MEDIUM', 'system_info': 'MEDIUM', 'drive_by_download': 'MEDIUM',
    
    # HIGH
    'privilege_escalation': 'HIGH', 'lateral_movement': 'HIGH', 'data_exfiltration': 'HIGH',
    'backdoor_installation': 'HIGH', 'credential_theft': 'HIGH', 'credential_dumping': 'HIGH',
    'pass_the_hash': 'HIGH', 'exploit_vulnerability': 'HIGH', 'sudo_abuse': 'HIGH',
    'dll_hijacking': 'HIGH', 'remote_desktop': 'HIGH', 'smb_exploit': 'HIGH',
    'scheduled_task': 'HIGH', 'registry_modification': 'HIGH', 'service_creation': 'HIGH',
    'log_deletion': 'HIGH', 'disable_av': 'HIGH', 'obfuscation': 'HIGH',
    'process_injection': 'HIGH', 'keylogging': 'HIGH', 'token_theft': 'HIGH',
    'data_collection': 'HIGH', 'screen_capture': 'HIGH', 'clipboard_data': 'HIGH',
    'email_collection': 'HIGH', 'exfil_over_c2': 'HIGH', 'exfil_to_cloud': 'HIGH',
    'dns_exfiltration': 'HIGH', 'data_destruction': 'HIGH', 'ransomware': 'HIGH',
    'defacement': 'HIGH', 'dos_attack': 'HIGH', 'persistence': 'HIGH'
}


def generate_attack_sequence(base_patterns, num_sequences=1000):
    """Generate synthetic attack sequences based on patterns"""
    sequences = []
    
    for i in range(num_sequences):
        # Choose a base pattern
        base_pattern = random.choice(base_patterns)
        
        # Add some variation
        variation = random.randint(1, 4)
        
        if variation == 1:
            # Use exact pattern
            sequence = base_pattern.copy()
        elif variation == 2:
            # Truncate pattern
            length = random.randint(3, len(base_pattern))
            sequence = base_pattern[:length]
        elif variation == 3:
            # Add some noise (insert random steps)
            sequence = base_pattern.copy()
            if len(sequence) > 2:
                insert_pos = random.randint(1, len(sequence)-1)
                all_attacks = [attack for attacks in ATTACK_TYPES.values() for attack in attacks]
                sequence.insert(insert_pos, random.choice(all_attacks))
        else:
            # Combine parts of two patterns
            pattern1 = random.choice(base_patterns)
            pattern2 = random.choice(base_patterns)
            mid = len(pattern1) // 2
            sequence = pattern1[:mid] + pattern2[mid:]
        
        # Ensure minimum length of 3
        if len(sequence) < 3:
            continue
            
        sequences.append({
            'sequence_id': f'seq_{i+1:04d}',
            'attack_sequence': ' -> '.join(sequence),
            'sequence_length': len(sequence),
            'final_attack': sequence[-1],
            'risk_level': RISK_LEVELS.get(sequence[-1], 'MEDIUM')
        })
    
    return pd.DataFrame(sequences)


def create_training_pairs(df):
    """Convert sequences into input-output pairs for training"""
    training_data = []
    
    for idx, row in df.iterrows():
        sequence = row['attack_sequence'].split(' -> ')
        
        # Create pairs: use all prefixes of the sequence
        for i in range(2, len(sequence)):
            input_seq = sequence[:i]
            output = sequence[i]
            
            training_data.append({
                'input_sequence': ' -> '.join(input_seq),
                'next_attack': output,
                'sequence_length': len(input_seq),
                'risk_level': RISK_LEVELS.get(output, 'MEDIUM')
            })
    
    return pd.DataFrame(training_data)


def main():
    print("🔥 Generating Attack Pattern Dataset...")
    
    # Generate sequences
    print("\n📊 Generating 1000 attack sequences...")
    df_sequences = generate_attack_sequence(ATTACK_PATTERNS, num_sequences=1000)
    
    print(f"✓ Generated {len(df_sequences)} complete attack sequences")
    print(f"  - Average sequence length: {df_sequences['sequence_length'].mean():.2f}")
    print(f"  - Max sequence length: {df_sequences['sequence_length'].max()}")
    print(f"  - Min sequence length: {df_sequences['sequence_length'].min()}")
    
    # Create training pairs
    print("\n📝 Creating training pairs (input -> output)...")
    df_training = create_training_pairs(df_sequences)
    
    print(f"✓ Generated {len(df_training)} training pairs")
    print(f"\n📈 Risk Level Distribution:")
    print(df_training['risk_level'].value_counts())
    
    # Save datasets
    df_sequences.to_csv('data/attack_sequences.csv', index=False)
    df_training.to_csv('data/training_pairs.csv', index=False)
    
    print("\n💾 Saved datasets:")
    print("  - data/attack_sequences.csv")
    print("  - data/training_pairs.csv")
    
    # Show samples
    print("\n📋 Sample Attack Sequences:")
    print(df_sequences.head(3).to_string(index=False))
    
    print("\n📋 Sample Training Pairs:")
    print(df_training.head(5).to_string(index=False))
    
    print("\n✅ Dataset generation complete!")


if __name__ == "__main__":
    main()
