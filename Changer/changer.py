__author__ = 'Sanhee Park'
__email__ = 'gteasan@gmail.com'
__version__ = '0.0.1'
__refer__ = 'Chanwoo Yoon'

import re

import hgtk
from tqdm.auto import tqdm

from kiwipiepy import Kiwi
from dictionary import informaldic, formaldic, abnormaldic
from utils import Utils

class Changer(object):
    def __init__(self):    
        try:
            self.kiwi = Kiwi()
            self.kiwi.prepare()
        except:
            print("[INFO] please install kiwipiepy   ")
            
        self.replace = formaldic()
        self.utils = Utils()

    def dechanger(self, stc):
        """
        change formal speech to informal
        Args : str
        """
        pattern = r'하세요|이예요|이에요|에요|예요|시겠어요|죠|합니까|습니까'
        pattern = re.compile(pattern)

        result = []


        stc = self.utils._remove_blank(stc)
        stc = self.utils._clean_up_tokenization(stc)

        if len(re.findall(pattern, stc)) > 0:
            tokens = self.kiwi.analyze(stc.replace(" ","|"))
            
            key = informaldic().keys()
            lk = list(key)
            key2 = abnormaldic().keys()
            ak = list(key2)
            
            tmp = []
            for token in tokens[0][0]:
                if token[:2] in lk:
                    #key로 value
                    token = informaldic().get(token[:2])
                if token[:2] in ak:
                    token = abnormaldic().get(token[:2])
                tmp.append(token)

            changed = ''
            for t in tmp:
                if isinstance(t[0], tuple):
                    for i in range(len(t[0])):
                        changed += hgtk.text.decompose(t[i][0])
                else:
                    changed += hgtk.text.decompose(t[0])
                    
            one_char = re.compile('ᴥ[ㅂㄴㄹ]ᴥ')
            if one_char.search(changed):
                words = changed.split('ᴥ')
                for idx in range(1,len(words)):
                    # 앞 글자가 종성이 없음
                    if len(words[idx]) == 1 and len(words[idx-1].replace('|',"")) == 2:
                        #앞 글자에 합침
                        words[idx - 1] = words[idx-1]+words[idx]
                        words[idx] = ""
                    # 있음
                    elif len(words[idx]) == 1 and len(words[idx-1].replace('|',"")) == 3:
                        shp = ['ㅆ','ㅍ','ㄱ','ㅄ','ㄶ']
                        ep = ['ㄹ']
                        if words[idx] == 'ㅂ' and len(words[idx - 1].replace('|', "")) == 3 :
                            if words[idx - 1][-1] in shp :
                                if words[idx].count("|") > 0:
                                    words[idx] = "|습"
                                else:
                                    words[idx ] = "습"
                                continue
                            else :
                                if words[idx].count("|") > 0:
                                    words[idx] = "|입"
                                else:
                                    words[idx] = "입"
                                # words[idx] = ""
                        elif words[idx] =='ㄴ' and len(words[idx-1].replace('|',"")) == 3 and words[idx - 1].endswith('ㄹ'):
                            if words[idx-1].count("|") >0 :
                                words[idx - 1] = "|" + words[idx - 1].replace("|","")[:2] + words[idx]
                            else :
                                words[idx - 1] = words[idx - 1][:2] + words[idx]
                            # 지움
                            words[idx] = ""
                        elif words[idx] =='ㄹ':
                            if words[idx].count("|") > 0:
                                words[idx] = "|일"
                            else:
                                words[idx] = "일"

                changed = "ᴥ".join([x for x in words if x is not ""])+"ᴥ"
            # For cases which wasn't covered,
            changed = self._makePretty(changed)
            changed = hgtk.text.compose(changed).replace("|"," ")
            # excetion 처리
            try:
                if changed[-1] == '요':
                    changed = re.sub('요', '', changed)
                changed = re.sub('그렇죠', '', changed)
            except:
                pass
            result.append(changed)

        else:
            try:
                result.append(stc)
            except:
                pass
        return result[0]
        

    def _makePretty(self, line):
        """
        Convert the jaso orderings which wasn't properly covered by
        Jaso restructuring process of function Mal_Gillge_Haeraing
        :param line: jaso orderings which wasn't properly covered
        :return: Converted jaso ordering
        """
        test = line
        test = test.replace("ᴥㅎㅏᴥㅇㅏᴥ", "ᴥㅎㅐᴥ")
        test = test.replace("ㅎㅏᴥㅇㅏᴥㅇㅛᴥ", "ᴥㅎㅐᴥ")
        test = test.replace("ㅎㅏᴥㄴㅣᴥㄷㅏᴥ", "ㅎㅏㅂᴥㄴㅣᴥㄷㅏᴥ")
        test = test.replace("ㅎㅏᴥㅇㅏㅆᴥ", "ᴥㅎㅐㅆᴥ")
        test = test.replace("ㄴㅏᴥㅇㅏㅆᴥ", "ᴥㅎㅐㅆᴥ")
        test = test.replace("ㄱㅏᴥㅇㅏㅆᴥ", "ᴥㄱㅏㅆᴥ")
        test = test.replace("ㅇㅣᴥㄴㅣᴥ", "ᴥㄴㅣᴥ")
        test = test.replace("ㄴㅓㄹㄴᴥ","ㄴㅓㄴᴥ")
        test = test.replace("ㄱㅡᴥㄹㅓㅎᴥㅇㅓᴥ","ㄱㅡᴥㄹㅐᴥ")
        test = test.replace("ㅡᴥㅇㅏᴥ","ㅏᴥ")
        test = test.replace("ㄱㅓㄹᴥㄴㅏᴥㅇㅛᴥ", "ㄱㅓㄴᴥㄱㅏᴥㅇㅛᴥ")
        return test

    def changer(self, text):
        """
        change informal speech to formal speech
        Args : str
        """
        tokens = self.kiwi.analyze(text.replace(" ","|"))
        
        key = formaldic().keys()
        key2 = abnormaldic().keys()
        lk = list(key)
        ak = list(key2)
        
        num = len(tokens[0][0])
        result = []
        for idx, token in enumerate(tokens[0][0]):
            if idx > int(num*0.8):        
                if token[:2] in lk:
                    #key로 value
                    token = formaldic().get(token[:2])
                    result.append(token)
                else:
                    if token[:2] in ak:
                        token = abnormaldic().get(token[:2])
                        result.append(token)
                    else:
                        result.append(token[:2])
            else:
                if token[:2] in ak:
                    token = abnormaldic().get(token[:2])
                    result.append(token)
                else:
                    result.append(token[:2])
                
        # change tuple to text
        changed = ''
        for t in result:
            if isinstance(t[0], tuple):
                for i in range(len(t[0])):
                    changed += hgtk.text.decompose(t[i][0])
            else:
                changed += hgtk.text.decompose(t[0])

        # Restructuring sentence from jaso ordering.
        one_char = re.compile('ᴥ[ㅂㄴㄹ]ᴥ')
        if one_char.search(changed):
            words = changed.split('ᴥ')
            for idx in range(1,len(words)):
                # 앞 글자가 종성이 없음
                if len(words[idx]) == 1 and len(words[idx-1].replace('|',"")) == 2:
                    #앞 글자에 합침
                    words[idx - 1] = words[idx-1]+words[idx]
                    words[idx] = ""
                # 있음
                elif len(words[idx]) == 1 and len(words[idx-1].replace('|',"")) == 3:
                    shp = ['ㅆ','ㅍ','ㄱ','ㅄ','ㄶ']
                    ep = ['ㄹ']
                    if words[idx] == 'ㅂ' and len(words[idx - 1].replace('|', "")) == 3 :
                        if words[idx - 1][-1] in shp :
                            if words[idx].count("|") > 0:
                                words[idx] = "|습"
                            else:
                                words[idx ] = "습"
                            continue
                        else :
                            if words[idx].count("|") > 0:
                                words[idx] = "|입"
                            else:
                                words[idx] = "입"
                            # words[idx] = ""
                    elif words[idx] =='ㄴ' and len(words[idx-1].replace('|',"")) == 3 and words[idx - 1].endswith('ㄹ'):
                        if words[idx-1].count("|") >0 :
                            words[idx - 1] = "|" + words[idx - 1].replace("|","")[:2] + words[idx]
                        else :
                            words[idx - 1] = words[idx - 1][:2] + words[idx]
                        # 지움
                        words[idx] = ""
                    elif words[idx] =='ㄹ':
                        if words[idx].count("|") > 0:
                            words[idx] = "|일"
                        else:
                            words[idx] = "일"

            changed = "ᴥ".join([x for x in words if x is not ""])+"ᴥ"
        # For cases which wasn't covered,
        changed = self._makePretty(changed)
        changed = hgtk.text.compose(changed).replace("|"," ")
        return changed
        
    def addData(self, key, val):
        """
        Add new data to dictionary, changer dictionary update
        :param key: key to be added into Dictionary self.replace
        :param val: Value to be added into Dictionary self.replace
        :return: None
        """
        with open('dictionary.py', 'r', encoding='utf-8') as f:
            data = f.read()

        lines = data.split("\n")
        lines[-2] += ','
        lines[-1] = "                    " + str(key) + ": " + str(val)
        with open('dictionary.py', 'w', encoding='utf-8') as f:
            for i in range(len(lines)):
                f.write(lines[i] + "\n")
            f.write("                    }")

    def checker(self, result):
        """
        Check the abnormal setnecnes and remove them.
        Args : result, updated, idx : list 
        """
        updated = []
        idxes = []
        normal = ['요', '까', '다', '죠', '가']
        for idx, stc in enumerate(result):
            try:
                if stc[-1] not in normal:
                    print(f"[INFO] Abnormal Sentence, remove {idx}....")
                    idxes.append(idx)
                else:
                    updated.append(stc)
            except:
                idxes.append(idx)

        return updated, idxes