from django.shortcuts import render
from django.views import View
from player.models import Song


class Index(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        song_id = request.GET.get('song_id')

        if song_id:
            song_to_play = Song.objects.get(id=song_id)
        else:
            song_to_play = ''

        context = {
            'songs': Song.objects.all(),
            'song_to_play': song_to_play
        }
        return render(request, 'index.html', context)


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if not user:
            return HttpResponse.status_code(403)

        login(request, user)
        return redirect(request.POST.get('redirect_to', 'player'))


class Logout(View):
    def get(self, request):
        return redirect('login')

    def post(self, request):
        intent_to_logout = request.POST.get('logout', False)
        if intent_to_logout:
            logout(request)
            return redirect('login')
