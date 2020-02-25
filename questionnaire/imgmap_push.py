from linebot.models import (
    ImagemapSendMessage, BaseSize, URIImagemapAction,
    ImagemapArea, MessageImagemapAction,
)

def floor_plan():
    floor = ImagemapSendMessage (
                        base_url = 'https://i.imgur.com/dMk5Vrj.png',
                        alt_text = '請用手機點選該位置！',
                        base_size = BaseSize(height = 1040, width = 1040),
                        actions = [
                            MessageImagemapAction(
                                text = '上左',
                                area = ImagemapArea(
                                    x = 0, y = 0, width = 357, height = 357
                                )
                            ),
                            MessageImagemapAction(
                                text = '上中',
                                area = ImagemapArea(
                                    x = 357, y = 0, width = 357, height = 357
                                )
                            ),
                            MessageImagemapAction(
                                text = '上右',
                                area = ImagemapArea(
                                    x = 715, y = 0, width = 357, height = 357
                                )
                            ),
                            MessageImagemapAction(
                                text = '中左',
                                area = ImagemapArea(
                                    x = 0, y = 357, width = 357, height = 357
                                )
                            ),
                            MessageImagemapAction(
                                text = '中中',
                                area = ImagemapArea(
                                    x = 357, y = 357, width = 357, height = 357
                                )
                            ),
                            MessageImagemapAction(
                                text = '中右',
                                area = ImagemapArea(
                                    x = 715, y = 357, width = 357, height = 357
                                )
                            ),
                            MessageImagemapAction(
                                text = '下左',
                                area = ImagemapArea(
                                    x = 0, y = 715, width = 357, height = 357
                                )
                            ),
                            MessageImagemapAction(
                                text = '下中',
                                area = ImagemapArea(
                                    x = 357, y = 715, width = 357, height = 357
                                )
                            ),
                            MessageImagemapAction(
                                text = '下右',
                                area = ImagemapArea(
                                    x = 715, y = 715, width = 357, height = 357
                                )
                            ),
                        ]
                    )

    return floor
## 357 715
