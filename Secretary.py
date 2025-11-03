documents = [
 {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
 {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
 {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

directories = {
 '1': ['2207 876234', '11-2'],
 '2': ['10006'],
 '3': []
}

def GetDocumentBy(searchKey, searchValue):
    for document in documents:
        if(searchKey in document):
            if(document[searchKey] == searchValue):
                return document

def GetDocumentOwner(documentNumber):
    return GetDocumentBy("number", documentNumber)["name"]

while True:
    print("Введите команду:")
    inp = input()
    match inp:
        case "q": break
        case "p":
            print("Введите номер документа:")
            docNum = input()
            print("Результат:")
            print("Владелец документа: " + GetDocumentOwner(docNum))
