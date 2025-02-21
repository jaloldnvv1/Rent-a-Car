import json
from abc import ABC, abstractmethod
from datetime import datetime


def ajratish():
    print("-" * 30)


class Transport(ABC):
    def __init__(self, brend, model, yil, kunlik_narx):
        self.brend = brend
        self.model = model
        self.yil = yil
        self.kunlik_narx = kunlik_narx

    @abstractmethod
    def mashina_turi(self):
        pass

    def __str__(self):
        return f"{self.yil} {self.brend} {self.model} - {self.kunlik_narx}-so'm/kun"

    def to_dict(self):
        return {
            "brend": self.brend,
            "model": self.model,
            "yil": self.yil,
            "kunlik_narx": self.kunlik_narx,
            "mashina_turi": self.mashina_turi(),
        }


class Malibu(Transport):
    def mashina_turi(self):
        return "Malibu 2"


class Gentra(Transport):
    def mashina_turi(self):
        return "Gentra"


class Kia(Transport):
    def mashina_turi(self):
        return "Kia K5"


class Mijoz:
    def __init__(self, ism, telefon):
        self.ism = ism
        self.telefon = telefon

    def mijoz_info(self):
        return f"Mijoz: {self.ism}\nTel: {self.telefon}"

    def to_dict(self):
        return {
            "ism": self.ism,
            "telefon": self.telefon,
        }


class Haydovchi:
    def __init__(self, ism, yosh, tajriba_yil):
        self.ism = ism
        self.yosh = yosh
        self.tajriba_yil = tajriba_yil

    def haydovchi_info(self):
        return f"Haydovchi: {self.ism}, Yosh: {self.yosh}, Tajriba: {self.tajriba_yil} yil"

    def to_dict(self):
        return {
            "ism": self.ism,
            "yosh": self.yosh,
            "tajriba_yil": self.tajriba_yil,
        }


class Buyurtma:
    def __init__(self, mijoz, transport, boshlanish_sanasi, tugash_sanasi, haydovchi=None):
        self.mijoz = mijoz
        self.transport = transport
        self.boshlanish_sanasi = boshlanish_sanasi
        self.tugash_sanasi = tugash_sanasi
        self.haydovchi = haydovchi
        self.umumiy_narx = self.narx_hisobla()

    def narx_hisobla(self):
        kunlar = (self.tugash_sanasi - self.boshlanish_sanasi).days
        return kunlar * self.transport.kunlik_narx

    def to_dict(self):
        return {
            "mijoz": self.mijoz.to_dict(),
            "transport": self.transport.to_dict(),
            "boshlanish_sanasi": self.boshlanish_sanasi.strftime("%Y-%m-%d"),
            "tugash_sanasi": self.tugash_sanasi.strftime("%Y-%m-%d"),
            "umumiy_narx": self.umumiy_narx,
            "haydovchi": self.haydovchi.to_dict() if self.haydovchi else None,
        }

    def __str__(self):
        buyurtma_info = (
            f"{self.mijoz.ism} uchun buyurtma: {self.transport} {self.boshlanish_sanasi.date()} dan "
            f"{self.tugash_sanasi.date()} gacha - Umumiy narx: {self.umumiy_narx}-so'm"
        )
        if self.haydovchi:
            buyurtma_info += f"\n{self.haydovchi.haydovchi_info()}"
        return buyurtma_info


class Tolov:
    def __init__(self, buyurtma, tolov_usuli):
        self.buyurtma = buyurtma
        self.tolov_usuli = tolov_usuli
        self.status = "To'lanmagan"

    def tolov_qilish(self):
        self.status = "To'landi"

    def to_dict(self):
        return {
            "buyurtma": self.buyurtma.to_dict(),
            "tolov_usuli": self.tolov_usuli,
            "status": self.status,
        }

    def __str__(self):
        return f"Buyurtma: {self.buyurtma.mijoz.ism}, To'lov usuli: {self.tolov_usuli}, Holat: {self.status}"


ajratish()
print("Rent Car - Avtomobil ijaraga olish ")
ajratish()

ism = input("Ismingizni kirting >>> ")
telefon = input("Telefon raqamingizni kiriting >>> ")
mijoz = Mijoz(ism, telefon)

mashina_tanlov = input("Qanday mashinani ijaraga olmoqchisz? (Malibu/Gentra/Kia): ").lower()
if mashina_tanlov == "malibu":
    transport = Malibu("Chevrolet", "Malibu 2", 2020, 500_000)
elif mashina_tanlov == "gentra":
    transport = Gentra("Chevrolet", "Gentra", 2022, 400_000)
elif mashina_tanlov == "kia":
    transport = Kia("Kia", "K5", 2021, 600_000)
else:
    print(f"Bizda {mashina_tanlov} rusumli mashina yoq.  Dasturdan chiqdingiz !!!")
    exit()

start_date = datetime.strptime(input("Ijara boshlanish sanasi (YYYY-MM-DD): "), "%Y-%m-%d")
end_date = datetime.strptime(input("Ijara tugash sanasi (YYYY-MM-DD): "), "%Y-%m-%d")

haydovchi = ""
if input("Haydovchi kerakmi ? (ha/yoq): ").lower() == "ha":
    haydovchi = Haydovchi("Sharifjon", 18, 2)

buyurtma = Buyurtma(mijoz, transport, start_date, end_date, haydovchi)

ajratish()
print(buyurtma)
ajratish()

tolov_usuli = input("To‘lov (Naqd/Karta): ").capitalize()
tolov = Tolov(buyurtma, tolov_usuli)
tolov.tolov_qilish()

ajratish()
print(tolov)
ajratish()

with open("rentcar.json", "w", encoding="utf-8") as file:
    json.dump(tolov.to_dict(), file, ensure_ascii=False, indent=4)
