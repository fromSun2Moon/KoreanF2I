import os

from tqdm.auto import tqdm
from utils import Utils
from changer import Changer
# global variable

informal = '나는 매일 저녁 배트를 만나러 다락방으로 가'
formal = '그랜드 캐년으로 가려면 어느 도시에서 가는 게 제일 쉽습니까?'
path = 'diag_src_kor'
# ready model
model = Changer()

# informal to formal 
print("formal to informal >>>>>>", model.dechanger(formal))

# formal to informal
print("informal to formal >>>>>>", model.changer(informal))

################################ User custom ################################
################################             ################################
#############################################################################

# If you need more dictionary, you can add them.
    # model.addData()
# check your words abnormal (only catch words behind. for instance, it doesn't end in 다 나 까 요 )
    # model.checker()
# If you want to read or write file, Use utils
utils = Utils()

    #utils.readfile(file_name)
    #utils.writefile(result, save_name)

