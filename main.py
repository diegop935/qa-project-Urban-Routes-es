import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:

    # Localizadores de Pago / Tarjeta
    payment_method_button = (By.XPATH, '//div[contains(@class, "pp-button")] | //div[contains(@class, "pp-text")] | //div[text()="Método de pago"]')
    add_card_button = (By.XPATH, '//div[contains(@class, "pp-row") and .//div[text()="Agregar tarjeta"]] | //div[text()="Agregar tarjeta"]')

    # IDs directos estándar de Urban Routes para los inputs del modal
    card_number_field = (By.ID, 'number')
    card_cvv_field = (By.XPATH, '//div[@class="card-code-input"]//input[@id="code"]')

    link_card_button = (By.XPATH, '//button[text()="Agregar" or text()="Enlazar"]')
    close_payment_modal_button = (By.XPATH, '//div[contains(@class, "payment-picker")]//button[contains(@class, "close-button")] | //div[contains(@class, "modal")]//button[contains(@class, "close-button")] | //div[contains(@class, "section active")]//button[contains(@class, "close-button")]')

    # Localizadores de direcciones
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Localizador del mensaje para el conductor
    message_field = (By.ID, 'comment')

    # Localizador mantas y pañuelos
    blanket_switch = (
        By.XPATH, '//div[contains(@class, "r-type-switch") and .//div[contains(@class, "r-sw-label") and normalize-space()="Manta y pañuelos"]]//span[contains(@class, "slider")]'
    )

    # Localizador seleccinnar dos helados
    ice_cream_plus = (
        By.XPATH, '//div[contains(@class, "r-counter")][.//div[contains(@class, "r-counter-label") and text()="Helado"]]//div[contains(@class, "counter-plus")]'
    )

    # Localizador pedir taxi
    order_taxi_button = (
        By.XPATH, '//button[contains(., "Pedir un taxi")]'
    )

    # Localizadores de tarifa Comfort
    smart_button = (By.XPATH, '//button[contains(@class, "button round") or contains(text(), "Pedir un taxi")]')
    comfort_card = (By.XPATH, '//div[contains(@class, "tcard") and .//div[text()="Comfort"]]')

    # LOCALIZADORES DE TELÉFONO (Asegúrate de incluir estas 5 líneas)
    phone_button = (By.XPATH, '//div[@class="np-text" and contains(text(), "Número de teléfono")]')
    phone_field = (By.ID, 'phone')
    next_phone_button = (By.XPATH, '//button[text()="Siguiente"]')
    sms_code_field = (By.ID, 'code')
    confirm_phone_button = (By.XPATH, '//button[text()="Confirmar"]')


    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_driver_message(self, message):
        message_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.message_field)
        )
        message_input.send_keys(message)

    def select_blanket_and_tissues(self):
        blanket = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.blanket_switch)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            blanket
        )
        blanket.click()

    def select_ice_cream(self):
        plus_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.ice_cream_plus)
        )

        plus_button.click()
        plus_button.click()

    def order_taxi(self):
        buttons = self.driver.find_elements(
            By.XPATH,
            '//button[contains(., "Pedir un taxi")]'
        )

        print("Cantidad de botones encontrados:", len(buttons))

        for button in buttons:
            print(
                "BOTÓN:",
                repr(button.text),
                "visible:",
                button.is_displayed(),
                "habilitado:",
                button.is_enabled()
            )

        visible_button = None

        for button in buttons:
            if button.is_displayed() and button.is_enabled():
                visible_button = button
                break

        if visible_button is None:
            raise Exception(
                "No se encontró un botón 'Pedir un taxi' visible y habilitado."
            )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            visible_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            visible_button
        )

    def select_comfort_tariff(self):
        button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.smart_button)
        )
        button.click()

        card = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.comfort_card)
        )
        card.click()

    def open_phone_modal_and_submit(self, phone_number):
        import time

        # 1. Clic en el botón para abrir el modal del teléfono
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.phone_button)
        ).click()

        # 2. Escribir el número de teléfono
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.phone_field)
        ).send_keys(phone_number)

        # 3. Clic en "Siguiente"
        next_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.next_phone_button)
        )
        next_btn.click()

        # 4. Esperar 1-2 segundos a que el servidor de TripleTen genere y envíe el código
        time.sleep(2)

    def enter_sms_code(self, code):
        import time
        # Localizar el campo del SMS e ingresar el código
        code_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "code"))
        )
        code_input.send_keys(code)

        # Clic en "Confirmar"
        confirm_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//button[text()="Confirmar"]'))
        )
        confirm_btn.click()

        # Esperar a que el modal del SMS desaparezca por completo
        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located((By.XPATH, '//div[contains(@class, "number-picker")]'))
        )
        time.sleep(1)

# --- NUEVO MÉTODO PARA TARJETA DE CRÉDITO ---

    def add_credit_card(self, card_number, card_cvv):
        import time

        time.sleep(1)

        # 1. Clic en "Método de pago"
        payment_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.payment_method_button)
        )
        self.driver.execute_script("arguments[0].click();", payment_btn)

        # 2. Clic en "Agregar tarjeta"
        add_card = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.add_card_button)
        )
        self.driver.execute_script("arguments[0].click();", add_card)

        # 3. Localizar inputs de tarjeta y CVV
        card_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.card_number_field)
        )
        cvv_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.card_cvv_field)
        )

        # 4. Inyectar datos vía JS
        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """, card_input, card_number)

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """, cvv_input, card_cvv)

        time.sleep(1)

        # 5. Clic en "Agregar" / "Enlazar"
        link_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.link_card_button)
        )
        self.driver.execute_script("arguments[0].click();", link_btn)

        time.sleep(1)

        # 6. Cerrar modal de pago (con manejo de excepciones si se cierra automáticamente)
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located(self.close_payment_modal_button)
            )
            self.driver.execute_script("arguments[0].click();", close_btn)
        except Exception:
            # Si el modal ya se cerró al agregar la tarjeta, continúa sin interrumpir
            pass

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)

        # Esperar a que la página cargue el campo 'from'
        WebDriverWait(self.driver, 20).until(
            expected_conditions.presence_of_element_located((By.ID, "from"))
        )

        routes_page = UrbanRoutesPage(self.driver)

        address_from = data.address_from
        address_to = data.address_to

        # 1. Configurar dirección (solo una vez)
        routes_page.set_route(address_from, address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        # 2. Seleccionar tarifa Comfort
        routes_page.select_comfort_tariff()

        # 3. Número de teléfono (se ejecuta SOLO UNA VEZ)
        routes_page.open_phone_modal_and_submit(data.phone_number)
        code = retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(code)

        # 4. Agregar tarjeta de crédito
        routes_page.add_credit_card(data.card_number, data.card_code)

        # 5. Escribir mensaje para el conductor
        routes_page.set_driver_message(data.message_for_driver)

        # 6. Pedir manta y pañuelos
        routes_page.select_blanket_and_tissues()

        # 7. Pedir 2 helados
        routes_page.select_ice_cream()

        # 8. Pedir taxi
        routes_page.order_taxi()

