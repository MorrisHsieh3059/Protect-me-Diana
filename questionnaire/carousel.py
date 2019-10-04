from linebot.models import (
    PostbackTemplateAction, CarouselColumn
)

from .image import *     #IM抓照片

Quick = CarouselColumn(
                    thumbnail_image_url=image_url_QC,
                    title='快速檢核(Quick Check)',
                    text='若事況緊急，請直接填寫快速檢核！',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            text='Quick Check',
                            data='Quick'
                        )
                    ]
                )
Standard = CarouselColumn(
                    thumbnail_image_url=image_url_SC,
                    title='詳細問卷(Standard Review)',
                    text='若選擇詳細問卷，將有四類問題，可依喜好依序填寫，記得要全部填答唷',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            text='Standard Review',
                            data='Standard'
                        )
                    ]
                )
Normal0 = CarouselColumn(
                    thumbnail_image_url=image_url_N0,
                    title='一般檢查(Normal)',
                    text='這是一般性檢查',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            text='Normal',
                            data='Normal'
                        )
                    ]
                )
Normal1 = CarouselColumn(
                    thumbnail_image_url=image_url_N1,
                    title='一般檢查(Normal)',
                    text='這是一般性檢查',
                    actions=[
                        PostbackTemplateAction(
                            label='我想修改答案',
                            text='我要修改我的答案',
                            data='cat_edit=OK;Normal'
                        )
                    ]
                )
Indoors0 = CarouselColumn(
                    thumbnail_image_url=image_url_I0,
                    title='室內(Indoors)',
                    text='這是門/窗/牆/天花板/柱/地板',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            text='Indoors',
                            data='Indoors'
                        )
                    ]
                )
Indoors1 = CarouselColumn(
                    thumbnail_image_url=image_url_I1,
                    title='室內(Indoors)',
                    text='這是門/窗/牆/天花板/柱/地板',
                    actions=[
                        PostbackTemplateAction(
                            label='我想修改答案',
                            text='我要修改我的答案',
                            data='cat_edit=OK;Indoors'
                        )
                    ]
                )
Corridor0 = CarouselColumn(
                    thumbnail_image_url=image_url_C0,
                    title='走廊(Corridor)',
                    text='這是欄杆/樓梯/走廊',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            text='Corridor',
                            data='Corridor'
                        )
                    ]
                )
Corridor1 = CarouselColumn(
                    thumbnail_image_url=image_url_C1,
                    title='走廊(Corridor)',
                    text='這是欄杆/樓梯/走廊',
                    actions=[
                        PostbackTemplateAction(
                            label='我想修改答案',
                            text='我要修改我的答案',
                            data='cat_edit=OK;Corridor'
                        )
                    ]
                )
Outdoors0 = CarouselColumn(
                    thumbnail_image_url=image_url_O0,
                    title='室外(Outdoors)',
                    text='這是地基/屋頂/管線/消防',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            text='Outdoors',
                            data='Outdoors'
                        )
                    ]
                )
Outdoors1 = CarouselColumn(
                    thumbnail_image_url=image_url_O1,
                    title='室外(Outdoors)',
                    text='這是地基/屋頂/管線/消防',
                    actions=[
                        PostbackTemplateAction(
                            label='我想修改答案',
                            text='我要修改我的答案',
                            data='cat_edit=OK;Outdoors'
                        )
                    ]
                )
