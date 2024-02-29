import pandas as pd
import os

class ClassManage:
    def __init__(self):
        is_file = os.path.isfile("./database/latest_class_database.csv")
        if is_file:
            self.classDataBase = pd.read_csv("./database/latest_class_database.csv", index_col=0, encoding="shift-jis")
        else:   
            self.classDataBase = pd.read_csv("./database/class_database.csv", index_col=0, encoding="shift-jis")
        #print(self.classDataBase)
        self.registaredCredit = pd.DataFrame(index=["fundamentalClass", "journalClub", "technologyEnglish", "industrycollaboration", "specializedClass1", "specializedClass2"], columns=["credit"])
        self.calcRegistaredCredit()
        self.judgeClassCredit()

    def registarClass(self, className):
        self.classDataBase.at[className, "registar"] = True

    def deleteClass(self, className):
        if self.classDataBase.at[className, "acquired"] == True:
            sg.popup("この科目はすでに履修済みです\n削除できません")
        else:
            self.classDataBase.at[className, "registar"] = False

    def acquiredClass(self, className):
        self.classDataBase.at[className, "acquired"] = True

    def printRegistarClass(self, className):
        if self.classDataBase.at[className, "registar"]:
            print(className + ": already registar")
        else:
            print(className + ": don`t registar")

    def printRegistarClassset(self):
        for row in self.classDataBase.itertuples():
            if row.registar:
                print(row.Index)

    def getYetRegistarClass(self):
        return list(self.classDataBase.query("registar == False").index)
    
    def getAllRegistarClass(self):
        return list(self.classDataBase.query("registar == True").index)

    def getRegistarClass(self):
        return list(self.classDataBase.query("registar == True & requried == False").index)

    def getYetAcquiredClass(self):
        return list(self.classDataBase.query("acquired == False & registar == True").index)
    
    def getAcquiredClass(self):
        return list(self.classDataBase.query("acquired == True & registar == True").index)

    def getDeleteCandidateClass(self):
        return list(set(self.getRegistarClass()) - set(self.getAcquiredClass()))

    def exportDataBaseCsv(self):
        self.classDataBase.to_csv("./database/latest_class_database.csv", encoding="shift-jis")

    def initializeDataBase(self):
        self.classDataBase = pd.read_csv("./database/class_database.csv", index_col=0, encoding="shift-jis")

    def calcRegistaredCredit(self):
        self.registaredCredit.at["fundamentalClass", "credit"] = self.classDataBase.query("type2 == '大学院基礎教育科目' & registar == True")["credit"].sum()
        self.registaredCredit.at["journalClub", "credit"] = self.classDataBase.query("type2 == '大学院輪講' & registar == True")["credit"].sum()
        self.registaredCredit.at["technologyEnglish", "credit"] = self.classDataBase.query("type2 == '大学院技術英語'")["credit"].sum()
        self.registaredCredit.at["industrycollaboration", "credit"] = self.classDataBase.query("type2 == '大学院産学連携科目' & registar == True")["credit"].sum()
        self.registaredCredit.at["specializedClass1", "credit"] = self.classDataBase.query("type2 == '専門科目1' & registar == True")["credit"].sum()
        self.registaredCredit.at["specializedClass2", "credit"] = self.classDataBase.query("type2 == '専門科目2' & registar == True")["credit"].sum()
        print(self.registaredCredit)
        print(self.registaredCredit["credit"].sum())

    def judgeClassCredit(self, return_type="df"):
        # 登録済みの単位を計算する
        self.calcRegistaredCredit()

        # 修了要件を満たしているかを真偽値で格納する辞書
        judgeCredit = pd.DataFrame(columns=["isFill", "credit", "lackCredit"])

        #それぞれの区分の単位数が修了要件を満たしているか
        judgeCredit.at["大学院基礎教育科目", "credit"]  = self.registaredCredit.at["fundamentalClass", "credit"]
        if self.registaredCredit.at["fundamentalClass", "credit"] >= 2:
            judgeCredit.at["大学院基礎教育科目", "isFill"] = True
            judgeCredit.at["大学院基礎教育科目", "lackCredit"]  = 0
        else:
            judgeCredit.at["大学院基礎教育科目", "isFill"] = False
            judgeCredit.at["大学院基礎教育科目", "lackCredit"] = 2 - self.registaredCredit.at["fundamentalClass", "credit"]

        judgeCredit.at["大学院産学連携科目", "credit"] = self.registaredCredit.at["industrycollaboration", "credit"]
        if self.registaredCredit.at["industrycollaboration", "credit"] >= 2:
            judgeCredit.at["大学院産学連携科目", "isFill"] = True
            judgeCredit.at["大学院産学連携科目", "lackCredit"] = 0
        else:
            judgeCredit.at["大学院産学連携科目", "isFill"] = False
            judgeCredit.at["大学院産学連携科目", "lackCredit"] = 2 - self.registaredCredit.at["industrycollaboration", "credit"]

        judgeCredit.at["専門科目1", "credit"] = self.registaredCredit.at["specializedClass1", "credit"]
        if self.registaredCredit.at["specializedClass1", "credit"] >= 10:
            judgeCredit.at["専門科目1", "isFill"] = True
            judgeCredit.at["専門科目1", "lackCredit"] = 0
        else:
            judgeCredit.at["専門科目1", "isFill"] = False
            judgeCredit.at["専門科目1", "lackCredit"] = 10 - self.registaredCredit.at["specializedClass1", "credit"]
 
        judgeCredit.at["専門科目2", "credit"] = self.registaredCredit.at["specializedClass2", "credit"]
        if self.registaredCredit.at["specializedClass2", "credit"] >= 8:
            judgeCredit.at["専門科目2", "isFill"] = True
            judgeCredit.at["専門科目2", "lackCredit"] = 0
        else:
            judgeCredit.at["専門科目2", "isFill"] = False
            judgeCredit.at["専門科目2", "lackCredit"] = 8 - self.registaredCredit.at["specializedClass2", "credit"]

        judgeCredit.at["総単位数", "credit"] = self.registaredCredit["credit"].sum()
        if self.registaredCredit["credit"].sum() >= 30:
            judgeCredit.at["総単位数", "isFill"] = True
            judgeCredit.at["総単位数", "lackCredit"] = 0
        else:
            judgeCredit.at["総単位数", "isFill"] = False
            judgeCredit.at["総単位数", "lackCredit"] = 30 - self.registaredCredit["credit"].sum()

        print(judgeCredit)
        if return_type == "df":
            return judgeCredit
        elif return_type == "list":
            return judgeCredit.reset_index().values.tolist()


