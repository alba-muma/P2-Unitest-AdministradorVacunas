"""Este archivo sirve para ejecutar los tests relacionados con el registro de la vacuna"""
import os
import json
import unittest
from pathlib import Path
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException


class MyTestCase3(unittest.TestCase):
    """La clase se encarga de realizar los tests que comrpobarán el correcto funcionamiento de vaccine_patient"""
    def test1_ok(self):
        """Test ok donde el archivo json time, no está vacio"""
        # Se crean los path de los archivos que vamos a utilizar
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"
        file_store = json_files_path + "store_patient.json"
        file_time = json_files_path + "store_time.json"
        file_test = json_files_path2 + "test1_ok.json"
        file_date = json_files_path + "store_date.json"

        # Se vacian los archivos, para validar bien el ejemplo
        if os.path.isfile(file_store):
            os.remove(file_store)
        if os.path.isfile(file_time):
            os.remove(file_time)
        if os.path.isfile(file_date):
            os.remove(file_date)
        # Creamos dos pacientes, para que no sea el primero y no cree el archivo el
        paciente1 = VaccineManager()
        paciente1.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e1", "Juan Perez Herrero",
                                         "regular", "123456789", "22")
        cita = paciente1.get_vaccine_date(file_test)
        paciente1.vaccine_patient(cita)
        # Creamos al paciente
        paciente = VaccineManager()
        paciente.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Juan Perez HerreroBlanquitou",
                                        "regular", "123456789", "22")
        # El paciente pide cita para la vacuna
        cita = paciente.get_vaccine_date(file_test)
        # El paciente llega a la cita
        resultado = paciente.vaccine_patient(cita)
        # Se abre el json donde se registra su vacunacion
        with open(file_time, "r", encoding="utf-8", newline="") as horas:
            data_list_dates = json.load(horas)
        # Se comprueba que los datos se han introducido en el archivo correctamente
        found = False
        for hora in data_list_dates:
            if cita == hora["_VaccinationAppoinment__date_signature"]:
                if 1647160055.448724 == hora["_VaccinationAppoinment__appoinment_date"]:
                    found = True
        # Devolvera si se ha introducido bien el registro de la vacuna
        self.assertTrue(found)
        # La funcion tiene que devolver true
        self.assertTrue(resultado)

    def test2_ok(self):
        """Test ok donde el archivo json time, no existe y lo crea"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"
        file_store = json_files_path + "store_patient.json"
        file_time = json_files_path + "store_time.json"
        file_test = json_files_path2 + "test1_ok.json"
        file_date = json_files_path + "store_date.json"

        if os.path.isfile(file_store):
            os.remove(file_store)
        if os.path.isfile(file_time):
            os.remove(file_time)
        if os.path.isfile(file_date):
            os.remove(file_date)
        # Al crear solo un paciente, este será el primero en registrarse, por lo que iniciara el el archivo
        paciente = VaccineManager()
        a= paciente.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Juan Perez HerreroBlanquitou",
                                        "regular", "123456789", "22")
        cita = paciente.get_vaccine_date(file_test)
        resultado = paciente.vaccine_patient(cita)

        with open(file_time, "r", encoding="utf-8", newline="") as horas:
            data_list_dates = json.load(horas)

        found = False
        for hora in data_list_dates:
            if cita == hora["_VaccinationAppoinment__date_signature"]:
                if 1647160055.448724 == hora["_VaccinationAppoinment__appoinment_date"]:
                    found = True
        self.assertTrue(found)
        self.assertTrue(resultado)

    def test3_not_ok(self):
        """Error el sha no tiene 64 caracteres, es decir el parametro que recibe no es valido"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"
        file_store = json_files_path + "store_patient.json"
        file_time = json_files_path + "store_time.json"
        file_test = json_files_path2 + "test1_ok.json"
        file_date = json_files_path + "store_date.json"

        if os.path.isfile(file_store):
            os.remove(file_store)
        if os.path.isfile(file_time):
            os.remove(file_time)
        if os.path.isfile(file_date):
            os.remove(file_date)

        paciente = VaccineManager()
        paciente.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Juan Perez HerreroBlanquitou",
                                        "regular", "123456789", "22")
        # Nombramos al error como e
        with self.assertRaises(VaccineManagementException) as e:
            paciente.get_vaccine_date(file_test)
            # Introducimo un SHA256 no valido (menor longitud)
            paciente.vaccine_patient("76c31d2072a87f50e76f57dc9d1d3164d45b7939529b828899b3cec83f1aa07")

        self.assertEqual(e.exception.message, "Error: el SHA256 no contiene 64 caracteres")

    def test4_not_ok(self):
        """Error el sha no es hexadecial, es decir el parametro que recibe no es valido"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"
        file_store = json_files_path + "store_patient.json"
        file_time = json_files_path + "store_time.json"
        file_test = json_files_path2 + "test1_ok.json"
        file_date = json_files_path + "store_date.json"

        if os.path.isfile(file_store):
            os.remove(file_store)
        if os.path.isfile(file_time):
            os.remove(file_time)
        if os.path.isfile(file_date):
            os.remove(file_date)

        paciente = VaccineManager()
        paciente.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Juan Perez HerreroBlanquitou",
                                        "regular", "123456789", "22")
        with self.assertRaises(VaccineManagementException) as e:
            paciente.get_vaccine_date(file_test)
            # Introducimo un SHA256 no valido (no hexadecimal)
            paciente.vaccine_patient("76c31d2072a87f50e76f57dc9d1d3164d45b7939529b828899b3cec83f1aa07z")

        self.assertEqual(e.exception.message, "Error: el SHA256 no es un hexadecimal")

    def test5_not_ok(self):
        """Test no valido, donde se borra el json de dates antes de llamar a la funcion vaccine patient"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"
        file_store = json_files_path + "store_patient.json"
        file_time = json_files_path + "store_time.json"
        file_test = json_files_path2 + "test1_ok.json"
        file_date = json_files_path + "store_date.json"

        if os.path.isfile(file_store):
            os.remove(file_store)
        if os.path.isfile(file_time):
            os.remove(file_time)
        if os.path.isfile(file_date):
            os.remove(file_date)

        paciente = VaccineManager()
        paciente.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Juan Perez HerreroBlanquitou",
                                        "regular", "123456789", "22")
        with self.assertRaises(VaccineManagementException) as e:
            cita = paciente.get_vaccine_date(file_test)

            # Borramos el archivo para forzar el error
            if os.path.isfile(file_date):
                os.remove(file_date)

            paciente.vaccine_patient(cita)

        self.assertEqual(e.exception.message, "Error: el JSON (store_date) no existe / el path es incorrecto")

    def test6_not_ok(self):
        """Test no valido donde el archivo json dates no esta en un formato correto"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"
        file_store = json_files_path + "store_patient.json"
        file_time = json_files_path + "store_time.json"
        file_test = json_files_path2 + "test1_ok.json"
        file_date = json_files_path + "store_date.json"

        if os.path.isfile(file_store):
            os.remove(file_store)
        if os.path.isfile(file_time):
            os.remove(file_time)
        if os.path.isfile(file_date):
            os.remove(file_date)

        paciente = VaccineManager()
        paciente.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc5411", "Juan Perez Nobita",
                                        "regular", "123456789", "22")
        # En vaccine manager hay un if que si se introduce este sha
        # cambiara la ruta del json a uno con el formato incorrecto
        with self.assertRaises(VaccineManagementException) as e:
            paciente.get_vaccine_date(file_test)
            paciente.vaccine_patient("76c31d2072a87f50e76f57dc9d1d3164d45b7939529b828899b3cec83f1aaabc")

        self.assertEqual(e.exception.message, "Error: el formato del JSON (store_date) es incorrecto")

    def test7_not_ok(self):
        """Test donde el paciente no tiene una cita registrada"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"
        file_store = json_files_path + "store_patient.json"
        file_test = json_files_path2 + "test1_ok.json"
        file_time = json_files_path + "store_time.json"
        file_date = json_files_path + "store_date.json"

        if os.path.isfile(file_store):
            os.remove(file_store)
        if os.path.isfile(file_time):
            os.remove(file_time)
        if os.path.isfile(file_date):
            os.remove(file_date)

        # Añadimos una cita de otro paciente para que el archivo de citas aparezca
        paciente1 = VaccineManager()
        paciente1.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e1", "Juan Perez Herrero",
                                         "regular", "123456789", "22")
        cita = paciente1.get_vaccine_date(file_test)
        paciente1.vaccine_patient(cita)

        paciente = VaccineManager()
        paciente.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Juan Perez HerreroBlanquitou",
                                        "regular", "123456789", "22")
        with self.assertRaises(VaccineManagementException) as e:
            paciente.vaccine_patient("76c31d2072a87f50e76f57dc9d1d3164d45b7939529b828899b3cec83f1aa567")
        self.assertEqual(e.exception.message, "Error: El paciente no tiene una cita registrada")

    def test8_not_ok(self):
        """Test donde el paciente no tiene cita ese dia"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        json_files_path2 = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"
        file_store = json_files_path + "store_patient.json"
        file_time = json_files_path + "store_time.json"
        file_test = json_files_path2 + "test8_not_ok.json"
        file_date = json_files_path + "store_date.json"

        if os.path.isfile(file_store):
            os.remove(file_store)
        if os.path.isfile(file_time):
            os.remove(file_time)
        if os.path.isfile(file_date):
            os.remove(file_date)

        paciente = VaccineManager()
        paciente.request_vaccination_id("bb5dbd61-d8b1-4131-8eb1-dd262cfc5123", "Juan Perez Aguilar",
                                            "regular", "123456712", "11")
        cita = paciente.get_vaccine_date(file_test)
        with self.assertRaises(VaccineManagementException) as e:
            paciente.vaccine_patient(cita)
        self.assertEqual(e.exception.message, "Error: El paciente no tiene ninguna cita hoy")
