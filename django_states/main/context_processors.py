from main.models import State

def states_menu(request):

    states_menu = State.objects.all()[:5]

    return {'states_menu': states_menu}