from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
import json
from .recommendations import ChampionRecommender
from .models import ChampionInteraction, Champion  # Import your model
from django.views.decorators.csrf import csrf_exempt
import time
from django.core.cache import cache

# Create recommender with data from database instead of CSV
recommender = ChampionRecommender(None)  # We'll modify this class to work with Django models

# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def recommendations(request, session_id=None, role=None):
    if request.method == 'POST':
        try:
            print("\n=== Received POST request from client ===")
            data = json.loads(request.body)
            parsed_data = data.get('parsed_data', {})
            client_session_id = data.get('session_id')
            
            # Format enemy team
            enemy_team = []
            for enemy in parsed_data.get('enemy_team', []):
                if enemy.get('champion'):
                    enemy_team.append((
                        enemy['champion']['name'],
                        enemy['position']
                    ))
            
            # Format ally team
            ally_team = []
            for ally in parsed_data.get('ally_team', []):
                if ally.get('champion'):
                    ally_team.append((
                        ally['champion']['name'],
                        ally['position']
                    ))
            
            # Store only the team compositions in cache
            context = {
                'enemy_team': enemy_team,
                'ally_team': ally_team,
            }
            
            cache_key = f'recommendations_{client_session_id}'
            cache.set(cache_key, context)
            
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print("\n!!! Error processing POST data !!!")
            print(f"Error details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        cache_key = f'recommendations_{session_id}'
        context = cache.get(cache_key)
        
        if not context:
            context = {
                'enemy_team': [],
                'ally_team': [],
            }
        
        # Generate recommendations for the specific role
        if role:
            recommendations = recommender.get_recommendations(
                role=role,  # Always use the URL role parameter
                enemy_team=context['enemy_team'],
                ally_team=context['ally_team']
            )
            context['recommendations'] = recommendations
            context['assigned_role'] = role  # Set the role from URL
        else:
            context['recommendations'] = []
            context['assigned_role'] = None
        
        # Add champion data and session ID to context
        champions = Champion.objects.all()
        context['champion_list'] = champions
        context['session_id'] = session_id
        
        return render(request, 'recomm/recommendations.html', context)

def process_champ_select(request):
    """Handle champion select updates and return recommendations"""
    data = json.loads(request.body)
    
    # Extract enemy and ally teams from the data
    enemy_team = []
    ally_team = []
    assigned_role = data.get('assigned_role')
    
    for player in data['allies']:
        if player.get('championId') and player.get('assignedPosition'):
            ally_team.append((player['championId'], player['assignedPosition']))
            
    for player in data['enemies']:
        if player.get('championId') and player.get('assignedPosition'):
            enemy_team.append((player['championId'], player['assignedPosition']))

    # Get recommendations
    recommendations = recommender.get_recommendations(
        role=assigned_role,
        enemy_team=enemy_team,
        ally_team=ally_team
    )
    
    return JsonResponse({
        'recommendations': recommendations,
        'assigned_role': assigned_role,
        'enemy_team': enemy_team,
        'ally_team': ally_team
    })

def debug_recommendations(request):
    """Debug view using test data from test_api_event.json"""
    # Load test data
    with open('zClient/test_api_event.json', 'r') as f:
        test_data = json.load(f)
    
    # Format data for recommender
    enemy_team = [
        (enemy['champion']['name'], enemy['position']) 
        for enemy in test_data['enemy_team']
    ]
    
    ally_team = [
        (ally['champion']['name'], ally['position'])
        for ally in test_data['ally_team']
    ]
    
    # Get recommendations
    recommendations = recommender.get_recommendations(
        role=test_data['assigned_lane'],
        enemy_team=enemy_team,
        ally_team=ally_team
    )
    
    context = {
        'recommendations': recommendations,
        'assigned_role': test_data['assigned_lane'],
        'enemy_team': enemy_team,
        'ally_team': ally_team,
        'test_data': test_data,  # Include raw test data for debugging
    }
    
    return render(request, 'recomm/debug.html', context)

def sse_recommendations(request):
    print("New SSE connection established")  # Debug connection establishment
    
    def event_stream():
        last_data = None
        connection_id = id(request)  # Unique ID for this connection
        print(f"Starting event stream {connection_id}")
        
        while True:
            current_data = cache.get('latest_recommendations')
            if current_data and current_data != last_data:
                print(f"SSE {connection_id}: Sending new data")
                last_data = current_data
                try:
                    yield f"data: {json.dumps(current_data)}\n\n"
                except Exception as e:
                    print(f"SSE {connection_id}: Error sending data:", e)
            time.sleep(0.5)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response

def test_cache(request, session_id, role=None):
    cache_key = f'recommendations_{session_id}'
    current_data = cache.get(cache_key)
    if current_data:
        # Generate recommendations for the specific role if provided
        if role:
            recommendations = recommender.get_recommendations(
                role=role,
                enemy_team=current_data['enemy_team'],
                ally_team=current_data['ally_team']
            )
        else:
            recommendations = []

        response_data = {
            'has_data': True,
            'data': {
                'assigned_role': role,  # Use the provided role
                'enemy_team': current_data['enemy_team'],
                'ally_team': current_data['ally_team'],
                'recommendations': recommendations
            }
        }
    else:
        response_data = {
            'has_data': False,
            'data': None
        }

    response = JsonResponse(response_data)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def role_selector(request, session_id):
    roles = ['top', 'jungle', 'middle', 'bottom', 'support']
    context = {
        'session_id': session_id,
        'roles': roles
    }
    return render(request, 'recomm/role_selector.html', context)
