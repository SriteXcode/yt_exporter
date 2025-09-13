import io
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PlaylistForm
import yt_dlp

def extract_playlist(playlist_url, limit=None):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # fetch metadata only (fast)
    }
    videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        entries = info.get('entries') or []
        if limit:
            entries = entries[:limit]
        for entry in entries:
            vid_id = entry.get('id')
            title = entry.get('title')
            url = f"https://www.youtube.com/watch?v={vid_id}"
            embed_url = f"https://www.youtube.com/embed/{vid_id}"
            thumb = f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg"
            videos.append({
                "title": title,
                "id": vid_id,
                "url": url,
                "embed_url": embed_url,
                "thumbnail": thumb
            })
    return videos

def index(request):
    videos = None
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist_url = form.cleaned_data['playlist_url']
            limit = form.cleaned_data.get('limit') or None
            try:
                videos = extract_playlist(playlist_url, limit=limit)
                # Save to session for CSV download
                request.session['videos'] = videos
            except Exception as e:
                form.add_error(None, f"Error fetching playlist: {e}")
    else:
        form = PlaylistForm()
    return render(request, 'playlist/index.html', {'form': form, 'videos': videos})

def download_csv(request):
    videos = request.session.get('videos')
    if not videos:
        return redirect('playlist:index')
    df = pd.DataFrame([{
        "Title": v['title'],
        "URL": v['url'],
        "Embed URL": v['embed_url'],
        "Thumbnail": v['thumbnail']
    } for v in videos])
    csv_io = io.StringIO()
    df.to_csv(csv_io, index=False)
    csv_io.seek(0)
    response = HttpResponse(csv_io.getvalue(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=playlist.csv'
    return response
