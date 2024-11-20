import sqlite3
class User:
    """ Clase que representa un usuario """
    def __init__(self,name = '',password = '',email = '',table_name = ''):
        self.name = name
        self.password = password 
        self.email = email
        self.table_name = table_name

class UserManager:
    """ Clase que actua como un crud para los usuarios """
    def __init__(self,db_path = 'data/Library.sqlite'):
        self.db_path = db_path

    def register_user(self,name,password,email,table):
        """ 
        Registra usuarios en la base de datos
            name(sting): Nombre del usuario
            password(string): Contraseña del usuario
            email(string): Correo del usuario
            table(string): Tipo de usuario(Lector, Bibliotecario, Administrador)
            Return:
                Sting: 'Exito'
        """
        user = User(name,password,email,table)
        # Ayuda a evitar inyecciones sql
        if self._validate_table(table) == False:
            print('Tabla no encontrada')
            return
        # Consulta 
        query = f'''
        INSERT INTO {table} (name, password, email)
        VALUES (?, ?, ?)
        '''
        try:
            con = sqlite3.connect(self.db_path)# Se conecta con la base de datos
            cursor = con.cursor()# Establece un cursor para ejecutar consutlar
            cursor.execute(query,(user.name,user.password,user.email))# Metodo que permite realizar consultas
            con.commit()# Asegura que los datos se guarden de manera permanente
        except ValueError as e:
            print('Error: ', e)
        finally:
            con.close() # Cierra la coneccion con la base de datos
            return 'Exito'

    def delete_user(self,table,column,date_of_column):
        """ 
        Elimina un usario registrado
            table (string): Define el tipo de usario
            column (string): Define el tipo de dato del usuario(nombre,correo,id)
            date_of_column (string): Define el dato del usario('Edier','guerraedier@gmail.com',2)
            Return:
                string: 'Exito'
        """
        if self._validate_table(table) == False:
            print('Tabla no encontrada')
            return
        query = f""" DELETE FROM {table} WHERE {column} = ? """
        try:
            con = sqlite3.connect(self.db_path)# Se conecta con la base de datos
            cursor = con.cursor()# Establece un cursor para ejecutar consutlar
            cursor.execute(query,(date_of_column,))
            con.commit()# Asegura que los datos se guarden de manera permanente
        except ValueError as e:
            print('Error: ', e)
        finally:
            con.close() # Cierra la coneccion con la base de datos
            return 'Exito'

    def update_user(self,table,column,date_of_column,tipe_date,new_date):
        """ 
        Actualiza el dato de un usuario en especifico
            table(string): Representa el tipo de usario
            column(string): Representa el tipo de dato unico(id) del usuario
            date_of_column(string): Es el dato unico del usuario 
            tipe_date(string): Representa el dato que queremos(nombre,correo,etc) actualizar
            new_date(string): Es el nuevo dato 
            Return
                String: 'Exito'
        """
        if self._validate_table(table) == False:
            print('Tabla no encontrada')
            return
        query = f""" UPDATE {table} SET {tipe_date} = ? WHERE {column} = ?; """
        try:
            con = sqlite3.connect(self.db_path)# Se conecta con la base de datos
            cursor = con.cursor()# Establece un cursor para ejecutar consutlar
            cursor.execute(query,(new_date,date_of_column))
            con.commit()# Asegura que los datos se guarden de manera permanente
        except ValueError as e:
            print('Error: ', e)
        finally:
            con.close() # Cierra la coneccion con la base de datos
            return 'Exito'

    def watch_user(self,table,id_reader):
        """  
        Permite visualizar un usario en especifico
            table(string): Tipo de usario
            id_reader(string): Tipo de usuario
            Return
                String: 'Exito'

        """
        if self._validate_table(table) == False:
            print('Tabla no encontrada')
            return
        query = f""" SELECT * FROM {table} WHERE id_reader = ?"""
        try:
            con = sqlite3.connect(self.db_path)# Se conecta con la base de datos
            cursor = con.cursor()# Establece un cursor para ejecutar consutlar
            cursor.execute(query,(id_reader))
            dates = cursor.fetchall()
            con.commit()# Asegura que los datos se guarden de manera permanente
            print(dates)
        except ValueError as e:
            print('Error: ', e)
        finally:
            con.close() # Cierra la coneccion con la base de datos
            return 'Exito'
    def _validate_table(self,table):# Comprueba que la tabla exista
        """ 
        Valida que la tabla exista en la base de datos
            table(string): Representa un tipo de usario
            Return
                Valor Booleano
        """
        tables = ['Reader','Librarian','Admin']
        return table in tables