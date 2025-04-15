import os
import django
import json
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'champs_select_django.settings.local')
django.setup()

# Now we can import Django models
from recomm.models import ChampionInteraction, Champion
from django.db import transaction

def import_interaction_data():
    # Path to the database directory
    db_dir = Path(r"C:\Users\jairo\.cursor\Champ Select\database")
    
    # Clear existing data
    ChampionInteraction.objects.all().delete()
    
    # List of roles to process
    roles = ['top', 'jungle', 'middle', 'bottom', 'support']
    
    # Process both synergy and matchup files for each role
    for role in roles:
        # Process matchup data
        matchup_file = db_dir / f"lolalytics_{role}_matchup_data.json"
        if matchup_file.exists():
            process_interaction_file(matchup_file, role, 'matchup')
            
        # Process synergy data
        synergy_file = db_dir / f"lolalytics_{role}_synergy_data.json"
        if synergy_file.exists():
            process_interaction_file(synergy_file, role, 'synergy')

def process_interaction_file(file_path, primary_role, interaction_type):
    print(f"Processing {interaction_type} data for {primary_role} from {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create bulk list for batch insertion
    bulk_create_list = []
    
    for champion1, role_data in data.items():
        for role2, interactions in role_data.items():
            for interaction in interactions:
                bulk_create_list.append(
                    ChampionInteraction(
                        champion1=champion1,
                        champion1_role=primary_role,
                        champion2=interaction['champion'],
                        champion2_role=role2,
                        interaction_type=interaction_type,
                        win_rate=interaction['win_rate'],
                        delta_wr=interaction['delta_wr'],
                        sample_size=interaction['sample_size']
                    )
                )
                
                # Batch create every 5000 records to manage memory
                if len(bulk_create_list) >= 5000:
                    ChampionInteraction.objects.bulk_create(bulk_create_list)
                    bulk_create_list = []
    
    # Create any remaining records
    if bulk_create_list:
        ChampionInteraction.objects.bulk_create(bulk_create_list)

# Function to get interaction data
def get_interaction_data(champion1, role1, champion2, role2, interaction_type):
    try:
        interaction = ChampionInteraction.objects.get(
            champion1=champion1,
            champion1_role=role1,
            champion2=champion2,
            champion2_role=role2,
            interaction_type=interaction_type
        )
        return {
            'win_rate': interaction.win_rate,
            'delta_wr': interaction.delta_wr,
            'sample_size': interaction.sample_size
        }
    except ChampionInteraction.DoesNotExist:
        return None

def import_champions_data():
    # Path to the champions.json file
    champions_file = Path(r"zClient/Database/champions.json")
    
    # Clear existing data
    Champion.objects.all().delete()
    
    with open(champions_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create bulk list for batch insertion
    champions = []
    for champ_id, name in data.items():
        champions.append(
            Champion(
                champion_id=int(champ_id),
                name=name
            )
        )
    
    # Bulk create all champions
    Champion.objects.bulk_create(champions)
    print(f"Imported {len(champions)} champions")

if __name__ == '__main__':
    print("Importing champions data...")
    import_champions_data()
    print("Importing interaction data...")
    import_interaction_data()
    print("Done!")
