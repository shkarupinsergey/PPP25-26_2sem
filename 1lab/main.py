from abc import ABC, abstractmethod

class Hod:
    def __init__(self, otkuda, kuda, figura, sbitaya=None, perviy_hod=False,
                 prohod=False, kletka_sbitiya=None, staraya_ep=None,
                 prevrashenie=False, staraya_figura=None, novaya_figura=None):
        self.otkuda = otkuda
        self.kuda = kuda
        self.figura = figura
        self.sbitaya = sbitaya
        self.perviy_hod = perviy_hod
        self.prohod = prohod
        self.kletka_sbitiya = kletka_sbitiya
        self.staraya_ep = staraya_ep
        self.prevrashenie = prevrashenie
        self.staraya_figura = staraya_figura
        self.novaya_figura = novaya_figura

class Figura(ABC):
    def __init__(self, cvet, stroka, stolbec):
        self.cvet = cvet
        self.stroka = stroka
        self.stolbec = stolbec
        self.hodil = False

    @abstractmethod
    def simvol(self):
        pass

    @abstractmethod
    def vozmozhnie_hodi(self, doska):
        pass

    def bukva(self):
        s = self.simvol()
        return s.upper() if self.cvet == "bel" else s.lower()

class Peshka(Figura):
    def simvol(self):
        return "p"

    def vozmozhnie_hodi(self, doska):
        spisok = []
        napr = -1 if self.cvet == "bel" else 1
        start = 6 if self.cvet == "bel" else 1

        ns = self.stroka + napr
        if doska.vnutri(ns, self.stolbec) and doska.poluchit_figuru(ns, self.stolbec) is None:
            spisok.append((ns, self.stolbec))
            ns2 = self.stroka + 2 * napr
            if self.stroka == start and doska.poluchit_figuru(ns2, self.stolbec) is None:
                spisok.append((ns2, self.stolbec))

        for dt in (-1, 1):
            ns, nt = self.stroka + napr, self.stolbec + dt
            if doska.vnutri(ns, nt):
                f = doska.poluchit_figuru(ns, nt)
                if f is not None and f.cvet != self.cvet:
                    spisok.append((ns, nt))

        if doska.en_passant is not None:
            ep_s, ep_t = doska.en_passant
            if ep_s == self.stroka + napr and abs(ep_t - self.stolbec) == 1:
                spisok.append((ep_s, ep_t))

        return spisok

class Ladya(Figura):
    def simvol(self):
        return "l"

    def vozmozhnie_hodi(self, doska):
        return doska.luchevie_hodi(self, [(-1, 0), (1, 0), (0, -1), (0, 1)])

class Kon(Figura):
    def simvol(self):
        return "k"

    def vozmozhnie_hodi(self, doska):
        spisok = []
        for ds, dt in [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]:
            ns, nt = self.stroka + ds, self.stolbec + dt
            if doska.vnutri(ns, nt):
                f = doska.poluchit_figuru(ns, nt)
                if f is None or f.cvet != self.cvet:
                    spisok.append((ns, nt))
        return spisok

class Slon(Figura):
    def simvol(self):
        return "s"

    def vozmozhnie_hodi(self, doska):
        return doska.luchevie_hodi(self, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

class Ferz(Figura):
    def simvol(self):
        return "f"

    def vozmozhnie_hodi(self, doska):
        return doska.luchevie_hodi(self, [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)])

class Korol(Figura):
    def simvol(self):
        return "o"

    def vozmozhnie_hodi(self, doska):
        spisok = []
        for ds in (-1, 0, 1):
            for dt in (-1, 0, 1):
                if ds == 0 and dt == 0:
                    continue
                ns, nt = self.stroka + ds, self.stolbec + dt
                if doska.vnutri(ns, nt):
                    f = doska.poluchit_figuru(ns, nt)
                    if f is None or f.cvet != self.cvet:
                        spisok.append((ns, nt))
        return spisok

class Mag(Figura):
    def simvol(self):
        return "m"

    def vozmozhnie_hodi(self, doska):
        spisok = doska.luchevie_hodi(self, [(-1, -1), (-1, 1), (1, -1), (1, 1)])
        for ds, dt in [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]:
            ns, nt = self.stroka + ds, self.stolbec + dt
            if doska.vnutri(ns, nt):
                f = doska.poluchit_figuru(ns, nt)
                if f is None or f.cvet != self.cvet:
                    spisok.append((ns, nt))
        itog = []
        for x in spisok:
            if x not in itog:
                itog.append(x)
        return itog

