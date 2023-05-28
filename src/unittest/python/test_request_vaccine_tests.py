"""Este archivo sirve para ejecutar los tests relacionados con la solicitud de la vacuna"""
import unittest
import os
import json
from pathlib import Path
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException


class MyTestCase(unittest.TestCase):
    """La clase se encarga de realizar los tests que comprobaran el correcto funcionamiento de request_vaccination_id"""

    def test_0_request_vaccination_valid(self):
        """En el metodo se crea el archivo JSON y se comprueba que se ha introducido
         el usuario en el propio archivo que previamente ha sido creado"""
        # Se crea un archivo JSON en el directorio especificado
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_store = json_files_path + "store_patient.json"
        # El condicional elimina el contenido del archivo JSON
        if os.path.isfile(file_store):
            os.remove(file_store)
        my_request = VaccineManager ()

        value = my_request.request_vaccination_id("ad7e7fb9-1370-426a-a904-9c782fedc1ee", "Pedro Perez", "regular",
                                                  "611402130", "7")
        # A continuacion, se comprobara si se ha introducido el valor esperado en el archivo
        self.assertEqual(value, "a2990b365e17d06551de6cc2c261ceb9")
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        # Se lleva a cabo un bucle for para buscar que el paciente haya sido introducido en el JSON
        for item in data_list:
            if item["_VaccinePatientRegister__patient_id"] =="ad7e7fb9-1370-426a-a904-9c782fedc1ee":
                found = True
        self.assertTrue(found)

    def test_1_request_vaccination_valid(self):
        """Este test comprueba que el ID del paciente corresponde a un uuid valido"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_store = json_files_path + "store_patient.json"
        if os.path.isfile(file_store):
            os.remove(file_store)
        my_request = VaccineManager()

        value = my_request.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                                                  "Juan Perez HerreroBlanquitou", "regular", "123456789", "125")
        self.assertEqual(value, "07b8f59635dbbaf183f589bc89345b6f")

    def test_2_request_vaccination_not_valid(self):
        """Este test comprueba que el ID del paciente es una uuid, pero de version 1"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as mogu_mogu:
            my_request.request_vaccination_id("bb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0", "Carmen Carrero ",
                                                      "regular", "123456789", "22")
        self.assertEqual("Error: UUID v4 formato invalido", mogu_mogu.exception.message)

    def test_3_request_vaccination_not_valid(self):
        """Este test comprueba que el ID del paciente no corresponde con uuid valido"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("zb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0", "Carmen Carrero",
                                                      "regular", "123456789", "22")
        self.assertEqual("Error: La ID recibida no es una UUID", cm.exception.message)

    def test_4_request_vaccination_not_valid(self):
        """Este test comprueba que el nombre completo del paciente incluye solo el nombre, pero no el apellido"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("3d41310a-9d79-447f-a5bc-0b907500edc9", "Pepe", "regular",
                                                      "987654321", "40")
        self.assertEqual("Error: El nombre recibido esta incompleto", cm.exception.message)

    def test_5_request_vaccination_valid(self):
        """Este test verifica que el nombre completo del paciente esta formado por mas de dos
         cadenas de caracteres y que se acepten nombre de 29 caracteres"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_store = json_files_path + "store_patient.json"
        if os.path.isfile(file_store):
            os.remove(file_store)

        my_request = VaccineManager()
        segundo_paciente = VaccineManager()
        segundo_paciente.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Juan Perez HerreroBlanquitou",
                                                "regular", "123456789", "22")
        value = my_request.request_vaccination_id("508258ad-5295-4fba-bf3e-79dd0d332fb1",
                                                  "Juan Perez HerreroBlanquitous", "regular", "123456780", "124")
        self.assertEqual(value, "f77f70fffc20f29b686e02aef49efb00")

    def test_6_request_vaccination_not_valid(self):
        """Este test comprueba mediante el analisis de valores limite que el nombre completo del paciente supera
        el limite establecido de 30 caracteres"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("f8e7fb26-ed71-47e7-bb02-f1c5165d92d2",
                                                      "Roberto GonzalezMartinezGarcias", "regular", "102345678", "25")
        self.assertEqual("Error: El nombre tiene mas de 30 caracteres", cm.exception.message)


    def test_7_request_vaccination_not_valid(self):
        """Este test comprueba que el numero de telefono del paciente contiene mas de 9 digitos, es decir,
        supera el limite establecido"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("54801c3d-1dc9-4d16-954a-a15615c6b1a3", "Jaime Ramos", "regular",
                                                      "6658951235", "36")
        self.assertEqual("Error: El telefono no tiene 9 digitos", cm.exception.message)


    def test_8_request_vaccination_not_valid(self):
        """Este test verifica que la edad del paciente se encuentra fuera del rango (menor del limite establecido)"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("419e24a9-0e8a-497b-9153-a65c52aaee43", "Andrea Campos",
                                                      "regular", "120345678", "5")
        self.assertEqual("Error: La edad esta fuera de rango", cm.exception.message)


    def test_9_request_vaccination_not_valid(self):
        """Este test verifica que la edad del paciente se encuentra fuera del rango (mayor del limite establecido)"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("2fc3a005-584f-4bb6-b0f7-c72778a9fc22", "Olga Blanco", "regular",
                                                      "123405678", "126")
        self.assertEqual("Error: La edad esta fuera de rango", cm.exception.message)


    def test_10_request_vaccination_not_valid(self):
        """Este test comprueba que el numero de telefono del paciente contiene menos de 9 digitos"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("c4df46eb-9b60-4539-877b-ea32e08aa211", "José María Pulgar",
                                                      "regular", "12345678", "51")
        self.assertEqual("Error: El telefono no tiene 9 digitos", cm.exception.message)


    def test_11_request_vaccination_not_valid(self):
        """Este test verifica que el tipo de registro introducido es family y no hay un ID del paciente registrado que
        corresponda al tutor legal"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("bb85be7c-7bf8-4c8d-bc4b-af84602ca12f", "Zoe Martinez", "family",
                                                      "123456078", "11")
        self.assertEqual("Error: No esta registrado su tutor legal", cm.exception.message)

    def test_12_request_vaccination_valid(self):
        """Este test verifica que el tipo de registro introducido es family y hay un identificator de un paciente ya registrado que corresponde
        al tutor legal"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_store = json_files_path + "store_patient.json"
        if os.path.isfile(file_store):
            os.remove(file_store)

        my_request = VaccineManager()
        padre = VaccineManager()
        hijo2 = VaccineManager()
        padre.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Eva Rubio", "regular", "123456908", "45")
        hijo2.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Laura Ladron", "family", "123456908",
                                     "11")
        value = my_request.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano", "family",
                                                  "123456908", "6")
        self.assertEqual("18d9ad1fbf9bf0a4868e8253ef55fcd8", value)

    def test_13_request_vaccination_not_valid(self):
        """Este test comprueba que el tipo de registro introducido es tanto distinto de family, como de regular"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("37d329ab-d816-4ef3-84f6-f29749f21901", "Rubi Roman", "registro",
                                                      "312456378", "11")
        self.assertEqual("Error: El tipo de registro introducido no es valido", cm.exception.message)


    def test_14_request_vaccination_not_valid(self):
        """Este test comprueba que el nombre completo del paciente contiene un numero y, por tanto, no es valido"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("7a829afa-fa5c-4e2c-98dd-0edf0ff39f9d", "Guiller5o Esteban",
                                                      "regular", "312456797", "23")
        self.assertEqual("Error: El nombre introducido contiene un caracter no valido", cm.exception.message)


    def test_15_request_vaccination_not_valid(self):
        """Este test comprueba que un numero de telefono introducido para un paciente contiene un caracter y, por tanto,
        se detecta que no es valido"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("6719a56d-0e81-4152-8daf-3f4bdb2b5d14", "Belén Pérez-Reverte",
                                                      "regular", "312h53690", "56")
        self.assertEqual("Error: El numero de telefono contiene un caracter no valido", cm.exception.message)


    def test_16_request_vaccination_not_valid(self):
        """Este test verifica que la edad del paciente introducida no es valida, ya que esta escrita con letras en lugar de digitos"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("466a6f9d-3a4b-48c7-9cd4-6ef31d443ed4", "Laura García", "regular",
                                                      "651123456", "once")
        self.assertEqual("Error: La Edad introducida no es un numero", cm.exception.message)


    def test_17_request_vaccination_not_valid(self):
        """Este test comprueba que el valor del ID del paciente no ha sido introducido"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("", "Pedro Rondo", "regular", "611402130", "46")
        self.assertEqual("Error: ID del paciente no se ha especificado", cm.exception.message)


    def test_18_request_vaccination_not_valid(self):
        """Este test comprueba que el tipo de registro no ha sido especificado"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("g7a7fC26-ed71-4fe7-ab02-f1c4163b92h2", "María Pedraza", "",
                                                      "613012159", "26")
        self.assertEqual("Error: Tipo de registro no especificado", cm.exception.message)


    def test_19_request_vaccination_not_valid(self):
        """Este test comprueba que el nombre completo del paciente no ha sido introducido"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("7a849abw-fc1c-aj2c-91db-0edf0fg39n8l", "", "regular",
                                                      "910245672", "12")
        self.assertEqual("Error: Nombre no introducido", cm.exception.message)


    def test_20_request_vaccination_not_valid(self):
        """Este test comprueba que el numero de telefono del paciente no ha sido introducido"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("f8e7fb13-ed71-23a7-gf21-g3c2365e92d2", "Carlos Martínez",
                                                      "regular", "", "78")
        self.assertEqual("Error: Numero de telefono no introducido", cm.exception.message)


    def test_21_request_vaccination_not_valid(self):
        """Este test comprueba que la edad del paciente no ha sido especificada"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("5c2535c7-6dd2-4873-ac83-c1b21c683b8c", "Verónica Matalarra ",
                                                      "regular", "912234678", "")
        self.assertEqual("Error: Edad no introducida", cm.exception.message)

    def test_22_request_vaccination_not_valid(self):
        """En este test se compara que el ID introducido del paciente coincide con otro paciente con el
        mismo ID, tipo, edad y nombre que ya hayan sido previamente registrados"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_store = json_files_path + "store_patient.json"
        if os.path.isfile(file_store):
            os.remove(file_store)

        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("5c2535c7-6dd2-4873-ac83-c1b21c683b8c", "Verónica Matalarra ",
                                                          "regular", "912234678", "12")
            my_request.request_vaccination_id("5c2535c7-6dd2-4873-ac83-c1b21c683b8c", "Verónica Matalarra ",
                                                      "regular", "912234678", "12")
        self.assertEqual("Error: La UUID introducida esta asignada a otro paciente", cm.exception.message)

    def test_23_request_vaccination_not_valid(self):
        """Este test compara que el ID introducido de un paciente coincide con el ID de otro paciente que ya haya
        sido previamente registrado (el resto de atributos no coinciden)"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_store = json_files_path + "store_patient.json"
        if os.path.isfile(file_store):
            os.remove(file_store)

        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("5c2535c7-6dd2-4873-ac83-c1b21c683b8c", "Charly SantaMaria ",
                                                          "regular", "912234478", "19")
            my_request.request_vaccination_id("5c2535c7-6dd2-4873-ac83-c1b21c683b8c", "Verónica Matalarra ",
                                                      "regular", "912234678", "12")
        self.assertEqual("Error: La UUID introducida esta asignada a otro paciente", cm.exception.message)

    def test_24_request_vaccination_not_valid(self):
        """Este test sirve para evaluar que se introducen o no dos hijos iguales"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_store = json_files_path + "store_patient.json"
        if os.path.isfile(file_store):
            os.remove(file_store)

        with self.assertRaises(VaccineManagementException) as cm:
            my_request = VaccineManager()
            padre = VaccineManager()
            hijo2 = VaccineManager()
            padre.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Eva Rubio", "regular", "123456908",
                                         "45")
            hijo2.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano", "family",
                                         "123456908", "13")
            my_request.request_vaccination_id("ac1e0ef3-5eda-4036-a078-9d1aa993f9b9", "Roberto Mandano",
                                                      "family", "123456908", "13")

        self.assertEqual("Error: Paciente family repetido", cm.exception.message)


    def test_25_request_vaccination_not_valid(self):
        """Este test comprueba que la identificator del paciente solo sea str"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id(5541, "Verónica Matalarra ", "regular", "912234678", "40")
        self.assertEqual("Error: ID del paciente no es de tipo str", cm.exception.message)

    def test_26_request_vaccination_not_valid(self):
        """Este test comprueba que la identificator del paciente tenga 36 caracteres"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("5c2535c7-6dd2-4873-ac83-c1b21c6838c", "Verónica Matalarra ",
                                                      "regular", "912234678", "40")
        self.assertEqual("Error: La ID recibida no es una UUID", cm.exception.message)

    def test_27_request_vaccination_not_valid(self):
        """Este test comprueba que la identificator del paciente tenga 36 caracteres"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as cm:
            my_request.request_vaccination_id("5c2535c7-6dd2-4873-ac83-c1b21c6838c5b", "Verónica Matalarra ",
                                                      "regular", "912234678", "40")
        self.assertEqual("Error: La ID recibida no es una UUID", cm.exception.message)



if __name__ == '__main__':
    unittest.main()
