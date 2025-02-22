from os.path import exists
from os import mkdir
from csv import writer


def isuser(uid, usertype="basic", nul=False):
    if usertype == "NaU":
        if nul:
            if not exists(f"UserFiles/U_{uid}") or isuser(uid, "basic", nul=True) or isuser(uid, "premium", nul=True):
                return False
        else:
            if not exists(f"UserFiles/U_{uid}") or isuser(uid, "basic") or isuser(uid, "premium"):
                return False
        return True
    elif usertype == "basic":
        with open("Accounts/Ubasic.csv", "rt", encoding="utf-8") as ubasIN:
            ubasIN.seek(0)
            for line in ubasIN:
                line = line.split(',')
                if nul:
                    if str(uid) == line[0]:
                        return True
                elif str(uid) == line[0] and int(line[1]) >= 1:
                    return True
        return False
    elif usertype == "premium":
        with open("Accounts/Upremium.csv", "rt", encoding="utf-8") as upremIN:
            upremIN.seek(0)
            for line in upremIN:
                line = line.split(',')
                if nul:
                    if str(uid) == line[0]:
                        return True
                elif str(uid) == line[0] and int(line[1]) >= 1:
                    return True
        return False


def reduce(uid, usertype="basic", howmuch=1):
    if usertype == "basic":
        with open("Accounts/Ubasic.csv", "r+t", encoding="utf-8") as ubasOUT:
            lines = ubasOUT.readlines()
            for i in range(len(lines)):
                ln = lines[i].split(',')
                if str(uid) == ln[0]:
                    ln[1] = str(int(ln[1]) - howmuch)
                    lines[i] = ','.join(ln) + '\n'
            ubasOUT.seek(0)
            ubasOUT.writelines(lines)
            ubasOUT.truncate()
    elif usertype == "premium":
        with open("Accounts/Upremium.csv", "r+t", encoding="utf-8") as upremOUT:
            lines = upremOUT.readlines()
            for i in range(len(lines)):
                ln = lines[i].split(',')
                if str(uid) == ln[0]:
                    ln[1] = str(int(ln[1]) - howmuch)
                    lines[i] = ','.join(ln) + '\n'
            upremOUT.seek(0)
            upremOUT.writelines(lines)
            upremOUT.truncate()


def adder(uid, usertype="basic", howmuch=2):
    if usertype == "basic":
        with open("Accounts/Ubasic.csv", "r+t", encoding="utf-8") as ubasOUT:
            lines = ubasOUT.readlines()
            for i in range(len(lines)):
                ln = lines[i].split(',')
                if str(uid) == ln[0]:
                    ln[1] = str(int(ln[1]) + howmuch)
                    lines[i] = ','.join(ln) + '\n'
            ubasOUT.seek(0)
            ubasOUT.writelines(lines)
            ubasOUT.truncate()
    elif usertype == "premium":
        with open("Accounts/Upremium.csv", "r+t", encoding="utf-8") as upremOUT:
            lines = upremOUT.readlines()
            for i in range(len(lines)):
                ln = lines[i].split(',')
                if str(uid) == ln[0]:
                    ln[1] = str(int(ln[1]) + howmuch)
                    lines[i] = ','.join(ln) + '\n'
            upremOUT.seek(0)
            upremOUT.writelines(lines)
            upremOUT.truncate()


def newuser(uid, usertype="basic", howmuch=2, lang='en'):
    if usertype == "NaU":
        if not exists(f"UserFiles/U_{uid}"):
            mkdir(f"UserFiles/U_{uid}")
            mkdir(f"UserFiles/U_{uid}/DataNotToShow")
            mkdir(f"UserFiles/U_{uid}/DataVisible")
            mkdir(f"UserFiles/U_{uid}/PDFs")

            with open(f'UserFiles/U_{uid}/DataNotToShow/language.txt', 'wt') as data:
                data.write(lang)
        if not exists(f"UserFiles/U_{uid}/DataNotToShow/files_id.csv"):
            with open(f'UserFiles/U_{uid}/DataNotToShow/files_id.csv', 'wt', encoding='utf-8',
                      newline='') as file:
                csv_writer = writer(file)
                csv_writer.writerow(('filename', 'fileid'))
    elif usertype == "basic":
        with open("Accounts/Ubasic.csv", "at", encoding="utf-8") as ubas:
            ubas.write(f"{str(uid)},{howmuch}\n")
            if not exists(f"UserFiles/U_{uid}"):
                mkdir(f"UserFiles/U_{uid}")
                mkdir(f"UserFiles/U_{uid}/DataNotToShow")
                mkdir(f"UserFiles/U_{uid}/DataVisible")
                mkdir(f"UserFiles/U_{uid}/PDFs")

                with open(f'UserFiles/U_{uid}/DataNotToShow/language.txt', 'wt') as data:
                    data.write(lang)
    elif usertype == "premium":
        with open("Accounts/Upremium.csv", "at", encoding="utf-8") as uprem:
            uprem.write(f"{str(uid)},{howmuch}\n")
            if not exists(f"UserFiles/U_{uid}"):
                mkdir(f"UserFiles/U_{uid}")
                mkdir(f"UserFiles/U_{uid}/DataNotToShow")
                mkdir(f"UserFiles/U_{uid}/DataVisible")
                mkdir(f"UserFiles/U_{uid}/PDFs")

                with open(f'UserFiles/U_{uid}/DataNotToShow/language.txt', 'wt') as data:
                    data.write(lang)

            if not exists(f"UserFiles/U_{uid}/DataNotToShow/files_id.csv"):
                with open(f'UserFiles/U_{uid}/DataNotToShow/files_id.csv', 'wt', encoding='utf-8', newline='') as file:
                    csv_writer = writer(file)
                    csv_writer.writerow(('filename', 'fileid'))


def accessnum(uid, usertype="basic"):
    if usertype == "basic":
        with open("Accounts/Ubasic.csv", "r+t", encoding="utf-8") as ubasOUT:
            lines = ubasOUT.readlines()
            for i in range(len(lines)):
                ln = lines[i].split(',')
                if str(uid) == ln[0]:
                    if int(ln[1]):
                        return ln[1]
        return "0   click /pay"
    elif usertype == "premium":
        with open("Accounts/Upremium.csv", "r+t", encoding="utf-8") as upremOUT:
            lines = upremOUT.readlines()
            for i in range(len(lines)):
                ln = lines[i].split(',')
                if str(uid) == ln[0]:
                    if int(ln[1]):
                        return ln[1]

        return "0   click /payplus"
