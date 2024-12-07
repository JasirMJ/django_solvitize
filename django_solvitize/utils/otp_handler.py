

# OTP_DISABLED = False

# def generateOTP(mobile):
#     # Todo Need to correct this
#     print("Generating OTP for mobile ", mobile)

#     if str(mobile) == "911111111111":
#         print("Test Number OTP not generated")
#         return True
        
#     # Test OTP code removed
#     # if str(mobile) not in ["917907960873", "919656460604"]:
#     #     print("live otp not generated")
#     #     return True
#     # else:
#     #     print("live otp generated")

#     settings_obj = SettingsModel.objects.filter(
#         field_name__in=["msg91_auth_key", "msg91_template_id"])

#     if settings_obj.count() == 2:
#         for setting in settings_obj:
#             if setting.field_name == "msg91_auth_key":
#                 authkey = setting.value
#             elif setting.field_name == "msg91_template_id":
#                 template_id = setting.value

#     url = "https://control.msg91.com/api/v5/otp?template_id={}&mobile={}&otp_length={}&authkey={}".format(
#         template_id,
#         mobile,
#         6,
#         authkey
#     )
#     print("OTP url : ", url)
#     payload = {}
#     headers = {
#         'authkey': authkey,
#     }
#     # payload = "{\"Value1\":\"Param1\",\"Value2\":\"Param2\",\"Value3\":\"Param3\"}"

#     headers = {'content-type': "application/json"}
#     print("Sending OTP, url : ", url)
#     response = requests.request("GET", url, headers=headers, data=payload)

#     print("MSG91 Response ", response.json())

#     if response.json()["type"] == "success":
#         return True
#     else:
#         return False


# def validateOTP(mobile, otp):
#     # Todo Need to correct this
#     print("Validating OTP for mobile ", mobile, otp)
#     # return True
#     if mobile == "911122334455":
#         if otp == "1122":
#             return True
#         return False

#     settings_obj = SettingsModel.objects.filter(
#         field_name__in=["msg91_auth_key", "msg91_template_id"])

#     if settings_obj.count() == 2:
#         for setting in settings_obj:
#             if setting.field_name == "msg91_auth_key":
#                 authkey = setting.value

#     url = f"http://api.msg91.com/api/verifyRequestOTP.php?authkey={authkey}&mobile=" + \
#           mobile + "&otp=" + otp
#     print("OTP Verify url : ", url)
#     payload = {}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, data=payload)

#     if response.json()["type"] == "success":
#         return True

#     return False
