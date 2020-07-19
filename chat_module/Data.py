class Data:
    def __init__(self):
        self.__data = {}

        ################
        #### setter ####
        ################

    def add_user(self, userid):
        """ 新增新的 userid """
        self.__data[userid] = {
                            "Answered":
                            {
                                "Quick": [],
                                "Normal":[],
                                "Indoors":[],
                                "Corridor":[],
                                "Outdoors":[],
                            },
                            "status": "pre",
                            "feedback": [],
                            "current": (),
                            "building": [],
                        }
        return
    def remove_user(self, userid):
        """ 刪除某填完問卷的 userid """
        del self.__data[userid] # delete key
        return
    def add_user_answered(self, userid, cat, ques):
        """ 新增某 user 某類別已填答的題號 """
        self.__data[userid]["Answered"][cat].append(ques)
        return
    def del_user_answered(self, userid, cat, ques):
        """ 刪除某 user 某類別已填答的題號 """
        self.__data[userid]["Answered"][cat].remove(ques)
        return
    def set_user_status(self, userid, status):
        """ 更改某 user 的 status """
        self.__data[userid]["status"] = status
        return
    def add_user_feedback(self, userid, feedback):
        """ 新增某 user 的 feedback """
        self.__data[userid]["feedback"].append(feedback)
        return
    def set_user_spec_feedback_pos(self, userid, pos):
        """ 新增某 user 該 feedback 所選擇的位置 """
        idx = self.__data[userid]["feedback"].index(self.__data[userid]["current"]) # find the corresponding idx in feedback
        self.__data[userid]["feedback"][idx] += (pos,)
        return
    def set_user_spec_feedback_img(self, userid, img_url):
        """ 新增某 user 該 feedback 所上傳的照片 """
        idx = self.__data[userid]["feedback"].index(self.__data[userid]["current"]) # find the corresponding idx in feedback
        self.__data[userid]["feedback"][idx] += (img_url,)
        return
    def set_user_feedback(self, userid, feedback):
        """ 整個 feedback (list) 換成新的 """
        self.__data[userid]["feedback"] = feedback
        return
    def set_user_current(self, userid, current):
        """ 更改某 user 的 current """
        self.__data[userid]["current"] = current
        return
    def set_user_building(self, userid, building):
        """ 紀錄某 user 的 building name """
        self.__data[userid]["building"].append(building)
        return

        ################
        #### getter ####
        ################

    def get_user(self, userid):
        return self.__data[userid] if userid in self.__data else {}
    def get_all_users(self):
        return self.__data
    def get_user_current(self, userid):
        return self.__data[userid]["current"]
    def get_user_feedback(self, userid):
        return self.__data[userid]["feedback"]
    def get_user_status(self, userid):
        return self.__data[userid]["status"]
    def get_user_building(self, userid):
        return self.__data[userid]["building"]
