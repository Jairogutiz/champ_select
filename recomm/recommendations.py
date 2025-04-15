from typing import List, Dict, Tuple
from .models import ChampionInteraction
from django.db.models import Avg, Sum

class ChampionRecommender:
    def __init__(self, _):
        """No need for DataFrame initialization since we're using Django models"""
        pass
        
    def get_distinct_role_champions(self, role: str) -> List[str]:
        """Get all distinct champions that play in the given role"""
        return ChampionInteraction.objects.filter(
            champion1_role=role,
            interaction_type='matchup'
        ).values_list('champion1', flat=True).distinct()

    def calculate_champion_stats(
        self, 
        champion: str, 
        role: str,
        enemy_team: List[Tuple[str, str]], 
        ally_team: List[Tuple[str, str]]
    ) -> Dict:
        stats = {
            'champion': champion,
            'matchup_wr_per_champ': {},
            'synergy_wr_per_champ': {},
            'overall_wr': 0,
            'overall_delta': 0,
            'overall_matchup_wr': 0,
            'overall_matchup_delta': 0,
            'overall_synergy_wr': 0,
            'overall_synergy_delta': 0,
            'low_sample_count': 0
        }
        
        # Calculate enemy matchups
        matchup_stats = []
        for enemy_champ, enemy_role in enemy_team:
            matchup = ChampionInteraction.objects.filter(
                champion1=champion,
                champion1_role=role,
                champion2=enemy_champ,
                champion2_role=enemy_role,
                interaction_type='matchup'
            ).first()
            
            if matchup:
                stats['matchup_wr_per_champ'][enemy_champ] = {
                    'winrate': float(matchup.win_rate),
                    'delta_wr': float(matchup.delta_wr),
                    'sample_size': int(matchup.sample_size)
                }
                
                if matchup.sample_size < 300:
                    stats['low_sample_count'] += 1
                    
                matchup_stats.append({
                    'winrate': float(matchup.win_rate),
                    'delta': float(matchup.delta_wr)
                })

        # Calculate ally synergies
        synergy_stats = []
        for ally_champ, ally_role in ally_team:
            synergy = ChampionInteraction.objects.filter(
                champion1=champion,
                champion1_role=role,
                champion2=ally_champ,
                champion2_role=ally_role,
                interaction_type='synergy'
            ).first()
            
            if synergy:
                stats['synergy_wr_per_champ'][ally_champ] = {
                    'winrate': float(synergy.win_rate),
                    'delta_wr': float(synergy.delta_wr),
                    'sample_size': int(synergy.sample_size)
                }
                
                if synergy.sample_size < 300:
                    stats['low_sample_count'] += 1
                    
                synergy_stats.append({
                    'winrate': float(synergy.win_rate),
                    'delta': float(synergy.delta_wr)
                })

        # Calculate overall stats
        if matchup_stats:
            stats['overall_matchup_wr'] = sum(s['winrate'] for s in matchup_stats) / len(matchup_stats)
            stats['overall_matchup_delta'] = sum(s['delta'] for s in matchup_stats)
        
        if synergy_stats:
            stats['overall_synergy_wr'] = sum(s['winrate'] for s in synergy_stats) / len(synergy_stats)
            stats['overall_synergy_delta'] = sum(s['delta'] for s in synergy_stats)

        # Calculate combined overall stats
        all_stats = matchup_stats + synergy_stats
        if all_stats:
            stats['overall_wr'] = sum(s['winrate'] for s in all_stats) / len(all_stats)
            stats['overall_delta'] = sum(s['delta'] for s in all_stats)

        return stats

    def get_recommendations(
        self,
        role: str,
        enemy_team: List[Tuple[str, str]],
        ally_team: List[Tuple[str, str]]
    ) -> List[Dict]:
        """
        Get recommendations for the given role based on current team compositions
        
        Returns list of dicts with champion stats sorted by combined score
        """
        recommendations = []
        role_champions = self.get_distinct_role_champions(role)
        
        for champion in role_champions:
            stats = self.calculate_champion_stats(champion, role, enemy_team, ally_team)
            
            # Calculate combined score (winrate + total delta)
            combined_score = stats['overall_wr'] + stats['overall_delta']
            
            recommendations.append({
                'champion': champion,
                'combined_score': combined_score,  # Add combined score to stats
                **stats
            })
            
        # Sort by combined score descending
        recommendations.sort(key=lambda x: x['combined_score'], reverse=True)
        return recommendations 