
import pymysql

class db:
    def __init__(x):
        x.connection = None
        x.cursor = None


    def connect(x):
        x.connection = pymysql.connect(
            host ='localhost',
            user ='root',
            password = '',
            db = 'testdatabase'
        )
        
        x.cursor = x.connection.cursor()

        print("<==== Succesfully connected to Database ====>")

    def close_connection(x):
        if x.connection:
            x.connection.close()


    def insert_people(x, id_user, name, last_name):
        try:
            x.cursor.execute("SELECT id_user FROM people WHERE id_user = $s", (id_user,))
            person_exist = x.cursor.fetchone()

            if person_exist:
                print(f"la persona identificada con {id_user} ya existe, intenta con otro ID")
            else:
                x.cursor.execute("INSERT INTO people (id_user, name, last_name) VALUES (%s, %s, %s)",
                (id_user, name, last_name))
                
                x.connection.commit()
                print(f"{name} Ha sido agregado")

        except pymysql.Error as xd:
            print(f"There was an error while trying to insert: {xd}")

    def insert_product(x, id_product, client_name, products_amount):
        try:
            x.cursor.execute(
                "INSERT INTO products (id_product, client_name, products_amount) VALUES (%s, %s, %s)",
                (id_product, client_name, products_amount)
            )
            x.connection.commit()
            print("Product/s added")
        except pymysql.Error as xd:
            print(f"There was an error while trying to insert: {xd}")


database = db()

class users:

    def __init__(x, user, password):
        x.__user = user
        x.__password = password

    def got_user(x):
        return x.__user
    
    def set_pass(x, password):
        x.__password = password

    def log(x, got_pass):
        return x.__password == got_pass
    
    def __str__(x):
        return f'User: {x.__user}'
    
class admin(users):
    def __init__(x, user, password):
        super().__init__(user, password)

    def __str__(x):
        return f'Admin User: {x.got_user}'
    
class people(users):
    def __init__(x, user, password):
        super().__init__(user, password)

    def __str__(x):
        return f'Regular user: {x.got_user}'
    
def print_user_info(username):
    print(username)

if_admin = lambda username: isinstance(username, admin)

administrator = admin("admin", "1234")
classic_user = people("user", "1234")

def loginmenu():
    while True:
        print("1. Login")
        print("2. Exit")
        option = input("Elige una opcion: ")

        if option == "1":
            user = input("User: ")
            password = input("Pass: ")

            if administrator.got_user() == user and administrator.log(password):
                database = connect()
                print("<=== ----- ===>")
                print("inicio de sesion exitoso")
                print("<=== ----- ===>")
                print_user_info(administrator)
                while True:
                    admin_option = input("¿Quieres agregar una persona?? (y/n): ").lower()
                    if admin_option == "y":
                        id_user = input("ID: ")
                        name = input("Nombre: ")
                        last_name = input("Apellido: ")

                        database.insert_people(id_user, name, last_name)
                        print(f"{name} agregado exitosamente")
                    elif admin_option == "n":
                        break
                    else:
                        print("selecciona una opcion valida")
            elif classic_user.got_user() == user and classic_user.log(password):
                database.connect()
                print("<=== ----- ===>")
                print("inicio de sesion exitoso")
                print("<=== ----- ===>")
                print_user_info(classic_user)
                while True:
                    classic_option = input("Quieres agregar un producto? (y/n): ").lower()
                    if classic_option == "y":
                        id_product = input("ID: ")
                        client_name = input("Nombre de Cliente: ")
                        products_amount = input("Cantidad de productos: ")

                        database.insert_product(id_product, client_name, products_amount)
                        print(f"Productos agregados")
                    elif classic_option == "n":
                        break
                database.close()
            else:
                print("Usuario o contraseña incorrectos, intenta otra vez")
        elif option == "2":
            database.close()
            break
        else:
            print("opcion Invalida")

loginmenu()