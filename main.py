import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:root@127.0.0.1:3306/inventario"
                                  "")
Base = declarative_base()

class Inventario(Base):
    __tablename__ = 'inventario'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    articulo = sqlalchemy.Column(sqlalchemy.String(length=100))
    cantidad = sqlalchemy.Column(sqlalchemy.String(length=20))

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def principal():
    Inventario()
    menu = """
1) Agregar nuevo articulo
2) Editar articulo existente
3) Eliminar articulo existente
4) Ver articulos
5) Buscar cantidad de un articulo
6) Salir
Elige: """
    eleccion = ""
    while eleccion != "6":
        eleccion = input(menu)
        if eleccion == "1":
            articulo = input("Ingresa el articulo: ")
            posible_cantidad = buscar_cantidad_articulo(articulo)
            if posible_cantidad:
                print(f"El articulo '{articulo}' ya existe")
            else:
                cantidad = input("Ingresa la cantidad: ")
                agregar_articulo(articulo, cantidad)
                print("Articulo agregado")
        if eleccion == "2":
            articulo = input("Ingresa el articulo que quieres editar: ")
            nueva_cantidad = input("Ingresa la nueva cantidad: ")
            editar_articulo(articulo, nueva_cantidad)
            print("Articulo actualizado")
        if eleccion == "3":
            articulo = input("Ingresa el articulo a eliminar: ")
            eliminar_articulo(articulo)
        if eleccion == "4":
            print("=== Lista de articulos ===")
            articulos = obtener_articulos()

        if eleccion == "5":
            articulo = input(
                "Ingresa el articulo del cual quieres saber la cantidad: ")
            cantidad = buscar_cantidad_articulo(articulo)




def agregar_articulo(articulo, cantidad):
    nuevoArticulo = Inventario(articulo=articulo, cantidad =cantidad)
    session.add(nuevoArticulo)
    session.commit()

def editar_articulo(articulo, nueva_cantidad):
    session.query(Inventario).filter(Inventario.articulo == articulo).delete()
    session.commit()
    nuevoArticulo = Inventario(articulo=articulo, cantidad=nueva_cantidad)
    session.add(nuevoArticulo)
    session.commit()

def eliminar_articulo(articulo):
    session.query(Inventario).filter(Inventario.articulo == articulo).delete()
    session.commit()

def obtener_articulos():
    articulos = session.query(Inventario).all()
    for articulo in articulos:
        print(articulo.articulo)

def buscar_cantidad_articulo(articulo):
    articulo = session.query(Inventario).filter_by(articulo=articulo)
    for articulo in articulo:
        print(" - " + articulo.articulo + ': ')
        print(articulo.cantidad)

if __name__ == '__main__':
    principal()