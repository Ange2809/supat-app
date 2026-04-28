import flet as ft
import psycopg2
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os

# ================= POSTGRES CONFIG =================
DB_CONFIG = {
    "dbname": "supat",
    "user": "supat_user",
    "password": "supat123",
    "host": "localhost",
    "port": "5432"
}

ADMIN = "admin"
PWD = "1234"

# ===== BACKGROUNDS =====
BG = "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1600&q=80"
BG_ADMIN = "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=1600&q=80"
BG_ANALYSE = "https://images.unsplash.com/photo-1579154204601-01588f351e67?auto=format&fit=crop&w=1600&q=80"


# ================= DB =================
def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    with get_conn() as c:
        cur = c.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS patients(
            id SERIAL PRIMARY KEY,
            nom TEXT,
            age INTEGER,
            sexe TEXT,
            adresse TEXT,
            email TEXT,
            telephone TEXT,
            maladie TEXT,
            created_at TEXT
        )
        """)
        c.commit()


def is_number(v):
    return v.isdigit()


# ================= ANALYSE =================
def generate_analysis():
    with get_conn() as c:
        df = pd.read_sql_query("SELECT * FROM patients", c)

    if df.empty:
        return None, None

    sexe = df["sexe"].value_counts()
    plt.figure()
    plt.pie(sexe, labels=sexe.index, autopct="%1.1f%%")
    plt.title("Répartition Sexe")
    plt.savefig("sexe.png")
    plt.close()

    mal = df["maladie"].value_counts()
    plt.figure()
    plt.bar(mal.index, mal.values)
    plt.xticks(rotation=30)
    plt.title("Maladies")
    plt.savefig("maladie.png")
    plt.close()

    return df, mal


# ================= APP =================
def main(page: ft.Page):
    page.assets_dir = "assets"
    init_db()
    page.title = "SUPAT HOSPITAL PRO"
    page.scroll = "auto"

    def bg(image_url, content, overlay="#00000080"):
        return ft.Stack([
            ft.Image(src=image_url, fit="cover", expand=True),
            ft.Container(expand=True, bgcolor=overlay),
            ft.Container(content, expand=True, padding=20),
        ])

    def card(content):
        return ft.Container(
            content=content,
            bgcolor="white",
            padding=20,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=20, color="black26")
        )

    # ================= HOME =================
    def home(e=None):
        page.controls.clear()
        page.add(bg(BG,
            ft.Column(
                alignment="center",
                horizontal_alignment="center",
                expand=True,
                controls=[

                    ft.Image(
                        src="SupaT.png",
                        width=120,
                        height=120,
                        fit="cover"
                    ),
                    ft.Text("Bienvenue sur SUPAT!🏥",
                            size=16, color="white"),
                    ft.Text("La plateforme ideale pour un recensement et une analyse descriptive des donnees dans le cadre médical.🏥",
                            size=16, color="white"),

                    ft.Container(height=20),

                    ft.Button("🔐 LOGIN PATIENT", on_click=form),
                    ft.Button("📊 ANALYSE", on_click=analyser),
                    ft.Button("🧑‍💼 ADMIN", on_click=admin_login),
                ]
            )
        ))
        page.update()

    # ================= FORM =================
    def form(e=None):
        page.controls.clear()

        nom = ft.TextField(label="Nom")
        age = ft.TextField(label="Age")
        sexe = ft.Dropdown(options=[
            ft.dropdown.Option("Homme"),
            ft.dropdown.Option("Femme")
        ])
        adresse = ft.TextField(label="Adresse")
        email = ft.TextField(label="Email")
        tel = ft.TextField(label="Téléphone")
        mal = ft.TextField(label="Maladie")

        msg = ft.Text(color="red")

        def save(e):
            if not is_number(age.value) or not is_number(tel.value):
                msg.value = "⚠️ Age et téléphone doivent être numériques"
                page.update()
                return

            with get_conn() as c:
                cur = c.cursor()
                cur.execute("""
                INSERT INTO patients
                (nom, age, sexe, adresse, email, telephone, maladie, created_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    nom.value,
                    int(age.value),
                    sexe.value,
                    adresse.value,
                    email.value,
                    tel.value,
                    mal.value,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                c.commit()

            page.controls.clear()
            page.add(bg(BG,
                ft.Column([
                    ft.Text("✅ Patient enregistré", color="white", size=22),
                    ft.Button("🏠 Retour", on_click=home)
                ])
            ))
            page.update()

        page.add(bg(BG,
            ft.Column([
                ft.Button("⬅ Retour", on_click=home),
                card(ft.Column([
                    nom, age, sexe,
                    adresse, email, tel,
                    mal,
                    ft.Button("Enregistrer", on_click=save),
                    msg
                ]))
            ])
        ))
        page.update()

    # ================= ANALYSE =================
    def analyser(e=None):
        page.controls.clear()

        df, mal = generate_analysis()

        if df is None:
            page.add(bg(BG, ft.Text("Aucune donnée", color="white")))
            return

        page.add(bg(BG_ANALYSE,
            ft.Column([
                ft.Button("⬅ Retour", on_click=home),
                ft.Text("📊 Analyse médicale", color="white", size=22),
                ft.Row([
                    ft.Image(src="sexe.png", width=350),
                    ft.Image(src="maladie.png", width=350),
                ])
            ])
        ))
        page.update()

    # ================= ADMIN =================
    def admin_login(e=None):
        page.controls.clear()

        user = ft.TextField(label="Admin")
        pwd = ft.TextField(label="Password", password=True)
        msg = ft.Text(color="red")

        def login(e):
            if user.value == ADMIN and pwd.value == PWD:
                admin_dashboard()
            else:
                msg.value = "❌ Accès refusé"
                page.update()

        page.add(bg(BG_ADMIN,
            ft.Column([
                ft.Text("LOGIN ADMIN", color="white"),
                user, pwd,
                ft.Button("Connexion", on_click=login),
                msg,
                ft.Button("⬅ Retour", on_click=home),
            ])
        ))
        page.update()

    # ================= DASHBOARD =================
    def admin_dashboard():
        page.controls.clear()

        with get_conn() as c:
            cur = c.cursor()
            cur.execute("SELECT * FROM patients")
            rows = cur.fetchall()

        total = len(rows)
        hommes = len([r for r in rows if r[3] == "Homme"])
        femmes = len([r for r in rows if r[3] == "Femme"])

        maladies = {}
        for r in rows:
            m = r[7]
            maladies[m] = maladies.get(m, 0) + 1

        stats = ft.Column([
            ft.Text("📊 STATISTIQUES", size=18, weight="bold", color="black"),
            ft.Divider(),

            ft.Container(ft.Text(f"👥 Total patients : {total}", color="white"),
                         bgcolor="#1565C0", padding=10, border_radius=10),

            ft.Container(ft.Text(f"👨 Hommes : {hommes}", color="white"),
                         bgcolor="#2E7D32", padding=10, border_radius=10),

            ft.Container(ft.Text(f"👩 Femmes : {femmes}", color="white"),
                         bgcolor="#C2185B", padding=10, border_radius=10),

            ft.Divider(),
            ft.Text("🦠 Par maladie :", weight="bold"),

            *[
                ft.Container(
                    ft.Text(f"{k} : {v}", color="white"),
                    bgcolor="#424242",
                    padding=8,
                    border_radius=8
                )
                for k, v in maladies.items()
            ]
        ])

        table_rows = []
        for r in rows:
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(r[1])),
                    ft.DataCell(ft.Text(str(r[2]))),
                    ft.DataCell(ft.Text(r[3])),
                    ft.DataCell(ft.Text(r[4])),
                    ft.DataCell(ft.Text(r[5])),
                    ft.DataCell(ft.Text(r[6])),
                    ft.DataCell(ft.Text(r[7])),
                    ft.DataCell(ft.Text(r[8])),
                ])
            )

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nom")),
                ft.DataColumn(ft.Text("Age")),
                ft.DataColumn(ft.Text("Sexe")),
                ft.DataColumn(ft.Text("Adresse")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Téléphone")),
                ft.DataColumn(ft.Text("Maladie")),
                ft.DataColumn(ft.Text("Date")),
            ],
            rows=table_rows
        )

        page.add(bg(BG_ADMIN,
            ft.Column([
                ft.Row([
                    ft.Button("🏠 Accueil", on_click=home),
                    ft.Button("🔄 Actualiser", on_click=admin_dashboard),
                    ft.Button("➕ Ajouter", on_click=form),
                ]),
                ft.Row([
                    card(stats),
                    card(table)
                ], scroll="auto")
            ])
        ))

        page.update()

    home()
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=8080
    )

ft.app(
    target=main,
    port=int(os.environ.get("PORT", 8080)),
    view=ft.WEB_BROWSER
)