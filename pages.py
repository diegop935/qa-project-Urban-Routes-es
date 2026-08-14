from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class UrbanRoutesPage:

    # Localizadores de Pago / Tarjeta
    payment_method_button = (
        By.XPATH,
        '//div[contains(@class, "pp-button")] | '
        '//div[contains(@class, "pp-text")] | '
        '//div[text()="Método de pago"]'
    )

    add_card_button = (
        By.XPATH,
        '//div[contains(@class, "pp-row") and .//div[text()="Agregar tarjeta"]] | '
        '//div[text()="Agregar tarjeta"]'
    )

    # IDs directos estándar de Urban Routes para los inputs del modal
    card_number_field = (By.ID, 'number')

    card_cvv_field = (
        By.XPATH,
        '//div[@class="card-code-input"]//input[@id="code"]'
    )

    link_card_button = (
        By.XPATH,
        '//button[text()="Agregar" or text()="Enlazar"]'
    )

    close_payment_modal_button = (
        By.XPATH,
        '//div[contains(@class, "payment-picker")]//button[contains(@class, "close-button")] | '
        '//div[contains(@class, "modal")]//button[contains(@class, "close-button")] | '
        '//div[contains(@class, "section active")]//button[contains(@class, "close-button")]'
    )

    card_number_display = (
        By.XPATH,
        '//div[contains(@class, "card-wrapper")]'
        '//input[contains(@class, "card-input")]'
    )

    # Localizadores de direcciones
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Localizador del mensaje para el conductor
    message_field = (By.ID, 'comment')

    # Localizador mantas y pañuelos
    blanket_switch = (
        By.XPATH,
        '//div[contains(@class, "r-type-switch") and '
        './/div[contains(@class, "r-sw-label") and normalize-space()="Manta y pañuelos"]]'
        '//span[contains(@class, "slider")]'
    )

    # Localizador seleccionar dos helados
    ice_cream_plus = (
        By.XPATH,
        '//div[contains(@class, "r-counter")][.//div[contains(@class, "r-counter-label") '
        'and text()="Helado"]]//div[contains(@class, "counter-plus")]'
    )

    ice_cream_count = (
        By.XPATH,
        '//div[contains(@class, "r-counter")][.//div[contains(@class, "r-counter-label") '
        'and text()="Helado"]]//div[contains(@class, "counter-value")]'
    )

    # Localizador pedir taxi
    order_taxi_button = (
        By.XPATH,
        '//button[contains(., "Pedir un taxi")]'
    )

    # Localizadores de tarifa Comfort
    smart_button = (
        By.XPATH,
        '//button[contains(@class, "button round") or contains(text(), "Pedir un taxi")]'
    )

    comfort_card = (
        By.XPATH,
        '//div[contains(@class, "tcard") and .//div[text()="Comfort"]]'
    )

    # Localizadores de teléfono
    phone_button = (
        By.XPATH,
        '//div[@class="np-text" and contains(text(), "Número de teléfono")]'
    )

    phone_field = (By.ID, 'phone')

    next_phone_button = (
        By.XPATH,
        '//button[text()="Siguiente"]'
    )

    sms_code_field = (By.ID, 'code')

    confirm_phone_button = (
        By.XPATH,
        '//button[text()="Confirmar"]'
    )

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
            expected_conditions.visibility_of_element_located(
                self.message_field
            )
        )
        message_input.send_keys(message)

    def select_blanket_and_tissues(self):
        blanket = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.blanket_switch
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            blanket
        )

        blanket.click()

    def is_blanket_selected(self):
        checkbox = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (
                    By.XPATH,
                    '//div[contains(@class, "r-type-switch") and '
                    './/div[contains(@class, "r-sw-label") and normalize-space()="Manta y pañuelos"]]'
                    '//input[@type="checkbox"]'
                )
            )
        )

        return checkbox.is_selected()

    def select_ice_cream(self):
        plus_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.ice_cream_plus
            )
        )

        plus_button.click()
        plus_button.click()

    def get_ice_cream_count(self):
        counter = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.ice_cream_count
            )
        )

        return counter.text

    def order_taxi(self):
        buttons = self.driver.find_elements(
            By.XPATH,
            '//button[contains(., "Pedir un taxi")]'
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
            expected_conditions.element_to_be_clickable(
                self.smart_button
            )
        )

        button.click()

        card = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.comfort_card
            )
        )

        card.click()

    def is_comfort_selected(self):
        card = self.driver.find_element(*self.comfort_card)
        return "active" in card.get_attribute("class")

    def open_phone_modal(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.phone_button
            )
        ).click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.phone_field
            )
        )

    def enter_sms_code(self, code):
        import time

        code_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "code")
            )
        )

        code_input.send_keys(code)

        confirm_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[text()="Confirmar"]')
            )
        )

        confirm_btn.click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "number-picker")]')
            )
        )

        time.sleep(1)

    def is_phone_modal_closed(self):
        elements = self.driver.find_elements(
            By.XPATH,
            '//div[contains(@class, "number-picker")]'
        )

        return not any(element.is_displayed() for element in elements)

    def open_phone_modal_and_submit(self, phone_number):
        self.open_phone_modal()

        phone_field = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.phone_field
            )
        )

        phone_field.send_keys(phone_number)

        next_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.next_phone_button
            )
        )

        next_btn.click()

    def add_credit_card(self, card_number, card_cvv):
        import time

        time.sleep(1)

        payment_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                self.payment_method_button
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            payment_btn
        )

        add_card = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                self.add_card_button
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            add_card
        )

        card_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                self.card_number_field
            )
        )

        cvv_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                self.card_cvv_field
            )
        )

        self.driver.execute_script(
            """
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            card_input,
            card_number
        )

        self.driver.execute_script(
            """
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            cvv_input,
            card_cvv
        )

        time.sleep(1)

        link_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                self.link_card_button
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            link_btn
        )

        time.sleep(1)

        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located(
                    self.close_payment_modal_button
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                close_btn
            )

        except Exception:
            pass

    def is_card_added(self):
        card_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                self.card_number_display
            )
        )

        return card_input.get_attribute("value") != ""

