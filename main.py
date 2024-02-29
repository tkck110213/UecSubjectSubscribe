import pandas as pd
import PySimpleGUI as sg
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

class WindowGUI:
    def __init__(self, classManage):
        sg.theme('BlueMono')
        self.initWindow(classManage)

    def initWindow(self, classManage):
        yetRegistarClassList = classManage.getYetRegistarClass()
        registarClassList = classManage.getRegistarClass()
        registaredAllClassList = classManage.getAllRegistarClass()
        yetAcquiredClassList = classManage.getYetAcquiredClass()
        acquiredClassList = classManage.getAcquiredClass()
        deleteCandidateClass = classManage.getDeleteCandidateClass()

        registarLayout = [
            [sg.Text('登録したい科目を選択して"登録"ボタンをクリック')],
            [sg.Combo(values=tuple(yetRegistarClassList), default_value="科目を選択してください", size=(35,1), key="-RegistaredClass-"), 
            sg.Button("登録")],
            [sg.Text('削除したい科目を選択して"削除"ボタンをクリック')],
            [sg.Combo(values=tuple(deleteCandidateClass), default_value="科目を選択してください", size=(35,1), key="-DeleteClass-"), 
            sg.Button("削除")],
            [sg.Text("\n".join(registaredAllClassList), key="-RegistaredClassList-")]
        ]

        acquiredLayout = [
            [sg.Text('習得した科目を選択して"習得"ボタンをクリック')],
            [sg.Combo(values=tuple(yetAcquiredClassList), default_value="科目を選択", size=(35,1), key="-AcquiredClass-"), 
             sg.Combo(values=tuple(["優", "良", "可", "不可"]), default_value="評価を選択", size=(5,1), key="-AcquiredClassEvaluation-"),
             sg.Button("習得")],
            [sg.Text("\n".join(acquiredClassList), key="-AcquiredClassList-")]
        ]

        registaredCreditLayout = [
            [sg.Table(classManage.judgeClassCredit(return_type="list"), headings=["科目区分", "修了要件", "現単位数", "残単位数"], key="-RegistarTable-")]
        ]

        initializeLayout = [
            [sg.Button("データベースを初期化する")]
        ]

        allLayout = [[sg.TabGroup([[sg.Tab('履修登録', registarLayout),
                                    sg.Tab('習得単位', acquiredLayout),
                                    sg.Tab('登録状況', registaredCreditLayout),
                                    sg.Tab('初期化', initializeLayout),
                                ]])]]

        self.window = sg.Window('電通大院成績管理システム', allLayout, size=(450, 400))

    def read(self):
        return self.window.read(timeout=100)

    def renewRegistarTable(self, classManage):
        registaredAllClassList = classManage.getAllRegistarClass()
        yetRegistarClassList = classManage.getYetRegistarClass()
        yetAcquiredClassList = classManage.getYetAcquiredClass()
        deleteCandidateClass = classManage.getDeleteCandidateClass()
        self.window["-RegistaredClassList-"].update("\n".join(registaredAllClassList))
        self.window["-RegistaredClass-"].update(values=tuple(yetRegistarClassList))
        self.window["-DeleteClass-"].update(values=tuple(deleteCandidateClass))
        self.window["-AcquiredClass-"].update(values=tuple(yetAcquiredClassList))
        self.window["-RegistarTable-"].update(classManage.judgeClassCredit(return_type="list"))

    def renewAcquiredTable(self, classManage):
        acquiredClassList = classManage.getAcquiredClass()
        yetAcquiredClassList = classManage.getYetAcquiredClass()
        deleteCandidateClass = classManage.getDeleteCandidateClass()
        self.window["-AcquiredClassList-"].update("\n".join(acquiredClassList))
        self.window["-AcquiredClass-"].update(values=tuple(yetAcquiredClassList))
        self.window["-DeleteClass-"].update(values=tuple(deleteCandidateClass))
        

def main():
    l_classManage = ClassManage()
    window = WindowGUI(l_classManage)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            l_classManage.exportDataBaseCsv()
            break
        elif event == "登録":
            l_classManage.registarClass(values["-RegistaredClass-"])
            window.renewRegistarTable(l_classManage)
        elif event == "削除":
            l_classManage.deleteClass(values["-DeleteClass-"])
            window.renewRegistarTable(l_classManage)
        elif event == "習得":
            l_classManage.acquiredClass(values["-AcquiredClass-"])
            window.renewAcquiredTable(l_classManage)
        elif event == "データベースを初期化する":
            l_classManage.initializeDataBase()
            window.initWindow(l_classManage)

main()


