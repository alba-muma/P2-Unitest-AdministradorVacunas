"""Archivo para llevar a cabo todos los tests que verifican el correcto funcionamiento
de la funcion RF2"""
import os
import json
import hashlib
import unittest
from pathlib import Path
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException


class MyTestCase2(unittest.TestCase):
    """La clase se encarga de realizar los tests que comrpobarán cualquier posible tipo de error"""

    def test1_ok(self):
        """Este test comprueba si la UUID del paciente esta en el archivo json"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_store = json_files_path + "store_patient.json"
        file_store2 = json_files_path + "store_date.json"
        # El condicional elimina el contenido del archivo JSON
        if os.path.isfile(file_store):
            os.remove(file_store)
        if os.path.isfile(file_store2):
            os.remove(file_store2)
        # Añade el paciente
        my_request = VaccineManager()
        my_request.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Juan Perez HerreroBlanquitou",
                                          "regular", "123456789", "22")

        # Comprueba la funcion get_vaccine_date
        file_test = json_files_path2 + "test1_ok.json"
        value = my_request.get_vaccine_date(file_test)
        self.assertEqual(value, "9aef3ed45f107e0fce79625450a1ae66e2524b59c89a99f9407d4c073ffbfb3e")

        # Verifica que el paciente ha sido introducido correctamente
        with open(file_store2, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for cita in data_list:
            identificador = "9aef3ed45f107e0fce79625450a1ae66e2524b59c89a99f9407d4c073ffbfb3e"
            if identificador in cita["_VaccinationAppoinment__date_signature"]:
                found = True
        self.assertTrue(found)

    def test_2_not_ok(self):
        """El fichero json esta vacio"""
        # Se generan 3 archivos json, uno para los pacientes, uno para las citas y otro
        # para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test2_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo y
        # verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests y
            # asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no ha sido
        # modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test3_not_ok(self):
        """La información del usuario se encuentra duplicada"""
        # Se generan 3 archivos json, uno para los pacientes, uno para
        # las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test3_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no ha
        # sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test4_not_ok(self):
        """El corchete inicial esta duplicado"""
        # Se generan 3 archivos json, uno para los pacientes,
        # uno para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test4_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no ha
        # sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test5_not_ok(self):
        """El corchete inicial no aparece (ha sido eliminado)"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test5_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los
            # tests y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test6_not_ok(self):
        """El "PatientSystemID" no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test6_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita
        # no ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test7_not_ok(self):
        """El "PatientSystemID" se encuentra repetido"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test7_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita
        # no ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test8_not_ok(self):
        """La coma que separa la informacion no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test8_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los
            # tests y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test9_not_ok(self):
        """La coma que separa la informacion se encuentra duplicada"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test9_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test10_not_ok(self):
        """La informacion del "ContactPhoneNumber" no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test10_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test11_not_ok(self):
        """La informacion del "ContactPhoneNumber" esta duplicada"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test11_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder añadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto",  e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test12_not_ok(self):
        """El corchete final no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test12_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder aÃ±adirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test13_not_ok(self):
        """El corchete final se encuentra duplicado"""
        # Se generan 3 archivos json, uno para los pacientes,
        # uno para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test13_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test14_not_ok(self):
        """En lugar de haber un corchete inicial, hay un parentesis"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test14_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test15_not_ok(self):
        """El str PatientSystemID no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test15_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test16_not_ok(self):
        """El str PatientSystemID esta duplicado"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test16_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder aÃ±adirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test17_not_ok(self):
        """Los primeros dos puntos (:) no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test17_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests y
            # asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test18_not_ok(self):
        """Los primeros dos puntos (:) estan duplicados"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test18_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo y
        # verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests y
            # asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test19_not_ok(self):
        """La ID hexadecimal del usuario no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test19_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test20_not_ok(self):
        """La ID hexadecimal del usuario se encuentra duplicada"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test20_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test21_not_ok(self):
        """En lugar de haber una coma, hay un punto"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test21_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test22_not_ok(self):
        """El str ContactPhoneNumber no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test22_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test23_not_ok(self):
        """El str ContactPhoneNumber se encuentra duplicado"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test23_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests y
            # asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test24_not_ok(self):
        """Los segundos dos puntos(:) no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test24_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test25_not_ok(self):
        """Los segundos dos puntos(:) estan duplicados"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test25_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder aÃ±adirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no ha
        # sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test26_not_ok(self):
        """El numero de telefono y sus comillas no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test26_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test27_not_ok(self):
        """El numero de telefono y sus comillas se encuentran repetidos"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test27_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test28_not_ok(self):
        """En lugar de un corchete final, hay un parentesis"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test28_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests y
            # asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test29_not_ok(self):
        """Las comillas iniciales de PatientSystemID no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test29_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder aÃ±adirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test30_not_ok(self):
        """Las comillas iniciales de PatientSystemID estan duplicadas"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test30_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test31_not_ok(self):
        """El str PatientSystemID ha sido modificado por IDPatientSystem"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test31_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: las keys del json no tienen el formato correcto",
                         e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test32_not_ok(self):
        """El str PatientSystemID no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test32_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: las keys del json no tienen el formato correcto",
                         e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test33_not_ok(self):
        """El str PatientSystemID se encuentra duplicado"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test33_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo y
        # verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests y
            # asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: las keys del json no tienen el formato correcto",
                         e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test34_not_ok(self):
        """Las comillas finales de PatientSystemID no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test34_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test35_not_ok(self):
        """Las comillas finales de PatientSystemID estan duplicadas"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test35_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo y
        # verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test36_not_ok(self):
        """En lugar de dos puntos(:) hay un guion(-)"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test36_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test37_not_ok(self):
        """Las comillas iniciales de la ID hexadecimal no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test37_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test38_not_ok(self):
        """Las comillas iniciales de la ID hexadecimal estan duplicadas"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test38_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test39_not_ok(self):
        """La ID hexadecimal no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test39_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el md5 no tiene 32 caracteres", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test40_not_ok(self):
        """La ID hexadecimal ha sido duplicada"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test40_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el md5 no tiene 32 caracteres", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test41_not_ok(self):
        """Las comillas finales de la ID hexadecimal no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test41_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder aÃ±adirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test42_not_ok(self):
        """Las comillas finales de la ID hexadecimal estan duplicadas"""
        # Se generan 3 archivos json, uno para los pacientes, uno para
        # las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test42_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test43_not_ok(self):
        """Las comillas iniciales del ContactPhoneNumber no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test43_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test44_not_ok(self):
        """Las comillas iniciales del ContactPhoneNumber estan duplicadas"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test44_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder aÃ±adirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test45_not_ok(self):
        """El str ContactPhoneNumber ha sido modificado por NumberContactPhone"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test45_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: las keys del json no tienen el formato correcto",
                         e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test46_not_ok(self):
        """El str ContactPhoneNumber no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test46_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: las keys del json no tienen el formato correcto",
                         e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test47_not_ok(self):
        """El str ContactPhoneNumber aparece duplicado"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test47_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: las keys del json no tienen el formato correcto",
                         e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test48_not_ok(self):
        """Las comillas finales del ContactPhoneNumber no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test48_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test49_not_ok(self):
        """Las comillas finales del ContactPhoneNumber estan duplicadas"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test49_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder aÃ±adirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test50_not_ok(self):
        """Los dos puntos del ContactPhoneNumber han sido modificados por un guion"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test50_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test51_not_ok(self):
        """Las comillas iniciales del numero de telefono no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test51_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test52_not_ok(self):
        """Las comillas iniciales del numero de telefono estan duplicadas"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test52_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test53_not_ok(self):
        """El numero de telefono no aparece"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test53_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el numero de telefono no tiene 9 digitos", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test54_not_ok(self):
        """El numero de telefono se encuentra duplicado"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test54_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el numero de telefono no tiene 9 digitos", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test55_not_ok(self):
        """Las comillas finales del numero de telefono no aparecen"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test55_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un
        # segundo y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test56_not_ok(self):
        """Las comillas finales del numero de telefono han sido duplicadas"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test56_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test57_not_ok(self):
        """Las comillas iniciales de PatientSystemID han sido modificadas por un asterisco"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test57_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test58_not_ok(self):
        """Las comillas finales de PatientSystemID han sido modificadas por un asterisco"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test58_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test59_not_ok(self):
        """Las comillas iniciales de la ID hexadecimal han sido modificadas por un asterisco"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test59_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test60_not_ok(self):
        """La ID hexadecimal ha sido modificada y se le han añadido dos z"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test60_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el md5 no es un hexadecimal", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test61_not_ok(self):
        """Las comillas finales de la ID hexadecimal han sido modificadas por un asterisco"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test61_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test62_not_ok(self):
        """Las comillas iniciales de ContactPhoneNumber han sido modificadas por un asterisco"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test62_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test63_not_ok(self):
        """Las comillas finales de ContactPhoneNumber han sido modificadas por un asterisco"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test63_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder aÃ±adirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test64_not_ok(self):
        """Las comillas iniciales del numero de telefono han sido modificadas por un asterisco"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test64_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test65_not_ok(self):
        """El numero de telefono ha sido modificado y se le han añadido tres caracteres"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test65_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)

    def test66_not_ok(self):
        """Las comillas finales del numero de telefono han sido modificadas por un asterisco"""
        # Se generan 3 archivos json, uno para los pacientes, uno
        # para las citas y otro para el propio test
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF2/"
        file_test = json_files_path + "test66_not_ok.json"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_date = json_files_path2 + "store_date.json"
        file_patient = json_files_path2 + "store_patient.json"
        # Es necesario crear un paciente para poder anadirlo y verificar el hash
        manager = VaccineManager()
        # Se borra el paciente
        if os.path.isfile(file_patient):
            os.remove(file_patient)
        # Se generan un primer hash para poder compararlo con un segundo
        # y verificar que el archivo no ha sido modificado
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_antes = hashlib.md5(date.__str__().encode()).hexdigest()

        with self.assertRaises(VaccineManagementException) as e:
            # Generamos un paciente, que sera igual para todos los tests
            # y asi facilitar la comprobacion de errores
            manager.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                           "regular", "123456908", "19")
            # Generamos una cita para el paciente creado
            manager.get_vaccine_date(file_test)
        # Se especifica el mensaje que se imprimira por pantalla en caso de error
        self.assertEqual("Error: el formato del JSON es incorrecto", e.exception.message)
        # Se genera el segundo hash necesario para la comprobacion del archivo
        with open(file_date, "r", encoding="utf-8", newline="") as date:
            hash_despues = hashlib.md5(date.__str__().encode()).hexdigest()
        # Comprueba que en un test no valido el fichero de la cita no
        # ha sido modificado verificando que ambos hash son iguales
        self.assertEqual(hash_despues, hash_antes)
