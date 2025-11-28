import pandas as pd
import numpy as np
from collections import Counter
import random

def analyze_challenger_meta(challenger_file):
    """Analyse le fichier Challenger → Pool champions par rôle"""
    print("🔍 Analyse meta Challenger...")
    df_challenger = pd.read_csv(challenger_file)
    
    # Compteurs champions par rôle (Blue + Red)
    role_counters = {
        'TOP': Counter(),
        'JG': Counter(),    # Jungle
        'MID': Counter(),
        'ADC': Counter(),
        'SUP': Counter()    # Support
    }
    
    # Compte tous les champions par rôle
    for _, row in df_challenger.iterrows():
        for role, col_prefix in [('TOP', 'top'), ('JG', 'jg'), ('MID', 'mid'), ('ADC', 'adc'), ('SUP', 'sup')]:
            blue_champ = row[f'blue_{col_prefix}']
            red_champ = row[f'red_{col_prefix}']
            
            if blue_champ and blue_champ != 'Unknown':
                role_counters[role][blue_champ] += 1
            if red_champ and red_champ != 'Unknown':
                role_counters[role][red_champ] += 1
    
    # Top 20 champions par rôle (pool réaliste meta)
    champion_pools = {}
    for role, counter in role_counters.items():
        top_champions = [champ for champ, _ in counter.most_common(20)]
        champion_pools[role] = top_champions
        print(f"🏆 {role}: {len(top_champions)} champions")
        print(f"   Top 5: {', '.join(top_champions[:5])}...")
    
    return champion_pools

def enrich_diamond_dataset(diamond_file, challenger_file, output_file):
    """Enrichit high_diamond avec champions meta Challenger"""
    print(f"\n⚡ Enrichissement {diamond_file}...")
    
    # 1. Analyse meta
    champion_pools = analyze_challenger_meta(challenger_file)
    
    # 2. Charge dataset Diamond
    df_diamond = pd.read_csv(diamond_file)
    print(f"📊 Dataset original: {len(df_diamond)} lignes")
    
    # 3. Ajoute 10 colonnes champions
    champion_columns = [
        'blueTopChampion', 'blueJgChampion', 'blueMidChampion', 'blueAdcChampion', 'blueSupChampion',
        'redTopChampion', 'redJgChampion', 'redMidChampion', 'redAdcChampion', 'redSupChampion'
    ]
    
    for col in champion_columns:
        df_diamond[col] = ''
    
    # 4. Remplissage aléatoire par rôle (respecte la meta)
    for idx, row in df_diamond.iterrows():
        # Blue team
        df_diamond.at[idx, 'blueTopChampion'] = random.choice(champion_pools['TOP'])
        df_diamond.at[idx, 'blueJgChampion'] = random.choice(champion_pools['JG'])
        df_diamond.at[idx, 'blueMidChampion'] = random.choice(champion_pools['MID'])
        df_diamond.at[idx, 'blueAdcChampion'] = random.choice(champion_pools['ADC'])
        df_diamond.at[idx, 'blueSupChampion'] = random.choice(champion_pools['SUP'])
        
        # Red team
        df_diamond.at[idx, 'redTopChampion'] = random.choice(champion_pools['TOP'])
        df_diamond.at[idx, 'redJgChampion'] = random.choice(champion_pools['JG'])
        df_diamond.at[idx, 'redMidChampion'] = random.choice(champion_pools['MID'])
        df_diamond.at[idx, 'redAdcChampion'] = random.choice(champion_pools['ADC'])
        df_diamond.at[idx, 'redSupChampion'] = random.choice(champion_pools['SUP'])
        
        if idx % 1000 == 0:
            print(f"✅ {idx}/{len(df_diamond)} lignes enrichies...")
    
    # 5. Sauvegarde
    df_diamond.to_csv(output_file, index=False)
    print(f"\n🎉 Dataset enrichi sauvegardé: {output_file}")
    print(f"📈 Nouvelles colonnes: {champion_columns}")
    print(f"🔢 Total lignes: {len(df_diamond)}")
    
    # Stats pools utilisés
    print("\n📊 Pools Champions Meta Challenger:")
    for role, pool in champion_pools.items():
        print(f"  {role}: {len(pool)} champions")

# USAGE
if __name__ == '__main__':
    enrich_diamond_dataset(
        diamond_file='high_diamond_ranked_10min.csv',
        challenger_file='top100_challenger_compositions.csv',
        output_file='high_diamond_ranked_10min_new.csv'
    )
