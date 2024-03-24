# -*- coding: utf-8 -*-

import os
import sys, traceback, time
import sqlalchemy as sa

from pymongo import MongoClient

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})

# Crea la conexión con MongoDB
mongo_client = MongoClient()

def getMongoCollection(mongoDB_client):
    mongo_db = mongoDB_client.si1
    return mongo_db.topUK

def mongoDBCloseConnect(mongoDB_client):
    mongoDB_client.close();

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()
   
def delState(state, bFallo, bSQL, seg, bCommit):
    # Array de trazas a mostrar en la página
    dbr = []

    try:
        # Establecer conexión y comenzar transacción
        connection = db_engine.connect()
        if bSQL:
            connection.execute(text("BEGIN"))

        if bFallo:
            # Orden de borrado incorrecto que provocará un fallo
            dbr.append("Intentando borrar registros en un orden que provocará un error")
            # Borra de una tabla que causa restricciones de clave foránea
            connection.execute(text("DELETE FROM public.customers WHERE city = :city"), estado=state)

        else:
            # Orden de borrado correcto
            dbr.append("Borrando registros de forma segura")
            connection.execute(text("DELETE FROM public.customers WHERE ciudad = :ciudad"), estado=state)

        # Suspender ejecución si se especifica
        if seg > 0:
            dbr.append(f"Suspendiendo ejecución por {seg} segundos")
            time.sleep(seg)

        # Commit intermedio
        if bCommit:
            dbr.append("Realizando commit intermedio")
            if bSQL:
                connection.execute(text("COMMIT"))
                connection.execute(text("BEGIN"))
            else:
                transaction.commit()
                transaction = connection.begin()

        # Confirmar cambios si todo va bien
        if bSQL:
            connection.execute(text("COMMIT"))
        else:
            transaction.commit()
        dbr.append("Borrado exitoso")

    except Exception as e:
        # Manejar errores y realizar rollback
        if bSQL:
            connection.execute(text("ROLLBACK"))
        else:
            transaction.rollback()
        dbr.append(f"Error: {str(e)}")
        return dbr

    finally:
        connection.close()

    return dbr

def delCity(city, bFallo, bSQL, seg, bCommit):
    dbr=[] # Array para guardar trazas

    dbr.append(f"Running function delCity with arguements: city = {city}, bFallo = {bFallo}, bSQL = {bSQL}, seg = {seg}, bCommit = {bCommit}")
    query_orderdetail = """
    WITH city_orders AS (
        SELECT o.orderid
        FROM orders o JOIN customers c ON c.customerid = o.customerid
        WHERE c.city = :city
    )

    DELETE 
    FROM orderdetail
    WHERE orderid IN (SELECT orderid FROM city_orders);
    """

    query_orders = """
    WITH city_customers AS (
        SELECT customerid 
        FROM customers 
        WHERE city = :city
    )
    
    DELETE 
    FROM orders
    WHERE customerid IN (SELECT customerid FROM city_customers);
    """

    query_customers = """
    DELETE 
    FROM customers
    WHERE city = :city;
    """
# Establece la conexión y comienza la transacción
    with db_engine.connect() as connection:
        
        # With SQL
        if bSQL:
            connection.execute(sa.text("BEGIN TRANSACTION;"))
            dbr.append("La transaccion ha comenzado")
            
            try:
                if bFallo:
                    # Orden de borrado incorrecto que provocará un fallo
                    dbr.append("Intentando borrar registros en un orden que provocará un error...")
                    connection.execute(sa.text(query_customers), {"city":city})

                    if bCommit: connection.execute(sa.text("COMMIT;")); dbr.append("Eliminacion de customers confirmada")
                    else : dbr.append("Customers eliminado")

                    connection.execute(sa.text(query_orders), {"city":city})

                    if bCommit: connection.execute(sa.text("COMMIT;")); dbr.append("Eliminacion de orders confirmada")
                    else : dbr.append("Orders eliminado")

                    connection.execute(sa.text(query_orderdetail), {"city":city})

                    if bCommit: dbr.append("Eliminacion de orderdetail confirmada")
                    else : dbr.append("Orderdetail eliminado")
                else:
                    connection.execute(sa.text(query_orderdetail), {"city":city})

                    if bCommit: connection.execute(sa.text("COMMIT;")); dbr.append("Orderdetail deletion commited")
                    else: dbr.append("Orderdetail eliminado")
                    
                    connection.execute(sa.text(query_orders), {"city":city})

                    if bCommit: connection.execute(sa.text("COMMIT;")); dbr.append("Eliminacion de orders confirmada")
                    else: dbr.append("Orders eliminado")
    
                    connection.execute(sa.text(query_customers), {"city":city})

                    if bCommit: dbr.append("Eliminacion de customers confirmada") 
                    else: dbr.append("Customers eliminado")
                    
                    
            except Exception as e:
                dbr.append(f"Error ejecutando consultas: {e}")
                connection.execute(sa.text("ROLLBACK;"))
                dbr.append("SQL rollback completado")

            else:
                time.sleep(seg)
                connection.execute(sa.text("COMMIT;"))
                dbr.append("SQL commit completado")

        else:
            transaction = connection.begin()
            dbr.append("Transaccion con funciones SQLALchemy")
            try:
                if bFallo:
                    dbr.append("Intentando borrar registros en un orden que provocará un error...")
                    connection.execute(sa.text(query_customers), {"city":city})
                    
                    if bCommit: connection.execute(sa.text("COMMIT;")); dbr.append("Eliminacion de customers confirmada")
                    else : dbr.append("Customers eliminado")

                    connection.execute(sa.text(query_orders), {"city":city})

                    if bCommit: connection.execute(sa.text("COMMIT;")); dbr.append("Eliminacion de orders confirmada")
                    else : dbr.append("Orders eliminado")

                    connection.execute(sa.text(query_orderdetail), {"city":city})

                    if bCommit: dbr.append("Eliminacion de orderdetail confirmada")
                    else : dbr.append("Orderdetail eliminado")
                else:
                    # Successful path
                    connection.execute(sa.text(query_orderdetail), {"city":city})

                    if bCommit: connection.execute(sa.text("COMMIT;")); dbr.append("Orderdetail deletion commited")
                    else: dbr.append("Orderdetail eliminado")
                    
                    connection.execute(sa.text(query_orders), {"city":city})

                    if bCommit: connection.execute(sa.text("COMMIT;")); dbr.append("Eliminacion de orders confirmada")
                    else: dbr.append("Orders eliminado")
    
                    connection.execute(sa.text(query_customers), {"city":city})

                    if bCommit: dbr.append("Eliminacion de customers confirmada") 
                    else: dbr.append("Customers eliminado")
                
            except Exception as e:
                dbr.append(f"Error ejecutando consultas: {e}")
                transaction.rollback()

                dbr.append("SQLAlchemy rollback completado")
            else:
                time.sleep(seg)
                transaction.commit()
                
                dbr.append("SQLAlchemy commit completado")

    dbr.append("Proceso completado")    

    return dbr
