import json

from server import req
from server.server import Server

Server().UpdateDns("104.20.180.50", "104.20.180.50")
# r = Server().Send(req.LoginReq("tonquer2", "tonquer2"), isASync=False)
Server().token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MDEyMjg3YzYxYWFlODJmZDJjMGQzNTUiLCJlbWFpbCI6InRvbnF1ZXIyIiwicm9sZSI6Im1lbWJlciIsIm5hbWUiOiJ0b25xdWVyMiIsInZlcnNpb24iOiIyLjIuMS4zLjMuNCIsImJ1aWxkVmVyc2lvbiI6IjQ1IiwicGxhdGZvcm0iOiJhbmRyb2lkIiwiaWF0IjoxNjM3MDI3NzkyLCJleHAiOjE2Mzc2MzI1OTJ9.XijmXi0w_uuxis7ZMFcVtn6lXjyTXyKLl9mpzSWVkKI"
r = Server().Send(req.InitAndroidReq(), isASync=False)
data = json.loads(r.raw.text)
r