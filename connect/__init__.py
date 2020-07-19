"""
0. overall() ./overall?assessment_id=1
data = {
            <county>: {
                          "check_ratio": <float>
                          "checked_num": <int>   # unit: building
                          "uncheck_num": <int>   # unit: building
                                  "TBD": {       # stock of per county
                                            "Quick": <int>
                                            "Normal": <int>
                                            "Indoors": <int>
                                            "Corridor": <int>
                                            "Outdoors": <int>
                                         }
                      }
       }

1. event() ./event
data = {
          "<assessment_id>": {
                                "assessment_id": <assessment_id>,
                                "event": <string>,
                                "time": <string>,     # GMT
                             }
       }

2. fetch(county, assessment_id) ./fetch?county=臺北市&assessment_id=1
data = {
          "<school_name>": {
                                "YN": "<checked_building>/<total_building>",
                                "address": <string>,
                                "county": <string>,
                                "latitude": <%5float>,
                                "longitude": <%5float>,
                                "name": <string>,
                                "phone": <string>,
                                "school_id": <int>,
                                "school_name": <string>,
                                "severity": <float>,      # checked_building / total_building * 100
                                "userid": <string>
                            },
       }

3. building(school_id) building?school_id=8&assessment_id=1
data = {
            "assessment_id": <int>,
            "building_id": [ <string> , ..., <string> ],
            "building_name": [ <string> , ..., <string> ],
            "yn": [ <bool>, ..., <bool> ],       # True if checked
            "serverity": [ <int> ,..., <int> ],  # score of each questionnaire
            "school_name": <string>,
       }

4. Detail(assessment_id, building_id) ./detail?assessment_id=1&building_id=363102-9
data = {
            <abs_q>: {
                        "content": <string>,
                        "description": <string>,
                        "img_url": <string>,     # imgur
                        "pos": <string>,         # 上上
                        "question": <string>,    # "Normal Q12"
                     },
       }
"""
