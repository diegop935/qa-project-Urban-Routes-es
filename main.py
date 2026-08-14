import data
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from helpers import retrieve_phone_code
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    def setup_method(self):
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        self.driver = webdriver.Chrome(options=options)

        self.driver.get(data.urban_routes_url)

        WebDriverWait(self.driver, 20).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "from")
            )
        )

        self.routes_page = UrbanRoutesPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    # ---------------------------------------------------------
    # MÉTODOS AUXILIARES PARA PREPARAR CADA PRUEBA
    # ---------------------------------------------------------

    def _set_route(self):
        self.routes_page.set_route(
            data.address_from,
            data.address_to
        )

        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

    def _select_comfort(self):
        self.routes_page.select_comfort_tariff()

    def _confirm_phone(self):
        self.routes_page.open_phone_modal_and_submit(
            data.phone_number
        )

        code = retrieve_phone_code(self.driver)

        self.routes_page.enter_sms_code(code)

    # ---------------------------------------------------------
    # 1. CONFIGURACIÓN DE DIRECCIÓN INICIAL
    # ---------------------------------------------------------

    def test_set_route(self):
        self._set_route()

        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

    # ---------------------------------------------------------
    # 2. SELECCIÓN DE LA TARIFA COMFORT
    # ---------------------------------------------------------

    def test_select_comfort_tariff(self):
        self._set_route()

        self._select_comfort()

        comfort_card = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.routes_page.comfort_card
            )
        )

        assert self.routes_page.is_comfort_selected()

    # ---------------------------------------------------------
    # 3. REGISTRO DEL NÚMERO TELEFÓNICO
    # ---------------------------------------------------------

    def test_enter_phone_number(self):
        self._set_route()
        self._select_comfort()

        self.routes_page.open_phone_modal()

        phone_field = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.routes_page.phone_field
            )
        )

        phone_field.send_keys(data.phone_number)

        assert phone_field.get_attribute("value") == data.phone_number

    # ---------------------------------------------------------
    # 4. AGREGAR TARJETA BANCARIA
    # ---------------------------------------------------------

    def test_add_credit_card(self):
        self._set_route()
        self._select_comfort()
        self._confirm_phone()

        self.routes_page.add_credit_card(
            data.card_number,
            data.card_code
        )

        assert self.routes_page.is_card_added()
    # ---------------------------------------------------------
    # 5. CONFIRMACIÓN DEL CÓDIGO DE SEGURIDAD
    # ---------------------------------------------------------

    def test_confirm_phone_code(self):
        self._set_route()
        self._select_comfort()

        self.routes_page.open_phone_modal_and_submit(
            data.phone_number
        )

        code = retrieve_phone_code(self.driver)

        self.routes_page.enter_sms_code(code)

        assert self.routes_page.is_phone_modal_closed()


    # ---------------------------------------------------------
    # 6. ENVÍO DE MENSAJE AL CONDUCTOR
    # ---------------------------------------------------------

    def test_set_driver_message(self):
        self._set_route()
        self._select_comfort()
        self._confirm_phone()
        self.routes_page.add_credit_card(
            data.card_number,
            data.card_code
        )

        self.routes_page.set_driver_message(
            data.message_for_driver
        )

        message_field = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.routes_page.message_field
            )
        )

        assert message_field.get_property("value") == data.message_for_driver

    # ---------------------------------------------------------
    # 7. SOLICITAR MANTA Y PAÑUELOS
    # ---------------------------------------------------------

    def test_select_blanket_and_tissues(self):
        self._set_route()
        self._select_comfort()
        self._confirm_phone()

        self.routes_page.add_credit_card(
            data.card_number,
            data.card_code
        )

        self.routes_page.select_blanket_and_tissues()

        assert self.routes_page.is_blanket_selected()

    # ---------------------------------------------------------
    # 8. PEDIR DOS HELADOS
    # ---------------------------------------------------------

    def test_select_two_ice_creams(self):
        self._set_route()
        self._select_comfort()
        self._confirm_phone()

        self.routes_page.add_credit_card(
            data.card_number,
            data.card_code
        )

        self.routes_page.select_ice_cream()

        assert self.routes_page.get_ice_cream_count() == "2"

    # ---------------------------------------------------------
    # 9. APARICIÓN DEL MODAL DE BÚSQUEDA DE TAXI
    # ---------------------------------------------------------

    def test_order_taxi(self):
        self._set_route()
        self._select_comfort()
        self._confirm_phone()

        self.routes_page.add_credit_card(
            data.card_number,
            data.card_code
        )

        self.routes_page.set_driver_message(
            data.message_for_driver
        )

        self.routes_page.select_blanket_and_tissues()
        self.routes_page.select_ice_cream()

        self.routes_page.order_taxi()

        search_modal = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                (
                    By.XPATH,
                    '//*[contains(text(), "Buscar automóvil")]'
                )
            )
        )

        assert search_modal.is_displayed()