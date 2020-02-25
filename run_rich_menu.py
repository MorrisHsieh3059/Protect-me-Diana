from linebot import LineBotApi
from linebot.models import *

line_bot_api = LineBotApi('apQkyD5cnxa8kanS8yfnr+ExfDR/yUoKmLXVu7epNzWsXqIoD1twn/YCGRnhIZLv4r36JYsjzVlpfWMHHaoTs9V4d/somxpkAI0ZNpiG8axYMp+xMbVvcC5vwyKEGizJWZ4CK1KX5DFqVxe5mb5lPgdB04t89/1O/w1cDnyilFU=')
"""
rich_menu_ref = []

with open("schoolmap_richmenu.json") as json_file:
    json_data = json.load(json_file)

richmenus = json_data['richmenus']

for i in range(len(richmenus)):
    rich_menu_data = richmenus[i]
    areas = []

    for j in range(len(rich_menu_data['areas'])):
        bounds_param = rich_menu_data['areas'][j]['bounds']
        action_param = rich_menu_data['areas'][j]['action']
        bounds = RichMenuBounds(x=bounds_param['x'], y=bounds_param['y'], width=bounds_param['width'], height=bounds_param['height'])
        action = MessageAction(text=action_param['text'])
        areas.append(RichMenuArea(bounds=bounds, action=action))

    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=True,
        name=rich_menu_data['name'],
        chat_bar_text=rich_menu_data['chatBarText'],
        areas = areas
    )

    rich_menu_id, name = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create), rich_menu_data['name']
    print(rich_menu_id, name + '\n')
    rich_menu_ref.append((rich_menu_id, name))

print(rich_menu_ref)
"""


# with open("./media/SchoolMap00.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-a2cd665487fbfb8ed9a43ea01b329256', 'image/png', f)
# with open("./media/SchoolMap01.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-b10d61385214045c56a13055a0b9f3a9', 'image/png', f)
# with open("./media/SchoolMap02.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-88b9ad4ad42288cd301cf35925f3d7c8', 'image/png', f)
# with open("./media/SchoolMap03.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-0fc92f8640d831b3159ebcdd62ee1ce3', 'image/png', f)
# with open("./media/SchoolMap04.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-34f7511662abc8adb612899b9f8c639a', 'image/png', f)
# with open("./media/SchoolMap05.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-a60905df9fa2705d972b805aeb0b70df', 'image/png', f)
# with open("./media/SchoolMap06.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-fa55218c41ab03a82de79fe321be875e', 'image/png', f)
# with open("./media/SchoolMap07.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-b933fec3e3de3e92bb271e805d8f473f', 'image/png', f)
# with open("./media/SchoolMap08.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-2e19234a741692098e3972ba4bd34451', 'image/png', f)
# with open("./media/SchoolMap09.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image('richmenu-ff85972065979651bcced6a651e554af', 'image/png', f)

# Set specific rich menu
line_bot_api.link_rich_menu_to_user('Uf06239f6f01f24d5664045d8333ab49d', 'richmenu-ff85972065979651bcced6a651e554af')

# unlink to default rich menu
# line_bot_api.unlink_rich_menu_from_user('Uf06239f6f01f24d5664045d8333ab49d')
