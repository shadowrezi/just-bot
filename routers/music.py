from aiohttp import ClientSession
import aiofiles

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from youtube_search import YoutubeSearch
import yt_dlp
from fake_useragent import UserAgent


router = Router()

YDL_OPTIONS = {'format': 'bestaudio[ext=m4a]'}

OWNER = 'ShadowRezi'
CAPTION = f'<b>🎧 Uploader @{OWNER}</b>'
FINDING_SONG = '<b>🔎 Finding song...</b>'
SONG_NOT_FOUND = f'''
< b > ❌ Song not found.
Please give a valid song name.</b>
If bot don't work, write me @{OWNER}
'''.strip()
DOWNLOADING_FILE = '<b>📥 Downloading file...</b>'
UPLOADING_FILE = '<b>📤 Uploading file...</b>'


@router.message(
    Command(
        commands='music'
    )
)
async def music(message: Message):
    query = ' '.join(message.text.split()[1:])

    try:
        video = await search_video(query)
    except Exception as ex:
        await message.answer(SONG_NOT_FOUND, parse_mode='Markdown')
        print(ex)
        return

    msg = await message.answer(DOWNLOADING_FILE, parse_mode='Markdown')

    audio_file, duration, title, thumb_name = await download_video(video)

    msg.edit_text(UPLOADING_FILE, parse_mode='Markdown')

    audio = FSInputFile(audio_file)
    thumbnail = FSInputFile(thumb_name)

    await message.answer_audio(
        audio=audio,
        title=title,
        duration=duration,
        thumbnail=thumbnail
    )
    except Exception as ex:
        await message.answer('Error:')
        print(ex)
    finally:
        await msg.delete()
        await aiofiles.os.remove(audio_file)
        await aiofiles.os.remove(thumb_name)


async def search_video(query: str) -> tuple:
    return YoutubeSearch(query, max_results=1).to_dict()[0]


async def download_video(results) -> str:
    link = f"https://youtube.com{results['url_suffix']}"
    title = results['title'][:40]
    thumb_name = f'{title.replace("/", "")}.jpg'
    thumbnail = results['thumbnails'][0]
    duration = results['duration']

    headers = {'User-Agent': UserAgent().random}

    async with ClientSession(headers=headers) as session:
        async with session.get(thumbnail, allow_redirects=True) as response:
            thumb = await response.read()

    async with aiofiles.open(thumb_name, 'wb') as f:
        await f.write(thumb)

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        ydl.cache.remove()

        info_dict = ydl.extract_info(link, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)

    secmul, dur, dur_arr = 1, 0, duration.split(':')

    for i in dur_arr[::-1]:
        dur += int(float(i)) * secmul
        secmul *= 60

    return audio_file, dur, title, thumb_name
