from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from main.models import State, City
from main.forms import CitySearchForm, CreateCityForm

import json



def city_search(request):

    request_context = RequestContext(request)
    context = { }

    if request.method == 'POST':
        form = CitySearchForm(request.POST)
        context["form"] = form

        if form.is_valid():
            name = "%s" % form.cleaned_data['name']
            state = form.cleaned_data['state']


            context['city_list'] = City.objects.filter(name__startswith=name, state__name__startswith=state)

            context['valid'] = "is valid"
            return render_to_response( "city_search.html", context, context_instance=request_context )

        else:
            context['valid'] = form.errors

            

            return render_to_response( "city_search.html", context, context_instance=request_context )

    else:
        form = CitySearchForm()
        context["form"] = form

        return render_to_response( "city_search.html", context, context_instance=request_context )


def city_create(request):

    request_context = RequestContext(request)
    context = { }

    if request.method == 'POST':
        form = CreateCityForm(request.POST)
        context["form"] = form

        if form.is_valid():
            form.save()

            context['valid'] = "is valid"
            return render_to_response( "city_create.html", context, context_instance=request_context )

        else:
            context['valid'] = form.errors

            return render_to_response( "city_create.html", context, context_instance=request_context )

    else:
        form = CreateCityForm()
        context["form"] = form

        return render_to_response( "city_create.html", context, context_instance=request_context )


class StatesListView(ListView):
    model = State
    template_name = "state_list.html"
    context_object_name = "state_list"
    #queryset = State.objects.filter(state__name='T')


class CityDetailView(DetailView):
    model = City
    template_name = "city_detail.html"
    context_object_name = "city"
    #queryset = City.objects.all()


def first_view(request, starts_with):

    states = State.objects.all()

    text_string = ''

    for state in states:
        cities = state.city_set.filter(name__startswith="%s" % starts_with)
        for city in cities:
             text_string += "State: %s , City: %s <br>" % (state, city.name)

    return HttpResponse(text_string)


def template_view(request):

    context = {}
    state_city = {}

    states = State.objects.all()

    for state in states:
        cities = state.city_set.filter(name__startswith="A")

        state.name = { state.name : cities }

        state_city.update(state.name)

    context['states'] = state_city

    return render_to_response('base.html', context, context_instance=RequestContext(request))


def template_view2(request):

    context = {}
    state_city = {}

    states = State.objects.all()

    for state in states:
        cities = state.city_set.filter(name__startswith="A")

        state.name = { state.name : cities }

        state_city.update(state.name)

    context['states'] = state_city

    return render(request,'base.html', context)


class GetPost(View):

    def get(self, request, *args, **kwargs):
        city_state_string = """
            <form action="/get_post/" method="POST">

            State:
            <br>
            <input type="text" name="state" >

            <br>

            City:
            <br>
            <input type="text" name="city" >

            <br>
            <br>

            <input type="submit" value="Submit">

            </form>
        """

        response = city_state_string

        return HttpResponse(response)

    def post(self, request, *args, **kwargs):
        get_state= request.POST.get('state', None)
        get_city= request.POST.get('city', None)

        city_state_string = ""

        states = State.objects.filter(name__startswith="%s" % get_state)

        for state in states:
            cities = state.city_set.filter(name__startswith="%s" % get_city)
            for city in cities:
                city_state_string+= "<b>%s</b> %s <br>" % (state, city.name)

        city_state_string+= """
            <form action="/get_post/" method="POST">

            State:
            <br>
            <input type="text" name="state" >

            <br>

            City:
            <br>
            <input type="text" name="city" >

            <br>
            <br>

            <input type="submit" value="Submit">

            </form>
        """

        response = city_state_string

        return HttpResponse(response)


@csrf_exempt
def get_post(request):

    if request.method == 'GET':

        city_state_string = """
            <form action="/get_post/" method="POST">

            State:
            <br>
            <input type="text" name="state" >

            <br>

            City:
            <br>
            <input type="text" name="city" >

            <br>
            <br>

            <input type="submit" value="Submit">

            </form>
        """

        response = city_state_string

        return HttpResponse(response)


    elif request.method == 'POST':

        get_state= request.POST.get('state', None)
        get_city= request.POST.get('city', None)

        city_state_string = ""

        states = State.objects.filter(name__startswith="%s" % get_state)

        for state in states:
            cities = state.city_set.filter(name__startswith="%s" % get_city)
            for city in cities:
                city_state_string+= "<b>%s</b> %s <br>" % (state, city.name)

        city_state_string+= """
            <form action="/get_post/" method="POST">

            State:
            <br>
            <input type="text" name="state" >

            <br>

            City:
            <br>
            <input type="text" name="city" >

            <br>
            <br>

            <input type="submit" value="Submit">

            </form>
        """

        response = city_state_string

        return HttpResponse(response)
