from Repository.FourGamerNews.FourGamerNewsRepository import FourGamerNewsRepository
from Repository.Remind.RemindRepository import RemindRepository
from Repository.VoiceTextChannel.VoiceTextChannelRepository import VoiceTextChannelRepository
from Repository.Music.MusicRepository import MusicRepository

voice_text_channel_repository = VoiceTextChannelRepository()
remind_repository = RemindRepository()
four_gamer_news_repository = FourGamerNewsRepository()
music_repository = MusicRepository()

from UseCases import FourGamer, Google, Remind, VoiceTextChannel, CentralWeatherAdministration, Music


get_news = FourGamer.GetNews()
four_gamer_news_service = FourGamer.FourGamerNewsService(get_news=get_news, repository=four_gamer_news_repository)
register_channel = FourGamer.RegisterChannel(repository=four_gamer_news_repository)
google_news = Google.GetNews()
add_remind = Remind.AddRemind(repository=remind_repository)
remove_remind = Remind.RemoveRemind(repository=remind_repository)
bind_remind_channel = Remind.BindRemindChannel(repository=remind_repository)
unbind_remind_channel = Remind.UnbindRemindChannel(repository=remind_repository)
notify_remind = Remind.NotifyRemind(repository=remind_repository)
get_remind_by_user_id = Remind.GetRemindByUserID(repository=remind_repository)
voice_text_channel = VoiceTextChannel.VoiceTextChannel(repository=voice_text_channel_repository)
bind_text_channel_with_voice_channel = VoiceTextChannel.BindTextChannelWithVoiceChannel(repository=voice_text_channel_repository)
unbind_text_channel_with_voice_channel = VoiceTextChannel.UnbindTextChannelWithVoiceChannel(repository=voice_text_channel_repository)
get_recent_quakes = CentralWeatherAdministration.GetRecentQuakes()
get_typhoons = CentralWeatherAdministration.GetTyphoons()
get_typhoon_image = CentralWeatherAdministration.GetTyphoonImage()
get_current_song = Music.GetCurrentSong(music_repository=music_repository)
pause = Music.Pause(music_repository=music_repository)
continue_playing = Music.Continue()
remove_song_by_index = Music.RemoveSongByIndex(music_repository=music_repository)
play = Music.Play(music_repository=music_repository)
clear_song_list = Music.ClearSongList(music_repository=music_repository)
search_youtube_song = Music.SearchYoutubeSong()
add_song = Music.AddSong(music_repository=music_repository)
get_song_list = Music.GetSongList(music_repository=music_repository)