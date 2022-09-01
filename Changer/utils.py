import re

class Utils(object):
    def __init__(self, option=False):
        # save path default 
        self.option = option
        
    def getsentence(self, path):
        """
        Args :return generator
        """
        texts = open(path, 'r').readlines()
        for text in texts:
            yield text

    def _remove_blank(self, text):
        """
        Args : str
        """
        text = text.replace('\xa0', ' ')
        text = text.strip('\n')
        text = re.sub('\n', '', text) # middle \n 제거
        return text

    def _clean_up_tokenization(self, out_string):
        """ Clean up a list of simple Korean tokenization artifacts like spaces before punctuations and abreviated forms.
            Args : str
        """
        out_string = out_string.replace('.', '')
        out_string = out_string.replace('?', '')
        out_string = out_string.replace('!', '')
        return out_string
     
    def readfile(self, path):
        """
        read file, usually text to list
        """
        corpus = open(path, 'r').readlines()
        
        if not self.option:
            return corpus
        else:
            corpus = self._remove_blank(corpus)
            corpus = self._clean_up_tokenization(corpus)
            return corpus
        
    def writefile(self, result, save_name : str):
        """
        Args :usually result list to text file
        """
        # write character at once - 'cp949' encoding
        with open(save_name, 'w') as f:
            for stc in result:
                f.write(stc +'\n')
            f.close()