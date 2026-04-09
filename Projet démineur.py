import tkinter as tk
import random

class Case:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_bomb = False
        self.is_revealed = False
        self.is_flagged = False
        self.value = 0


class Grille:
    def __init__(self, rows, cols, num_bombs):
        self.rows = rows
        self.cols = cols
        self.num_bombs = num_bombs
        self.grille = [[Case(r, c) for c in range(cols)] for r in range(rows)]
        self.bombes_placees = False

    def placer_bombes(self, safe_row, safe_col):
        positions_interdites = [
            (safe_row + dr, safe_col + dc)
            for dr in [-1, 0, 1]
            for dc in [-1, 0, 1]
        ]

        bombes = 0
        while bombes < self.num_bombs:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if (r, c) in positions_interdites:
                continue

            case = self.grille[r][c]
            if not case.is_bomb:
                case.is_bomb = True
                bombes += 1

        self.mettre_a_jour_valeurs()
        self.bombes_placees = True

    def mettre_a_jour_valeurs(self):
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        for r in range(self.rows):
            for c in range(self.cols):
                case = self.grille[r][c]

                if case.is_bomb:
                    continue

                count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.grille[nr][nc].is_bomb:
                            count += 1

                case.value = count


class Jeu:
    def __init__(self, root, rows=8, cols=8, bombs=10):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        self.grille = Grille(rows, cols, bombs)
        self.buttons = []
        self.partie_terminee = False

        self.creer_interface()

    def creer_interface(self):
        for r in range(self.rows):
            ligne = []
            for c in range(self.cols):
                btn = tk.Button(self.root, width=3, height=1,
                                command=lambda r=r, c=c: self.clic_gauche(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.clic_droit(r, c))
                btn.grid(row=r, column=c)
                ligne.append(btn)
            self.buttons.append(ligne)

    def clic_gauche(self, row, col):
        if self.partie_terminee:
            return

        if not self.grille.bombes_placees:
            self.grille.placer_bombes(row, col)

        case = self.grille.grille[row][col]

        if case.is_flagged or case.is_revealed:
            return

        self.reveler_case(row, col)
        self.verifier_victoire()

    def clic_droit(self, row, col):
        if self.partie_terminee:
            return

        case = self.grille.grille[row][col]
        if not case.is_revealed:
            case.is_flagged = not case.is_flagged
            self.buttons[row][col]["text"] = "F" if case.is_flagged else ""

    def reveler_case(self, row, col):
        case = self.grille.grille[row][col]
        btn = self.buttons[row][col]

        if case.is_revealed or case.is_flagged:
            return

        case.is_revealed = True

        if case.is_bomb:
            btn.config(text="*", bg="red")
            self.fin_partie(False)
            return

        btn.config(text=str(case.value) if case.value > 0 else "", bg="lightgrey")

        if case.value == 0:
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveler_case(nr, nc)

    def verifier_victoire(self):
        for row in self.grille.grille:
            for case in row:
                if not case.is_bomb and not case.is_revealed:
                    return

        self.fin_partie(True)

    def fin_partie(self, victoire):
        self.partie_terminee = True

        for r in range(self.rows):
            for c in range(self.cols):
                case = self.grille.grille[r][c]
                if case.is_bomb:
                    self.buttons[r][c].config(text="*")

        titre = "Victoire !" if victoire else "Défaite"
        print(titre)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Démineur")
    jeu = Jeu(root, 8, 8, 10)
    root.mainloop()