import spacy
import json
import re


IT_LANG = "it"
EN_LANG = "en_core_web_sm"

GRAMMATICAL = "g"
LOGICAL = "l"
POETIC = "p"

#NLP -> natural language processing
class TextNLP:
    def __init__(self):
        pass

    def analysis(self, _type,text):
        if( _type == GRAMMATICAL ):
            output = self.analysisGram(text)
        elif ( _type == LOGICAL ):
            output = self.analysisLogic(text)
        elif ( _type == POETIC ):
            output = self.analysisPoe(text)
        else:
            output = "vaffanculo"

        return output

    def _GramProcessing(self, text):
        self.doc = self.nlp(text)

        data = {}
        for token in self.doc:
            data[token.text] = token.tag_
            json_data = json.dumps(data)

        return json_data

    def _LogicalProcessing(self, text):
        self.doc = self.nlp(text)

        data = {}
        for token in self.doc:
            data[token.text] = token.dep_
            json_data = json.dumps(data)

        return json_data

    def _PoeProcessing( self, text ):
        self.doc = self.nlp(text)
        # TODO Poetic Processing
        return "TODO"


class ItNLP(TextNLP):
    p_artis = None
    map_en2it = None
    def __init__(self):
        self.nlp = spacy.load(IT_LANG)
        #preposizioni articolate
        ItNLP.p_artis, ItNLP.map_en2it = self.load_data()
        # nmod  -> dopo il case
        # amod -> aggettivo


    # da formattare

    def load_data(self):
        fin = open("data_it")
        p_artis = dict()
        map_en2it = dict()

        #now reading
        nr = None
        for line in fin:
            line = line.splitlines()[0]

            #commento lo salta
            if(line[0] == "#"):
                continue

            if(line == "p"):
                nr = "p"
                continue

            if(line == "DictEn2It"):
                continue

            if(line == "e"):
                map_en2it[""] = dict()

            if(line[0]=="}"):
                nr = None
                continue

            if (line[0] == "{"):
                continue

            if (nr == None):
                map_en2it[line] = dict()
                nr = line
                continue

            row = line.split(";")
            for element in row:
                pair = element.split("=")
                if nr == "p":
                    p_artis[pair[0]] = pair[1]
                elif nr == "e":
                    map_en2it[""][pair[0]] = pair[1]
                else:
                    map_en2it[nr][pair[0]] = pair[1]

        #print(map_en2it)
        fin.close()
        return p_artis,map_en2it


    def _postProcessing(self, row):
        #rimpiazza TUTTA la stringa, se utente scrive Gender nella frase da analizzare quest'ultima viente tradotta
        #for index, value in ItNLP.map_en2it.items():
            #row = row.replace(index, value)

        for key, values in ItNLP.map_en2it.items():
            for k, v in values.items():
                if key == "":
                    row = row.replace(k + "=", v + "=")
                elif key == "i":
                    row = row.replace(k, v)
                else:
                    row = row.replace(key + "=" + k,key + "=" + v)
            row = row.replace("|", ";")

        return row

    def analysisGram(self,text):
        row = self._GramProcessing(text)
        formated = self._postProcessing(row)
        return formated

    # in realtà le ripetizioni di una parola non viene considerata
    # dunque fare restituire l'analisi diretta sarebbe scorretto
    # bensì si deve scorrere la frase di nuovo per poi assegnare ad ogni
    # pezzo il suo ruolo nella frase
    def analysisLogic(self,text):
        text = self._preProcLogicalText(text)
        row = self._LogicalProcessing(text)
        formated = row
        return formated

    @staticmethod
    def _preProcLogicalText(text):
        #cerca preposizioni articolate
        for index, value in ItNLP.p_artis.items():
            text = text.replace(index, value)
        return text

    def analysisPoe(self,text):
        row = self._PoeProcessing(text)
        formated = row
        return formated

class EnNLP(TextNLP):
    def __init__(self):
        self.nlp = spacy.load(EN_LANG)

    def analysisGram(self,text):
        row = self._GramProcessing(text)
        formated = row
        return formated

    def analysisLogic(self,text):
        row = self._LogicalProcessing(text)
        formated = row
        return formated

    def analysisPoe(self,text):
        row = self._PoeProcessing(text)
        formated = row
        return formated