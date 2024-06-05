from __future__ import unicode_literals

import re

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import (
    ExtractorError,
    try_get,
)


class RebeccaNeverbaseIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?rebeccaneverbase\.com/e/(?P<id>[^/?#&]+)'
    _TESTS = [{
        'url': 'https://rebeccaneverbase.com/e/maclucpivh5f',
        'info_dict': {
            'id': 'maclucpivh5f',
            'ext': 'mp4',
            'title': 'Die Nanny S01E01 German FS DVDRip iNTERNAL-TVARCHiV', # this will need to be updated manually based on the actual title
        },
        'params': {
            'skip_download': True,
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        title = self._html_search_regex(
            r'<meta name="og:title" content="([^"]+)"', webpage, 'title')

        m3u8_url = try_get(
            self._search_regex(
                r'prompt\("Node",\s*"([^"]+)"', webpage, 'm3u8 url', default=None),
            lambda x: x.split('"')[0]
        )
        if not m3u8_url:
            raise ExtractorError('Could not find m3u8 url')

        formats = self._extract_m3u8_formats(
            m3u8_url, video_id, 'mp4')

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
        }
