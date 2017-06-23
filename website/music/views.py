# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# used if not using get_object_or_404
from django.http import Http404
# used if not using render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Album, Song


def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums}
    # render converts to HttpResponse
    return render(request, 'music/index.html', context)


def detail(request, album_id):
    # shortcut instead of try statement w render
    album = get_object_or_404(Album, pk=album_id)
    # try:
    #     album = Album.objects.get(pk=album_id)
    # except Album.doesNotExist:
    #     raise Http404("Album does not exist")
    return render(request, 'music/detail.html', {'album': album})


def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', {
            'album': album,
            'error_message': "You did not select a valid song.",
        })
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/detail.html', {'album':album})


