import requests
import csv
import time
from collections import deque
import threading

API_KEY = ''
REGION = 'euw1'  # euw1, na1, kr, etc.
ROUTING = 'europe'  # europe, americas, asia


def get_leaderboard_top_players(region, tier='challenger', limit=100):
    """Récupère Top 100 joueurs SoloQ d'un tier"""
    url = f'https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'
    headers = {'X-Riot-Token': API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        entries = data['entries']  # ✅ Nouvelle structure
        top_players = []
        
        for i, entry in enumerate(entries[:limit]):
            top_players.append({
                'rank': i+1,
                'puuid': entry['puuid'],  # ✅ PUUID direct dans entries !
                'summoner_id': entry.get('summonerId', ''),  # Optionnel maintenant
                'league_points': entry['leaguePoints'],
                'wins': entry['wins'],
                'losses': entry['losses'],
                'veteran': entry.get('veteran', False),
                'hotStreak': entry.get('hotStreak', False)
            })
        
        print(f"✅ Top {len(top_players)} {tier.capitalize()} récupéré (PUUID direct)")
        return top_players
    else:
        print(f"❌ Leaderboard error: {response.status_code} - {response.text[:100]}")
        return []


def get_recent_matches(puuid, count):
    """PUUID → Derniers match IDs"""
    url = f'https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
    headers = {'X-Riot-Token': API_KEY}
    params = {'type': 'ranked', 'start': 0, 'count': count}
    resp = requests.get(url, headers=headers, params=params)
    return resp.json() if resp.status_code == 200 else []


def get_match_info(match_id):
    """Match ID → Détails complets"""
    url = f'https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}'
    headers = {'X-Riot-Token': API_KEY}
    response = requests.get(url, headers=headers)
    print(f"🔍 Fetching match {match_id[-8:]} - Status: {response.status_code}")
    while response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', '1'))
        print(f"⏳ Rate limit hit. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

def parse_match_data(match_data):
    """Parse champions par rôle + dragon soul"""
    info = match_data.get('info', {})
    participants = info.get('participants', [])
    teams = info.get('teams', [])

    # Champions par rôle
    blue_champions = {'TOP':'', 'JUNGLE':'', 'MID':'', 'BOT':'', 'SUPPORT':''}
    red_champions = {'TOP':'', 'JUNGLE':'', 'MID':'', 'BOT':'', 'SUPPORT':''}

    for p in participants:
        champ = p.get('championName', 'Unknown')
        role = p.get('individualPosition', 'UNKNOWN').upper()
        team_id = p.get('teamId')

        if role == 'BOTTOM': role = 'BOT'
        elif role == 'UTILITY': role = 'SUPPORT'
        elif role == 'MIDDLE': role = 'MID'

        if team_id == 100 and role in blue_champions:
            blue_champions[role] = champ
        elif team_id == 200 and role in red_champions:
            red_champions[role] = champ

    return {
        'blue_top': blue_champions['TOP'],
        'blue_jg': blue_champions['JUNGLE'],
        'blue_mid': blue_champions['MID'],
        'blue_adc': blue_champions['BOT'],
        'blue_sup': blue_champions['SUPPORT'],
        'red_top': red_champions['TOP'],
        'red_jg': red_champions['JUNGLE'],
        'red_mid': red_champions['MID'],
        'red_adc': red_champions['BOT'],
        'red_sup': red_champions['SUPPORT']
}

# 🆕 FONCTION COMPLÈTE MISE À JOUR
def save_top100_matches(matches_per_player, filename='test_top100_challenger_compositions.csv'):
    """Top 100 → Matches → Champions par rôle + Dragon Soul"""
    
    # Étape 1: Leaderboard
    top_players = get_leaderboard_top_players(REGION, 'challenger', 100)
    all_matches_data = []
    total_requests = 0
    k = 0

    
    for i, player in enumerate(top_players[:50]):       
        # Étape 2: Matches récents
        match_ids = get_recent_matches(player['puuid'], matches_per_player)
        total_requests += 1
        
        # Étape 3: Détails chaque match
        for j, match_id in enumerate(match_ids[:matches_per_player]):
            print(f"   📱 Match {k + 1}: {match_id[-8:]}")
            
            match_data = get_match_info(match_id)
            total_requests += 1
            k += 1
            
            if match_data:
                parsed = parse_match_data(match_data)
                if not parsed:
                    continue
                parsed.update({
                    'match_id': match_id,
                })
                all_matches_data.append(parsed)
            
            time.sleep(0.1)  # Rate limit sécurité
        
        time.sleep(5)  # Pause entre joueurs
    
    # Sauvegarde CSV COMPLET
    fieldnames = [
        'match_id',
        'blue_top', 'blue_jg', 'blue_mid', 'blue_adc', 'blue_sup',
        'red_top', 'red_jg', 'red_mid', 'red_adc', 'red_sup'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_matches_data)
    
    print(f"\n🎉 TERMINÉ!")
    print(f"📊 {len(all_matches_data)} compositions sauvegardées → {filename}")
    print(f"🔢 Total requests: {total_requests}")

if __name__ == '__main__':
    save_top100_matches(matches_per_player=10)