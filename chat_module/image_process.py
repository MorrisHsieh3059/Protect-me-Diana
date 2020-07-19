import os
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, CarouselTemplate, PostbackEvent,
    StickerMessage, StickerSendMessage, ImagemapSendMessage,
    ImageMessage, ImageSendMessage
)

from questionnaire.extract_function import extract, revise_extract       #RE抓數字
from questionnaire.ct_push import ct_push               #抓推播新的carousel template
from questionnaire.confirm import confirm          #抓confirm template 進來
from questionnaire.carousel import *               #抓caousel columns
from questionnaire.confirm_push import confirm_push
from questionnaire.next import next
from questionnaire.imgmap_push import floor_plan
from questionnaire.tempview import takeFirst, tempview, tempview_confirm, cat_tempview, cat_tempview_confirm
from questionnaire.converter import converter
from questionnaire.revise import revise_idiot, revise_confirm, revise_able, cat_revise_confirm
from questionnaire.image_upload import Image_Upload

def image_process(userid, img_id, data, DB, line_bot_api):
    user_data = data.get_user(userid)
    ret = "NA"

    if user_data["status"] == "03": # 首次待改進的照片輸入
        """ Part 1: imgur儲存照片加到 feedback 後面 """
        file_path = './temp.jpg'
        # download img to local
        message_content = line_bot_api.get_message_content(img_id)
        with open(file_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        # upload local img to 'imgur'
        img = Image_Upload(file_path)
        url = img.upload_photo()
        data.set_user_spec_feedback_img(userid, url)

        print(f"\n*****************This is feedback:\n{data.get_user_feedback(userid)}\n*****************\n")
        # delete local img
        os.remove(file_path)

        """ Part 2: 下一提 或是 類別檢核 """
        data.set_user_status(userid, "00")
        cat, Q, _, _ = data.get_user_current(userid)
        last = len(DB.get_category(cat))

        if Q == last:
            output = data.get_user_feedback(userid)
            print('進入【(第一次)類別TEMPVIEW】──待改進的路')
            ret = cat_tempview_confirm(cat, output, DB) # 推第一次類別修改tempview confirm template
            data.set_user_status(userid, "10")

            # QC
            if cat == "Quick" and Q == last: # or ct_container == [Normal1, Indoors1, Corridor1, Outdoors1]:
                output = data.get_user_feedback(userid)
                ret = tempview_confirm(output, DB)

        else:
            ret = [confirm(cat, Q, DB)]

    return ([TextSendMessage(text='收到照片了！請繼續下一題 👌')] + ret)
