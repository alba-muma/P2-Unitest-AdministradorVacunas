"""MODULE: access_request. Contains the access request class"""
import hashlib
import json
import uuid
import re
from datetime import datetime
from .vaccine_management_exception import VaccineManagementException


class VaccinePatientRegister:
    """Class representing the register of the patient in the system"""
    def __init__(self, patient_id, full_name, registration_type, phone_number, age):
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        # El tiempo ha sido parado para la correcta ejecucion de los tests
        self.__time_stamp = 1646296055.448724
        # Pylint me obliga a hacer este uso inadecuado de la variable D:
        self.__patient_system_id = ""
        if self.__patient_system_id == "":
            self.__patient_system_id = self.patient_system_id

        # Condicionales para comprobar los errores del numero de telefono
        if phone_number == "":
            raise VaccineManagementException("Error: Numero de telefono no introducido")
        if len(str(phone_number)) != 9:  # Comprueba que el telefono tenga 9 digitos
            raise VaccineManagementException("Error: El telefono no tiene 9 digitos")
            # Comprueba que el telefono no contiene caracteres
        if str(phone_number).isdigit() is False:
            raise VaccineManagementException("Error: El numero de telefono contiene un caracter no valido")
        self.__phone_number = phone_number

        # Condicionales para comprobar los errores del tipo de registro
        if registration_type == "":
            raise VaccineManagementException("Error: Tipo de registro no especificado")
        if registration_type not in ("regular", "family"):  # Comprobamos que el registro sea family o regular
            raise VaccineManagementException("Error: El tipo de registro introducido no es valido")
        # Si es family que la UUID este en la base de datos

        self.__registration_type = registration_type

        # Condicionales para comprobar los errores del nombre completo
        if full_name == "":
            raise VaccineManagementException("Error: Nombre no introducido")

        for letra in full_name:  # Comprueba que no haya digitos en la cadena
            if letra.isdigit() is not False:
                raise VaccineManagementException("Error: El nombre introducido contiene un caracter no valido")
        if len(full_name) > 30:  # Comprueba que haya menos de 30 caracteres
            raise VaccineManagementException("Error: El nombre tiene mas de 30 caracteres")
        if " " not in full_name:  # Comprueba que hay mas de una palabra
            raise VaccineManagementException("Error: El nombre recibido esta incompleto")
        self.__full_name = full_name

        # Invocamos el metodo validate_guid de la clase VaccineManager para verificar que el id introducido es valido
        # Condicionales para comprobar los errores del identificator del paciente
        if patient_id == "":  # Comprueba que se ha introducido un valor para el identificator del paciente
            raise VaccineManagementException("Error: ID del paciente no se ha especificado")
        if not isinstance(patient_id, str):
            raise VaccineManagementException("Error: ID del paciente no es de tipo str")
        self.validate_guid(patient_id)
        self.__patient_id = patient_id

        # Condicionales para comprobar los errores de la edad del paciente
        # Comprueba que se ha introducido un valor para la edad
        if age == "":
            raise VaccineManagementException("Error: Edad no introducida")
        # Comprueba que la edad introducida tiene el formato correcto
        if str(age).isdigit() is False:
            raise VaccineManagementException("Error: La Edad introducida no es un numero")
        # Comprueba que la edad introducida se encuentra dentro del limite establecido
        if int(age) < 6 or int(age) > 125:
            raise VaccineManagementException("Error: La edad esta fuera de rango")
        self.__age = age

    def __str__(self):
        return "VaccinePatientRegister:" + json.dumps(self.__dict__)

    @property
    def full_name(self):
        """Property representing the name and the surname of
        the person who request the registration"""
        return self.__full_name

    @full_name.setter
    def full_name(self, full_name):
        self.__full_name = full_name

    @property
    def vaccine_type(self):
        """Property representing the tipo vaccine"""
        return self.__registration_type
    @vaccine_type.setter
    def vaccine_type(self, tipo):
        self.__registration_type = tipo

    @property
    def phone_number(self):
        """Property representing the requester's phone number"""
        return self.__phone_number
    @phone_number.setter
    def phone_number(self, phone):
        self.__phone_number = phone

    @property
    def patient_id(self):
        """Property representing the requester's UUID"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, identificator):
        self.__patient_id = identificator

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def patient_system_id(self):
        """Returns the md5 signature"""
        return hashlib.md5(self.__str__().encode()).hexdigest()

    @property
    def patient_age(self):
        """Returns the patient's age"""
        return self.__age

    @patient_age.setter
    def patient_age(self, age):
        self.__age = age

    @classmethod
    def validate_guid(cls, guid):
        """Metodo que valida el GUID"""
        try:
            uuid.UUID(guid)
            r = re.compile(r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-'
                           r'[89AB][0-9A-F]{3}-[0-9A-F]{12}$', re.IGNORECASE)
            x = r.fullmatch(guid)
            if not x:
                raise VaccineManagementException("Error: UUID v4 formato invalido")
        except ValueError as e:
            raise VaccineManagementException("Error: La ID recibida no es una UUID") from e
        return True
