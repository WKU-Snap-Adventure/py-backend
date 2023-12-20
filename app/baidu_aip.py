from aip import AipImageClassify
from . import app

client = AipImageClassify(
    app.config['AIP_APP_ID'],
    app.config['AIP_API_KEY'],
    app.config['AIP_SECRET_KEY']
    )

def objectDetect(image):
    """ 调用通用物体识别 """
    return client.advancedGeneral(image)