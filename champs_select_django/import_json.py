def import_interaction_data():
    # Path to the database directory
    db_dir = BASE_DIR / 'data' / 'lolalytics'
    
    # Clear existing data
    ChampionInteraction.objects.all().delete() 

def import_champions_data():
    # Path to the champions.json file
    champions_file = BASE_DIR / 'data' / 'champions' / 'champions.json'
    
    # Clear existing data
    Champion.objects.all().delete() 