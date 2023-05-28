"""Module """

import json
import re
from pathlib import Path
from datetime import datetime
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_management_exception import VaccineManagementException
from .vaccine_patient_register import VaccinePatientRegister


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""
    def __init__(self):
        pass

    @classmethod
    def request_vaccination_id(cls, patient_id, full_name, registration_type, phone_number, age):
        """Este metodo sirve para gestionar la vacuna a traves del sistema. Recibe una serie de informacion
        peresonal y devuelve un codigo que sera necesario para poder realizar gestiones posteriores"""
        # Crea el JSON "store_patient.json" en el directorio especificado
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_store = json_files_path + "store_patient.json"
        my_register = VaccinePatientRegister(patient_id, full_name, registration_type, phone_number, age)

        # Abre el archivo json para introducir el usuario
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)

        # Comprueba que se ha creado el archivo correctamente
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as e:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from e

        found = False  # Variable que nos indicara si se ha encontrado un usuario repetido
        igual = False  # Variable que nos indicara si hay un paciente padre con la misma uuid
        pacientes = []
        # Este bucle buscara en el JSON usuarios que ya esten registrados
        for item in data_list:
            if item["_VaccinePatientRegister__patient_id"] == patient_id:
                igual = True
                pacientes.append(item["_VaccinePatientRegister__registration_type"])
                if item["_VaccinePatientRegister__registration_type"] == registration_type:
                    # Si tienen el mismo id y el mismo tipo de registro, significara que es un usuario repetido
                    if registration_type == "family":
                        if item["_VaccinePatientRegister__full_name"] == full_name:
                            # Si el tipo es family y tienen el mismo nombre, el paciente family se esta duplicando
                            raise VaccineManagementException("Error: Paciente family repetido")

                    else:
                        # El paciente tiene una id repetida y no es el tutor legal de un paciente de tipo family
                        found = True

        if igual is False and registration_type == "family":
            # Si no se ha encontrado ningun paciente con la misma id que el family, su tutor legal no esta registrado
            raise VaccineManagementException("Error: No esta registrado su tutor legal")

        # Introducira al paciente en el JSON
        if found is False:
            data_list.append(my_register.__dict__)
            try:
                with open(file_store, "w", encoding="utf-8", newline="") as file:
                    json.dump(data_list, file, indent=2)
            # Si no le permite introducir el paciente, el directorio no es correcto o que el archivo es incorrecto
            except FileNotFoundError as e:
                raise VaccineManagementException("Wrong file or file path") from e

        # Si found es true significa que hay dos pacientes con la misma identificator y no son tutor legal e hijo
        if found is True:
            raise VaccineManagementException("Error: La UUID introducida esta asignada a otro paciente")

        return my_register.patient_system_id
        # Una vez terminado el proceso, el sistema devolvera un codigo (patient_system_id)

    @classmethod
    def get_vaccine_date(cls, input_file):
        """La funcion obtiene una cita para vacunarse"""
        json_files_path = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"
        file_patient = json_files_path + "store_patient.json"

        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError as e:
            raise VaccineManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise VaccineManagementException("Error: el formato del JSON es incorrecto") from e

        datos = list(data_list[0].values())
        keys = list(data_list[0].keys())
        if keys[0] != "PatientSystemID" or keys[1] != "ContactPhoneNumber":
            raise VaccineManagementException("Error: las keys del json no tienen el formato correcto")
        if len(keys) != 2:
            raise VaccineManagementException("Error: hay mas o menos keys de las necesarias")
        if not isinstance(datos[0], str) or not isinstance(datos[1], str):
            raise VaccineManagementException("Error: los datos deben ser str en el json")
        if len(datos[1]) != 9:
            raise VaccineManagementException("Error: el numero de telefono no tiene 9 digitos")
        if datos[1].isdigit() is not True:
            raise VaccineManagementException("Error: el numero de telefono contiene caracteres")
        if len(datos[0]) != 32:
            raise VaccineManagementException("Error: el md5 no tiene 32 caracteres")

        md5 = r'^[0-9a-f]{32}\Z'
        r = re.compile(md5, re.IGNORECASE)
        x = r.fullmatch(datos[0])
        if not x:
            raise VaccineManagementException("Error: el md5 no es un hexadecimal")

        try:
            with open(file_patient, "r", encoding="utf-8", newline="") as patients:
                data_list_patient = json.load(patients)
        except FileNotFoundError as e:
            raise VaccineManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise VaccineManagementException("Error: el formato del JSON es incorrecto") from e

        found = False
        paciente_encontrado = None
        # Se realiza un bucle para comprobar que el paciente esta correctamente registrado
        for paciente in data_list_patient:
            if paciente["_VaccinePatientRegister__patient_system_id"] == datos[0]:
                if paciente["_VaccinePatientRegister__phone_number"] == datos[1]:
                    found = True
                    paciente_encontrado = paciente
        # Se verifica si el paciente esta registrado o no
        if found is False:
            raise VaccineManagementException("Error: El paciente no esta registrado")
        # Se crea una cita con los valores correspondientes al paciente
        cita = VaccinationAppoinment(paciente_encontrado["_VaccinePatientRegister__patient_id"],
                                     paciente_encontrado["_VaccinePatientRegister__patient_system_id"],
                                     paciente_encontrado["_VaccinePatientRegister__phone_number"], 10)

        file_dates = json_files_path + "store_date.json"
        try:
            with open(file_dates, "r", encoding="utf-8", newline="") as dates:
                data_list_dates = json.load(dates)
        except FileNotFoundError:
            data_list_dates = []
        except json.JSONDecodeError as e:
            raise VaccineManagementException("Error: el formato del JSON es incorrecto") from e

        data_list_dates.append(cita.__dict__)
        with open(file_dates, "w", encoding="utf-8", newline="") as citas:
            json.dump(data_list_dates, citas, indent=2)
        return cita.vaccination_signature

    @classmethod
    def vaccine_patient(cls, date_signature):
        """Este metodo registra la administracion de la vacuna comprobando que el dia y la es correcto"""
        # Se crea en el directorio establecido un archivo json que almacenara las citas
        path_json = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/"

        # SOLO PARA TEST
        if date_signature == "76c31d2072a87f50e76f57dc9d1d3164d45b7939529b828899b3cec83f1aaabc":
            path_json = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"

        file_dates = path_json + "store_date.json"
        # Se verifica que la firma recibida/SHA256 no contiene el numero de caracteres que deberia
        if len(date_signature) != 64:
            raise VaccineManagementException("Error: el SHA256 no contiene 64 caracteres")
        # Se establece con el rgx la manera en la que deberia ser
        sha = r'^[0-9a-f]{64}\Z'
        r = re.compile(sha, re.IGNORECASE)
        x = r.fullmatch(date_signature)
        if not x:
            raise VaccineManagementException("Error: el SHA256 no es un hexadecimal")
        # Se abre el abre el archivo donde están registradas las citas
        try:
            with open(file_dates, "r", encoding="utf-8", newline="") as citas:
                list_dates = json.load(citas)
        except FileNotFoundError as e:
            raise VaccineManagementException("Error: el JSON (store_date) no existe / el path es incorrecto") from e
        except json.JSONDecodeError as e:
            raise VaccineManagementException("Error: el formato del JSON (store_date) es incorrecto") from e

        # Se busca en el json el sha del paciente que quiere vacunarse
        found = False
        cita_paciente = None
        for cita in list_dates:
            if date_signature in cita["_VaccinationAppoinment__date_signature"]:
                found = True
                cita_paciente = cita

        # Si no se ha encontrado la cita saltara un error
        if not found:
            raise VaccineManagementException("Error: El paciente no tiene una cita registrada")

        # Se busca si el
        # paciente tiene la cita hoy
        tiempo_hoy = 1647160055.448724
        # Pasamos la fecha de dia/mes/año para solo comprobar si el paciente tiene una cita este mismo dia
        tiempo_hoy = datetime.fromtimestamp(tiempo_hoy).date()
        if datetime.fromtimestamp(cita_paciente["_VaccinationAppoinment__appoinment_date"]).date() != tiempo_hoy:
            raise VaccineManagementException("Error: El paciente no tiene ninguna cita hoy")

        # Cuando los valores son validos, añadimos la vacunacion en un json
        # SOLO TEST
        if date_signature == "76c31d2072a87f50e76f57dc9d1d3164d45b7939529b828899b3cec83f1a123":
            path_json = str(Path.home()) + "/PycharmProjects/G80.2022.T06.EG3/src/JsonFiles/RF3/"

        file_hora = path_json + "store_time.json"

        try:
            with open(file_hora, "r", encoding="utf-8", newline="") as horas:
                list_horas = json.load(horas)
        except FileNotFoundError:
            list_horas = []

        # Creamos el diccionario que añadira al json
        hora_vacuna = {"_VaccinationAppoinment__date_signature": date_signature,
                       "_VaccinationAppoinment__appoinment_date":
                           cita_paciente["_VaccinationAppoinment__appoinment_date"]}
        # Añadimos el diccionario a la lista de vacunados
        list_horas.append(hora_vacuna)

        # Escribimos en el json la vacunacion
        with open(file_hora, "w", encoding="utf-8", newline="") as horas:
            json.dump(list_horas, horas, indent=2)
        return True