class Luchnik(Figura):
    def simvol(self):
        return "u"

    def vozmozhnie_hodi(self, doska):
        spisok = []
        for ds, dt in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ns, nt = self.stroka + ds, self.stolbec + dt
            if doska.vnutri(ns, nt):
                f = doska.poluchit_figuru(ns, nt)
                if f is None or f.cvet != self.cvet:
                    spisok.append((ns, nt))
        for ds, dt in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            ns, nt = self.stroka + ds, self.stolbec + dt
            if doska.vnutri(ns, nt):
                f = doska.poluchit_figuru(ns, nt)
                if f is not None and f.cvet != self.cvet:
                    spisok.append((ns, nt))
        return spisok

class Verblyud(Figura):
    def simvol(self):
        return "v"

    def vozmozhnie_hodi(self, doska):
        spisok = []
        for ds, dt in [(-3, -1), (-3, 1), (3, -1), (3, 1), (-1, -3), (-1, 3), (1, -3), (1, 3)]:
            ns, nt = self.stroka + ds, self.stolbec + dt
            if doska.vnutri(ns, nt):
                f = doska.poluchit_figuru(ns, nt)
                if f is None or f.cvet != self.cvet:
                    spisok.append((ns, nt))
        return spisok

class Doska:
    def __init__(self):
        self.pole = [[None for _ in range(8)] for _ in range(8)]
        self.istoriya = []
        self.en_passant = None

    def vnutri(self, stroka, stolbec):
        return 0 <= stroka < 8 and 0 <= stolbec < 8

    def postavit(self, figura):
        self.pole[figura.stroka][figura.stolbec] = figura

    def ubrat(self, stroka, stolbec):
        self.pole[stroka][stolbec] = None

    def poluchit_figuru(self, stroka, stolbec):
        return self.pole[stroka][stolbec]

    def luchevie_hodi(self, figura, napravleniya):
        spisok = []
        for ds, dt in napravleniya:
            ns, nt = figura.stroka + ds, figura.stolbec + dt
            while self.vnutri(ns, nt):
                drugaya = self.poluchit_figuru(ns, nt)
                if drugaya is None:
                    spisok.append((ns, nt))
                else:
                    if drugaya.cvet != figura.cvet:
                        spisok.append((ns, nt))
                    break
                ns += ds
                nt += dt
        return spisok

    def standartnaya_rasstanovka(self):
        figuri = [Ladya, Kon, Slon, Ferz, Korol, Slon, Kon, Ladya]
        for i in range(8):
            self.postavit(figuri[i]("chern", 0, i))
            self.postavit(Peshka("chern", 1, i))
            self.postavit(Peshka("bel", 6, i))
            self.postavit(figuri[i]("bel", 7, i))

    def variant_s_novimi_figurami(self):
        self.standartnaya_rasstanovka()
        for s, t in [(7, 1), (0, 1), (7, 6), (0, 6), (7, 2), (0, 2)]:
            self.ubrat(s, t)
        self.postavit(Mag("bel", 7, 1))
        self.postavit(Mag("chern", 0, 1))
        self.postavit(Verblyud("bel", 7, 6))
        self.postavit(Verblyud("chern", 0, 6))
        self.postavit(Luchnik("bel", 7, 2))
        self.postavit(Luchnik("chern", 0, 2))

    def nayti_korolya(self, cvet):
        for s in range(8):
            for t in range(8):
                f = self.pole[s][t]
                if f is not None and isinstance(f, Korol) and f.cvet == cvet:
                    return f
        return None

    def vse_figuri(self, cvet=None):
        spisok = []
        for ryad in self.pole:
            for f in ryad:
                if f is not None and (cvet is None or f.cvet == cvet):
                    spisok.append(f)
        return spisok

    def kletka_pod_udarom(self, stroka, stolbec, cvet_atakuyushego):
        for f in self.vse_figuri(cvet_atakuyushego):
            if isinstance(f, Peshka):
                napr = -1 if f.cvet == "bel" else 1
                for dt in (-1, 1):
                    ns, nt = f.stroka + napr, f.stolbec + dt
                    if self.vnutri(ns, nt) and ns == stroka and nt == stolbec:
                        return True
            else:
                if (stroka, stolbec) in f.vozmozhnie_hodi(self):
                    return True
        return False

    def shah(self, cvet):
        korol = self.nayti_korolya(cvet)
        if korol is None:
            return False
        vrag = "chern" if cvet == "bel" else "bel"
        return self.kletka_pod_udarom(korol.stroka, korol.stolbec, vrag)

    def kopiya(self):
        novaya = Doska()
        novaya.en_passant = self.en_passant
        klassi = {
            Peshka: Peshka, Ladya: Ladya, Kon: Kon, Slon: Slon,
            Ferz: Ferz, Korol: Korol, Mag: Mag, Luchnik: Luchnik, Verblyud: Verblyud
        }
        for s in range(8):
            for t in range(8):
                f = self.pole[s][t]
                if f is not None:
                    nf = klassi[type(f)](f.cvet, f.stroka, f.stolbec)
                    nf.hodil = f.hodil
                    novaya.postavit(nf)
        return novaya

    def bezopasniy_hod(self, figura, kuda_s, kuda_t):
        proba = self.kopiya()
        figura2 = proba.poluchit_figuru(figura.stroka, figura.stolbec)
        proba.sdelat_hod(figura2.stroka, figura2.stolbec, kuda_s, kuda_t, False)
        return not proba.shah(figura2.cvet)

    def zakonnie_hodi(self, figura):
        return [(s, t) for s, t in figura.vozmozhnie_hodi(self) if self.bezopasniy_hod(figura, s, t)]

    def sdelat_hod(self, ot_s, ot_t, k_s, k_t, zapis=True):
        figura = self.poluchit_figuru(ot_s, ot_t)
        sbitaya = self.poluchit_figuru(k_s, k_t)

        hod = Hod((ot_s, ot_t), (k_s, k_t), figura, sbitaya, figura.hodil, False, None, self.en_passant)

        if isinstance(figura, Peshka) and self.en_passant == (k_s, k_t) and sbitaya is None:
            hod.prohod = True
            hod.kletka_sbitiya = (ot_s, k_t)
            hod.sbitaya = self.poluchit_figuru(ot_s, k_t)
            self.ubrat(ot_s, k_t)

        self.ubrat(ot_s, ot_t)
        if sbitaya is not None:
            self.ubrat(k_s, k_t)

        figura.stroka, figura.stolbec = k_s, k_t
        self.postavit(figura)

        self.en_passant = None
        if isinstance(figura, Peshka) and abs(k_s - ot_s) == 2:
            self.en_passant = ((k_s + ot_s) // 2, k_t)

        figura.hodil = True

        if isinstance(figura, Peshka) and ((figura.cvet == "bel" and k_s == 0) or (figura.cvet == "chern" and k_s == 7)):
            novaya = Ferz(figura.cvet, k_s, k_t)
            novaya.hodil = True
            hod.prevrashenie = True
            hod.staraya_figura = figura
            hod.novaya_figura = novaya
            self.postavit(novaya)

        if zapis:
            self.istoriya.append(hod)

    def otmenit_hod(self):
        if not self.istoriya:
            print("Нет ходов для отмены")
            return

        hod = self.istoriya.pop()
        self.en_passant = hod.staraya_ep

        figura = hod.staraya_figura if hod.prevrashenie else self.poluchit_figuru(hod.kuda[0], hod.kuda[1])

        self.ubrat(hod.kuda[0], hod.kuda[1])
        figura.stroka, figura.stolbec = hod.otkuda
        figura.hodil = hod.perviy_hod
        self.postavit(figura)

        if hod.prohod and hod.sbitaya is not None:
            hod.sbitaya.stroka, hod.sbitaya.stolbec = hod.kletka_sbitiya
            self.postavit(hod.sbitaya)
        elif hod.sbitaya is not None:
            hod.sbitaya.stroka, hod.sbitaya.stolbec = hod.kuda
            self.postavit(hod.sbitaya)

    def est_hodi(self, cvet):
        for f in self.vse_figuri(cvet):
            if self.zakonnie_hodi(f):
                return True
        return False

    def figuri_pod_ugrozoy(self, cvet):
        vrag = "chern" if cvet == "bel" else "bel"
        return [f for f in self.vse_figuri(cvet) if self.kletka_pod_udarom(f.stroka, f.stolbec, vrag)]

    def pokazat(self):
        pod_bel = {(f.stroka, f.stolbec) for f in self.figuri_pod_ugrozoy("bel")}
        pod_chern = {(f.stroka, f.stolbec) for f in self.figuri_pod_ugrozoy("chern")}

        print("   a  b  c  d  e  f  g  h")
        print("  ------------------------")
        for s in range(8):
            txt = str(8 - s) + "|"
            for t in range(8):
                f = self.pole[s][t]
                znak = "." if f is None else f.bukva()
                txt += ("!" if (s, t) in pod_bel or (s, t) in pod_chern else " ") + znak
            txt += "|" + str(8 - s)
            print(txt)
        print("  ------------------------")
        print("   a  b  c  d  e  f  g  h")

    def pokazat_hodi_figuri(self, stroka, stolbec):
        figura = self.poluchit_figuru(stroka, stolbec)
        if figura is None:
            print("На этой клетке нет фигуры")
            return
        hodi = self.zakonnie_hodi(figura)
        if not hodi:
            print("У фигуры нет доступных ходов")
            return
        print("Доступные ходы:")
        print(", ".join(self.v_notaciyu(s, t) for s, t in hodi))

    def v_notaciyu(self, stroka, stolbec):
        return chr(ord("a") + stolbec) + str(8 - stroka)

    def iz_notacii(self, tekst):
        tekst = tekst.strip().lower()
        return 8 - int(tekst[1]), ord(tekst[0]) - ord("a")

class Igra:
    def __init__(self, s_novimi=True):
        self.doska = Doska()
        if s_novimi:
            self.doska.variant_s_novimi_figurami()
        else:
            self.doska.standartnaya_rasstanovka()
        self.tekushiy = "bel"

    def pomenyat_hod(self):
        self.tekushiy = "chern" if self.tekushiy == "bel" else "bel"

    def nazvanie_cveta(self):
        return "белые" if self.tekushiy == "bel" else "черные"

    def status(self):
        if self.doska.shah(self.tekushiy):
            print("Шах королю")
        opasnie = self.doska.figuri_pod_ugrozoy(self.tekushiy)
        if opasnie:
            print("Под боем:", ", ".join(type(f).__name__ + "(" + self.doska.v_notaciyu(f.stroka, f.stolbec) + ")" for f in opasnie))

    def sdelat_hod_igroka(self, otkuda, kuda):
        ot_s, ot_t = self.doska.iz_notacii(otkuda)
        k_s, k_t = self.doska.iz_notacii(kuda)

        figura = self.doska.poluchit_figuru(ot_s, ot_t)
        if figura is None:
            print("На этой клетке нет фигуры")
            return False

        if figura.cvet != self.tekushiy:
            print("Сейчас ход другого игрока")
            return False

        if (k_s, k_t) not in self.doska.zakonnie_hodi(figura):
            print("Так ходить нельзя")
            return False

        self.doska.sdelat_hod(ot_s, ot_t, k_s, k_t)
        self.pomenyat_hod()

        if self.doska.shah(self.tekushiy):
            print("Поставлен шах")

        if not self.doska.est_hodi(self.tekushiy):
            if self.doska.shah(self.tekushiy):
                print("Мат")
            else:
                print("Пат")
            return "konec"
        return True

    def start(self):
        print("Шахматный симулятор ООП")
        print("Команды:")
        print("move e2 e4")
        print("hint e2")
        print("undo")
        print("exit")

        while True:
            print()
            self.doska.pokazat()
            self.status()
            print("Ход:", self.nazvanie_cveta())
            komanda = input("Введите команду: ").strip().lower()

            if komanda == "exit":
                print("Игра завершена")
                break

            if komanda == "undo":
                self.doska.otmenit_hod()
                self.pomenyat_hod()
                continue

            if komanda.startswith("hint "):
                chast = komanda.split()
                if len(chast) == 2:
                    s, t = self.doska.iz_notacii(chast[1])
                    self.doska.pokazat_hodi_figuri(s, t)
                else:
                    print("Неправильная команда")
                continue

            if komanda.startswith("move "):
                chast = komanda.split()
                if len(chast) == 3:
                    rez = self.sdelat_hod_igroka(chast[1], chast[2])
                    if rez == "konec":
                        self.doska.pokazat()
                        break
                else:
                    print("Неправильная команда")
                continue

            print("Такой команды нет")

igra = Igra(s_novimi=True)
igra.start()
